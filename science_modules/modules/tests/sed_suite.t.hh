#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/modules/sed.hh"
#include "tao/modules/lightcone.hh"

using namespace hpc;
using namespace tao;

#include "mpi_fixture.hh"

///
/// SED class test suite.
///
class sed_suite : public CxxTest::TestSuite
{
public:

   ///
   /// Test default constructor.
   ///
   void test_ctor()
   {
      tao::sed sed;
   }

   ///
   /// Test redshift to age calculation. Ned's cosmological calculator
   /// from online suggests with constants of H0=73, OmegaM=0.25 and
   /// OmegaV=0.75 we should get an age for redshift 3 of 2.211 Gyr.
   ///
   void test_redshift_to_age()
   {
      tao::sed sed;
      double age = sed._calc_age( 3.0 );
      TS_ASSERT_DELTA( age, 2.211, 1e-3 )
   }

   ///
   /// Tree setup:
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
   void test_rebin_recurse()
   {
      tao::sed sed;

      // Prepare some fake snapshot ages.
      sed._snap_ages.resize( 5 );
      sed._snap_ages[0] = sed._calc_age( 4 );
      sed._snap_ages[1] = sed._calc_age( 3 );
      sed._snap_ages[2] = sed._calc_age( 2 );
      sed._snap_ages[3] = sed._calc_age( 1 );
      sed._snap_ages[4] = sed._calc_age( 0.2 );

      // Prepare a fake parent tree.
      sed._parents.insert( 0, 1 );
      sed._parents.insert( 1, 2 );
      sed._parents.insert( 1, 3 );
      sed._parents.insert( 2, 4 );
      sed._parents.insert( 3, 5 );
      sed._parents.insert( 3, 6 );

      // Fake snapshots.
      sed._snaps.resize( 7 );
      sed._snaps[0] = 4;
      sed._snaps[1] = 3;
      sed._snaps[2] = 2;
      sed._snaps[3] = 2;
      sed._snaps[4] = 1;
      sed._snaps[5] = 1;
      sed._snaps[6] = 1;

      // SFRs.
      sed._sfrs.resize( 7 );
      sed._sfrs[0] = 1;
      sed._sfrs[1] = 1;
      sed._sfrs[2] = 1;
      sed._sfrs[3] = 1;
      sed._sfrs[4] = 1;
      sed._sfrs[5] = 1;
      sed._sfrs[6] = 1;
      sed._bulge_sfrs.resize( 7 );
      sed._bulge_sfrs[0] = 1;
      sed._bulge_sfrs[1] = 1;
      sed._bulge_sfrs[2] = 1;
      sed._bulge_sfrs[3] = 1;
      sed._bulge_sfrs[4] = 1;
      sed._bulge_sfrs[5] = 1;
      sed._bulge_sfrs[6] = 1;

      // Metals/coldgas.
      sed._metals.resize( 7 );
      sed._metals[0] = 1;
      sed._metals[1] = 1;
      sed._metals[2] = 1;
      sed._metals[3] = 1;
      sed._metals[4] = 1;
      sed._metals[5] = 1;
      sed._metals[6] = 1;
      sed._cold_gas.resize( 7 );
      sed._cold_gas[0] = 10;
      sed._cold_gas[1] = 10;
      sed._cold_gas[2] = 10;
      sed._cold_gas[3] = 10;
      sed._cold_gas[4] = 10;
      sed._cold_gas[5] = 10;
      sed._cold_gas[6] = 10;

      // Rebinning ages.
      sed._bin_ages.resize( 6 );
      sed._bin_ages[0] = 0;
      sed._bin_ages[1] = 1;
      sed._bin_ages[2] = 2;
      sed._bin_ages[3] = 4;
      sed._bin_ages[4] = 8;
      sed._bin_ages[5] = 10;
      sed._dual_ages.resize( 5 );
      sed._dual_ages[0] = 0.5;
      sed._dual_ages[1] = 1.5;
      sed._dual_ages[2] = 3;
      sed._dual_ages[3] = 6;
      sed._dual_ages[4] = 9;

      // Results.
      sed._age_masses.resize( sed._bin_ages.size() );
      sed._bulge_age_masses.resize( sed._age_masses.size() );
      sed._age_metals.resize( sed._age_masses.size() );
      std::fill( sed._age_masses.begin(), sed._age_masses.end(), 0.0 );
      std::fill( sed._bulge_age_masses.begin(), sed._bulge_age_masses.end(), 0.0 );
      std::fill( sed._age_metals.begin(), sed._age_metals.end(), 0.0 );

      // Call the recursive rebinning.
      sed._rebin_recurse( 0, sed._snap_ages[sed._snaps[0]] );
   }

   ///
   /// Test no galaxies.
   ///
   void test_no_galaxies()
   {
   }

