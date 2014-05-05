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
                                          const typename rdb<typename Backend::real_type>::table_type&,
                                          std::forward_iterator_tag,
                                          const typename rdb<typename Backend::real_type>::table_type& >
      {
         friend class boost::iterator_core_access;

      public:

         typedef Backend backend_type;
         typedef typename Backend::real_type real_type;
         typedef typename rdb<real_type>::table_type table_type;
         typedef const table_type& value_type;
         typedef value_type reference_type;

         tile_table_iterator()
            : _tile( NULL ),
              _be( NULL ),
              _done( true )
         {
         }

         tile_table_iterator( const tao::tile<real_type>& tile,
                              const backend_type& backend,
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

         tile_table_iterator( const tile_table_iterator& src )
            : _be( src._be ),
              _tile( src._tile ),
              _ph( src._ph ),
              _planes( src._planes ),
              _walls( src._walls ),
              _tables( src._tables ),
              _work( src._work ),
              _done( src._done )
         {
            // Iterator needs to be modified.
            _it = _tables.begin() + (src._it - src._tables.begin());
         }

         tile_table_iterator&
         operator=( const tile_table_iterator& op )
         {
            _be = op._be;
            _tile = op._tile;
            _ph = op._ph;
            _planes = op._planes;
            _walls = op._walls;
            _tables = op._tables;
            _work = op._work;
            _done = op._done;

            // Iterator needs to be modified.
            _it = _tables.begin() + (op._it - op._tables.begin());

            return *this;
         }

         const typename hpc::view<std::vector<std::array<real_type,3>>>
         polyhedra() const
         {
            return _ph;
         }

         const std::list<std::array<real_type,4>>&
         planes() const
         {
            return _planes;
         }

         const backend_type*
         backend() const
         {
            return _be;
         }

         const tao::tile<real_type>*
         tile() const
         {
            return _tile;
         }

         const std::vector<std::array<real_type,3>>&
         walls() const
         {
            return _walls;
         }

         const std::vector<table_type>&
         tables() const
         {
            return _tables;
         }

         const typename std::vector<table_type>::const_iterator&
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
         equal( const tile_table_iterator& op ) const
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

            // Need the points of the polyhedron. Don't forget to
            // offset by the tile we're using.
            _calc_polyhedron();
            for( auto& pnt : _ph )
            {
               for( unsigned ii = 0; ii < 3; ++ii )
               {
                  pnt[ii] -= _tile->min()[ii];
                  pnt[ii] += _tile->origin()[ii];
               }
            }

            // Now convert to planes.
            _calc_polygon_planes();

            // Cache some information.
            const std::array<unsigned,3>& axis = _tile->rotation();
            const std::array<real_type,3>& offs = _tile->translation();

            // Shift each table bounding box along each wall direction to
            // see if there is any periodic overlap with the cone.
            std::set<table_type> tables;
            for( auto it = _be->table_begin(); it != _be->table_end(); ++it )
            {
               // Apply each periodic side to the box and check.
               for( const auto& wall : _walls )
               {
                  std::array<real_type,3> tmp_min, tmp_max;
                  for( unsigned jj = 0; jj < 3; ++jj )
                  {
                     real_type box_size = _tile->max()[axis[jj]] - _tile->min()[axis[jj]];
                     tmp_min[jj] = it->min()[axis[jj]] + wall[axis[jj]]*box_size + offs[axis[jj]];
                     tmp_max[jj] = it->max()[axis[jj]] + wall[axis[jj]]*box_size + offs[axis[jj]];
                  }
                  if( _check_overlap( tmp_min, tmp_max ) )
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
                          []( const table_type& x, const table_type& y )
                          {
                             return y.size() < x.size();
                          } );
#ifndef NLOGDEBUG
               LOGD( "Ordered table vector: " );
               for( const auto& tbl : tbl_vec )
                  LOGD( "(", tbl.name(), ", ", tbl.size(), "), " );
               LOGDLN( "" );
#endif

               // Sort the work vector based on lowest amount of work done.
               std::sort( work.begin(), work.end(),
                          []( const std::pair<unsigned long long,int>& x,
                              const std::pair<unsigned long long,int>& y )
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
         _check_overlap( const std::array<real_type,3>& min,
                         const std::array<real_type,3>& max )
         {
            // Clip the box against the parent box.
            std::array<real_type,3> par_min{ { 0, 0, 0 } }, par_max;
            for( unsigned ii = 0; ii < 3; ++ii )
               par_max[ii] = _tile->max()[ii] - _tile->min()[ii];
            std::array<real_type,3> clip_min, clip_max;
            box_box_clip(
               min.begin(), min.end(),
               max.begin(),
               par_min.begin(),
               par_max.begin(),
               clip_min.begin(),
               clip_max.begin()
               );

            // If there is no volume left, return false.
            if( hpc::approx( box_volume( clip_min.begin(), clip_min.end(), clip_max.begin() ), 0.0, 1e-8 ) )
               return false;

            // Check for overlap with cone.
            for( const auto& plane : _planes )
            {
               if( !box_half_space_overlap( clip_min.begin(), clip_min.end(), clip_max.begin(), plane.begin() ) )
                  return false;
            }

            return true;
         }

         void
         _calc_polyhedron()
         {
            // Cache some information from the lightcone.
            real_type ra_min = _tile->lightcone()->min_ra() + _tile->lightcone()->viewing_angle();
            real_type ra_max = _tile->lightcone()->max_ra() + _tile->lightcone()->viewing_angle();
            real_type dec_min = _tile->lightcone()->min_dec();
            real_type dec_max = _tile->lightcone()->max_dec();
            real_type dist_max = _tile->lightcone()->max_dist();

            // Use midpoints of the RA and DEC to find the center
            // point of the furthest plane.
            std::array<real_type,4> end_plane;
            hpc::num::ecs_to_cartesian(
               ra_min + 0.5*(ra_max - ra_min),
               dec_min + 0.5*(dec_max - dec_min),
               end_plane[0], end_plane[1], end_plane[2]
               );
            end_plane[3] = dist_max;

            // Use the midpoint of the RA and the lowest DEC to
            // get the point at the bottom of the curvature.
            std::array<real_type,4> low_plane;
            {
               hpc::num::ecs_to_cartesian(
                  ra_min + 0.5*(ra_max - ra_min),
                  dec_min,
                  low_plane[0], low_plane[1], low_plane[2]
                  );

               // Cross products to get proper plane.
               std::array<real_type,3> z_axis{ { 0, 0, 1 } };
               std::array<real_type,3> left;
               cross_product_3( low_plane, z_axis, left );
               cross_product_3( low_plane, left, z_axis );
               real_type inv_mag = 1.0/magnitude( z_axis.begin(), z_axis.end() );
               low_plane[0] = inv_mag*z_axis[0];
               low_plane[1] = inv_mag*z_axis[1];
               low_plane[2] = inv_mag*z_axis[2];
               low_plane[3] = 0;
            }

            // Calculate the intersection of each of the four lines
            // coming from the edges of my light cone with the
            // plane.
            std::array<real_type,3> zero{ { 0, 0, 0 } };
            std::array<real_type,3> line;
            std::array<real_type,3> pnt;
            std::array<real_type,3> top0, top1, low0, low1;

            // Calculate temporary points.
            hpc::num::ecs_to_cartesian( ra_min, dec_max, top0[0], top0[1], top0[2] );
            hpc::num::ecs_to_cartesian( ra_max, dec_max, top1[0], top1[1], top1[2] );
            hpc::num::ecs_to_cartesian( ra_min, dec_min, low0[0], low0[1], low0[2] );
            hpc::num::ecs_to_cartesian( ra_max, dec_min, low1[0], low1[1], low1[2] );

            // Intersect with end plane to get new points.
            line_half_space_intersection(
               zero.begin(), zero.end(),
               top0.begin(), top0.end(),
               end_plane.begin(),
               pnt.begin()
               );
            top0 = pnt;
            line_half_space_intersection(
               zero.begin(), zero.end(),
               top1.begin(), top1.end(),
               end_plane.begin(),
               pnt.begin()
               );
            top1 = pnt;
            line_half_space_intersection(
               zero.begin(), zero.end(),
               low0.begin(), low0.end(),
               end_plane.begin(),
               pnt.begin()
               );
            low0 = pnt;
            line_half_space_intersection(
               zero.begin(), zero.end(),
               low1.begin(), low1.end(),
               end_plane.begin(),
               pnt.begin()
               );
            low1 = pnt;

            // Use the points to calculate the intersection with the low plane,
            // thus providing the bottom end points.
            line_half_space_intersection(
               top0.begin(), top0.end(),
               low0.begin(), low0.end(),
               low_plane.begin(),
               pnt.begin()
               );
            low0 = pnt;
            line_half_space_intersection(
               top1.begin(), top1.end(),
               low1.begin(), low1.end(),
               low_plane.begin(),
               pnt.begin()
               );
            low1 = pnt;

            // Push points into the list.
            _ph.clear();
            _ph.push_back( std::array<real_type,3>{ { 0, 0, 0 } } );
            _ph.push_back( low0 );
            _ph.push_back( low1 );
            _ph.push_back( top0 );
            _ph.push_back( top1 );
         }

         void
         _calc_polygon_planes()
         {
            _planes.clear();
            std::array<real_type,4> plane;
            _calc_plane( _ph[0], _ph[1], _ph[3], plane );
            _planes.push_back( plane );
            _calc_plane( _ph[0], _ph[3], _ph[4], plane );
            _planes.push_back( plane );
            _calc_plane( _ph[0], _ph[4], _ph[2], plane );
            _planes.push_back( plane );
            _calc_plane( _ph[0], _ph[2], _ph[1], plane );
            _planes.push_back( plane );
            _calc_plane( _ph[1], _ph[2], _ph[3], plane );
            _planes.push_back( plane );
            LOGDLN( "Table iterator planes: ", _planes );

#ifndef NDEBUG
            // Do a quick sanity check. Pick two points, one inside
            // and one outside and check they work correctly.
            std::array<real_type,3> in_pnt{ {
               0.2*_ph[0][0],
               0.2*_ph[0][1],
               0.2*_ph[0][2]
               } };
            for( unsigned ii = 1; ii < 5; ++ii )
            {
               in_pnt[0] += 0.2*_ph[ii][0];
               in_pnt[1] += 0.2*_ph[ii][1];
               in_pnt[2] += 0.2*_ph[ii][2];
            }
            std::array<real_type,3> out_pnt{ {
               _ph[0][0] - 1.0,
               _ph[0][1] - 1.0,
               _ph[0][2] - 1.0
               } };
            bool in = true;
            for( const auto& plane : _planes )
            {
               if( !inside( in_pnt.begin(), in_pnt.end(), plane.begin() ) )
               {
                  LOGBLOCKD( "Not inside: " );
                  LOGDLN( "Plane: ", plane );
                  LOGDLN( "Point: ", in_pnt );
                  LOGDLN( "Evaluated: ", half_space_eval( in_pnt.begin(), in_pnt.end(), plane.begin() ) );
                  in = false;
                  break;
               }
            }
            ASSERT( in );
            in = true;
            for( const auto& plane : _planes )
            {
               if( !inside( out_pnt.begin(), out_pnt.end(), plane.begin() ) )
               {
                  in = false;
                  break;
               }
            }
            ASSERT( !in );
#endif
         }

         template< class Point,
                   class Plane >
         void
         _calc_plane( const Point& point_a,
                      const Point& point_b,
                      const Point& point_c,
                      Plane& plane )
         {
            Point ab;
            ab[0] = point_b[0] - point_a[0];
            ab[1] = point_b[1] - point_a[1];
            ab[2] = point_b[2] - point_a[2];
            Point ac;
            ac[0] = point_c[0] - point_a[0];
            ac[1] = point_c[1] - point_a[1];
            ac[2] = point_c[2] - point_a[2];
            plane[0] = -(ab[1]*ac[2] - ab[2]*ac[1]);
            plane[1] = -(-ab[0]*ac[2] + ab[2]*ac[0]);
            plane[2] = -(ab[0]*ac[1] - ab[1]*ac[0]);
            typename Point::value_type inv_mag = 1.0/sqrt( plane[0]*plane[0] + plane[1]*plane[1] + plane[2]*plane[2] );
            plane[0] *= inv_mag;
            plane[1] *= inv_mag;
            plane[2] *= inv_mag;
            plane[3] = (plane[0]*point_a[0] + plane[1]*point_a[1] + plane[2]*point_a[2]);
         }

      protected:

         const backend_type* _be;
         const tao::tile<real_type>* _tile;
         std::vector<std::array<real_type,3>> _ph;
         std::list<std::array<real_type,4>> _planes;
         std::vector<std::array<real_type,3>> _walls;
         std::vector<table_type> _tables;
         boost::optional<hpc::view<std::vector<std::pair<unsigned long long,int>>>> _work;
         typename std::vector<table_type>::const_iterator _it;
         bool _done;
      };

   }
}

#endif
