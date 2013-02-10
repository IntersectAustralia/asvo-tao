#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/modules/sed.hh"
#include "tao/modules/lightcone.hh"

using namespace hpc;
using namespace tao;

#include "mpi_fixture.hh"
#include "db_fixture.hh"

///
/// SED class test suite.
///
class sed_suite : public CxxTest::TestSuite
{
public:

   // ///
   // /// Test default constructor.
   // ///
   // void test_ctor()
   // {
   //    tao::sed sed;
   // }

   // ///
   // /// Test no galaxies.
   // ///
   // void test_no_galaxies()
   // {
   // }

   // ///
   // /// Test no time-points.
   // ///
   // void test_no_timepoints()
   // {
   // }

   // ///
   // /// Test invalid input array sizes.
   // ///
   // /// The stellar mass production rates and metallicities must all
   // /// be the correct sized arrays in order to function. I expect
   // /// errors to be raised if this is not the case.
   // ///
   // void test_array_sizes()
   // {
   // }

   // ///
   // /// Test invalid spectral bands.
   // ///
   // /// While it's possible to run the code with zero spectral
   // /// bands, it doesn't make much sense. I expect an error to
   // /// be raised if this happens.
   // ///
   // void test_num_spectral_bands()
   // {
   // }

   // ///
   // /// Test single-stellar population array size.
   // ///
   // /// When reading from the SSP table, it should return a row
   // /// of the same size as the number of spectral bands. I
   // /// expect an error to be thrown if this is not the case.
   // ///
   // void test_ssp_size()
   // {
   // }

   // ///
   // /// Test metallicity interpolation.
   // ///
   // /// Check the regions of metallicity interpolation. It should
   // /// look like the following:
   // ///
   // ///    Metallicity range | Index
   // ///   ---------------------------
   // ///    0.0000 - 0.0005   | 0
   // ///    0.0005 - 0.0025   | 1
   // ///    0.0025 - 0.0070   | 2
   // ///    0.0070 - 0.0150   | 3
   // ///    0.0150 - 0.0300   | 4
   // ///    0.0300 - 0.0550   | 5
   // ///    0.0550 - inf      | 6
   // ///
   // void test_metal_interp()
   // {
   // }

   // // ///
   // // /// Test load table linear.
   // // ///
   // // void test_load_table_linear()
   // // {
   // //    lightcone lc;
   // //    sed sed;
   // //    setup_sed( lc, sed );
   // //    sed._load_table( 0, "tree_1" );

   // //    TS_ASSERT_EQUALS( sed._descs.size(), 4 );
   // //    TS_ASSERT_EQUALS( sed._descs[0], -1 );
   // //    TS_ASSERT_EQUALS( sed._descs[1], 0 );
   // //    TS_ASSERT_EQUALS( sed._descs[2], 1 );
   // //    TS_ASSERT_EQUALS( sed._descs[3], 2 );

   // //    TS_ASSERT_EQUALS( sed._parents.size(), 3 );
   // //    TS_ASSERT_EQUALS( sed._parents.get( 0 ), 1 );
   // //    TS_ASSERT_EQUALS( sed._parents.get( 1 ), 2 );
   // //    TS_ASSERT_EQUALS( sed._parents.get( 2 ), 3 );
   // //    TS_ASSERT( !sed._parents.has( 3 ) );

   // //    TS_ASSERT_EQUALS( sed._sfrs.size(), 4 );
   // //    TS_ASSERT_DELTA( sed._sfrs[0], 10.0, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._sfrs[1], 8.0, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._sfrs[2], 6.0, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._sfrs[3], 4.0, 1e-8 );

   // //    TS_ASSERT_EQUALS( sed._bulge_sfrs.size(), 4 );
   // //    TS_ASSERT_DELTA( sed._bulge_sfrs[0], 8.0, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._bulge_sfrs[1], 6.0, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._bulge_sfrs[2], 4.0, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._bulge_sfrs[3], 2.0, 1e-8 );

   // //    TS_ASSERT_EQUALS( sed._metals.size(), 4 );
   // //    TS_ASSERT_DELTA( sed._metals[0], 0.8, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._metals[1], 0.6, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._metals[2], 0.4, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._metals[3], 0.2, 1e-8 );

   // //    TS_ASSERT_EQUALS( sed._bulge_metals.size(), 4 );
   // //    TS_ASSERT_DELTA( sed._bulge_metals[0], 0.6, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._bulge_metals[1], 0.4, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._bulge_metals[2], 0.2, 1e-8 );
   // //    TS_ASSERT_DELTA( sed._bulge_metals[3], 0.0, 1e-8 );

   // //    TS_ASSERT_EQUALS( sed._snaps.size(), 4 );
   // //    TS_ASSERT_EQUALS( sed._snaps[0], 0 );
   // //    TS_ASSERT_EQUALS( sed._snaps[1], 1 );
   // //    TS_ASSERT_EQUALS( sed._snaps[2], 2 );
   // //    TS_ASSERT_EQUALS( sed._snaps[3], 3 );