   ///
   /// Test no time-points.
   ///
   void test_no_timepoints()
   {
   }

   ///
   /// Test invalid input array sizes. The stellar mass production
   /// rates and metallicities must all be the correct sized arrays
   /// in order to function. I expect errors to be raised if this
   /// is not the case.
   ///
   void test_array_sizes()
   {
   }

   ///
   /// Test invalid spectral bands. While it's possible to run
   /// the code with zero spectral bands, it doesn't make much
   /// sense. I expect an error to be raised if this happens.
   ///
   void test_num_spectral_bands()
   {
   }

   ///
   /// Test single-stellar population array size. When reading
   /// from the SSP table, it should return a row of the same
   /// size as the number of spectral bands. I expect an error
   /// to be thrown if this is not the case.
   ///
   void test_ssp_size()
   {
   }

   ///
   /// Test metallicity interpolation. Check the regions of
   /// metallicity interpolation. It should look like the following:
   ///
   ///    Metallicity range | Index
   ///   ---------------------------
   ///    0.0000 - 0.0005   | 0
   ///    0.0005 - 0.0025   | 1
   ///    0.0025 - 0.0070   | 2
   ///    0.0070 - 0.0150   | 3
   ///    0.0150 - 0.0300   | 4
   ///    0.0300 - 0.0550   | 5
   ///    0.0550 - inf      | 6
   ///
   void test_metal_interp()
   {
   }

   // ///
   // /// Test load table linear.
   // ///
   // void test_load_table_linear()
   // {
   // 	  LOG_PUSH( new hpc::mpi::logger( "TestCasesLogFileSED.log" ) );
   //    lightcone lc;
   //    sed sed;
   //    setup_sed( lc, sed );
   //    sed._load_table( 0, "tree_1" );

   //    TS_ASSERT_EQUALS( sed._descs.size(), 4 );
   //    TS_ASSERT_EQUALS( sed._descs[0], 1 );
   //    TS_ASSERT_EQUALS( sed._descs[1], 2 );
   //    TS_ASSERT_EQUALS( sed._descs[2], 3 );
   //    TS_ASSERT_EQUALS( sed._descs[3], -1 );

   //    TS_ASSERT_EQUALS( sed._parents.size(), 3 );
   //    TS_ASSERT_EQUALS( sed._parents.get( 1 ), 0 );
   //    TS_ASSERT_EQUALS( sed._parents.get( 2 ), 1 );
   //    TS_ASSERT_EQUALS( sed._parents.get( 3 ), 2 );
   //    TS_ASSERT( !sed._parents.has( 0 ) );

   //    TS_ASSERT_EQUALS( sed._sfrs.size(), 4 );
   //    TS_ASSERT_DELTA( sed._sfrs[0], 10.0, 1e-8 );
   //    TS_ASSERT_DELTA( sed._sfrs[1], 8.0, 1e-8 );
   //    TS_ASSERT_DELTA( sed._sfrs[2], 6.0, 1e-8 );
   //    TS_ASSERT_DELTA( sed._sfrs[3], 4.0, 1e-8 );

   //    TS_ASSERT_EQUALS( sed._bulge_sfrs.size(), 4 );
   //    TS_ASSERT_DELTA( sed._bulge_sfrs[0], 8.0, 1e-8 );
   //    TS_ASSERT_DELTA( sed._bulge_sfrs[1], 6.0, 1e-8 );
   //    TS_ASSERT_DELTA( sed._bulge_sfrs[2], 4.0, 1e-8 );
   //    TS_ASSERT_DELTA( sed._bulge_sfrs[3], 2.0, 1e-8 );

   //    TS_ASSERT_EQUALS( sed._metals.size(), 4 );
   //    TS_ASSERT_DELTA( sed._metals[0], 0.8, 1e-8 );
   //    TS_ASSERT_DELTA( sed._metals[1], 0.6, 1e-8 );
   //    TS_ASSERT_DELTA( sed._metals[2], 0.4, 1e-8 );
   //    TS_ASSERT_DELTA( sed._metals[3], 0.2, 1e-8 );

   //    TS_ASSERT_EQUALS( sed._snaps.size(), 4 );
   //    TS_ASSERT_EQUALS( sed._snaps[0], 0 );
   //    TS_ASSERT_EQUALS( sed._snaps[1], 1 );
   //    TS_ASSERT_EQUALS( sed._snaps[2], 2 );
   //    TS_ASSERT_EQUALS( sed._snaps[3], 3 );

