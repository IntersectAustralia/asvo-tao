#ifndef tao_modules_table_iterator_hh
#define tao_modules_table_iterator_hh

#include <boost/iterator/iterator_facade.hpp>
#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include <libhpc/containers/combination.hpp>
#include "GrahamScanConvexHull.h"
#include "clip.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class table_iterator
      : public boost::iterator_facade< table_iterator<T>,
                                       const std::string&,
				       std::forward_iterator_tag >
   {
      friend class boost::iterator_core_access;

   public:

      typedef T real_type;
      typedef const std::string& value_type;
      typedef value_type reference_type;

      table_iterator( soci::session& sql,
		      real_type box_size,
		      const array<real_type,3>& box,
		      const array<real_type,3>& offset,
		      const array<int,3>& axis,
		      real_type ra_min,
		      real_type ra_max,
		      real_type dec_min,
		      real_type dec_max,
		      real_type max_dist )
	 : _sql( sql ),
	   _box_size( box_size ),
	   _box( box ),
	   _offs( offset ),
	   _axis( axis ),
	   _ra_min( to_radians( ra_min ) ),
	   _ra_max( to_radians( ra_max ) ),
	   _dec_min( to_radians( dec_min ) ),
	   _dec_max( to_radians( dec_max ) ),
	   _max_dist( max_dist )
      {
	 vector<real_type> perms( 9 );
	 for( unsigned ii = 0; ii < 3; ++ii )
	 {
	    perms[ii] = -1;
	    perms[ii + 3] = 0;
	    perms[ii + 6] = 1;
	 }
	 do
	 {
	    _walls.emplace_back( perms[0], perms[1], perms[2] );
	 }
	 while( boost::next_partial_permutation( perms.begin(), perms.begin() + 3, perms.end() ) );
	 LOGDLN( "Walls: ", _walls );

	 // _wall_planes.resize( 6 );
	 // _wall_planes[0] = array<real_type,4>(  1,  0,  0, 0 );
	 // _wall_planes[1] = array<real_type,4>(  0,  1,  0, 0 );
	 // _wall_planes[2] = array<real_type,4>(  0,  0,  1, 0 );
	 // _wall_planes[3] = array<real_type,4>( -1,  0,  0, -_box_size );
	 // _wall_planes[4] = array<real_type,4>(  0, -1,  0, -_box_size );
	 // _wall_planes[5] = array<real_type,4>(  0,  0, -1, -_box_size );

	 _begin();
      }

      bool
      done() const
      {
	 return _it == _table_names.cend();
      }

   protected:

      void
      increment()
      {
	 ++_it;
      }

      bool
      equal( const table_iterator& op ) const
      {
         return _it == op._it;
      }

      const reference_type
      dereference() const
      {
         return *_it;
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

	 // // Now apply the rotations. These are always 90 degree rotations,
	 // // so it is just a matter of swapping axiis.
	 // for( auto& pnt : _ph )
	 // {
	 //    auto tmp = pnt;
	 //    for( unsigned ii = 0; ii < 3; ++ii )
	 //       pnt[ii] = tmp[_axis[ii]];
	 // }

	 // Now convert to planes.
	 _calc_polygon_planes();

	 // Extract all the boxes.
	 std::vector<double> minx, miny, minz, maxx, maxy, maxz;
	 std::vector<std::string> names;
	 {
	    int size;
	    _sql << "SELECT COUNT(*) FROM summary", soci::into( size );
	    minx.resize( size );
	    miny.resize( size );
	    minz.resize( size );
	    maxx.resize( size );
	    maxy.resize( size );
	    maxz.resize( size );
	    names.resize( size );
	 }
	 _sql << "SELECT minx, miny, minz, maxx, maxy, maxz, tablename FROM summary",
	    soci::into( minx ), soci::into( miny ), soci::into( minz ),
	    soci::into( maxx ), soci::into( maxy ), soci::into( maxz ),
	    soci::into( names );

	 set<string> table_names;
	 for( unsigned ii = 0; ii < names.size(); ++ii )
	 {
	    array<real_type,3> min( minx[ii], miny[ii], minz[ii] ), max( maxx[ii], maxy[ii], maxz[ii] );

	    // // Rotate.
	    // for( unsigned ii = 0; ii < 3; ++ii )
	    // {
	    //    min[ii] += _offs[ii];
	    //    max[ii] += _offs[ii];
	    // }

	    // // Offset this box.
	    // for( unsigned ii = 0; ii < 3; ++ii )
	    // {
	    //    min[ii] += _offs[ii];
	    //    max[ii] += _offs[ii];
	    // }

	    // // Check if this box has at least any part inside the
	    // // walls.
	    // if( _check_overlap( min, max ) )
	    // {
	    //    _table_names.push_back( names[ii] );
	    //    continue;
	    // }

	    // Apply each periodic side to the box and check.
	    for( const auto& wall : _walls )
	    {
	       array<real_type,3> tmp_min, tmp_max;
	       for( unsigned ii = 0; ii < 3; ++ii )
	       {
		  tmp_min[ii] = min[_axis[ii]] + wall[_axis[ii]]*_box_size + _offs[_axis[ii]];
		  tmp_max[ii] = max[_axis[ii]] + wall[_axis[ii]]*_box_size + _offs[_axis[ii]];
	       }
	       if( _check_overlap( tmp_min, tmp_max ) )
	       {
		  table_names.insert( names[ii] );
		  break;
	       }
	    }
	 }

	 _table_names.reallocate( table_names.size() );
	 std::copy( table_names.begin(), table_names.end(), _table_names.begin() );
	 _it = _table_names.begin();
      }

      bool
      _check_overlap( const array<real_type,3>& min,
		      const array<real_type,3>& max )
      {
	 LOG_ENTER();

	 // Clip the box against the parent box.
	 array<real_type,3> par_min( 0, 0, 0), par_max( _box_size, _box_size, _box_size );
	 array<real_type,3> clip_min, clip_max;
	 box_box_clip(
	    min.begin(), min.end(),
	    max.begin(),
	    par_min.begin(),
	    par_max.begin(),
	    clip_min.begin(),
	    clip_max.begin()
	    );
	 LOGDLN( "Original box: ", min, ", ", max );
	 LOGDLN( "Clipped box:  ", clip_min, ", ", clip_max );

	 // If there is no volume left, return false.
	 if( num::approx( box_volume( clip_min.begin(), clip_min.end(), clip_max.begin() ), 0.0, 1e-8 ) )
	 {
	    LOGDLN( "Zero sized box." );
	    LOG_EXIT();
	    return false;
	 }

	 // Check for overlap with cone.
	 for( const auto& plane : _planes )
	 {
	    if( !box_half_space_overlap( clip_min.begin(), clip_min.end(), clip_max.begin(), plane.begin() ) )
	    {
	       LOGDLN( "Box outside lightcone geometry." );
	       LOG_EXIT();
	       return false;
	    }
	 }
	 LOGDLN( "Box inside lightcone geometry." );
	 LOG_EXIT();
	 return true;
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

      void
      _calc_polygon_planes()
      {
	 vector<array<real_type,3> > ph( _ph.size() );
	 std::copy( _ph.begin(), _ph.end(), ph.begin() );

	 _planes.clear();
	 array<real_type,4> plane;
	 _calc_plane( ph[0], ph[1], ph[3], plane );
	 _planes.push_back( plane );
	 _calc_plane( ph[0], ph[3], ph[4], plane );
	 _planes.push_back( plane );
	 _calc_plane( ph[0], ph[4], ph[2], plane );
	 _planes.push_back( plane );
	 _calc_plane( ph[0], ph[2], ph[1], plane );
	 _planes.push_back( plane );
	 _calc_plane( ph[1], ph[2], ph[3], plane );
	 _planes.push_back( plane );

#ifndef NDEBUG
	 // Do a quick sanity check. Pick two points, one inside
	 // and one outside and check they work correctly.
	 array<real_type,3> in_pnt(
	    0.2*ph[0][0],
	    0.2*ph[0][1],
	    0.2*ph[0][2]
	    );
	 for( unsigned ii = 1; ii < 4; ++ii )
	 {
	    in_pnt[0] += 0.2*ph[ii][0];
	    in_pnt[1] += 0.2*ph[ii][1];
	    in_pnt[2] += 0.2*ph[ii][2];
	 }
	 array<real_type,3> out_pnt(
	    ph[0][0] - 1.0,
	    ph[0][1] - 1.0,
	    ph[0][2] - 1.0
	    );
	 bool in = true;
	 for( const auto& plane : _planes )
	 {
	    if( !inside( in_pnt.begin(), in_pnt.end(), plane.begin() ) )
	    {
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
	 Point ab( point_b[0] - point_a[0], point_b[1] - point_a[1], point_b[2] - point_a[2] );
	 Point ac( point_c[0] - point_a[0], point_c[1] - point_a[1], point_c[2] - point_a[2] );
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

      list<array<real_type,3> > _ph;
      list<array<real_type,4> > _planes;
      vector<array<real_type,3> > _walls;
      // vector<array<real_type,4> > _wall_planes;
      vector<string> _table_names;
      vector<string>::const_iterator _it;

      soci::session& _sql;
      real_type _box_size;
      array<real_type,3> _box;
      array<real_type,3> _offs;
      array<int,3> _axis;
      real_type _ra_min, _ra_max;
      real_type _dec_min, _dec_max;
      real_type _max_dist;
   };
}

#endif
