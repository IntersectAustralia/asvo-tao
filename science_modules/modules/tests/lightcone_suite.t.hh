#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include <libhpc/logging/logging.hh>
#include "tao/modules/lightcone.hh"
#include <stdio.h>

using namespace hpc;
using namespace tao;

#include "mpi_fixture.hh"
// #include "db_fixture.hh"

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
   /// Redshift to distance (comoving).
   ///
   void test_redshift_to_distance()
   {
      lightcone lc;
      lc._h0 = 73;
      real_type dist = lc._redshift_to_distance( 3 );
      TS_ASSERT_DELTA( dist, 4690.3, 10 );
   }

   ///
   /// Box snapshot.
   ///
   void test_box_snapshot()
   {
      lightcone lc;

      // Setup some redshifts.
      lc._snap_redshifts.resize( 10 );
      hpc::iota( lc._snap_redshifts, 0.0 );

      for( unsigned ii = 0; ii < 10; ++ii )
      {
	 // Check exact values.
	 TS_ASSERT_EQUALS( lc._box_snapshot( (double)ii ), ii );

	 // Check values off by a little.
	 TS_ASSERT_EQUALS( lc._box_snapshot( ((double)ii) - 0.00001 ), ii );
	 TS_ASSERT_EQUALS( lc._box_snapshot( ((double)ii) + 0.00001 ), ii );
      }

      // Check for exception when giving a bad value.
      TS_ASSERT_THROWS_ANYTHING( lc._box_snapshot( -10.0 ) );
   }

   // ///
   // ///
   // ///
   // void test_redshift_to_distance_consistency()
   // {
   //    lightcone lc;

   //    // Insert some values.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO snap_redshift VALUES(0, 1)";
   //       sql << "INSERT INTO snap_redshift VALUES(1, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(3, 3, 3, 2, 0, 0, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(4, 4, 4, 3, 0, 0, 3, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 4, 1, 1, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 5, 1, 1, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(3, 3, 3, 6, 1, 1, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(4, 4, 4, 7, 1, 1, 3, 0, 0, 0, 0, 0)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict.sub( "workflow:light-cone" );
   //    dict["geometry"] = "box";
   //    dict["redshift"] = "1";
   //    dict["query-box-size"] = "10";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );

   //    setup_lightcone( lc );

   //    // Test directly.
   //    TS_ASSERT_DELTA( lc._distance_to_redshift( lc._redshift_to_distance( 0 ) ), 0, 1e-3 );
   //    for( double z = 0.0; z < 1.0; z += 0.1 )
   //    {
   // 	 TS_ASSERT_DELTA( lc._distance_to_redshift( lc._redshift_to_distance( z ) ), z, 1e-3 );
   //    }
   //    TS_ASSERT_DELTA( lc._distance_to_redshift( lc._redshift_to_distance( 1.0 ) ), 1.0, 1e-3 );

   //    // Now test as read from the galaxy object.
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   // 	 double dist = sqrt( gal.values<real_type>( "pos_x" )[0]*gal.values<real_type>( "pos_x" )[0] + 
   //                           gal.values<real_type>( "pos_y" )[0]*gal.values<real_type>( "pos_y" )[0] + 
   //                           gal.values<real_type>( "pos_z" )[0]*gal.values<real_type>( "pos_z" )[0] );
   // 	 TS_ASSERT_DELTA( lc._redshift_to_distance( gal.values<real_type>( "redshift" )[0] ), dist, 1e-1 );

   //    }
   // }

   // ///
   // ///
   // ///
   // void test_box_size()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._unique = true;

   //    // Insert some values.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO snap_redshift VALUES(0, 0.001)";
   //       sql << "INSERT INTO snap_redshift VALUES(1, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(3, 3, 3, 2, 0, 0, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(4, 4, 4, 3, 0, 0, 3, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 4, 1, 1, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 5, 1, 1, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(3, 3, 3, 6, 1, 1, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(4, 4, 4, 7, 1, 1, 3, 0, 0, 0, 0, 0)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict.sub( "workflow:light-cone" );
   //    dict["geometry"] = "box";
   //    dict["redshift"] = "0.001";

   //    // Place to store row IDs.
   //    vector<long long> ids;

   //    // Only row 0.
   //    dict["query-box-size"] = "1.5";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 0 );

   //    // Only row 1.
   //    dict["query-box-size"] = "2.5";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 2 );
   //    TS_ASSERT_EQUALS( ids[0], 0 );
   //    TS_ASSERT_EQUALS( ids[1], 1 );
   // }

   // ///
   // ///
   // ///
   // void test_box_z_snap()
   // {

   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._unique = true;

   //    // Insert some values.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO snap_redshift VALUES(0, 0.001)";
   //       sql << "INSERT INTO snap_redshift VALUES(1, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(3, 3, 3, 2, 0, 0, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(4, 4, 4, 3, 0, 0, 3, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 4, 1, 1, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 5, 1, 1, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(3, 3, 3, 6, 1, 1, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(4, 4, 4, 7, 1, 1, 3, 0, 0, 0, 0, 0)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict.sub( "workflow:light-cone" );
   //    dict["geometry"] = "box";
   //    dict["query-box-size"] = "4.5";
   //    dict["h0"]="0.73";
   //    // Place to store row IDs.
   //    vector<long long> ids;

   //    // Only row 0.
   //    dict["redshift"] = "0.001";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );

   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );

   //    }

   //    TS_ASSERT_EQUALS( ids.size(), 4 );
   //    for( unsigned ii = 0; ii < 4; ++ii )
   //       TS_ASSERT_EQUALS( ids[ii], ii );

   //    // Only row 1.
   //    dict["redshift"] = "0";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );

   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 4 );
   //    for( unsigned ii = 0; ii < 4; ++ii )
   //       TS_ASSERT_EQUALS( ids[ii], 4 + ii );
   // }

   // ///
   // ///
   // ///
   // void test_ra_minmax()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._unique = true;

   //    // Insert some values.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO snap_redshift VALUES(0, 0.001)";
   //       sql << "INSERT INTO snap_redshift VALUES(1, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 0.001, 0.001, 0, 0, 0, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(0.866, 0.5, 0.001, 1, 0, 0, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(0.5, 0.866, 0.001, 2, 0, 0, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(0.001, 1, 0.001, 3, 0, 0, 3, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 0.001, 0.001, 4, 1, 1, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(0.866, 0.5, 0.001, 5, 1, 1, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(0.5, 0.866, 0.001, 6, 1, 1, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(0.001, 1, 0.001, 7, 1, 1, 3, 0, 0, 0, 0, 0)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict.sub( "workflow:light-cone" );
   //    dict["geometry"] = "light-cone";
   //    dict["redshift-min"] = "0";
   //    dict["dec-min"] = "0";
   //    dict["dec-max"] = "90";

   //    // Place to store row IDs.
   //    vector<long long> ids;

   //    // Only row 0.
   //    dict["ra-min"] = "0.0";
   //    dict["ra-max"] = "0.1";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 4 );

   //    // Only row 1.
   //    dict["ra-min"] = "29.9";
   //    dict["ra-max"] = "30.1";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 5 );

   //    // Only row 2.
   //    dict["ra-min"] = "59.9";
   //    dict["ra-max"] = "60.1";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 6 );

   //    // Only row 3.
   //    dict["ra-min"] = "89.9";
   //    dict["ra-max"] = "90.0";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );

   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 7 );
   // }

   // ///
   // ///
   // ///
   // void test_dec_minmax()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._unique = true;

   //    // Insert some values.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO snap_redshift VALUES(0, 0.001)";
   //       sql << "INSERT INTO snap_redshift VALUES(1, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(0.707, 0.707, 0.001, 0, 0, 0, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(0.612, 0.612, 0.5, 1, 0, 0, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(0.354, 0.354, 0.866, 2, 0, 0, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(0.001, 0.001, 1, 3, 0, 0, 3, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(0.707, 0.707, 0.001, 0, 1, 1, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(0.612, 0.612, 0.5, 1, 1, 1, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(0.354, 0.354, 0.866, 2, 1, 1, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(0.001, 0.001, 1, 3, 1, 1, 3, 0, 0, 0, 0, 0)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict.sub( "workflow:light-cone" );
   //    dict["redshift-min"] = "0";
   //    dict["ra-min"] = "0";
   //    dict["ra-max"] = "90";

   //    // Place to store row IDs.
   //    vector<long long> ids;

   //    // Only row 0.
   //    dict["dec-min"] = "0.0";
   //    dict["dec-max"] = "0.1";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 0 );

   //    // Only row 1.
   //    dict["dec-min"] = "29.9";
   //    dict["dec-max"] = "30.1";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 1 );

   //    // Only row 2.
   //    dict["dec-min"] = "59.9";
   //    dict["dec-max"] = "60.1";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 2 );

   //    // Only row 3.
   //    dict["dec-min"] = "89.9";
   //    dict["dec-max"] = "90.0";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );

   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 3 );
   // }

   // ///
   // ///
   // ///
   // void test_redshift_minmax()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._unique = true;

   //    // Insert some values. Place the points on the lower walls
   //    // to get picked up by the neighboring boxes.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO snap_redshift VALUES(0, 0.001)";
   //       sql << "INSERT INTO snap_redshift VALUES(1, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(34, 34, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(57, 57, 57, 1, 0, 0, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(230, 230, 230, 2, 0, 0, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(34, 34, 34, 3, 1, 1, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(57, 57, 57, 4, 1, 1, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(230, 230, 230, 5, 1, 1, 2, 0, 0, 0, 0, 0)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict.sub( "workflow:light-cone" );
   //    dict["ra-min"] = "0";
   //    dict["ra-max"] = "90";
   //    dict["dec-min"] = "0";
   //    dict["dec-max"] = "90";

   //    // Place to store row IDs.
   //    vector<long long> ids;

   //    // Capture first point.
   //    dict["redshift-min"] = "0.0001";
   //    dict["redshift-max"] = "0.0002";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 3 );

   //    // Capture first and second.
   //    dict["redshift-min"] = "0.0002";
   //    dict["redshift-max"] = "0.0003";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 4 );

   //    // Capture all three.
   //    dict["redshift-min"] = "0.0009";
   //    dict["redshift-max"] = "0.001";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 2 );
   // }

   // ///
   // ///
   // ///
   // void test_extended_box_generation()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._unique = true;

   //    // Insert some values. Place the points on the lower walls
   //    // to get picked up by the neighboring boxes.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO snap_redshift VALUES(0, 0.0001)";
   //       sql << "INSERT INTO snap_redshift VALUES(1, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(10, 10, 10, 1, 0, 0, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(10, 10, 10, 2, 0, 0, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(10, 10, 10, 3, 1, 1, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(10, 10, 10, 4, 1, 1, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(10, 10, 10, 5, 1, 1, 2, 0, 0, 0, 0, 0)";

   // 	 // Update the domain size.
   // 	 sql << "UPDATE metadata SET metavalue='21' WHERE metakey='boxsize'";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict.sub( "workflow:light-cone" );
   //    dict["redshift-min"] = "0";
   //    dict["ra-min"] = "0";
   //    dict["ra-max"] = "90";
   //    dict["dec-min"] = "0";
   //    dict["dec-max"] = "90";

   //    // Place to store row IDs.
   //    vector<long long> ids;

   //    // Generate all results.
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 12 );
   //    TS_ASSERT_EQUALS( ids[0], 3 );
   //    TS_ASSERT_EQUALS( ids[1], 4 );
   //    TS_ASSERT_EQUALS( ids[2], 5 );
   //    for( unsigned ii = 0; ii < 9; ++ii )
   //       TS_ASSERT_EQUALS( ids[3 + ii], ii%3 );
   // }

   // ///
   // ///
   // ///
   // void test_filter()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._unique = true;

   //    // Insert some values.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO snap_redshift VALUES(0, 0.001)";
   //       sql << "INSERT INTO snap_redshift VALUES(1, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(3, 3, 3, 2, 0, 0, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(4, 4, 4, 3, 0, 0, 3, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 4, 1, 1, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 5, 1, 1, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(3, 3, 3, 6, 1, 1, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(4, 4, 4, 7, 1, 1, 3, 0, 0, 0, 0, 0)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict.sub( "workflow:light-cone" );
   //    dict["geometry"] = "box";
   //    dict["redshift"] = "0.001";
   //    db_setup.dict["workflow:record-filter:filter-type"] = "pos_x";
   //    db_setup.dict["workflow:record-filter:filter-min"] = "1.5";
   //    db_setup.dict["workflow:record-filter:filter-max"] = "2.5";

   //    // Place to store row IDs.
   //    vector<long long> ids;

   //    // Only row 0.
   //    dict["query-box-size"] = "1.5";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 0 );

   //    // Only row 1.
   //    dict["query-box-size"] = "4.5";
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    ids.resize( 0 );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       ids.push_back( gal.values<long long>( "globalindex" )[0] );
   //    }
   //    TS_ASSERT_EQUALS( ids.size(), 1 );
   //    TS_ASSERT_EQUALS( ids[0], 1 );
   // }

   // ///
   // ///
   // ///
   // void test_output_fields()
   // {
   //    lightcone lc;

   //    // Turn off random rotation and shifting.
   //    lc._unique = true;

   //    // Insert some values.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO snap_redshift VALUES(0, 0.001)";
   //       sql << "INSERT INTO snap_redshift VALUES(1, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 1, 0, 0, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(3, 3, 3, 2, 0, 0, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(4, 4, 4, 3, 0, 0, 3, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 4, 1, 1, 0, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 5, 1, 1, 1, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_3 VALUES(3, 3, 3, 6, 1, 1, 2, 0, 0, 0, 0, 0)";
   //       sql << "INSERT INTO tree_4 VALUES(4, 4, 4, 7, 1, 1, 3, 0, 0, 0, 0, 0)";
   //    }

   //    // Prepare base dictionary.
   //    options::dictionary& dict = db_setup.dict.sub( "workflow:light-cone" );
   //    dict["geometry"] = "box";
   //    dict["redshift"] = "0.001";
   //    dict["query-box-size"] = "4.5";

   //    // Try without snapshot.
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       TS_ASSERT_THROWS_ANYTHING( gal.values<int>( "snapnum" )[0] );
   //    }

   //    // Now with snapshot.
   //    dict["output-fields"] = "snapnum";;
   //    db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    setup_lightcone( lc );
   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   //       TS_ASSERT_EQUALS( gal.values<int>( "snapnum" )[0], 0 );
   //    }
   // }

   // void setup_lightcone( lightcone& lc )
   // {
   //    // If we are already connected, disconnect.
   //    lc._db_disconnect();

   //    // Read in the dictionary from XML.
   //    options::xml_dict dict;
   //    dict.read( db_setup.xml_filename);
   //    lc.initialise( dict );

   // }

   void setUp()
   {
   }

   void tearDown()
   {
      // // Erase the table data.
      // soci::session sql( soci::sqlite3, db_setup.db_filename );
      // sql << "DELETE FROM snap_redshift";
      // sql << "DELETE FROM tree_1";
      // sql << "DELETE FROM tree_2";
      // sql << "DELETE FROM tree_3";
      // sql << "DELETE FROM tree_4";
   }
};
