#ifndef tao_base_box_table_iterator_hh
#define tao_base_box_table_iterator_hh

#include <boost/iterator/iterator_facade.hpp>
#include <libhpc/libhpc.hh>
#include <libhpc/containers/combination.hpp>
#include "clip.hh"
#include "rdb_backend.hh"
#include "box.hh"

class box_table_iterator_suite;

namespace tao {
   namespace backends {
      using namespace hpc;

      template< class Backend >
      class box_table_iterator
         : public boost::iterator_facade< box_table_iterator<Backend>,
                                          const typename rdb<typename Backend::real_type>::table_type&,
                                          std::forward_iterator_tag,
                                          const typename rdb<typename Backend::real_type>::table_type& >
      {
         friend class ::box_table_iterator_suite;
         friend class boost::iterator_core_access;

      public:

         typedef Backend backend_type;
         typedef typename Backend::real_type real_type;
         typedef typename rdb<real_type>::table_type table_type;
         typedef const table_type& value_type;
         typedef value_type reference_type;

         box_table_iterator()
            : _done( true )
         {
         }

         box_table_iterator( const box<real_type>* box,
                             const backend_type* backend )
            : _box( box ),
              _be( backend ),
              _done( false )
         {
            // Only go through construction if this isn't the end
            // iterator.
            if( !_done )
            {
               // Construct the walls I'll be using to clip the lightcone
               // approximation.
               vector<real_type> perms( 9 );
               for( unsigned ii = 0; ii < 3; ++ii )
               {
                  perms[ii] = -1;
                  perms[ii + 3] = 0;
                  perms[ii + 6] = 1;
               }
               do
               {
                  _walls.emplace_back( array<real_type,3>{ { perms[0], perms[1], perms[2] } } );
               }
               while( boost::next_partial_permutation( perms.begin(), perms.begin() + 3, perms.end() ) );

               // Get to the first position.
               _begin();
            }
         }

         box_table_iterator( const box_table_iterator& src )
            : _be( src._be ),
              _box( src._box ),
              _walls( src._walls ),
              _tbls( src._tbls ),
              _done( src._done )
         {
            // Iterator needs to be modified.
            _it = _tbls.begin() + (src._it - src._tbls.begin());
         }

      protected:

         void
         increment()
         {
            if( ++_it == _tbls.end() )
               _done = true;
         }

         bool
         equal( const box_table_iterator& op ) const
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
            LOGDLN( "Calculating overlapping tables.", setindent( 2 ) );

            // Cache some information.
            const array<unsigned,3>& axis = _box->rotation();
            const array<real_type,3>& offs = _box->translation();

            // Shift each table bounding box along each wall direction to
            // see if there is any periodic overlap with the box.
            set<table_type> tables;
            for( auto it = _be->table_begin(); it != _be->table_end(); ++it )
            {
               // Apply each periodic side to the box and check.
               for( const auto& wall : _walls )
               {
                  array<real_type,3> tmp_min, tmp_max;
                  for( unsigned jj = 0; jj < 3; ++jj )
                  {
                     real_type box_size = _box->max()[axis[jj]] - _box->min()[axis[jj]];
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

            // Transfer to a vector.
            _tbls.reallocate( tables.size() );
            std::copy( tables.begin(), tables.end(), _tbls.begin() );
            _it = _tbls.begin();

            LOGDLN( "Done.", setindent( -2 ) );
         }

         bool
         _check_overlap( const array<real_type,3>& min,
                         const array<real_type,3>& max )
         {
            // Clip the box against the parent box.
            array<real_type,3> par_min{ { 0, 0, 0 } }, par_max;
            for( unsigned ii = 0; ii < 3; ++ii )
               par_max[ii] = _box->max()[ii] - _box->min()[ii];
            array<real_type,3> clip_min, clip_max;
            box_box_clip(
               min.begin(), min.end(),
               max.begin(),
               par_min.begin(),
               par_max.begin(),
               clip_min.begin(),
               clip_max.begin()
               );

            // If there is no volume left, return false.
            if( num::approx( box_volume( clip_min.begin(), clip_min.end(), clip_max.begin() ), 0.0, 1e-8 ) )
               return false;

            return true;
         }

      protected:

         const backend_type* _be;
         const box<real_type>* _box;
         vector<array<real_type,3>> _walls;
         vector<table_type> _tbls;
         typename vector<table_type>::const_iterator _it;
         bool _done;
      };

   }
}

#endif
