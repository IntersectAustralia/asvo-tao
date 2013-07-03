#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/base/sfh.hh"
#include "mpi_fixture.hh"

using namespace hpc;
using namespace tao;

///
/// Star-formation history class test suite.
///
class sfh_suite : public CxxTest::TestSuite
{
public:

   ///
   /// Test default constructor.
   ///
   void test_default_constructor()
   {
      sfh<double> sfh;
      TS_ASSERT( !sfh._snap_ages );
      TS_ASSERT( !sfh._bin_ages );
      TS_ASSERT_EQUALS( sfh._thresh, 1000000 );
   }

   ///
   /// Test load tree data from database.
   ///
   void test_load_tree_data()
   {
      soci::session sql( soci::sqlite3, ":memory:" );
      setup_tree_table( sql );

      sfh<double> sfh;
      sfh.load_tree_data( sql, "tree_1", 1 );

      // Accumulation must be disabled.
      TS_ASSERT( !sfh._accum );

      // Check descendants.
      TS_ASSERT_EQUALS( sfh._descs.size(), 7 );
      TS_ASSERT_EQUALS( sfh._descs[0], -1 );
      TS_ASSERT_EQUALS( sfh._descs[1], 0 );
      TS_ASSERT_EQUALS( sfh._descs[2], 1 );
      TS_ASSERT_EQUALS( sfh._descs[3], 1 );
      TS_ASSERT_EQUALS( sfh._descs[4], 2 );
      TS_ASSERT_EQUALS( sfh._descs[5], 3 );
      TS_ASSERT_EQUALS( sfh._descs[6], 3 );

      // Check snapshots.
      TS_ASSERT_EQUALS( sfh._snaps.size(), 7 );
      TS_ASSERT_EQUALS( sfh._snaps[0], 4 );
      TS_ASSERT_EQUALS( sfh._snaps[1], 3 );
      TS_ASSERT_EQUALS( sfh._snaps[2], 2 );
      TS_ASSERT_EQUALS( sfh._snaps[3], 2 );
      TS_ASSERT_EQUALS( sfh._snaps[4], 1 );
      TS_ASSERT_EQUALS( sfh._snaps[5], 1 );
      TS_ASSERT_EQUALS( sfh._snaps[6], 1 );

      // Check SFRs.
      TS_ASSERT_EQUALS( sfh._sfrs.size(), 7 );
      TS_ASSERT_EQUALS( sfh._sfrs[0], 1 );
      TS_ASSERT_EQUALS( sfh._sfrs[1], 1 );
      TS_ASSERT_EQUALS( sfh._sfrs[2], 1 );
      TS_ASSERT_EQUALS( sfh._sfrs[3], 1 );
      TS_ASSERT_EQUALS( sfh._sfrs[4], 1 );
      TS_ASSERT_EQUALS( sfh._sfrs[5], 1 );
      TS_ASSERT_EQUALS( sfh._sfrs[6], 1 );

      // Check table cache.
      TS_ASSERT( sfh._cur_table == "tree_1" );
      TS_ASSERT_EQUALS( sfh._cur_tree_id, 1 );
   }

   ///
   /// Test load tree data from database when tree size is
   /// greater than threshold.
   ///
   void test_load_tree_data_threshold()
   {
      soci::session sql( soci::sqlite3, ":memory:" );
      setup_tree_table( sql );

      sfh<double> sfh;
      sfh._thresh = 1;
      sfh.load_tree_data( sql, "tree_1", 2 );

      // Accumulation must be enabled.
      TS_ASSERT( sfh._accum );

      // Arrays must be empty.
      TS_ASSERT( sfh._descs.empty() );
      TS_ASSERT( sfh._snaps.empty() );
      TS_ASSERT( sfh._sfrs.empty() );

      // Check table cache.
      TS_ASSERT( sfh._cur_table == "tree_1" );
      TS_ASSERT_EQUALS( sfh._cur_tree_id, 2 );
   }

   ///
   /// Test data rebinning.
   ///
   void test_rebin()
   {
      soci::session sql( soci::sqlite3, ":memory:" );
      setup_tree_table( sql );

      age_line<double> snap_ages, bin_ages;
      snap_ages.load_ages( sql );
      {
         vector<double> ages( 5 );
         ages[0] = redshift_to_age<double>( 5 );
         ages[1] = redshift_to_age<double>( 2 );
         ages[2] = redshift_to_age<double>( 1 );
         ages[3] = redshift_to_age<double>( 0.9 );
         ages[4] = redshift_to_age<double>( 0.8 );
         bin_ages.set_ages( ages );
      }

      vector<double> age_masses( 5 ), bulge_age_masses( 5 ), age_metals( 5 );
      sfh<double> sfh;
      sfh.set_snapshot_ages( &snap_ages );
      sfh.set_bin_ages( &bin_ages );
      sfh.load_tree_data( sql, "tree_1", 2 );
      sfh.rebin<double>( sql, 0, age_masses, bulge_age_masses, age_metals );
   }

