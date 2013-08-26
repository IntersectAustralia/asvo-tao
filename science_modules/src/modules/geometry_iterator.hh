#ifndef tao_modules_geometry_iterator_hh
#define tao_modules_geometry_iterator_hh

#include <boost/iterator/iterator_facade.hpp>
#include <libhpc/libhpc.hh>
#include "GrahamScanConvexHull.h"
#include "clip.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class geometry_iterator
      : public boost::iterator_facade< geometry_iterator<T>,
                                       const list<array<T,2> >&,
				       std::forward_iterator_tag,
                                       const list<array<T,2> > >
   {
      friend class boost::iterator_core_access;

   public:

      typedef T real_type;
      typedef list<array<real_type,2> > value_type;
      typedef list<array<real_type,2> > reference_type;

      geometry_iterator( real_type box_size,
			 const array<real_type,3>& box,
			 const array<real_type,3>& offset,
			 const array<int,3>& axis,
			 real_type ra_min,
			 real_type ra_max,
			 real_type dec_min,
			 real_type dec_max,
			 real_type max_dist )
	 : _box_size( box_size ),
	   _box( box ),
	   _offs( offset ),
	   _axis( axis ),
	   _ra_min( to_radians( ra_min ) ),
	   _ra_max( to_radians( ra_max ) ),
	   _dec_min( to_radians( dec_min ) ),
	   _dec_max( to_radians( dec_max ) ),
	   _max_dist( max_dist )
      {
	 _walls.resize( 9 );
	 _walls[0][0] = -1; _walls[0][1] = -1;
	 _walls[1][0] = 0;  _walls[1][1] = -1;
	 _walls[2][0] = 1;  _walls[2][1] = -1;
	 _walls[3][0] = -1; _walls[3][1] = 0;
	 _walls[4][0] = 0;  _walls[4][1] = 0;
	 _walls[5][0] = 1;  _walls[5][1] = 0;
	 _walls[6][0] = -1; _walls[6][1] = 1;
	 _walls[7][0] = 0;  _walls[7][1] = 1;
	 _walls[8][0] = 1;  _walls[8][1] = 1;
	 _begin();
      }

      bool
      done() const
      {
	 return _it == _walls.cend() && _val.empty();
      }

   protected:

      void
      increment()
      {
	 // Clear out the value.
	 _val.clear();

	 // Only proceed if we're not at the end.
	 if( _it != _walls.cend() )
	 {
	    do
	    {
	       // Need a temporary place to hold the new shape.
	       value_type tmp;

	       // Translate the various dimensions.
	       for( const auto& pnt : _base )
	       {
		  array<real_type,2> new_pnt;
		  for( unsigned ii = 0; ii < 2; ++ii )
		     new_pnt[ii] = pnt[ii] + (*_it)[ii]*_box_size;

		  // Insert the new point into the value.
		  tmp.push_back( new_pnt );
	       }

	       // Now clip the translated shape.
	       _val.clear();
	       clip_polygon(
		  _box_size,
		  tmp.begin(), tmp.end(),
		  std::insert_iterator<value_type>( _val, _val.begin() )
		  );
	    }
	    while( ++_it != _walls.cend() && _val.empty() );
	 }
      }

      bool
      equal( const geometry_iterator& op ) const
      {
         return _val == op._val;
      }

      const reference_type
      dereference() const
      {
         return _val;
      }

      void
      _begin()
      {
	 // Need the points of the polyhedron. Don't foget to
	 // offset by the box we're using.
	 _calc_polyhedron();
	 for( auto& pnt : _ph )
	 {
	    for( unsigned ii = 0; ii < 3; ++ii )
	       pnt[ii] -= _box[ii];
	 }

	 // Now apply the rotations. These are always 90 degree rotations,
	 // so it is just a matter of swapping axiis.
	 for( auto& pnt : _ph )
	 {
	    auto tmp = pnt;
	    for( unsigned ii = 0; ii < 3; ++ii )
	       pnt[ii] = tmp[_axis[ii]];
	 }

	 // Because of the way I've defined my x,y,z system,
	 // I need to clip out y. Actually, that's not true.
	 // I need to clip Z to match Amr's method.
	 list<array<real_type,2>> pg;
	 for( const auto& pnt : _ph )
	    pg.emplace_back( pnt[0], pnt[1] );

	 // Now compute the convex hull.
	 list<array<real_type,2>> hull;
	 {
	    std::vector<point2d> __pnts( pg.size() ), __hull;
	    {
	       unsigned ii = 0;
	       for( const auto& pnt : pg )
		  __pnts[ii++] = point2d( pnt[0], pnt[1] );
	    }
	    GrahamScanConvexHull()( __pnts, __hull );
	    for( const auto& pnt : __hull )
	       hull.push_back( array<real_type,2>( pnt.x, pnt.y ) );

	    // Need to reverse the hull, as we need elements
	    // in counter clockwise order.
	    hull.reverse();
	 }

	 // Clip the convex hull against the box boundary.
	 clip_polygon(
	    _box_size,
	    hull.begin(), hull.end(),
	    std::insert_iterator<value_type>( _base, _base.begin() )
	    );

	 // Offset by the random translation.
	 for( auto& pnt : _base )
	 {
	    // We skip the Z dimension, as any translation
	    // in that axis will not have any effect.
	    for( unsigned ii = 0; ii < 2; ++ii )
	       pnt[ii] += _offs[ii];
	 }

	 // Use the increment routine to find the first non-empty
	 // shape.
	 _it = _walls.cbegin();
	 increment();
      }

      void
      _calc_polyhedron()
      {
	 // Use midpoints of the RA and DEC to find the center
	 // point of my plane.
	 array<real_type,4> plane;
	 numerics::ecs_to_cartesian(
	    _ra_min + 0.5*(_ra_max - _ra_min),
	    _dec_min + 0.5*(_dec_max - _dec_min),
	    plane[0], plane[1], plane[2]
	    );

	 // Calculate the distance from the origin to the plane.
	 plane[3] = _max_dist;

	 // Insert the first point at 0,0,0.
	 _ph.clear();
	 _ph.push_back( array<real_type,3>( 0, 0, 0 ) );

	 // Calculate the intersection of each of the four lines
	 // coming from the edges of my light cone with the
	 // plane.
	 array<real_type,3> zero( 0, 0, 0 );
	 array<real_type,3> line;
	 array<real_type,3> pnt;
	 numerics::ecs_to_cartesian( _ra_min, _dec_min, line[0], line[1], line[2] );
	 line_half_space_intersection(
	    zero.begin(), zero.end(),
	    line.begin(), line.end(),
	    plane.begin(),
	    pnt.begin()
	    );
	 _ph.push_back( pnt );
	 numerics::ecs_to_cartesian( _ra_max, _dec_min, line[0], line[1], line[2] );
	 line_half_space_intersection(
	    zero.begin(), zero.end(),
	    line.begin(), line.end(),
	    plane.begin(),
	    pnt.begin()
	    );
	 _ph.push_back( pnt );
	 numerics::ecs_to_cartesian( _ra_min, _dec_max, line[0], line[1], line[2] );
	 line_half_space_intersection(
	    zero.begin(), zero.end(),
	    line.begin(), line.end(),
	    plane.begin(),
	    pnt.begin()
	    );
	 _ph.push_back( pnt );
	 numerics::ecs_to_cartesian( _ra_max, _dec_max, line[0], line[1], line[2] );
	 line_half_space_intersection(
	    zero.begin(), zero.end(),
	    line.begin(), line.end(),
	    plane.begin(),
	    pnt.begin()
	    );
	 _ph.push_back( pnt );
      }

   protected:

      real_type _box_size;
      array<real_type,3> _box;
      array<real_type,3> _offs;
      array<int,3> _axis;
      value_type _base;
      value_type _val;
      list<array<real_type,3> > _ph;
      vector<array<real_type,2> > _walls;
      typename vector<array<real_type,2> >::const_iterator _it;

      real_type _ra_min, _ra_max;
      real_type _dec_min, _dec_max;
      real_type _max_dist;
   };
}

#endif
