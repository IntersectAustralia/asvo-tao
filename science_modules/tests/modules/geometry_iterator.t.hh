#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/modules/geometry_iterator.hh"

using namespace hpc;
using namespace tao;

///
/// Geometry iterator test suite.
///
class geometry_iterator_suite : public CxxTest::TestSuite
{
public:

   ///
   ///
   ///
   void test_constructor()
   {
      geometry_iterator<double> it(
   	 10,
   	 array<double,3>( 0, 0, 0 ),
   	 array<double,3>( 0, 0, 0 ),
   	 array<int,3>( 0, 1, 2 ),
   	 0, 90,
   	 0, 90,
	 100.0
   	 );
   }

   ///
   ///
   ///
   void test_covered()
   {
      geometry_iterator<double> it(
   	 10,
   	 array<double,3>( 0, 0, 0 ),
   	 array<double,3>( 0, 0, 0 ),
   	 array<int,3>( 0, 1, 2 ),
   	 0, 90,
   	 0, 90,
	 100.0
   	 );
   }

   ///
   ///
   ///
   void test_offset()
   {
      geometry_iterator<double> it(
   	 10,
   	 array<double,3>( 0, 0, 0 ),
   	 array<double,3>( 5, 0, 0 ),
   	 array<int,3>( 0, 1, 2 ),
   	 30, 60,
   	 30, 60,
	 100.0
   	 );
   }

   ///
   ///
   ///
   void test_rotation()
   {
      geometry_iterator<double> it(
	 10,
	 array<double,3>( 0, 0, 0 ),
	 array<double,3>( 0, 0, 0 ),
	 array<int,3>( 0, 1, 2 ),
	 0, 0.01,
	 0, 10,
	 100.0
	 );

      std::cout << "\n";
      for( ; !it.done(); ++it )
      {
      	 std::cout << *it << "\n";
      }
   }

   void setUp()
   {
   }

   void tearDown()
   {
   }
};
