#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/modules/diff.hh"

using namespace hpc;
using namespace tao;

///
/// Differentiation test suite.
///
class diff_suite : public CxxTest::TestSuite
{
public:

   ///
   ///
   ///
   void test_empty()
   {
      vector<double> func, diff;
      differentate( func.begin(), func.end(), diff.begin(), 1 );
   }

   ///
   ///
   ///
   void test_one()
   {
      vector<double> func( 1 ), diff( 1 );
      func[0] = 2;
      func[1] = 0;
      differentate( func.begin(), func.end(), diff.begin(), 1 );
      TS_ASSERT_EQUALS( func[0], 2 );
      TS_ASSERT_EQUALS( func[1], 0 );
   }

   ///
   ///
   ///
   void test_flat()
   {
      vector<double> func( 10 ), diff( 10 );
      std::fill( func.begin(), func.end(), 4 );
      differentate( func.begin(), func.end(), diff.begin(), 1 );
      for( auto val : func )
      {
	 TS_ASSERT_EQUALS( val, 4 );
      }
      for( auto val : diff )
      {
	 TS_ASSERT_DELTA( val, 0, 1e-4 );
      }
   }

   ///
   ///
   ///
   void test_linear()
   {
      vector<double> func( 10 ), diff( 10 );
      std::iota( func.begin(), func.end(), 3 );
      differentate( func.begin(), func.end(), diff.begin(), 1 );
      for( unsigned ii = 0; ii < 10; ++ii )
      {
	 TS_ASSERT_DELTA( func[ii], 3 + ii, 1e-4 );
      }
      for( auto val : diff )
      {
	 TS_ASSERT_DELTA( val, 1, 1e-4 );
      }
   }

   ///
   ///
   ///
   void test_linear_step_size()
   {
      vector<double> func( 10 ), diff( 10 );
      std::iota( func.begin(), func.end(), 3 );
      differentate( func.begin(), func.end(), diff.begin(), 2 );
      for( unsigned ii = 0; ii < 10; ++ii )
      {
	 TS_ASSERT_DELTA( func[ii], 3 + ii, 1e-4 );
      }
      for( auto val : diff )
      {
	 TS_ASSERT_DELTA( val, 0.5, 1e-4 );
      }
   }

   ///
   ///
   ///
   void test_quadratic()
   {
      vector<double> func( 10 ), diff( 10 );
      for( unsigned ii = 0; ii < 10; ++ii )
	 func[ii] = (ii - 5)*(ii - 5);
      differentate( func.begin(), func.end(), diff.begin(), 1 );
      for( unsigned ii = 0; ii < 10; ++ii )
      {
	 TS_ASSERT_DELTA( func[ii], (ii - 5)*(ii - 5), 1e-4 );
      }
      for( unsigned ii = 0; ii < 10; ++ii )
      {
	 TS_ASSERT_DELTA( diff[ii], 2*(ii - 5), 1e-4 );
      }
   }
};
