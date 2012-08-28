#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include <libhpc/logging/logging.hh>
#include "tao/lightcone/lightcone.hh"

using namespace hpc;
using namespace tao;

#include "mpi_fixture.hh"

///
/// Database preparation fixture.
///
class db_setup_fixture : public CxxTest::GlobalFixture
{
public:

   bool setUp()
   {
      return true;
   }

   bool tearDown()
   {
      return true;
   }

   bool setUpWorld()
   {
      // Create the database file.
      db_filename = tmpnam( NULL );
      {
         std::ofstream file( db_filename, std::fstream::out | std::fstream::app );
      }

      // Open it using SOCI, create a table.
      {
         // Open our sqlite connection.
         soci::session sql( soci::sqlite3, db_filename );

         // Add tables.
         sql << "create table snapshot_000 (Pos1 double precision, Pos2 double precision, Pos3 double precision, id integer)";
         sql << "create table snapshot_001 (Pos1 double precision, Pos2 double precision, Pos3 double precision, id integer)";
         sql << "create table snapshot_002 (Pos1 double precision, Pos2 double precision, Pos3 double precision, id integer)";
         sql << "create table snapshot_003 (Pos1 double precision, Pos2 double precision, Pos3 double precision, id integer)";

         // // Add some values to test distances.
         // sql << "insert into snapshot_000 values (1, 1, 1, 0)";
         // sql << "insert into snapshot_001 values (14.43, 14.43, 14.43, 0)";
         // sql << "insert into snapshot_002 values (3, 3, 3, 0)";
         // sql << "insert into snapshot_003 values (4, 4, 4, 0)";

         // // Add some values to test RA.


         // // Add some values to test dec.
         // sql << "insert into snapshot_000 values (1, 0, 0, 5)";
         // sql << "insert into snapshot_000 values (0.866, 0.5, 0, 6)";
         // sql << "insert into snapshot_000 values (0.5, 0.866, 0, 7)";
         // sql << "insert into snapshot_000 values (1, 0, 0, 8)";
      }

      // Create the XML file by calling the lightcone options setup and filling in the
      // details, then dumping to file.
      lightcone lc;
      lc.setup_options( dict );
      dict.compile();
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_filename;
      dict["box_type"] = "cone";
      dict["box_side"] = "100";
      dict["snapshots"] = "0.01, 0.009, 0.008, 0";
      dict["z_min"] = "0";
      xml_filename = tmpnam( NULL );
      xml.write( xml_filename, dict );

      return true;
   }

   bool tearDownWorld()
   {
      remove( db_filename.c_str() );
      remove( xml_filename.c_str() );
      dict.clear();
      return true;
   }

   options::dictionary dict;
   options::xml xml;
   std::string db_filename, xml_filename;
};

static db_setup_fixture db_setup;

///
/// Lightcone class test suite.
///
class lightcone_suite : public CxxTest::TestSuite
{
public:

   ///
   /// Test default constructor.
   ///
   void test_ctor()
   {
      lightcone lc;
   }

   ///
   ///
   ///
   void test_ra_minmax()
   {
      lightcone lc;

      // Insert some values.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "insert into snapshot_000 values (1, 0.001, 0.001, 0)";
         sql << "insert into snapshot_000 values (0.866, 0.5, 0.001, 1)";
         sql << "insert into snapshot_000 values (0.5, 0.866, 0.001, 2)";
         sql << "insert into snapshot_000 values (0.001, 1, 0.001, 3)";
      }

      // Prepare base dictionary.
      options::dictionary& dict = db_setup.dict;
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_setup.db_filename;
      dict["box_type"] = "cone";
      dict["box_side"] = "100";
      dict["snapshots"] = "0.01";
      dict["z_min"] = "0";
      dict["decl_min"] = "0";
      dict["decl_max"] = "90";

      // Place to store row IDs.
      vector<int> ids;

      // Only row 0.
      dict["rasc_min"] = "0.0";
      dict["rasc_max"] = "0.1";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 0 );

      // Only row 1.
      dict["rasc_min"] = "29.9";
      dict["rasc_max"] = "30.1";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 1 );

      // Only row 2.
      dict["rasc_min"] = "59.9";
      dict["rasc_max"] = "60.1";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 2 );

      // Only row 3.
      dict["rasc_min"] = "89.9";
      dict["rasc_max"] = "90.0";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );

      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 3 );

      // Erase the table data.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "delete from snapshot_000";
      }
   }

   ///
   ///
   ///
   void test_dec_minmax()
   {
      LOG_PUSH( new logging::file( "test.log" ) );

      lightcone lc;

      // Insert some values.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "insert into snapshot_000 values (0.707, 0.707, 0.001, 0)";
         sql << "insert into snapshot_000 values (0.612, 0.612, 0.5, 1)";
         sql << "insert into snapshot_000 values (0.354, 0.354, 0.866, 2)";
         sql << "insert into snapshot_000 values (0.001, 0.001, 1, 3)";
      }

      // Prepare base dictionary.
      options::dictionary& dict = db_setup.dict;
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_setup.db_filename;
      dict["box_type"] = "cone";
      dict["box_side"] = "100";
      dict["snapshots"] = "0.01";
      dict["z_min"] = "0";
      dict["rasc_min"] = "0";
      dict["rasc_max"] = "90";

      // Place to store row IDs.
      vector<int> ids;

      // Only row 0.
      dict["decl_min"] = "0.0";
      dict["decl_max"] = "0.1";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 0 );

      // Only row 1.
      dict["decl_min"] = "29.9";
      dict["decl_max"] = "30.1";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 1 );

      // Only row 2.
      dict["decl_min"] = "59.9";
      dict["decl_max"] = "60.1";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 2 );

      // Only row 3.
      dict["decl_min"] = "89.9";
      dict["decl_max"] = "90.0";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );

      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 3 );

      // Erase the table data.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "delete from snapshot_000";
      }
   }

   void setup_lightcone( lightcone& lc )
   {
      options::dictionary dict;
      lc.setup_options( dict );
      dict.compile();
      options::xml xml;
      xml.read( db_setup.xml_filename, dict );
      lc.initialise( dict );
   }

   void setUp()
   {
      CLEAR_STACK_TRACE();

      this->num_ranks = mpi::comm::world.size();
      this->my_rank = mpi::comm::world.rank();
   }

   void tearDown()
   {
   }

private:

   int num_ranks, my_rank;
};
