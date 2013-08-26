#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/base/age_line.hh"
#include "tao/base/utils.hh"
#include "mpi_fixture.hh"
#include "db_fixture.hh"

using namespace hpc;
using namespace tao;

///
/// age_line class test suite.
///
class age_line_suite : public CxxTest::TestSuite
{
public:

   ///
   /// Test default constructor.
   ///
   void test_default_constructor()
   {
      age_line<double> al;
      TS_ASSERT( al._ages.empty() );
      TS_ASSERT( al._dual.empty() );
   }

   ///
   /// Test database load constructor.
   ///
   void test_load_constructor()
   {
      // Create a test table.
      soci::session sql( soci::sqlite3, ":memory:" );
      db_fix.setup_snapshot_table( sql );

      // Construct.
      age_line<double> al( sql );

      // Ages must be correct.
      TS_ASSERT_EQUALS( al._ages.size(), 5 );
      TS_ASSERT_DELTA( al._ages[0], redshift_to_age<double>( 127 ), 1e-3 );
      TS_ASSERT_DELTA( al._ages[1], redshift_to_age<double>( 80 ), 1e-3 );
      TS_ASSERT_DELTA( al._ages[2], redshift_to_age<double>( 63 ), 1e-3 );
      TS_ASSERT_DELTA( al._ages[3], redshift_to_age<double>( 20 ), 1e-3 );
      TS_ASSERT_DELTA( al._ages[4], redshift_to_age<double>( 10 ), 1e-3 );

      // Duals must be correct.
      TS_ASSERT_EQUALS( al._dual.size(), 4 );
      TS_ASSERT_DELTA( al._dual[0], 0.5*(redshift_to_age<double>( 127 ) + redshift_to_age<double>( 80 )), 1e-3 );
      TS_ASSERT_DELTA( al._dual[1], 0.5*(redshift_to_age<double>( 80 ) + redshift_to_age<double>( 63 )), 1e-3 );
      TS_ASSERT_DELTA( al._dual[2], 0.5*(redshift_to_age<double>( 63 ) + redshift_to_age<double>( 20 )), 1e-3 );
      TS_ASSERT_DELTA( al._dual[3], 0.5*(redshift_to_age<double>( 20 ) + redshift_to_age<double>( 10 )), 1e-3 );
   }

   ///
   /// Test bin location.
   ///
   void test_find_bin()
   {
      // Create a test table.
      soci::session sql( soci::sqlite3, ":memory:" );
      db_fix.setup_snapshot_table( sql );

      // Construct.
      age_line<double> al( sql );

      // Test below minimum.
      TS_ASSERT_EQUALS( al.find_bin( redshift_to_age<double>( 2 ) ), 4 );

      // Test above maximum.
      TS_ASSERT_EQUALS( al.find_bin( redshift_to_age<double>( 130 ) ), 0 );

      // Bins.
      TS_ASSERT_EQUALS( al.find_bin( 0.51*(redshift_to_age<double>( 127 ) + redshift_to_age<double>( 80 )) ), 1 );
      TS_ASSERT_EQUALS( al.find_bin( 0.51*(redshift_to_age<double>( 80 ) + redshift_to_age<double>( 63 )) ), 2 );
      TS_ASSERT_EQUALS( al.find_bin( 0.51*(redshift_to_age<double>( 63 ) + redshift_to_age<double>( 20 )) ), 3 );
   }
};
