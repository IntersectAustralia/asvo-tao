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
      soci::rowset<soci::row> rowset = (sql.prepare << "SELECT * FROM blah");
      const soci::row& row = *rowset.begin();
      string table = "blah";
      galaxy gal( row, table );
      gal.set_field<int>( "an_int", 4 );
      gal.set_field<double>( "a_double", 2.0 );
      gal.set_field<string>( "a_string", "hello" );
      TS_ASSERT_EQUALS( gal.value<int>( "an_int" ), 4 );
      TS_ASSERT_EQUALS( gal.value<double>( "a_double" ), 2.0 );
      TS_ASSERT( gal.value<string>( "a_string" ) == "hello" );
   }

   ///
   ///
   ///
   void test_use_row()
   {
      soci::rowset<soci::row> rowset = (sql.prepare << "SELECT * FROM blah");
      const soci::row& row = *rowset.begin();
      string table = "blah";
      galaxy gal( row, table );
      TS_ASSERT_EQUALS( gal.value<double>( "redshift" ), 100.0 );
   }

   void setUp()
   {
      db_filename = tmpnam( NULL );
      sql.open( soci::sqlite3, db_filename );
      sql << "CREATE TABLE blah (redshift DOUBLE PRECISION)";
      sql << "INSERT INTO blah VALUES(100)";
   }

   void tearDown()
   {
      sql.close();
      remove( db_filename.c_str() );
   }

protected:

   string db_filename;
   soci::session sql;
};