   ///
   /// Test data rebinning with accumulation.
   ///
   void test_rebin_accumulate()
   {
      soci::session sql( soci::sqlite3, ":memory:" );
      setup_tree_table( sql );

      age_line<double> snap_ages, bin_ages;
      snap_ages.load_ages( sql );
      {
         vector<double> ages( 5 );
         ages[0] = redshift_to_age<double>( 5 );
         ages[1] = redshift_to_age<double>( 2 );
         ages[2] = redshift_to_age<double>( 1 );
         ages[3] = redshift_to_age<double>( 0.9 );
         ages[4] = redshift_to_age<double>( 0.8 );
         bin_ages.set_ages( ages );
      }

      vector<double> age_masses( 5 ), bulge_age_masses( 5 ), age_metals( 5 );
      sfh<double> sfh;
      sfh._thresh = 1;
      sfh.set_snapshot_ages( &snap_ages );
      sfh.set_bin_ages( &bin_ages );
      sfh.load_tree_data( sql, "tree_1", 2 );
      sfh.rebin<double>( sql, 0, age_masses, bulge_age_masses, age_metals );
   }

   ///
   /// Prepare a tree table. There are two trees to test proper
   /// tree selection.
   ///
   /// Tree 1 setup:
   ///
   ///           z   snap
   ///           4    0
   ///   4 5 6   3    1
   ///   | |/
   ///   2 3     2    2
   ///   |/
   ///   1       1    3
   ///   |
   ///   0       0.2  4
   ///
   /// Tree 2 setup:
   ///
   ///           z   snap
   ///           4    0
   ///   1 2     1    3
   ///   |/
   ///   0       0.2  4
   ///
   void
   setup_tree_table( soci::session& sql )
   {
      sql << "CREATE TABLE tree_1 (globalgalaxyid BIGINT, localgalaxyid INTEGER, globaltreeid BIGINT, "
         "descendant INTEGER, snapnum INTEGER, sfr DOUBLE PRECISION, sfrbulge DOUBLE PRECISION, "
         "coldgas DOUBLE PRECISION, metalscoldgas DOUBLE PRECISION)";
      sql << "CREATE TABLE snap_redshift (snapnum INTEGER, redshift DOUBLE PRECISION)";

      // Tree 1.
      sql << "INSERT INTO tree_1 VALUES(100, 0, 1, -1, 4, 1, 1, 1, 1)";
      sql << "INSERT INTO tree_1 VALUES(101, 1, 1,  0, 3, 1, 1, 1, 1)";
      sql << "INSERT INTO tree_1 VALUES(102, 2, 1,  1, 2, 1, 1, 1, 1)";
      sql << "INSERT INTO tree_1 VALUES(103, 3, 1,  1, 2, 1, 1, 1, 1)";
      sql << "INSERT INTO tree_1 VALUES(104, 4, 1,  2, 1, 1, 1, 1, 1)";
      sql << "INSERT INTO tree_1 VALUES(105, 5, 1,  3, 1, 1, 1, 1, 1)";
      sql << "INSERT INTO tree_1 VALUES(106, 6, 1,  3, 1, 1, 1, 1, 1)";

      // Tree 2.
      sql << "INSERT INTO tree_1 VALUES(200, 0, 2, -1, 4, 1, 1, 1, 1)";
      sql << "INSERT INTO tree_1 VALUES(201, 1, 2,  0, 3, 1, 1, 1, 1)";
      sql << "INSERT INTO tree_1 VALUES(202, 2, 2,  0, 3, 1, 1, 1, 1)";

      // Snapshots.
      sql << "INSERT INTO snap_redshift VALUES(0, 4)";
      sql << "INSERT INTO snap_redshift VALUES(1, 3)";
      sql << "INSERT INTO snap_redshift VALUES(2, 2)";
      sql << "INSERT INTO snap_redshift VALUES(3, 1)";
      sql << "INSERT INTO snap_redshift VALUES(4, 0.2)";
   }

   void
   setup_snapshot_table( soci::session& sql )
   {
      sql << "CREATE TABLE snap_redshift (snapnum INTEGER, redshift DOUBLE PRECISION)";
      sql << "INSERT INTO snap_redshift VALUES(0, 127)";
      sql << "INSERT INTO snap_redshift VALUES(1, 80)";
      sql << "INSERT INTO snap_redshift VALUES(2, 63)";
      sql << "INSERT INTO snap_redshift VALUES(3, 20)";
      sql << "INSERT INTO snap_redshift VALUES(4, 10)";
   }
};
