#include <vector>
#include <boost/lexical_cast.hpp>
#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include "tao/base/types.hh"
#include "tao/base/globals.hh"
#include "tao/base/soci_backend.hh"

///
/// Prepare a tree table. Setup a variety of trees
/// to test fringe cases.
///
/// Tree 1 setup (normal):
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
/// Tree 2 setup (normal/small):
///
///           z   snap
///           4    0
///   1 2     1    3
///   |/
///   0       0.2  4
///
/// Tree 3 setup (forest):
///
///             z   snap
///             4    0
///   1 2 4 5   1    3
///   |/  |/
///   0   3     0.2  4
///
/// Tree 4 setup (unit):
///
///       z   snap
///       4    0
///   0   0.2  4
///
///
struct db_fixture
{
   db_fixture()
   {
      // Build the database.
      sql.open( soci::sqlite3, ":memory:" );
      setup_tree_table( sql );
      setup_snapshot_table( sql );
      setup_summary_table( sql );
      setup_metadata_table( sql );

      // Setup backend.
      be.connect( sql );
      sim.set_box_size( 500 );
      sim.set_cosmology( 71.0, 0.25, 0.75 );
      std::vector<tao::real_type> redshifts( 5 );
      redshifts[0] = 127;
      redshifts[1] = 80;
      redshifts[2] = 63;
      redshifts[3] = 20;
      redshifts[4] = 0;
      sim.set_snapshot_redshifts( redshifts );
      be.set_simulation( &sim );
      lc.set_simulation( &sim );
      lc.set_geometry( 0, 89, 0, 89, 127 );
      tile.set_lightcone( &lc );
   }

   void
   setup_tree_table( ::soci::session& sql )
   {
      for( int ii = 1; ii <= 5; ++ii )
      {
         std::string sql_str = std::string( "CREATE TABLE tree_" ) + boost::lexical_cast<std::string>( ii ) +
            " (globalindex BIGINT, localgalaxyid INTEGER, globaltreeid BIGINT, "
            "descendant INTEGER, snapnum INTEGER, sfrdisk DOUBLE PRECISION, sfrbulge DOUBLE PRECISION, "
            "coldgas DOUBLE PRECISION, metalscoldgas DOUBLE PRECISION, "
            "posx DOUBLE PRECISION, posy DOUBLE PRECISION, posz DOUBLE PRECISION, "
            "velx DOUBLE PRECISION, vely DOUBLE PRECISION, velz DOUBLE PRECISION, "
            "depthfirst_traversalorder INTEGER, subtree_count INTEGER, "
            "sfrdiskz DOUBLE PRECISION, sfrbulgez DOUBLE PRECISION, "
            "stellarmass DOUBLE PRECISION, mergetype INTEGER, dt DOUBLE PRECISION)";
         this->sql << sql_str;
      }

      //                                gid  l  tr  d sn  sfr sfrb cg mcg  x  y  z vx vy vz df sc   dz   bz

      // Tree 1.
      sql << "INSERT INTO tree_1 VALUES(100, 0, 1, -1, 4, 0.1, 0.8, 1,  8, 1, 1, 1, 0, 0, 0, 0, 7, 1.1, 1.8, 4.1, 0, 0)";
      sql << "INSERT INTO tree_1 VALUES(101, 1, 1,  0, 3, 0.2, 0.9, 2,  9, 1, 0, 0, 0, 0, 0, 1, 6, 1.2, 1.9, 4.2, 0, 0)";
      sql << "INSERT INTO tree_1 VALUES(102, 2, 1,  1, 2, 0.3, 1.0, 3, 10, 2, 0, 0, 0, 0, 0, 2, 2, 1.3, 2.0, 4.3, 0, 0)";
      sql << "INSERT INTO tree_1 VALUES(103, 3, 1,  1, 2, 0.4, 1.1, 4, 11, 0, 1, 0, 0, 0, 0, 4, 3, 1.4, 2.1, 4.4, 0, 0)";
      sql << "INSERT INTO tree_1 VALUES(104, 4, 1,  2, 1, 0.5, 1.2, 5, 12, 0, 2, 0, 0, 0, 0, 3, 1, 1.5, 2.2, 4.5, 0, 0)";
      sql << "INSERT INTO tree_1 VALUES(105, 5, 1,  3, 1, 0.6, 1.3, 6, 13, 0, 3, 0, 0, 0, 0, 5, 1, 1.6, 2.3, 4.6, 0, 0)";
      sql << "INSERT INTO tree_1 VALUES(106, 6, 1,  3, 1, 0.7, 1.4, 7, 14, 0, 0, 1, 0, 0, 0, 6, 1, 1.7, 2.4, 4.7, 0, 0)";

      // Tree 2.
      sql << "INSERT INTO tree_2 VALUES(200, 0, 2, -1, 4, 1, 1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_2 VALUES(201, 1, 2,  0, 3, 1, 1, 1, 1, 0, 0, 3, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_2 VALUES(202, 2, 2,  0, 3, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0)";

      // Tree 5 setup:
      //
      //            z   snap
      //            21   0
      //   2  3 4   10   1
      //   |  | |
      //   1  1 2   3    2
      //   |  |/
      //   0  0     0    3
      //                                gid  l  tr  d sn sfr sfrb cg mcg  x  y  z vx vy vz df sc  dz bz
      sql << "INSERT INTO tree_5 VALUES(500, 0, 5, -1, 3, 1, 10, 1, 1, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(501, 1, 5,  0, 2, 2, 20, 1, 1, 0, 0, 3, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(502, 2, 5,  1, 1, 3, 30, 1, 1, 1, 1, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0)";
      // ICS
      sql << "INSERT INTO tree_5 VALUES(503, 0, 6, -1, 3, 1, 10, 1, 1, 0, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(504, 1, 6,  0, 2, 2, 20, 1, 1, 0, 0, 3, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(505, 2, 6,  0, 2, 2, 20, 1, 1, 0, 0, 3, 0, 0, 0, 3, 2, 0, 0, 0, 4, 0)";
      sql << "INSERT INTO tree_5 VALUES(506, 3, 6,  1, 1, 3, 30, 1, 1, 1, 1, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(507, 4, 6,  2, 1, 3, 30, 1, 1, 1, 1, 1, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0)";
      // Minor
      sql << "INSERT INTO tree_5 VALUES(508, 0, 7, -1, 3, 1, 10, 1, 1, 0, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(509, 1, 7,  0, 2, 2, 20, 1, 1, 0, 0, 3, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(510, 2, 7,  0, 2, 2, 20, 1, 1, 0, 0, 3, 0, 0, 0, 3, 2, 0, 0, 0, 1, 0)";
      sql << "INSERT INTO tree_5 VALUES(511, 3, 7,  1, 1, 3, 30, 1, 1, 1, 1, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(512, 4, 7,  2, 1, 3, 30, 1, 1, 1, 1, 1, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0)";
      // Major
      sql << "INSERT INTO tree_5 VALUES(513, 0, 8, -1, 3, 1, 10, 1, 1, 0, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(514, 1, 8,  0, 2, 2, 20, 1, 1, 0, 0, 3, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(515, 2, 8,  0, 2, 2, 20, 1, 1, 0, 0, 3, 0, 0, 0, 3, 2, 0, 0, 0, 2, 0)";
      sql << "INSERT INTO tree_5 VALUES(516, 3, 8,  1, 1, 3, 30, 1, 1, 1, 1, 1, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0)";
      sql << "INSERT INTO tree_5 VALUES(517, 4, 8,  2, 1, 3, 30, 1, 1, 1, 1, 1, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0)";
   }