   // //    TS_ASSERT_EQUALS( sed._cur_tree_id, 0 );
   // // }

   // ///
   // /// Test load table non-linear.
   // ///
   // void test_load_table_nonlinear()
   // {
   //    lightcone lc;
   //    sed sed;
   //    setup_sed( lc, sed );
   //    sed._load_table( 1, "tree_2" );

   //    TS_ASSERT_EQUALS( sed._descs.size(), 9 );
   //    TS_ASSERT_EQUALS( sed._descs[0], -1 );
   //    TS_ASSERT_EQUALS( sed._descs[1], 0 );
   //    TS_ASSERT_EQUALS( sed._descs[2], 0 );
   //    TS_ASSERT_EQUALS( sed._descs[3], 1 );
   //    TS_ASSERT_EQUALS( sed._descs[4], 2 );
   //    TS_ASSERT_EQUALS( sed._descs[5], 2 );
   //    TS_ASSERT_EQUALS( sed._descs[6], 3 );
   //    TS_ASSERT_EQUALS( sed._descs[7], 3 );
   //    TS_ASSERT_EQUALS( sed._descs[8], 5 );

   //    TS_ASSERT_EQUALS( sed._parents.size(), 8 );
   //    auto rng = sed._parents.equal_range( 0 );
   //    TS_ASSERT_EQUALS( std::distance( rng.first, rng.second ), 2 );
   //    std::pair<unsigned,unsigned> par = *rng.first++;
   //    TS_ASSERT_EQUALS( par.second, 1 );
   //    par = *rng.first++;
   //    TS_ASSERT_EQUALS( par.second, 2 );
   //    rng = sed._parents.equal_range( 1 );
   //    TS_ASSERT_EQUALS( std::distance( rng.first, rng.second ), 1 );
   //    par = *rng.first++;
   //    TS_ASSERT_EQUALS( par.second, 3 );
   //    rng = sed._parents.equal_range( 2 );
   //    TS_ASSERT_EQUALS( std::distance( rng.first, rng.second ), 2 );
   //    par = *rng.first++;
   //    TS_ASSERT_EQUALS( par.second, 4 );
   //    par = *rng.first++;
   //    TS_ASSERT_EQUALS( par.second, 5 );
   //    rng = sed._parents.equal_range( 3 );
   //    TS_ASSERT_EQUALS( std::distance( rng.first, rng.second ), 2 );
   //    par = *rng.first++;
   //    TS_ASSERT_EQUALS( par.second, 6 );
   //    par = *rng.first++;
   //    TS_ASSERT_EQUALS( par.second, 7 );
   //    rng = sed._parents.equal_range( 5 );
   //    TS_ASSERT_EQUALS( std::distance( rng.first, rng.second ), 1 );
   //    par = *rng.first++;
   //    TS_ASSERT_EQUALS( par.second, 8 );
   //    TS_ASSERT( !sed._parents.has( 4 ) );
   //    TS_ASSERT( !sed._parents.has( 6 ) );
   //    TS_ASSERT( !sed._parents.has( 7 ) );
   //    TS_ASSERT( !sed._parents.has( 8 ) );

   //    TS_ASSERT_EQUALS( sed._snaps.size(), 9 );
   //    TS_ASSERT_EQUALS( sed._snaps[0], 0 );
   //    TS_ASSERT_EQUALS( sed._snaps[1], 1 );
   //    TS_ASSERT_EQUALS( sed._snaps[2], 1 );
   //    TS_ASSERT_EQUALS( sed._snaps[3], 2 );
   //    TS_ASSERT_EQUALS( sed._snaps[4], 2 );
   //    TS_ASSERT_EQUALS( sed._snaps[5], 2 );
   //    TS_ASSERT_EQUALS( sed._snaps[6], 3 );
   //    TS_ASSERT_EQUALS( sed._snaps[7], 3 );
   //    TS_ASSERT_EQUALS( sed._snaps[8], 3 );

   //    TS_ASSERT_EQUALS( sed._cur_tree_id, 1 );
   // }

   // ///
   // ///
   // ///
   // void test_setup_snap_ages()
   // {
   //    lightcone lc;
   //    sed sed;
   //    setup_sed( lc, sed );
   //    sed._load_table( 1, "tree_2" );

   //    TS_ASSERT_EQUALS( sed._snap_ages.size(), 4 );
   //    TS_ASSERT_DELTA( sed._snap_ages[3], 0.128088, 1e-5 );
   //    TS_ASSERT_DELTA( sed._snap_ages[2], 0.013605, 1e-5 );
   //    TS_ASSERT_DELTA( sed._snap_ages[1], 0.0013689, 1e-6 );
   //    TS_ASSERT_DELTA( sed._snap_ages[0], 0.0, 1e-8 );
   // }

