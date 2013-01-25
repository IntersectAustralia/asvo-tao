#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/modules/clip.hh"

using namespace hpc;
using namespace tao;

///
/// Clip test suite.
///
class clip_suite : public CxxTest::TestSuite
{
public:

   ///
   ///
   ///
   void test_inner_product()
   {
      array<int,3> vec1( 1, 2, 3 ), vec2( 2, 3, 4 );
      TS_ASSERT_EQUALS( inner_product( vec1.begin(), vec1.end(), vec2.begin() ), 20 );
   }

   ///
   ///
   ///
   void test_inside()
   {
      array<double,3> vec1( 2, 1, 1 ), vec2( 0.5, 1, 1 );
      array<double,4> hsp( 1.0/sqrt( 3.0 ), 1/sqrt( 3.0 ), 1/sqrt( 3.0 ), 2 );
      TS_ASSERT( inside( vec1.begin(), vec1.end(), hsp.begin() ) );
      TS_ASSERT( !inside( vec2.begin(), vec2.end(), hsp.begin() ) );
   }

   ///
   ///
   ///
   void test_half_space_eval()
   {
      array<double,3> vec( 2, 3, 4 );
      array<double,4> hsp( 1.0/sqrt( 3.0 ), 1/sqrt( 3.0 ), 1/sqrt( 3.0 ), 2 );
      TS_ASSERT_DELTA( half_space_eval( vec.begin(), vec.end(), hsp.begin() ), 3.196, 1e-3 );
   }

   ///
   ///
   ///
   void test_line_half_space_intersection()
   {
      array<double,3> vec1( -1, -1, -1 ), vec2( 1, 1, 1 ), vec3;
      array<double,4> hsp( 1.0/sqrt( 3.0 ), 1/sqrt( 3.0 ), 1/sqrt( 3.0 ), 2 );
      line_half_space_intersection( vec1.begin(), vec1.end(), vec2.begin(), vec2.end(), hsp.begin(), vec3.begin() );
      for( auto x : vec3 )
	TS_ASSERT_DELTA( x, 1.1547, 1e-3 );
   }

   ///
   ///
   ///
   void test_polygon_area()
   {
      list<array<double,2> > shape;
      shape.emplace_back( 0.0, 0.0 );
      shape.emplace_back( 2.0, 0.0 );
      shape.emplace_back( 2.0, 2.0 );
      shape.emplace_back( 0.0, 2.0 );
      auto area = polygon_area( shape.begin(), shape.end() );
      TS_ASSERT_DELTA( area, 4.0, 1e-6 );
   }

   ///
   ///
   ///
   void test_clip_edge()
   {
      list<array<double,2> > shape, result;
      array<double,3> left_edge( 1.0, 0.0, 0.0 );
      shape.emplace_back( -1.0, 0.0 );
      shape.emplace_back( 1.0, 1.0 );
      shape.emplace_back( 1.0, 2.0 );
      shape.emplace_back( -1.0, 2.0 );
      clip_edge(
	 left_edge.begin(),
	 shape.begin(), shape.end(),
	 std::insert_iterator<list<array<double,2> > >( result, result.begin() )
	 );
   }

   ///
   ///
   ///
   void test_clip_edge_final_edge()
   {
      list<array<double,2> > shape, result;
      array<double,3> left_edge( 1.0, 0.0, 0.0 );
      shape.emplace_back( 1.0, 1.0 );
      shape.emplace_back( 1.0, 2.0 );
      shape.emplace_back( -1.0, 2.0 );
      shape.emplace_back( -1.0, 0.0 );
      clip_edge(
	 left_edge.begin(),
	 shape.begin(), shape.end(),
	 std::insert_iterator<list<array<double,2> > >( result, result.begin() )
	 );
   }

   ///
   ///
   ///
   void test_clip_polygon()
   {
      list<array<double,2> > poly, result;
      poly.emplace_back( 1.0, 1.0 );
      poly.emplace_back( 1.0, 2.0 );
      poly.emplace_back( -1.0, 2.0 );
      poly.emplace_back( -1.0, 0.0 );
      clip_polygon(
	 1.0,
	 poly.begin(), poly.end(),
	 std::insert_iterator<list<array<double,2> > >( result, result.begin() )
	 );
   }

   ///
   ///
   ///
   void test_clip_polygon_full()
   {
      list<array<double,2> > poly, result;
      poly.emplace_back( -10.0, -10.0 );
      poly.emplace_back( 10.0, -10.0 );
      poly.emplace_back( 10.0, 10.0 );
      poly.emplace_back( -10.0, 10.0 );
      clip_polygon(
	 1.0,
	 poly.begin(), poly.end(),
	 std::insert_iterator<list<array<double,2> > >( result, result.begin() )
	 );
   }

   void setUp()
   {
      CLEAR_STACK_TRACE();
   }

   void tearDown()
   {
   }

private:

   int num_ranks, my_rank;
};
