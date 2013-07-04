#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/modules/sed.hh"
#include "mpi_fixture.hh"
#include "base/tests/db_fixture.hh"

using namespace hpc;
using namespace tao;

///
/// SED class test suite.
///
class sed_suite : public CxxTest::TestSuite
{
public:

   ///
   /// Test default constructor.
   ///
   void test_default_constructor()
   {
      tao::sed sed;
   }

   ///
   /// Test processing of galaxy object.
   ///
   void test_process_galaxy()
   {
#ifndef MULTIDB
      tao::sed sed;

      // Create a test table.
      sed._sql.open( soci::sqlite3, ":memory:" );
      db_fix.setup_tree_table( sed._sql );

      // Create a test galaxy.
      galaxy gal;
      db_fix.setup_galaxy( gal );

      // Prepare the ages and SFH processor.
      {
         vector<double> ages( 5 );
         ages[0] = redshift_to_age<double>( 5 );
         ages[1] = redshift_to_age<double>( 2 );
         ages[2] = redshift_to_age<double>( 1 );
         ages[3] = redshift_to_age<double>( 0.9 );
         ages[4] = redshift_to_age<double>( 0.8 );
         sed._bin_ages.set_ages( ages );
      }
      sed._snap_ages.load_ages( sed._sql );
      sed._sfh.set_snapshot_ages( &sed._snap_ages );
      sed._sfh.set_bin_ages( &sed._bin_ages );

      // Setup SSP, metals and spectra.
      sed._num_spectra = 4;
      sed._num_metals = 7;
      sed._ssp.reallocate( sed._bin_ages.size()*sed._num_spectra*sed._num_metals );
      std::fill( sed._ssp.begin(), sed._ssp.end(), 1 );

      // Setup rebinning array sizes.
      sed._age_masses.resize( sed._bin_ages.size() );
      sed._bulge_age_masses.resize( sed._bin_ages.size() );
      sed._age_metals.resize( sed._bin_ages.size() );

      // Setup summation arrays.
      sed._disk_spectra.reallocate( sed._num_spectra, gal.batch_size() );
      sed._bulge_spectra.reallocate( sed._num_spectra, gal.batch_size() );
      sed._total_spectra.reallocate( sed._num_spectra, gal.batch_size() );

      // Call the processing code.
      sed.process_galaxy( gal );
#endif
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
};
