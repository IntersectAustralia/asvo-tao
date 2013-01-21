#ifndef tao_modules_clip_hh
#define tao_modules_clip_hh

#include <boost/iterator/zip_iterator.hpp>
#include <libhpc/libhpc.hh>

namespace tao {
   using namespace hpc;

   template< class Iterator1,
	     class Iterator2 >
   typename std::iterator_traits<Iterator1>::value_type
   inner_product( Iterator1 first1,
		  const Iterator1& last1,
		  Iterator2 first2 )
   {
      typedef typename std::iterator_traits<Iterator1>::value_type real_type;
      real_type sum = 0.0;
      while( first1 != last1 )
	 sum += (*first1++)*(*first2++);
      return sum;
   }

   template< class PointIterator,
	     class HalfSpaceIterator >
   bool
   inside( PointIterator point_first,
	   const PointIterator& point_last,
	   HalfSpaceIterator half_space_first )
   {
      typedef typename std::iterator_traits<PointIterator>::value_type real_type;
      real_type sum = 0.0;
      while( point_first != point_last )
	 sum += (*half_space_first++)*(*point_first++);
      return sum >= *half_space_first;
   }

   template< class PointIterator,
	     class HalfSpaceIterator >
   typename std::iterator_traits<PointIterator>::value_type
   half_space_eval( PointIterator point_first,
		    const PointIterator& point_last,
		    HalfSpaceIterator half_space_first )
   {
      typedef typename std::iterator_traits<PointIterator>::value_type real_type;
      real_type sum = 0.0;
      while( point_first != point_last )
	 sum += (*half_space_first++)*(*point_first++);
      return sum - *half_space_first;
   }

   template< class Point1Iterator,
	     class Point2Iterator,
	     class HalfSpaceIterator,
	     class ResultIterator >
   void
   line_half_space_intersection( Point1Iterator point1_first,
				 const Point1Iterator& point1_last,
				 Point2Iterator point2_first,
				 const Point2Iterator& point2_last,
				 HalfSpaceIterator half_space_first,
				 ResultIterator result )
   {
      typedef typename std::iterator_traits<Point1Iterator>::value_type real1_type;
      typedef typename std::iterator_traits<Point2Iterator>::value_type real2_type;
      auto func = expand2(
	 compose2(
	    std::minus<real1_type>(),
	    element_tuple<boost::tuple<real2_type,real1_type>,0>(),
	    element_tuple<boost::tuple<real2_type,real1_type>,1>()
	    )
	 );
	 
      real1_type denom = inner_product(
      	 boost::make_transform_iterator(
      	    boost::make_zip_iterator( boost::make_tuple( point2_first, point1_first ) ),
      	    func
      	    ),
      	 boost::make_transform_iterator(
      	    boost::make_zip_iterator( boost::make_tuple( point2_last, point1_last ) ),
      	    func
      	    ),
      	 half_space_first
      	 );
      denom = 1.0/denom;
      real1_type enumr = half_space_eval( point1_first, point1_last, half_space_first );
      while( point1_first != point1_last )
      {
      	 *result++ = *point1_first - (*point2_first - *point1_first)*enumr*denom;
	 ++point1_first;
	 ++point2_first;
      }
   }