   // ///
   // ///
   // ///
   // void test_read_ssp()
   // {
   //    lightcone lc;
   //    sed sed;
   //    setup_sed( lc, sed );
   //    sed._read_ssp( db_setup.ssp_filename );

   //    TS_ASSERT_EQUALS( sed._bin_ages.size(), 3 );
   //    TS_ASSERT_EQUALS( sed._disk_age_masses.size(), 3 );
   //    TS_ASSERT_EQUALS( sed._bulge_age_masses.size(), 3 );
   //    TS_ASSERT_EQUALS( sed._disk_age_metals.size(), 3 );
   //    TS_ASSERT_EQUALS( sed._bulge_age_metals.size(), 3 );
   //    TS_ASSERT_EQUALS( sed._ssp.size(), 42 );
   // }

   // ///
   // ///
   // ///
   // void test_find_bin()
   // {
   //    lightcone lc;
   //    sed sed;
   //    setup_sed( lc, sed );
   //    sed._read_ssp( db_setup.ssp_filename );

   //    TS_ASSERT_EQUALS( sed._find_bin( 0.0 ), 0 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.05 ), 0 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.1 ), 0 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.14 ), 0 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.16 ), 1 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.2 ), 1 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.24 ), 1 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.26 ), 2 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.8 ), 2 );
   // }

   ///
   ///
   ///
   void test_rebin_info_linear()
   {
      LOG_FILE( "test.log" );

      lightcone lc;
      sed sed;
      setup_sed( lc, sed );

      for( lc.begin(); !lc.done(); ++lc )
      {
         const galaxy& gal = *lc;
	 if( gal.tree_id() == 0 )
	 {
	    sed._load_table( gal.tree_id(), gal.table() );
	    sed._rebin_info( gal );

	    std::cout << "\n" << sed._disk_age_masses << "\n";
	    std::cout << "\n" << sed._bulge_age_masses << "\n";
	 }
      }
   }

   void setup_sed( tao::lightcone& lc, tao::sed& sed )
   {
      // Turn off random rotation and shifting.
      lc._unique = true;

      // Insert some values.
      {
         soci::session sql( soci::sqlite3, db_setup.db_filename );
         sql << "INSERT INTO snap_redshift VALUES(0, 0.3)";
         sql << "INSERT INTO snap_redshift VALUES(1, 0.2)";
         sql << "INSERT INTO snap_redshift VALUES(2, 0.1)";
         sql << "INSERT INTO snap_redshift VALUES(3, 0.0)";
	 // posx, posy, posz, globalindex, snapnu, localgalaxyid, globaltreeid, desc, ...
         sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 0,  0, 0, 0,  1, 0.8, 0.6, 10, 8)";
         sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 1,  1, 1, 0,  2, 0.6, 0.4, 8,  6)";
         sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 2,  2, 2, 0,  3, 0.4, 0.2, 6,  4)";
         sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 3,  3, 3, 0, -1, 0.2, 0,   4,  2)";
         sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 4,  0, 0, 1, -1, 0.8, 0.6, 10, 8)";
         sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 5,  1, 1, 1,  0, 0.6, 0.4, 8,  6)";
         sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 6,  1, 2, 1,  0, 0.6, 0.4, 8,  6)";
         sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 7,  2, 3, 1,  1, 0.4, 0.2, 6,  4)";
         sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 8,  2, 4, 1,  2, 0.4, 0.2, 6,  4)";
         sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 9,  2, 5, 1,  2, 0.4, 0.2, 6,  4)";
         sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 10, 3, 6, 1,  3, 0.2, 0,   4,  2)";
         sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 11, 3, 7, 1,  3, 0.2, 0,   4,  2)";
         sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 12, 3, 8, 1,  5, 0.2, 0,   4,  2)";
      }

      // Prepare base dictionary.
      {
	 options::dictionary& dict = db_setup.dict.sub( "light-cone" );
	 dict["query-box-size"] = "10";
	 dict["geometry"] = "box";
	 dict["redshift"] = "0";
	 db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
      }

      // If we are already connected, disconnect.
      lc._db_disconnect();
      sed._db_disconnect();

      // Read in the dictionary from XML.
      options::dictionary dict;
      setup_common_options( dict );
      lc.setup_options( dict, "light-cone" );
      sed.setup_options( dict, "sed" );
      dict.compile();
      options::xml xml;
      xml.read( db_setup.xml_filename, dict );
      lc.initialise( dict, "light-cone" );
      sed.initialise( dict, "sed" );
   }

   void tearDown()
   {
      // Erase the table data.
      soci::session sql( soci::sqlite3, db_setup.db_filename );
      sql << "DELETE FROM snap_redshift";
      sql << "DELETE FROM tree_1";
      sql << "DELETE FROM tree_2";
   }
};
