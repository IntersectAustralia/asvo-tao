#include <soci/postgresql/soci-postgresql.h>
#include "tao/base/types.hh"

using namespace tao;

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
struct db_fixture
{
   db_fixture()
   {
      try
      {
         sql.open( soci::postgresql, "dbname=tao_unit_test" );
         sql << "SELECT * FROM hello";
      }
      catch( std::exception& ex )
      {
         std::cout << ex.what();
         exit(1);
      }
      // setup_tree_table( sql );
      // setup_snapshot_table( sql );
      // be.connect( sql );
   }

   void
   setup_tree_table( ::soci::session& sql )
   {
      this->sql << "CREATE TABLE tree_1 (globalgalaxyid BIGINT, localgalaxyid INTEGER, globaltreeid BIGINT, "
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

   // ///
   // /// Prepare the galaxies as described in the trees above.
   // ///
   // void
   // setup_galaxy( tao::galaxy& gal )
   // {
   //    gal.set_batch_size( 10 );
   //    table = "tree_1";
   //    gal.set_table( table );

   //    globalindex.resize( 10 );
   //    for( unsigned ii = 0; ii < 7; ++ii )
   //       globalindex[ii]  = 100 + ii;
   //    for( unsigned ii = 0; ii < 3; ++ii )
   //       globalindex[7 + ii]  = 200 + ii;
   //    gal.set_field<long long>( "globalindex", globalindex );

   //    globaltreeid.resize( 10 );
   //    for( unsigned ii = 0; ii < 7; ++ii )
   //       globaltreeid[ii] = 1;
   //    for( unsigned ii = 0; ii < 3; ++ii )
   //       globaltreeid[7 + ii] = 2;
   //    gal.set_field<long long>( "globaltreeid", globaltreeid );

   //    localgalaxyid.resize( 10 );
   //    for( unsigned ii = 0; ii < 7; ++ii )
   //       localgalaxyid[ii] = ii;
   //    for( unsigned ii = 0; ii < 3; ++ii )
   //       localgalaxyid[7 + ii] = ii;
   //    gal.set_field<int>( "localgalaxyid", localgalaxyid );
   // }

   // hpc::string table;
   // hpc::vector<long long> globalindex;
   // hpc::vector<long long> globaltreeid;
   // hpc::vector<int> localgalaxyid;

   soci::session sql;
   tao::backends::soci<real_type> be;
};