   template< class HalfSpaceIterator,
	     class PointIterator,
	     class ResultIterator >
   void
   clip_edge( const HalfSpaceIterator& half_space,
	      PointIterator first,
	      const PointIterator& last,
	      ResultIterator result )
   {
      typedef typename std::iterator_traits<HalfSpaceIterator>::value_type real_type;

      // If we have nothing, return nothing.
      if( first == last )
	 return;

      // Need to keep track of two points per edge.
      PointIterator pnts[2], first_point = first;
      unsigned edge[2] = { 0, 1 };
      bool intersect[2], first_intersect;

      // Set the first point and check if it's interior.
      pnts[0] = first++;
      intersect[0] = inside( pnts[0]->begin(), pnts[0]->end(), half_space );
      if( intersect[0] )
      {
	 *result++ = *pnts[0];
	 first_intersect = true;
      }
      else
	 first_intersect = false;

      // Now process remaining edges/points.
      while( first != last )
      {
	 pnts[edge[1]] = first++;
	 intersect[edge[1]] = inside( pnts[edge[1]]->begin(), pnts[edge[1]]->end(), half_space );

	 // Case 1, edge goes from outside window to outside.
	 if( !intersect[edge[0]] && !intersect[edge[1]] )
	 {
	    // Do nothing.
	 }

	 // Case 2, edge goes from outside window to inside.
	 else if( !intersect[edge[0]] && intersect[edge[1]] )
	 {
	    // Save both intersection and inside vertex.
	    array<real_type,2> tmp;
	    line_half_space_intersection(
	       pnts[edge[0]]->begin(), pnts[edge[0]]->end(),
	       pnts[edge[1]]->begin(), pnts[edge[1]]->end(),
	       half_space,
	       tmp.begin()
	       );
	    *result++ = tmp;
	    *result++ = *pnts[edge[1]];
	 }

	 // Case 3, edge goes from inside window to outside.
	 else if( intersect[edge[0]] && !intersect[edge[1]] )
	 {
	    // Save intersection.
	    array<real_type,2> tmp;
	    line_half_space_intersection(
	       pnts[edge[0]]->begin(), pnts[edge[0]]->end(),
	       pnts[edge[1]]->begin(), pnts[edge[1]]->end(),
	       half_space,
	       tmp.begin()
	       );
	    *result++ = tmp;
	 }

	 // Case 4, edge goes from inside window to inside.
	 else
	 {
	    // Save inside vertex.
	    *result++ = *pnts[edge[1]];
	 }

	 // Swap edge ends.
	 std::swap( edge[0], edge[1] );
      }

      // Are the first and last points on opposite sides? We use edge[0]
      // because of the swap.
      if( first_intersect ^ intersect[edge[0]] )
      {
	 array<real_type,2> tmp;
	 line_half_space_intersection(
	    pnts[edge[0]]->begin(), pnts[edge[0]]->end(),
	    first_point->begin(), first_point->end(),
	    half_space,
	    tmp.begin()
	    );
	 *result++ = tmp;
      }
   }

   template< class PointIterator,
	     class ResultIterator >
   void
   clip_polygon( double box_size,
		 PointIterator poly_start,
		 const PointIterator& poly_finish,
		 ResultIterator result )
   {
      typedef typename std::iterator_traits<PointIterator>::value_type point_type;
      typedef typename point_type::value_type real_type;

      // We will need temporary storage.
      list<point_type> tmp[2];

      // Need to know the number of dimensions to clip in.
      unsigned dim = poly_start->size();

      // Prepare the plane equation.
      vector<real_type> hsp( dim + 1 );

      // First clip the X axis.
      std::fill( hsp.begin(), hsp.end(), 0 );
      hsp[0] = 1;
      clip_edge( hsp.begin(), poly_start, poly_finish,
		 std::insert_iterator<list<point_type> >( tmp[0], tmp[0].begin() ) );
      hsp[0] = -1;
      hsp[dim] = -box_size;
      if( dim == 1 )
      {
	 clip_edge( hsp.begin(), tmp[0].begin(), tmp[0].end(), result );
      }
      else
      {
	 clip_edge( hsp.begin(), tmp[0].begin(), tmp[0].end(),
		    std::insert_iterator<list<point_type> >( tmp[1], tmp[1].begin() ) );
      }

      // Now clip middle dimensions.
      for( unsigned ii = 1; ii < dim - 1; ++ii )
      {
	 std::fill( hsp.begin(), hsp.end(), 0 );
	 hsp[ii] = 1;
	 tmp[0].clear();
	 clip_edge( hsp.begin(), tmp[1].begin(), tmp[1].end(),
		    std::insert_iterator<list<point_type> >( tmp[0], tmp[0].begin() ) );
	 hsp[ii] = -1;
	 hsp[dim] = -box_size;
	 tmp[1].clear();
	 clip_edge( hsp.begin(), tmp[0].begin(), tmp[0].end(),
		    std::insert_iterator<list<point_type> >( tmp[1], tmp[1].begin() ) );
      }

      // Now the final dimension.
      std::fill( hsp.begin(), hsp.end(), 0 );
      hsp[dim - 1] = 1;
      tmp[0].clear();
      clip_edge( hsp.begin(), tmp[1].begin(), tmp[1].end(),
		 std::insert_iterator<list<point_type> >( tmp[0], tmp[0].begin() ) );
      hsp[dim - 1] = -1;
      hsp[dim] = -box_size;
      clip_edge( hsp.begin(), tmp[0].begin(), tmp[0].end(), result );
   }
}

#endif
