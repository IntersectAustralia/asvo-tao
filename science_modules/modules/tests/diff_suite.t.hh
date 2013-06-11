#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include <libhpc/containers/vector.hh>
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
      differentiate( func.begin(), func.end(), diff.begin(), 1 );
   }

   ///
   ///
   ///
   void test_one()
   {
      vector<double> func( 1 ), diff( 1 );
      func[0] = 2;
      diff[0] = 0;
      differentiate( func.begin(), func.end(), diff.begin(), 1 );
      TS_ASSERT_EQUALS( func[0], 2 );
      TS_ASSERT_EQUALS( diff[0], 0 );
   }

   ///
   ///
   ///
   void test_flat()
   {
      vector<double> func( 10 ), diff( 10 );
      std::fill( func.begin(), func.end(), 4 );
      differentiate( func.begin(), func.end(), diff.begin(), 1 );
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
      differentiate( func.begin(), func.end(), diff.begin(), 1 );
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
      differentiate( func.begin(), func.end(), diff.begin(), 2 );
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
      for( int ii = 0; ii < 10; ++ii )
	 func[ii] = (ii - 5)*(ii - 5);
      differentiate( func.begin(), func.end(), diff.begin(), 1 );
      for( int ii = 0; ii < 10; ++ii )
      {
	 TS_ASSERT_DELTA( func[ii], (ii - 5)*(ii - 5), 1e-4 );
      }
      TS_ASSERT_DELTA( diff[0], -9, 1e-4 );
      for( int ii = 1; ii < 9; ++ii )
      {
	 TS_ASSERT_DELTA( diff[ii], 2*(ii - 5), 1e-4 );
      }
      TS_ASSERT_DELTA( diff[9], 7, 1e-4 );
   }
};
