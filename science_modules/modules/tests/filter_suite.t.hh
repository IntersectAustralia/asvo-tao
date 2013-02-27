#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/modules/filter.hh"
#include "tao/modules/sed.hh"
#include "tao/modules/lightcone.hh"

using namespace hpc;
using namespace tao;

#include "mpi_fixture.hh"
#include "db_fixture.hh"

#define M_C 2.99792458e18 // angstrom/s

///
/// Filter class test suite.
///
class filter_suite : public CxxTest::TestSuite
{
public:

   ///
   /// Test default constructor.
   ///
   void test_default_constructor()
   {
      tao::filter filt;
   }

   // ///
   // /// Test process galaxy with unity values. Run the process_galaxy
   // /// method with prepared values designed to produce unity as results.
   // ///
   // void test_process_vega()
   // {
   //    LOG_FILE( "test.log" );

   //    filter filt;
   //    filt._load_filter( "v.dat" );
   //    filt._process_vega( "A0V_KUR_BB.SED" );

   //    std::cout << "\n" << filt._integrate( filt._filters[0] ) << "\n";
   //    std::cout << filt._integrate_nu( filt._filters[0] ) << "\n";
   // }

   ///
   /// Test process galaxy with unity values. Run the process_galaxy
   /// method with prepared values designed to produce unity as results.
   /// Note, I've gotten the sytem to produce unity as a result of the
   /// intensity integral, the magnitudes will not be such.
   ///
   void test_process_galaxy_unity()
   {
      LOG_FILE( "test.log" );

      // Prepare the galaxy object. Unfortunately the filter converts
      // redshift to a distance, which is a tricky calculation. I'll have
      // to factor out the distance at the end.
      tao::galaxy gal;
      gal._z = 1.0;

      // Prepare the spectra.
      unsigned num_waves = 10;
      vector<real_type> spectra( num_waves );
      std::fill( spectra.begin(), spectra.end(), 3.0*M_C/7.0 );

      // Prepare the filter's wavelengths.
      string wave_filename = "waves.txt"; //tmpnam( NULL );
      {
         std::ofstream file( wave_filename );
         for( unsigned ii = 0; ii < num_waves; ++ii )
            file << 1.0 + (double)ii*(1.0/(double)(num_waves - 1)) << "\n";
      }

      // Prepare a band-pass filter. Be sure the wavelengths
      // are offset to the filter's to test the splines.
      string bpf_filename = "bpf.txt"; //tmpnam( NULL );
      {
         std::ofstream file( bpf_filename );
         file << 15 << "\n";
         for( unsigned ii = 0; ii < 15; ++ii )
            file << 1.0 + ii*(1/14.0) << "  " << 1.0 << "\n";
      }

      // Prepare the filter object.
      filter filt;
      filt._read_wavelengths( wave_filename );
      filt._load_filter( bpf_filename );
      filt._app_mags.resize( 1 );
      filt._abs_mags.resize( 1 );

      // Call the function.
      filt.process_galaxy( gal, spectra );

      // Check that the apparent magnitude is right.
      real_type dist = numerics::redshift_to_luminosity_distance( 1.0, 1000 );
      real_type area = log10( 4.0*M_PI ) + 2.0*log10( dist*3.08568025e24 ); // result in cm^2
      real_type f_a = log10( 1.0 ) - area - log10( 1.0 );
      real_type mag_ab = -2.5*f_a - 48.6;

      // Do the check.
      TS_ASSERT_DELTA( filt._app_mags[0], mag_ab, 1e-8 );
   }
};
