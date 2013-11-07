#include <libhpc/debug/unit_test_main.hh>
#include "tao/base/filter.hh"

using namespace hpc;
using namespace hpc::test;
using namespace tao;

struct vega_fixture
{
   vega_fixture()
      : vega( "data/A0V_KUR_BB.SED" ),
        bpf( "data/bandpass_filters/v.dat" )
   {
   }

   tao::sed<> vega;
   tao::bandpass bpf;
};

test_case<vega_fixture> ANON(
   "/base/magnitudes/absolute/vega",
   "Use the Vega spectrum to calculate absolute magnitudes.",
   []( vega_fixture& fix )
   {
      real_type mag = absolute_magnitude( fix.vega, fix.bpf );
      DELTA( mag, 2.0e-3, 1e-3 );
   }
   );

test_case<vega_fixture> ANON(
   "/base/magnitudes/apparent/vega",
   "Use the Vega spectrum to calculate apparent magnitudes.",
   []( vega_fixture& fix )
   {
      real_type mag = apparent_magnitude( fix.vega, fix.bpf, calc_area( 0.01 ) );
      DELTA( mag, 2.0e-3, 1e-3 );
   }
   );

test_case<vega_fixture> ANON(
   "/base/magnitudes/k_correction/unity",
   "The magnitudes calculated using k-correction with a bandpass "
   "filter of unity across all wavelengths should have the same values.",
   []( vega_fixture& fix )
   {
      real_type orig_mag = apparent_magnitude( fix.vega, fix.unity_bpf, calc_area( 1.0 ) );
      spectra_k_correction(
         fix.vega.spectrum().knot_values().begin(),
         fix.vega.spectrum().knot_values().end(),
         1.0,
         fix.vega.spectrum().knot_values().begin()
         );
      wavelengths_k_correction(
         fix.vega.spectrum().knot_points().begin(),
         fix.vega.spectrum().knot_points().end(),
         1.0,
         fix.vega.spectrum().knot_points().begin()
         );
      real_type new_mag = apparent_magnitude( fix.vega, fix.unity_bpf, calc_area( 1.0 ) );
      DELTA( orig_mag, new_mag, 1e-6 );
   }
   );
