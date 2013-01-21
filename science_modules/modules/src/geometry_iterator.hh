#ifndef tao_modules_geometry_iterator_hh
#define tao_modules_geometry_iterator_hh

#include <boost/geometry/geometry.hpp>
#include <boost/iterator/iterator_facade.hpp>
#include <libhpc/libhpc.hh>

namespace tao {
   using namespace hpc;

   template< class T >
   class geometry_iterator
      : public boost::iterator_facade< geometry_iterator<T>,
                                       const list<array<T,2> >&,
				       std::forward_iterator_tag,
                                       const list<array<T,2> >& >
   {
      friend class boost::iterator_core_access;

   public:

      typedef T real_type;
      typedef list<array<real_type,2> > value_type;
      typedef list<array<real_type,2> > reference_type;

      geometry_iterator( real_type box_size,
			 const array<real_type,3>& box,
			 const array<real_type,3>& offset,
			 const array<int,3>& axis )
	 : _box_size,
	   _box( box ),
	   _offs( offset ),
	   _axis( axis )
      {
	 _begin();
      }

   protected:

      void
      _begin()
      {
	 // Need the points of the polyhedron. Don't foget to
	 // offset by the box we're using.
	 list<array<real_type,3>> ph;
	 ph.push_back( array<real_type,3>( p[0] - (*_box)[0],
					   p[1] - (*_box)[1],
					   p[2] - (*_box)[2] ) );

	 // Now apply the rotations. These are always 90 degree rotations,
	 // so it is just a matter of swapping axiis.
	 for( auto& pnt : ph )
	 {
	    auto tmp = pnt;
	    for( unsigned ii = 0; ii < _axis_swap; ++ii )
	       pnt[ii] = tmp[_axis[ii]];
	 }

	 // Now clip out the Z direction to project onto
	 // the X-Y plane.
	 list<array<real_type,2>> pg;
	 for( const auto& pnt : ph )
	    pg.emplace_back( pnt[0], pnt[1] );

	 // Now compute the convex hull.
	 list<array<real_type,2>> hull;
	 boost::geometry::convex_hull( pg, hull );

	 // Clip the convex hull against the box boundary.
	 clip_polygon( _box_size, hull.begin(), hull.end(), _base.begin() );

	 // Offset by the random translation.
	 for( auto& pnt : _base )
	 {
	    // We skip the Z dimension, as any translation
	    // in that axis will not have any effect.
	    for( unsigned ii = 0; ii < 2; ++ii )
	       pnt[ii] += _offs[ii];
	 }

	 // Clip against the bounding box, keeping all interior
	 // points and creating new lines against the walls.
	 clip_polygon( _box_size, _base.begin(), _base.end(), _cur.begin() );

	 // Repeat while empty until all possibilities have been taken care of.
	 // TODO
      }

      void
      increment()
      {
         // If low now points to the end, add the remaining range.
         if( _low == _upp )
         {
            if( _cur_rng.finish() < _range.finish() )
            {
               _cur_rng.set( _cur_rng.finish(), _range.finish() );
               auto res = ((typename range_map<T,Value>::super_type&)_map).insert( _cur_rng, _value );
               ASSERT( res.second, "Element should not have existed" );
               _cur_val = &res.first->second;
            }
            else
               _cur_val = NULL;
         }

         // Where are we compared to the last visited finish point?
         else if( _cur_rng.finish() < _low->first.start() )
         {
            // Fill in the gap.
            _cur_rng.set( _cur_rng.finish(), _low->first.start() );
            auto res = ((typename range_map<T,Value>::super_type&)_map).insert( _cur_rng, _value );
            ASSERT( res.second, "Element should not have existed" );
            _cur_val = &res.first->second;
         }
         else
         {
            _overlap();
            ++_low;
         }
      }

      bool
      equal( const geometry_iterator& op ) const
      {
         return _cur_val == op._cur_val;
      }

      const reference_type
      dereference() const
      {
         return _val;
      }

   protected:

      value_type _val;
   };
}

#endif
