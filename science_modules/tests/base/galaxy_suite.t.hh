#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/base/galaxy.hh"

using namespace hpc;
using namespace tao;

///
/// Galaxy test suite.
///
class galaxy_suite : public CxxTest::TestSuite
{
public:

   ///
   ///
   ///
   void test_set_field()
   {
      galaxy gal;
      gal.set_batch_size( 1 );

      vector<int> an_int( 1 );
      an_int[0] = 4;
      gal.set_field<int>( "an_int", an_int );
      vector<double> a_double( 1 );
      a_double[0] = 4.0;
      gal.set_field<double>( "a_double", a_double );
      vector<string> a_string( 1 );
      a_string[0] = "hello";
      gal.set_field<string>( "a_string", a_string );

      TS_ASSERT_EQUALS( gal.values<int>( "an_int" )[0], 4 );
      TS_ASSERT_EQUALS( gal.values<double>( "a_double" )[0], 4.0 );
      TS_ASSERT( gal.values<string>( "a_string" )[0] == "hello" );
   }
};
