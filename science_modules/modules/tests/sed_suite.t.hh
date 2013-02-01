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
      // Setup filenames.
      db_filename = tmpnam( NULL );
      xml_filename = tmpnam( NULL );
      ssp_filename = tmpnam( NULL );

      // Open the database.
      soci::session sql( soci::sqlite3, db_filename );

      // Write a simple set of galaxies.
      sql << "create table snapshot_000 (Pos1 double precision, Pos2 double precision, Pos3 double precision, id integer)";
      sql << "create table snapshot_001 (Pos1 double precision, Pos2 double precision, Pos3 double precision, id integer)";
      sql << "insert into snapshot_000 values (1, 0.001, 0.001, 0)";
      sql << "insert into snapshot_000 values (0.866, 0.5, 0.001, 1)";
      sql << "insert into snapshot_000 values (0.5, 0.866, 0.001, 2)";
      sql << "insert into snapshot_001 values (1, 0.001, 0.001, 0)";
      sql << "insert into snapshot_001 values (0.866, 0.5, 0.001, 1)";
      sql << "insert into snapshot_001 values (0.5, 0.866, 0.001, 2)";

      // Write a sample set of star formation histories/metallicities.
      sql << "create table disk_star_formation (galaxy_id integer, history double precision, "
         "metal double precision, age double precision)";
      sql << "create table bulge_star_formation (galaxy_id integer, history double precision, "
         "metal double precision, age double precision)";
      sql << "insert into disk_star_formation values (0, 1, 0.00, 3)";
      sql << "insert into disk_star_formation values (0, 2, 0.01, 2)";
      sql << "insert into disk_star_formation values (0, 3, 0.02, 1)";
      sql << "insert into disk_star_formation values (1, 4, 0.00, 3)";
      sql << "insert into disk_star_formation values (1, 5, 0.01, 2)";
      sql << "insert into disk_star_formation values (1, 6, 0.02, 1)";
      sql << "insert into disk_star_formation values (2, 7, 0.00, 3)";
      sql << "insert into disk_star_formation values (2, 8, 0.01, 2)";
      sql << "insert into disk_star_formation values (2, 9, 0.02, 1)";
      sql << "insert into bulge_star_formation values (0, 10, 0.00, 3)";
      sql << "insert into bulge_star_formation values (0, 11, 0.01, 2)";
      sql << "insert into bulge_star_formation values (0, 12, 0.02, 1)";
      sql << "insert into bulge_star_formation values (1, 13, 0.00, 3)";
      sql << "insert into bulge_star_formation values (1, 14, 0.01, 2)";
      sql << "insert into bulge_star_formation values (1, 15, 0.02, 1)";
      sql << "insert into bulge_star_formation values (2, 16, 0.00, 3)";
      sql << "insert into bulge_star_formation values (2, 17, 0.01, 2)";
      sql << "insert into bulge_star_formation values (2, 18, 0.02, 1)";

      // Write a sample SSP file, assuming num_times=3, num_spectra=2, num_metals=7.
      std::ofstream file( ssp_filename, std::ios::out );
      unsigned val = 0;
      for( unsigned ii = 0; ii < 3; ++ii )
      {
         for( unsigned jj = 0; jj < 2; ++jj )
         {
            for( unsigned kk = 0; kk < 7; ++kk )
               file << to_string( val++ ) << " ";
            file << "\n";
         }
      }

      // Create an appropriate XML file for both the lightcone and
      // the SED modules.
      lightcone lc;
      tao::sed sed;
      options::dictionary* lc_dict = new options::dictionary( "lightcone" );
      options::dictionary* sed_dict = new options::dictionary( "sed" );
      options::dictionary dict;
      dict.add_dictionary( lc_dict );
      dict.add_dictionary( sed_dict );
      lc.setup_options( *lc_dict );
      sed.setup_options( *sed_dict );
      dict.compile();

      dict["lightcone-database_type"] = "sqlite";
      dict["lightcone-database_name"] = db_filename;
      dict["lightcone-box_type"] = "cone";
      dict["lightcone-box_side"] = "100";
      dict["lightcone-snapshots"] = "0.01,0";

      dict["sed-database_type"] = "sqlite";
      dict["sed-database_name"] = db_filename;
      dict["sed-ssp_filename"] = ssp_filename;
      dict["sed-num_times"] = "3";
      dict["sed-num_spectra"] = "2";
      dict["sed-num_metals"] = "7";

      xml_filename = tmpnam( NULL );
      xml.write( xml_filename, dict );

      return true;
   }

   bool tearDownWorld()
   {
      remove( db_filename.c_str() );
      remove( xml_filename.c_str() );
      remove( ssp_filename.c_str() );
      return true;
   }

   options::xml xml;
   std::string db_filename, xml_filename, ssp_filename;
};

static db_setup_fixture db_setup;

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
   /// Test invalid input array sizes.
   ///
   /// The stellar mass production rates and metallicities must all
   /// be the correct sized arrays in order to function. I expect
   /// errors to be raised if this is not the case.
   ///
   void test_array_sizes()
   {
   }

   ///
   /// Test invalid spectral bands.
   ///
   /// While it's possible to run the code with zero spectral
   /// bands, it doesn't make much sense. I expect an error to
   /// be raised if this happens.
   ///
   void test_num_spectral_bands()
   {
   }

   ///
   /// Test single-stellar population array size.
   ///
   /// When reading from the SSP table, it should return a row
   /// of the same size as the number of spectral bands. I
   /// expect an error to be thrown if this is not the case.
   ///
   void test_ssp_size()
   {
   }

   ///
   /// Test metallicity interpolation.
   ///
   /// Check the regions of metallicity interpolation. It should
   /// look like the following:
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

   ///
   /// Test spectral summation.
   ///
   void test_sepctral_sum()
   {
      tao::lightcone lc;
      tao::sed sed;
      setup_sed( lc, sed );

      unsigned galaxy = 0;
      for( lc.begin(); !lc.done(); ++lc, ++galaxy )
      {
         sed.process_galaxy( *lc );

         // Each galaxy will have a different set of values.
         if( galaxy == 0 )
         {
            TS_ASSERT( num::approx( sed.disk_spectra()[0]*1e10, 130.0, 1e-8 ) );
            TS_ASSERT( num::approx( sed.disk_spectra()[1]*1e10, 172.0, 1e-8 ) );
            TS_ASSERT( num::approx( sed.bulge_spectra()[0]*1e10, 571.0, 1e-8 ) );
            TS_ASSERT( num::approx( sed.bulge_spectra()[1]*1e10, 802.0, 1e-8 ) );
         }
         else if( galaxy == 1 )
         {
            TS_ASSERT( num::approx( sed.disk_spectra()[0]*1e10, 277.0, 1e-8 ) );
            // TODO: Finish the galaxies.
         }
      }
   }

   void setup_sed( tao::lightcone& lc, tao::sed& sed )
   {
      // Setup the dictionary.
      options::dictionary dict;
      lc.setup_options( dict, "lightcone" );
      sed.setup_options( dict, "sed" );
      dict.compile();
      db_setup.xml.read( db_setup.xml_filename, dict );

      // Initialise modules.
      lc.initialise( dict, "lightcone" );
      sed.initialise( dict, "sed" );

      // Switch off random rotation and shifting.
      lc._unique = true;
   }
};
