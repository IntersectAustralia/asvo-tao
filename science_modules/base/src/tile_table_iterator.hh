#ifndef tao_base_tile_table_iterator_hh
#define tao_base_tile_table_iterator_hh

#include <boost/iterator/iterator_facade.hpp>
#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include <libhpc/containers/combination.hpp>
#include "GrahamScanConvexHull.h"
#include "clip.hh"

namespace tao {
   namespace backends {
   using namespace hpc;

   template< class Backend >
   class tile_table_iterator
      : public boost::iterator_facade< tile_table_iterator<T>,
                                       const typename rdb<T>::table&
				       std::forward_iterator_tag,
                                       const typename rdb<T>::table& >
   {
      friend class boost::iterator_core_access;

   public:

      typedef Backend backend_type;
      typedef typename Backend::real_type real_type;
      typedef typename rdb<real_type>::table table_type;
      typedef const table_type& value_type;
      typedef value_type reference_type;

      tile_table_iterator( const tao::tile& tile,
                           const backend_type& backend,
                           bool done = false )
         : _tile( tile ),
           _be( backend ),
           _done( done )
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
               _walls.emplace_back( perms[0], perms[1], perms[2] );
            }
            while( boost::next_partial_permutation( perms.begin(), perms.begin() + 3, perms.end() ) );

            // Get to the first position.
            _begin();
         }
      }

   protected:

      void
      increment()
      {
	 ++_it;
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
         LOGDLN( "Calculating overlapping tables.", setindent( 2 ) );

	 // Need the points of the polyhedron. Don't foget to
	 // offset by the box we're using.
	 _calc_polyhedron();
	 for( auto& pnt : _ph )
	 {
	    for( unsigned ii = 0; ii < 3; ++ii )
	       pnt[ii] -= _tile.min()[ii];
	 }

	 // Now convert to planes.
	 _calc_polygon_planes();

         // Cache some information.
         const array<unsigned,3>& axis = _tile.rotation();
         const array<real_type,3>& offs = _tile.translation();

         // Shift each table bounding box along each wall direction to
         // see if there is any periodic overlap with the cone.
	 set<table_type> tables;
         for( auto it = _be.table_begin(); it != _be.table_end(); ++it )
	 {
	    // Apply each periodic side to the box and check.
	    for( const auto& wall : _walls )
	    {
	       array<real_type,3> tmp_min, tmp_max;
	       for( unsigned jj = 0; jj < 3; ++jj )
	       {
                  real_type box_size = _tile.max()[axis[jj]] - _tile.min()[axis[jj]];
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
	 _tables.reallocate( tables.size() );
	 std::copy( tables.begin(), tables.end(), _tables.begin() );
	 _it = _tables.begin();

         LOGDLN( "Done.", setindent( -2 ) );
      }

      bool
      _check_overlap( const array<real_type,3>& min,
		      const array<real_type,3>& max )
      {
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

	 // If there is no volume left, return false.
	 if( num::approx( box_volume( clip_min.begin(), clip_min.end(), clip_max.begin() ), 0.0, 1e-8 ) )
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
         real_type ra_min = _tile.lightcone().min_ra();
         real_type ra_max = _tile.lightcone().max_ra();
         real_type dec_min = _tile.lightcone().min_dec();
         real_type dec_max = _tile.lightcone().max_dec();
         real_type dist_max = _tile.lightcone().max_dist();

	 // Use midpoints of the RA and DEC to find the center
	 // point of the furthest plane.
	 array<real_type,4> end_plane;
	 numerics::ecs_to_cartesian(
	    ra_min + 0.5*(ra_max - ra_min),
	    dec_min + 0.5*(dec_max - dec_min),
	    end_plane[0], end_plane[1], end_plane[2],
	    );
	 end_plane[3] = dist_max;

         // Use the midpoint of the RA and the lowest DEC to
         // get the point at the bottom of the curvature.
         array<real_type,4> low_plane;
         {
            numerics::ecs_to_cartesian(
               ra_min + 0.5*(ra_max - ra_min),
               dec_min + 0.5*(dec_max - dec_min),
               low_plane[0], low_plane[1], low_plane[2],
               );

            // Cross products to get proper plane.
            array<real_type,3> y_axis( 0, 1, 0 );
            array<real_type,3> left;
            cross_product_3( low_plane, y_axis, left );
            cross_product_3( low_plane, left, y_axis );
            real_type inv_mag = 1.0/magnitude( y_axis.begin(), y_axis.end() );
            low_plane[0] = inv_mag*y_axis[0];
            low_plane[1] = inv_mag*y_axis[1];
            low_plane[2] = inv_mag*y_axis[2];
            low_plane[3] = 0;
         }

	 // Calculate the intersection of each of the four lines
	 // coming from the edges of my light cone with the
	 // plane.
	 array<real_type,3> zero( 0, 0, 0 );
	 array<real_type,3> line;
	 array<real_type,3> pnt;
         array<real_type,3> top0, top1, low0, low1;

         // Calculate temporary points.
	 numerics::ecs_to_cartesian( _ra_min, _dec_max, top0[0], top0[1], top0[2] );
	 numerics::ecs_to_cartesian( _ra_max, _dec_max, top1[0], top1[1], top1[2] );
	 numerics::ecs_to_cartesian( _ra_min, _dec_min, low0[0], low0[1], low0[2] );
	 numerics::ecs_to_cartesian( _ra_max, _dec_min, low1[0], low1[1], low1[2] );

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
	 _ph.push_back( array<real_type,3>( 0, 0, 0 ) );
         _ph.push_back( low0 );
         _ph.push_back( low1 );
         _ph.push_back( top0 );
         _ph.push_back( top1 );
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
	 LOGDLN( "Table iterator planes: ", _planes );

#ifndef NDEBUG
	 // Do a quick sanity check. Pick two points, one inside
	 // and one outside and check they work correctly.
	 array<real_type,3> in_pnt(
	    0.2*ph[0][0],
	    0.2*ph[0][1],
	    0.2*ph[0][2]
	    );
	 for( unsigned ii = 1; ii < 5; ++ii )
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
	       LOGDLN( "Not inside: ", setindent( 2 ) );
	       LOGDLN( "Plane: ", plane );
	       LOGDLN( "Point: ", in_pnt );
	       LOGDLN( "Evaluated: ", half_space_eval( in_pnt.begin(), in_pnt.end(), plane.begin() ) );
	       LOGD( setindent( -2 ) );
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

      const tao::tile<real_type>& _tile;
      list<array<real_type,3> > _ph;
      list<array<real_type,4> > _planes;
      vector<array<real_type,3> > _walls;
      vector<table_type> _tables;
      vector<table_type>::const_iterator _it;
      bool _done;
   };

   }
}

#endif