   void
   setup_snapshot_table( soci::session& sql )
   {
      sql << "CREATE TABLE snap_redshift (snapnum INTEGER, redshift DOUBLE PRECISION)";
      sql << "INSERT INTO snap_redshift VALUES(0, 34)";
      sql << "INSERT INTO snap_redshift VALUES(1, 21)";
      sql << "INSERT INTO snap_redshift VALUES(2, 10)";
      sql << "INSERT INTO snap_redshift VALUES(3, 3)";
      sql << "INSERT INTO snap_redshift VALUES(4, 0)";
   }

   void
   setup_summary_table( soci::session& sql )
   {
      sql << "CREATE TABLE summary (tablename VARCHAR, "
         "minx DOUBLE PRECISION, miny DOUBLE PRECISION, minz DOUBLE PRECISION, "
         "maxx DOUBLE PRECISION, maxy DOUBLE PRECISION, maxz DOUBLE PRECISION, "
	 "galaxycount INTEGER)";
      sql << "INSERT INTO summary VALUES('tree_1', 0, 0, 0, 1, 1, 1, 10)";
      sql << "INSERT INTO summary VALUES('tree_2', 0, 0, 0, 1, 1, 1, 10)";
   }

   void
   setup_metadata_table( soci::session& sql )
   {
      // Add a metadata table and insert a value.
      sql << "CREATE TABLE metadata (metakey CHARACTER VARYING, metavalue CHARACTER VARYING)";
      sql << "INSERT INTO metadata VALUES('boxsize', '500')";
      sql << "INSERT INTO metadata VALUES('hubble', '71.0')";
      sql << "INSERT INTO metadata VALUES('omega_m', '0.25')";
      sql << "INSERT INTO metadata VALUES('omega_l', '0.75')";
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
   tao::backends::soci<tao::real_type> be;
   tao::simulation sim;
   tao::lightcone lc;
   tao::tile<tao::real_type> tile;
};
