#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include <libhpc/logging/logging.hh>
#include "tao/modules/lightcone.hh"

using namespace hpc;
using namespace tao;

#include "mpi_fixture.hh"
#include "db_fixture.hh"

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

      LOG_PUSH( new logging::file( "test.log", 0 ) );

      // Turn off random rotation and shifting.
      lc._use_random = false;

      // Insert some values.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "INSERT INTO snap_redshift VALUES(0, 0)";
         sql << "INSERT INTO snap_redshift VALUES(1, 0.01)";
         sql << "INSERT INTO tree_1 VALUES(1, 0.001, 0.001, 0, 0)";
         sql << "INSERT INTO tree_2 VALUES(0.866, 0.5, 0.001, 1, 0)";
         sql << "INSERT INTO tree_3 VALUES(0.5, 0.866, 0.001, 2, 0)";
         sql << "INSERT INTO tree_4 VALUES(0.001, 1, 0.001, 3, 0)";
         sql << "INSERT INTO tree_1 VALUES(1, 0.001, 0.001, 4, 1)";
         sql << "INSERT INTO tree_2 VALUES(0.866, 0.5, 0.001, 5, 1)";
         sql << "INSERT INTO tree_3 VALUES(0.5, 0.866, 0.001, 6, 1)";
         sql << "INSERT INTO tree_4 VALUES(0.001, 1, 0.001, 7, 1)";
      }

      // Prepare base dictionary.
      options::dictionary& dict = db_setup.dict;
      dict["z_min"] = "0";
      dict["dec_min"] = "0";
      dict["dec_max"] = "90";

      // Place to store row IDs.
      vector<int> ids;

      // Only row 0.
      dict["ra_min"] = "0.0";
      dict["ra_max"] = "0.1";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const galaxy& gal = *lc;
         ids.push_back( gal.id() );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 0 );

      // Only row 1.
      dict["ra_min"] = "29.9";
      dict["ra_max"] = "30.1";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const galaxy& gal = *lc;
         ids.push_back( gal.id() );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 1 );

      // Only row 2.
      dict["ra_min"] = "59.9";
      dict["ra_max"] = "60.1";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const galaxy& gal = *lc;
         ids.push_back( gal.id() );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 2 );

      // Only row 3.
      dict["ra_min"] = "89.9";
      dict["ra_max"] = "90.0";
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );

      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const galaxy& gal = *lc;
         ids.push_back( gal.id() );
      }
      TS_ASSERT_EQUALS( ids.size(), 1 );
      TS_ASSERT_EQUALS( ids[0], 3 );
   }

   // ///
   // ///
   // ///
   // void test_dec_minmax()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._use_random = false;

   //    // Insert some values.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO meta VALUES(0, 0, 100)";
   //       sql << "INSERT INTO meta VALUES(1, 0.01, 100)";
   //       sql << "INSERT INTO snapshot_000 VALUES(0.707, 0.707, 0.001, 0)";
   //       sql << "INSERT INTO snapshot_000 VALUES(0.612, 0.612, 0.5, 1)";
   //       sql << "INSERT INTO snapshot_000 VALUES(0.354, 0.354, 0.866, 2)";
   //       sql << "INSERT INTO snapshot_000 VALUES(0.001, 0.001, 1, 3)";
   //       sql << "INSERT INTO snapshot_001 VALUES(0.707, 0.707, 0.001, 0)";
   //       sql << "INSERT INTO snapshot_001 VALUES(0.612, 0.612, 0.5, 1)";
   //       sql << "INSERT INTO snapshot_001 VALUES(0.354, 0.354, 0.866, 2)";
   //       sql << "INSERT INTO snapshot_001 VALUES(0.001, 0.001, 1, 3)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict;
   //    dict["z_min"] = "0";
   //    dict["ra_min"] = "0";
   //    dict["ra_max"] = "90";

   //    // Place to store row IDs.
   //    vector<int> ids;

   //    // Only row 0.
   //    dict["dec_min"] = "0.0";
   //    dict["dec_max"] = "0.1";
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 0 );

   //    // Only row 1.
   //    dict["dec_min"] = "29.9";
   //    dict["dec_max"] = "30.1";
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 1 );

   //    // Only row 2.
   //    dict["dec_min"] = "59.9";
   //    dict["dec_max"] = "60.1";
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 2 );

   //    // Only row 3.
   //    dict["dec_min"] = "89.9";
   //    dict["dec_max"] = "90.0";
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );

   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 3 );

   //    // Erase the table data.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "DELETE FROM meta";
   //       sql << "DELETE FROM snapshot_000";
   //       sql << "DELETE FROM snapshot_001";
   //    }
   // }

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
         sql << "INSERT INTO snap_redshift VALUES(0, 0)";
         sql << "INSERT INTO snap_redshift VALUES(1, 0.05)";
	 sql << "INSERT INTO tree_1 VALUES(1, 14, 14, 0, 0)";
         sql << "INSERT INTO tree_2 VALUES(14, 1, 14, 1, 0)";
         sql << "INSERT INTO tree_3 VALUES(14, 14, 1, 2, 0)";
         sql << "INSERT INTO tree_1 VALUES(1, 14, 14, 3, 1)";
         sql << "INSERT INTO tree_2 VALUES(14, 1, 14, 4, 1)";
         sql << "INSERT INTO tree_3 VALUES(14, 14, 1, 5, 1)";
      }

      // Prepare base dictionary.
      options::dictionary& dict = db_setup.dict;
      dict["z_min"] = "0";
      dict["ra_min"] = "0";
      dict["ra_max"] = "90";
      dict["dec_min"] = "0";
      dict["dec_max"] = "90";

      // Place to store row IDs.
      vector<int> ids;

      // Generate all results.
      db_setup.xml.write( db_setup.xml_filename, dict );
      setup_lightcone( lc );
      ids.resize( 0 );
      for( lc.begin(); !lc.done(); ++lc )
      {
         const galaxy& gal = *lc;
         ids.push_back( gal.id() );
      }
      TS_ASSERT_EQUALS( ids.size(), 12 );
      for( unsigned ii = 0; ii < 12; ++ii )
         TS_ASSERT_EQUALS( ids[ii], ii%3 );
   }

   // ///
   // ///
   // ///
   // void test_distances()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._use_random = false;

   //    // Insert some values. Place the points on the lower walls
   //    // to get picked up by the neighboring boxes.
   //    soci::session sql( soci::sqlite3, db_setup.db_filename );
   //    sql << "INSERT INTO snapshot_000 VALUES(5.77, 5.77, 5.77, 0)";
   //    sql << "INSERT INTO snapshot_000 VALUES(11.55, 11.55, 11.55, 1)";
   //    sql << "INSERT INTO snapshot_000 VALUES(17.32, 17.32, 17.32, 2)";
   //    sql << "INSERT INTO snapshot_001 VALUES(5.77, 5.77, 5.77, 0)";
   //    sql << "INSERT INTO snapshot_001 VALUES(11.55, 11.55, 11.55, 1)";
   //    sql << "INSERT INTO snapshot_001 VALUES(17.32, 17.32, 17.32, 2)";

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict;
   //    dict["z_min"] = "0";
   //    dict["ra_min"] = "0";
   //    dict["ra_max"] = "90";
   //    dict["dec_min"] = "0";
   //    dict["dec_max"] = "90";

   //    // Place to store row IDs.
   //    vector<int> ids;

   //    // Capture first point.
   //    sql << "INSERT INTO meta VALUES(0, 0, 100)";
   //    sql << "INSERT INTO meta VALUES(1, 0.005, 100)";
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 0 );

   //    // Capture first and second.
   //    sql << "DELETE FROM meta";
   //    sql << "INSERT INTO meta VALUES(0, 0, 100)";
   //    sql << "INSERT INTO meta VALUES(1, 0.008, 100)";
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 2 );
   //    TS_ASSERT_EQUALS( ids[0], 0 );
   //    TS_ASSERT_EQUALS( ids[1], 1 );

   //    // Capture all three.
   //    sql << "DELETE FROM meta";
   //    sql << "INSERT INTO meta VALUES(0, 0, 100)";
   //    sql << "INSERT INTO meta VALUES(1, 0.011, 100)";
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 3 );
   //    TS_ASSERT_EQUALS( ids[0], 0 );
   //    TS_ASSERT_EQUALS( ids[1], 1 );
   //    TS_ASSERT_EQUALS( ids[2], 2 );

   //    // Erase the table data.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "DELETE FROM meta";
   //       sql << "DELETE FROM snapshot_000";
   //       sql << "DELETE FROM snapshot_001";
   //    }
   // }

   // ///
   // ///
   // ///
   // void test_redshift_minmax()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._use_random = false;

   //    // Insert some values. Place the points on the lower walls
   //    // to get picked up by the neighboring boxes.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO meta VALUES(0, 0, 100)";
   //       sql << "INSERT INTO meta VALUES(1, 1, 100)";
   //       sql << "INSERT INTO snapshot_000 VALUES(5.77, 5.77, 5.77, 0)";
   //       sql << "INSERT INTO snapshot_000 VALUES(11.55, 11.55, 11.55, 1)";
   //       sql << "INSERT INTO snapshot_000 VALUES(17.32, 17.32, 17.32, 2)";
   //       sql << "INSERT INTO snapshot_001 VALUES(5.77, 5.77, 5.77, 0)";
   //       sql << "INSERT INTO snapshot_001 VALUES(11.55, 11.55, 11.55, 1)";
   //       sql << "INSERT INTO snapshot_001 VALUES(17.32, 17.32, 17.32, 2)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict;
   //    dict["ra_min"] = "0";
   //    dict["ra_max"] = "90";
   //    dict["dec_min"] = "0";
   //    dict["dec_max"] = "90";

   //    // Place to store row IDs.
   //    vector<int> ids;

   //    // Capture first point.
   //    dict["z_min"] = "0.003";
   //    dict["z_max"] = "0.004";
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 0 );

   //    // Capture first and second.
   //    dict["z_min"] = "0.006";
   //    dict["z_max"] = "0.007";
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 1 );

   //    // Capture all three.
   //    dict["z_min"] = "0.010";
   //    dict["z_max"] = "0.011";
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 2 );

   //    // Erase the table data.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "DELETE FROM meta";
   //       sql << "DELETE FROM snapshot_000";
   //       sql << "DELETE FROM snapshot_001";
   //    }
   // }

   // ///
   // ///
   // ///
   // void test_snapshots()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._use_random = false;

   //    // Insert some values. Place the points on the lower walls
   //    // to get picked up by the neighboring boxes.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO meta VALUES(0, 0.003, 100)";
   //       sql << "INSERT INTO meta VALUES(1, 0.007, 100)";
   //       sql << "INSERT INTO meta VALUES(2, 0.011, 100)";
   //       sql << "INSERT INTO snapshot_000 VALUES(5.77, 5.77, 5.77, 0)";
   //       sql << "INSERT INTO snapshot_000 VALUES(11.55, 11.55, 11.55, 1)";
   //       sql << "INSERT INTO snapshot_000 VALUES(17.32, 17.32, 17.32, 2)";
   //       sql << "INSERT INTO snapshot_001 VALUES(5.77, 5.77, 5.77, 3)";
   //       sql << "INSERT INTO snapshot_001 VALUES(11.55, 11.55, 11.55, 4)";
   //       sql << "INSERT INTO snapshot_001 VALUES(17.32, 17.32, 17.32, 5)";
   //       sql << "INSERT INTO snapshot_002 VALUES(5.77, 5.77, 5.77, 6)";
   //       sql << "INSERT INTO snapshot_002 VALUES(11.55, 11.55, 11.55, 7)";
   //       sql << "INSERT INTO snapshot_002 VALUES(17.32, 17.32, 17.32, 8)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict;
   //    dict["ra_min"] = "0";
   //    dict["ra_max"] = "90";
   //    dict["dec_min"] = "0";
   //    dict["dec_max"] = "90";
   //    dict["z_min"] = "0";
   //    dict["z_max"] = "1";

   //    // Place to store row IDs.
   //    vector<int> ids;

   //    // Should encounter each point from each snapshot in a
   //    // unique order.
   //    db_setup.xml.write( db_setup.xml_filename, dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.id() );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 3 );
   //    TS_ASSERT_EQUALS( ids[0], 0 );
   //    TS_ASSERT_EQUALS( ids[1], 4 );
   //    TS_ASSERT_EQUALS( ids[2], 8 );

   //    // Erase the table data.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "DELETE FROM meta";
   //       sql << "DELETE FROM snapshot_000";
   //       sql << "DELETE FROM snapshot_001";
   //       sql << "DELETE FROM snapshot_002";
   //    }
   // }

   void setup_lightcone( lightcone& lc )
   {
      // If we are already connected, disconnect.
      lc._db_disconnect();

      // Read in the dictionary from XML.
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
      num_ranks = mpi::comm::world.size();
      my_rank = mpi::comm::world.rank();
   }

   void tearDown()
   {
      // Erase the table data.
      soci::session sql( soci::sqlite3, db_setup.db_filename );
      sql << "DELETE FROM snap_redshift";
      sql << "DELETE FROM tree_1";
      sql << "DELETE FROM tree_2";
      sql << "DELETE FROM tree_3";
      sql << "DELETE FROM tree_4";
   }

private:

   int num_ranks, my_rank;
};