   //    TS_ASSERT_EQUALS( sed._cur_tree_id, 0 );
   // }

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
   //    TS_ASSERT_DELTA( sed._snap_ages[3], 0.0, 1e-5 );
   //    TS_ASSERT_DELTA( sed._snap_ages[2], 0.1280, 1e-3 );
   //    TS_ASSERT_DELTA( sed._snap_ages[1], 0.2402, 1e-3 );
   //    TS_ASSERT_DELTA( sed._snap_ages[0], 0.3387, 1e-3 );
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

   //    TS_ASSERT_EQUALS( sed._bin_ages.size(), 4 );
   //    TS_ASSERT_EQUALS( sed._disk_age_masses.size(), 4 );
   //    TS_ASSERT_EQUALS( sed._bulge_age_masses.size(), 4 );
   //    TS_ASSERT_EQUALS( sed._disk_age_metals.size(), 4 );
   //    TS_ASSERT_EQUALS( sed._bulge_age_metals.size(), 4 );
   //    TS_ASSERT_EQUALS( sed._ssp.size(), 56 );
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
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.01 ), 0 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.014 ), 0 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.016 ), 1 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.02 ), 1 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.039 ), 1 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.041 ), 2 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.1 ), 2 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.276 ), 3 );
   //    TS_ASSERT_EQUALS( sed._find_bin( 0.8 ), 3 );
   // }

   // ///
   // ///
   // ///
   // void test_rebin_info_linear()
   // {
   //    lightcone lc;
   //    sed sed;
   //    setup_sed( lc, sed );

   //    for( lc.begin(); !lc.done(); ++lc )
   //    {
   //       const galaxy& gal = *lc;
   // 	 if( gal.values<long long>( "globaltreeid" )[0] == 0 )
   // 	 {
   // 	    sed._load_table( gal.values<long long>( "globaltreeid" )[0], gal.table() );
   // 	    sed._rebin_info( gal, 0 );
   // 	 }
   //    }
   // }

   // void setup_sed( tao::lightcone& lc, tao::sed& sed )
   // {
   //    // Turn off random rotation and shifting.
   //    lc._unique = true;

   //    // Insert some values.
   //    {
   //       soci::session sql( soci::sqlite3, db_setup.db_filename );
   //       sql << "INSERT INTO snap_redshift VALUES(0, 0.3)";
   //       sql << "INSERT INTO snap_redshift VALUES(1, 0.2)";
   //       sql << "INSERT INTO snap_redshift VALUES(2, 0.1)";
   //       sql << "INSERT INTO snap_redshift VALUES(3, 0.0)";
   // 	 // posx, posy, posz, globalindex, snapnu, localgalaxyid, globaltreeid, desc, ...
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 0,  0, 0, 0,  1, 0.8, 0.6, 10, 8)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 1,  1, 1, 0,  2, 0.6, 0.4, 8,  6)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 2,  2, 2, 0,  3, 0.4, 0.2, 6,  4)";
   //       sql << "INSERT INTO tree_1 VALUES(1, 1, 1, 3,  3, 3, 0, -1, 0.2, 0,   4,  2)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 4,  0, 0, 1, -1, 0.8, 0.6, 10, 8)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 5,  1, 1, 1,  0, 0.6, 0.4, 8,  6)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 6,  1, 2, 1,  0, 0.6, 0.4, 8,  6)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 7,  2, 3, 1,  1, 0.4, 0.2, 6,  4)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 8,  2, 4, 1,  2, 0.4, 0.2, 6,  4)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 9,  2, 5, 1,  2, 0.4, 0.2, 6,  4)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 10, 3, 6, 1,  3, 0.2, 0,   4,  2)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 11, 3, 7, 1,  3, 0.2, 0,   4,  2)";
   //       sql << "INSERT INTO tree_2 VALUES(2, 2, 2, 12, 3, 8, 1,  5, 0.2, 0,   4,  2)";
   //    }

   //    // Prepare base dictionary.
   //    {
   // 	 options::dictionary& dict = db_setup.dict.sub( "workflow:light-cone" );
   // 	 dict["query-box-size"] = "10";
   // 	 dict["geometry"] = "box";
   // 	 dict["redshift"] = "0";
   //       dict["h0"] = "73";
   // 	 db_setup.xml.write( db_setup.xml_filename, db_setup.dict );
   //    }

   //    // If we are already connected, disconnect.
   //    lc._db_disconnect();
   //    sed._db_disconnect();

   //    // Read in the dictionary from XML.
   //    options::xml_dict dict;



   //    dict.read( db_setup.xml_filename );
   //    lc.initialise( dict );
   //    sed.initialise( dict );
   // }

   // void tearDown()
   // {
   //    // Erase the table data.
   //    soci::session sql( soci::sqlite3, db_setup.db_filename );
   //    sql << "DELETE FROM snap_redshift";
   //    sql << "DELETE FROM tree_1";
   //    sql << "DELETE FROM tree_2";
   // }
};
