#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include <libhpc/logging/logging.hh>
#include "tao/modules/lightcone.hh"

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

      // Turn off random rotation and shifting.
      lc._use_random = false;

      // Insert some values.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "insert into snapshot_000 values (1, 0.001, 0.001, 0)";
         sql << "insert into snapshot_000 values (0.866, 0.5, 0.001, 1)";
         sql << "insert into snapshot_000 values (0.5, 0.866, 0.001, 2)";
         sql << "insert into snapshot_000 values (0.001, 1, 0.001, 3)";
         sql << "insert into snapshot_001 values (1, 0.001, 0.001, 0)";
         sql << "insert into snapshot_001 values (0.866, 0.5, 0.001, 1)";
         sql << "insert into snapshot_001 values (0.5, 0.866, 0.001, 2)";
         sql << "insert into snapshot_001 values (0.001, 1, 0.001, 3)";
      }

      // Prepare base dictionary.
      options::dictionary& dict = db_setup.dict;
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_setup.db_filename;
      dict["box_type"] = "cone";
      dict["box_side"] = "100";
      dict["snapshots"] = "0.01,0";
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
         sql << "delete from snapshot_001";
      }
   }

   ///
   ///
   ///
   void test_dec_minmax()
   {
      lightcone lc;

      // Turn off random rotation and shifting.
      lc._use_random = false;

      // Insert some values.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "insert into snapshot_000 values (0.707, 0.707, 0.001, 0)";
         sql << "insert into snapshot_000 values (0.612, 0.612, 0.5, 1)";
         sql << "insert into snapshot_000 values (0.354, 0.354, 0.866, 2)";
         sql << "insert into snapshot_000 values (0.001, 0.001, 1, 3)";
         sql << "insert into snapshot_001 values (0.707, 0.707, 0.001, 0)";
         sql << "insert into snapshot_001 values (0.612, 0.612, 0.5, 1)";
         sql << "insert into snapshot_001 values (0.354, 0.354, 0.866, 2)";
         sql << "insert into snapshot_001 values (0.001, 0.001, 1, 3)";
      }

      // Prepare base dictionary.
      options::dictionary& dict = db_setup.dict;
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_setup.db_filename;
      dict["box_type"] = "cone";
      dict["box_side"] = "100";
      dict["snapshots"] = "0.01,0";
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
         sql << "delete from snapshot_001";
      }
   }

   ///
   ///
   ///
   void test_extended_box_generation()
   {
      lightcone lc;

      // Turn off random rotation and shifting.
      lc._use_random = false;

      // Insert some values. Place the points on the lower walls
      // to get picked up by the neighboring boxes.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "insert into snapshot_000 values (1, 14, 14, 0)";
         sql << "insert into snapshot_000 values (14, 1, 14, 1)";
         sql << "insert into snapshot_000 values (14, 14, 1, 2)";
         sql << "insert into snapshot_001 values (1, 14, 14, 0)";
         sql << "insert into snapshot_001 values (14, 1, 14, 1)";
         sql << "insert into snapshot_001 values (14, 14, 1, 2)";
      }

      // Prepare base dictionary.
      options::dictionary& dict = db_setup.dict;
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_setup.db_filename;
      dict["box_type"] = "cone";
      dict["box_side"] = "100";
      dict["snapshots"] = "0.05,0";
      dict["z_min"] = "0";
      dict["rasc_min"] = "0";
      dict["rasc_max"] = "90";
      dict["decl_min"] = "0";
      dict["decl_max"] = "90";

      // Place to store row IDs.
      vector<int> ids;

      // Generate all results.
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 12 );
      for( unsigned ii = 0; ii < 12; ++ii )
         TS_ASSERT_EQUALS( ids[ii], ii%3 );

      // Erase the table data.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "delete from snapshot_000";
         sql << "delete from snapshot_001";
      }
   }

   ///
   ///
   ///
   void test_distances()
   {
      lightcone lc;

      // Turn off random rotation and shifting.
      lc._use_random = false;

      // Insert some values. Place the points on the lower walls
      // to get picked up by the neighboring boxes.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "insert into snapshot_000 values (5.77, 5.77, 5.77, 0)";
         sql << "insert into snapshot_000 values (11.55, 11.55, 11.55, 1)";
         sql << "insert into snapshot_000 values (17.32, 17.32, 17.32, 2)";
         sql << "insert into snapshot_001 values (5.77, 5.77, 5.77, 0)";
         sql << "insert into snapshot_001 values (11.55, 11.55, 11.55, 1)";
         sql << "insert into snapshot_001 values (17.32, 17.32, 17.32, 2)";
      }

      // Prepare base dictionary.
      options::dictionary& dict = db_setup.dict;
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_setup.db_filename;
      dict["box_type"] = "cone";
      dict["box_side"] = "100";
      dict["z_min"] = "0";
      dict["rasc_min"] = "0";
      dict["rasc_max"] = "90";
      dict["decl_min"] = "0";
      dict["decl_max"] = "90";

      // Place to store row IDs.
      vector<int> ids;

      // Capture first point.
      dict["snapshots"] = "0.005,0";
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

      // Capture first and second.
      dict["snapshots"] = "0.008,0";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 2 );
      TS_ASSERT_EQUALS( ids[0], 0 );
      TS_ASSERT_EQUALS( ids[1], 1 );

      // Capture all three.
      dict["snapshots"] = "0.011,0";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 3 );
      TS_ASSERT_EQUALS( ids[0], 0 );
      TS_ASSERT_EQUALS( ids[1], 1 );
      TS_ASSERT_EQUALS( ids[2], 2 );

      // Erase the table data.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "delete from snapshot_000";
         sql << "delete from snapshot_001";
      }
   }

   ///
   ///
   ///
   void test_redshift_minmax()
   {
      lightcone lc;

      // Turn off random rotation and shifting.
      lc._use_random = false;

      // Insert some values. Place the points on the lower walls
      // to get picked up by the neighboring boxes.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "insert into snapshot_000 values (5.77, 5.77, 5.77, 0)";
         sql << "insert into snapshot_000 values (11.55, 11.55, 11.55, 1)";
         sql << "insert into snapshot_000 values (17.32, 17.32, 17.32, 2)";
         sql << "insert into snapshot_001 values (5.77, 5.77, 5.77, 0)";
         sql << "insert into snapshot_001 values (11.55, 11.55, 11.55, 1)";
         sql << "insert into snapshot_001 values (17.32, 17.32, 17.32, 2)";
      }

      // Prepare base dictionary.
      options::dictionary& dict = db_setup.dict;
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_setup.db_filename;
      dict["box_type"] = "cone";
      dict["box_side"] = "100";
      dict["snapshots"] = "1,0";
      dict["rasc_min"] = "0";
      dict["rasc_max"] = "90";
      dict["decl_min"] = "0";
      dict["decl_max"] = "90";

      // Place to store row IDs.
      vector<int> ids;

      // Capture first point.
      dict["z_min"] = "0.003";
      dict["z_max"] = "0.004";
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

      // Capture first and second.
      dict["z_min"] = "0.006";
      dict["z_max"] = "0.007";
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

      // Capture all three.
      dict["z_min"] = "0.010";
      dict["z_max"] = "0.011";
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

      // Erase the table data.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "delete from snapshot_000";
         sql << "delete from snapshot_001";
      }
   }

   ///
   ///
   ///
   void test_snapshots()
   {
      lightcone lc;

      // Turn off random rotation and shifting.
      lc._use_random = false;

      // Insert some values. Place the points on the lower walls
      // to get picked up by the neighboring boxes.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "insert into snapshot_000 values (5.77, 5.77, 5.77, 0)";
         sql << "insert into snapshot_000 values (11.55, 11.55, 11.55, 1)";
         sql << "insert into snapshot_000 values (17.32, 17.32, 17.32, 2)";
         sql << "insert into snapshot_001 values (5.77, 5.77, 5.77, 3)";
         sql << "insert into snapshot_001 values (11.55, 11.55, 11.55, 4)";
         sql << "insert into snapshot_001 values (17.32, 17.32, 17.32, 5)";
         sql << "insert into snapshot_002 values (5.77, 5.77, 5.77, 6)";
         sql << "insert into snapshot_002 values (11.55, 11.55, 11.55, 7)";
         sql << "insert into snapshot_002 values (17.32, 17.32, 17.32, 8)";
      }

      // Prepare base dictionary.
      options::dictionary& dict = db_setup.dict;
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_setup.db_filename;
      dict["box_type"] = "cone";
      dict["box_side"] = "100";
      dict["snapshots"] = "0.011,0.007,0.003";
      dict["rasc_min"] = "0";
      dict["rasc_max"] = "90";
      dict["decl_min"] = "0";
      dict["decl_max"] = "90";
      dict["z_min"] = "0";
      dict["z_max"] = "1";

      // Place to store row IDs.
      vector<int> ids;

      LOG_PUSH( new logging::file( "test.log" ) );

      // Should encounter each point from each snapshot in a
      // unique order.
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const lightcone::row_type& row = *lc;
         ids.push_back( row.get<int>( "id" ) );
      }
      TS_ASSERT_EQUALS( ids.size(), 3 );
      TS_ASSERT_EQUALS( ids[0], 0 );
      TS_ASSERT_EQUALS( ids[1], 4 );
      TS_ASSERT_EQUALS( ids[2], 8 );

      // Erase the table data.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "delete from snapshot_000";
         sql << "delete from snapshot_001";
         sql << "delete from snapshot_002";
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
