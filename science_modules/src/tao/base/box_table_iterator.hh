#ifndef tao_base_box_table_iterator_hh
#define tao_base_box_table_iterator_hh

#include <vector>
#include <set>
#include <boost/iterator/iterator_facade.hpp>
#include <libhpc/algorithm/combination.hpp>
#include <libhpc/numerics/clip.hh>
#include "rdb_backend.hh"
#include "box.hh"

namespace tao {
   namespace backends {

      template< class Backend >
      class box_table_iterator
         : public boost::iterator_facade< box_table_iterator<Backend>,
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

         box_table_iterator()
	    : _box( 0 ),
	      _be( 0 ),
	      _done( true )
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
               // Get to the first position.
               _begin();
            }
         }

         box_table_iterator( const box_table_iterator& src )
            : _be( src._be ),
              _box( src._box ),
              _tbls( src._tbls ),
              _done( src._done )
         {
            // Iterator needs to be modified.
            _it = _tbls.begin() + (src._it - src._tbls.begin());
         }

         box_table_iterator&
         operator=( const box_table_iterator& op )
         {
            _be = op._be;
            _box = op._box;
            _tbls = op._tbls;
            _done = op._done;

            // Iterator needs to be modified.
            _it = _tbls.begin() + (op._it - op._tbls.begin());

            return *this;
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
            LOGBLOCKD( "Calculating overlapping tables." );

            // Shift each table bounding box along each wall direction to
            // see if there is any periodic overlap with the box.
            std::set<table_type> tables;
            for( auto it = _be->table_begin(); it != _be->table_end(); ++it )
            {
	       // Check if the table overlaps the box size.
	       bool okay = true;
	       for( unsigned ii = 0; ii < 3; ++ii )
	       {
		  if( it->min()[ii] > _box->max()[ii] || it->max()[ii] < _box->min()[ii] )
		  {
		     okay = false;
		     break;
		  }
	       }
	       if( okay )
		  tables.insert( *it );
            }

            // Transfer to a vector, leaving out any tables not in my
	    // parallel set.
	    unsigned first_table = (mpi::comm::world.rank()*tables.size())/mpi::comm::world.size();
	    unsigned last_table = ((mpi::comm::world.rank() + 1)*tables.size())/mpi::comm::world.size();
            _tbls.reallocate( last_table - first_table );
	    {
	       auto it = tables.begin();
	       unsigned ii;
	       for( ii = 0; ii < first_table; ++ii, ++it );
	       for( ; ii < last_table; ++ii, ++it )
		  _tbls[ii - first_table] = *it;
	    }
	    LOGILN( "Overlapping tables: ", _tbls );
            _it = _tbls.begin();

            // If there are no tables flag that we're done.
            _done = _tbls.empty();
         }

      protected:

         const backend_type* _be;
         const box<real_type>* _box;
         std::vector<table_type> _tbls;
         typename std::vector<table_type>::const_iterator _it;
         bool _done;
      };

   }
}

#endif
