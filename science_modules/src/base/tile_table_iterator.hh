#ifndef tao_base_tile_table_iterator_hh
#define tao_base_tile_table_iterator_hh

#include <vector>
#include <array>
#include <list>
#include <set>
#include <boost/iterator/iterator_facade.hpp>
#include <boost/optional.hpp>
#include <libhpc/system/view.hh>
#include <libhpc/system/reallocate.hh>
#include <libhpc/algorithm/combination.hpp>
#include <libhpc/numerics/clip.hh>
#include <libhpc/numerics/coords.hh>
#include <libhpc/mpi.hh>
#include "rdb_backend.hh"
#include "tile.hh"

namespace tao {
   namespace backends {

      namespace mpi = hpc::mpi;

      template< class Backend >
      class tile_table_iterator
         : public boost::iterator_facade< tile_table_iterator<Backend>,
                                          typename rdb<typename Backend::real_type>::table_type const&,
                                          std::forward_iterator_tag,
                                          typename rdb<typename Backend::real_type>::table_type const& >
      {
         friend class boost::iterator_core_access;

      public:

         typedef Backend backend_type;
         typedef typename Backend::real_type real_type;
         typedef typename rdb<real_type>::table_type table_type;
         typedef table_type const& value_type;
         typedef value_type reference_type;

         tile_table_iterator()
            : _tile( NULL ),
              _be( NULL ),
              _done( true )
         {
         }

         tile_table_iterator( tao::tile<real_type> const& tile,
                              backend_type const& backend,
                              boost::optional<hpc::view<std::vector<std::pair<unsigned long long,int>>>> work = boost::optional<hpc::view<std::vector<std::pair<unsigned long long,int>>>>() )
            : _tile( &tile ),
              _be( &backend ),
              _work( work ),
              _done( false )
         {
            // Construct the walls I'll be using to clip the lightcone
            // approximation.
            std::vector<real_type> perms( 9 );
            for( unsigned ii = 0; ii < 3; ++ii )
            {
               perms[ii] = -1;
               perms[ii + 3] = 0;
               perms[ii + 6] = 1;
            }
            do
            {
               _walls.emplace_back( std::array<real_type,3>{ { perms[0], perms[1], perms[2] } } );
            }
            while( boost::next_partial_permutation( perms.begin(), perms.begin() + 3, perms.end() ) );

            // Get to the first position.
            _begin();
         }

         tile_table_iterator( tile_table_iterator const& src )
            : _be( src._be ),
              _tile( src._tile ),
              _walls( src._walls ),
              _tables( src._tables ),
              _work( src._work ),
              _done( src._done )
         {
            // Iterator needs to be modified.
            if( !src._tables.empty() )
               _it = _tables.begin() + (src._it - src._tables.begin());
         }

         tile_table_iterator&
         operator=( tile_table_iterator const& op )
         {
            _be = op._be;
            _tile = op._tile;
            _walls = op._walls;
            _tables = op._tables;
            _work = op._work;
            _done = op._done;

            // Iterator needs to be modified.
            if( !op._tables.empty() )
               _it = _tables.begin() + (op._it - op._tables.begin());

            return *this;
         }

         backend_type const*
         backend() const
         {
            return _be;
         }

         tao::tile<real_type> const*
         tile() const
         {
            return _tile;
         }

         std::vector<std::array<real_type,3>> const&
         walls() const
         {
            return _walls;
         }

         std::vector<table_type> const&
         tables() const
         {
            return _tables;
         }

         typename std::vector<table_type>::const_iterator const&
         table_iter() const
         {
            return _it;
         }

      protected:

         void
         increment()
         {
            if( ++_it == _tables.end() )
               _done = true;
         }

         bool
         equal( tile_table_iterator const& op ) const
         {
            return _done == op._done;
         }

         reference_type
         dereference() const
         {
            return *_it;
         }

         void
         _begin()
         {
            LOGBLOCKD( "Calculating overlapping tables." );

            // Use a set to cache tables to eliminate duplicates.
            std::set<table_type> tables;

            // Cache some information from the lightcone.
            real_type ra_min = _tile->lightcone()->min_ra() + _tile->lightcone()->viewing_angle();
            real_type ra_max = _tile->lightcone()->max_ra() + _tile->lightcone()->viewing_angle();
            real_type dec_min = _tile->lightcone()->min_dec();
            real_type dec_max = _tile->lightcone()->max_dec();
            real_type dist_min = _tile->lightcone()->min_dist();
            real_type dist_max = _tile->lightcone()->max_dist();

            // Need the info in array format.
            std::array<real_type,3> ecs_min = { ra_min, dec_min, dist_min };
            std::array<real_type,3> ecs_max = { ra_max, dec_max, dist_max };
            LOGDLN( "Have minimum ECS coordinates: ", ecs_min );
            LOGDLN( "Have maximum ECS coordinates: ", ecs_max );

            // Cache some information.
            std::array<unsigned,3> const& axis = _tile->rotation();
            std::array<real_type,3> const& offs = _tile->translation();
            LOGDLN( "Using rotation: ", axis );
            LOGDLN( "Using translation: ", offs );

            // Shift each table bounding box along each wall direction to
            // see if there is any periodic overlap with the cone.
            for( auto it = _be->table_begin(); it != _be->table_end(); ++it )
            {
               LOGBLOCKD( "Current table box (sans origin): ", it->min(), ", ", it->max() );

               // Apply each periodic side to the box and check.
               for( auto const& wall : _walls )
               {
                  LOGBLOCKD( "Using wall: ", wall );

                  std::array<real_type,3> tmp_min, tmp_max;
                  for( unsigned jj = 0; jj < 3; ++jj )
                  {
                     real_type box_size = _tile->max()[axis[jj]] - _tile->min()[axis[jj]];
                     tmp_min[jj] = _tile->min()[jj] +
                                   it->min()[axis[jj]] + 
                                   wall[axis[jj]]*box_size + 
                                   offs[axis[jj]];
                     tmp_max[jj] = _tile->min()[jj] +
                                   it->max()[axis[jj]] + 
                                   wall[axis[jj]]*box_size + 
                                   offs[axis[jj]];
                  }
                  if( _check_overlap( ecs_min, ecs_max, tmp_min, tmp_max ) )
                  {
                     tables.insert( *it );
                     break;
                  }
               }
            }

            // If we've been given a work vector to use, then do so.
            if( _work )
            {
               LOGBLOCKD( "Using a work vector to balance tables." );
               auto work = *_work;

               // Transfer to a vector and sort on size.
               std::vector<table_type> tbl_vec( tables.size() );
               std::copy( tables.begin(), tables.end(), tbl_vec.begin() );
               std::sort( tbl_vec.begin(), tbl_vec.end(),
                          []( table_type const& x, table_type const& y )
                          {
                             return y.size() < x.size();
                          } );
#ifndef NLOGDEBUG
               LOGD( "Ordered table vector: " );
               for( auto const& tbl : tbl_vec )
                  LOGD( "(", tbl.name(), ", ", tbl.size(), "), " );
               LOGDLN( "" );
#endif

               // Sort the work vector based on lowest amount of work done.
               std::sort( work.begin(), work.end(),
                          []( std::pair<unsigned long long,int> const& x,
                              std::pair<unsigned long long,int> const& y )
                          {
                             return x.first < y.first;
                          } );
               LOGDLN( "Ordered work vector: ", work );

               // Cache maximum work.
               unsigned long long max_work = work.back().first;

               // Start adding tables to each process.
               _tables.clear();
               auto tbl_it = tbl_vec.begin();
               auto work_it = work.begin();
               while( tbl_it != tbl_vec.end() )
               {
                  do
                  {
                     work_it->first += tbl_it->size();
                     if( work_it->second == mpi::comm::world.rank() )
                        _tables.push_back( *tbl_it );
                     ++tbl_it;
                  }
                  while( tbl_it != tbl_vec.end() && work_it->first < max_work );
		  max_work = std::max( max_work, work_it->first );
                  ++work_it;
                  if( work_it == work.end() )
                     work_it = work.begin();
               }

               LOGILN( "Parallel work vector: ", work );
            }
            else
            {
               unsigned first_table = (mpi::comm::world.rank()*tables.size())/mpi::comm::world.size();
               unsigned last_table = ((mpi::comm::world.rank() + 1)*tables.size())/mpi::comm::world.size();
               hpc::reallocate( _tables, last_table - first_table );
               {
                  auto it = tables.begin();
                  unsigned ii;
                  for( ii = 0; ii < first_table; ++ii, ++it );
                  for( ; ii < last_table; ++ii, ++it )
                     _tables[ii - first_table] = *it;
               }
            }

            // Set table iterator.
            LOGILN( "Overlapping tables: ", _tables );
            _it = _tables.begin();

            // If there are no tables flag that we're done.
            _done = _tables.empty();
         }

         bool
         _check_overlap( std::array<real_type,3> const& ecs_min,
                         std::array<real_type,3> const& ecs_max,
                         std::array<real_type,3> const& min,
                         std::array<real_type,3> const& max )
         {
            LOGBLOCKD( "Checking overlap with box: ", min, ", ", max );

            // Clip the box against the parent box.
            std::array<real_type,3> clip_min, clip_max;
            box_box_clip(
               min.begin(), min.end(),
               max.begin(),
               _tile->min().begin(),
               _tile->max().begin(),
               clip_min.begin(),
               clip_max.begin()
               );

            // If there is no volume left, return false.
            if( hpc::approx( box_volume( clip_min.begin(), clip_min.end(), clip_max.begin() ), 0.0, 1e-8 ) )
            {
               LOGDLN( "Outside tile." );
               return false;
            }

            // Move it as a result of the cone origin.
            for( int ii = 0; ii < 3; ++ii )
            {
               clip_min[ii] -= _tile->origin()[ii];
               clip_max[ii] -= _tile->origin()[ii];
            }

            // Check for overlap with cone.
            auto res = hpc::ecs_box_collision( ecs_min, ecs_max, clip_min, clip_max );
#ifndef NLOG
            if( res )
               LOGDLN( "Overlap with cone." );
            else
               LOGDLN( "No overlap." );
#endif
            return res;
         }

      protected:

         backend_type const* _be;
         tao::tile<real_type> const* _tile;
         std::vector<std::array<real_type,3>> _walls;
         std::vector<table_type> _tables;
         boost::optional<hpc::view<std::vector<std::pair<unsigned long long,int>>>> _work;
         typename std::vector<table_type>::const_iterator _it;
         bool _done;
      };

   }
}

#endif
