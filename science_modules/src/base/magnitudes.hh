#ifndef tao_base_magnitudes_hh
#define tao_base_magnitudes_hh

#include "types.hh"
#include "sed.hh"
#include "bandpass.hh"

namespace tao {
   using namespace hpc;

   real_type
   calc_area( real_type redshift );

   real_type
   calc_abs_area();

   real_type
   apparent_magnitude( real_type spec_int,
                       real_type bp_int,
                       real_type area );

   template< class Spline >
   real_type
   apparent_magnitude( const tao::sed<Spline>& sed,
                       const bandpass& bp,
                       real_type area )
   {
      real_type spec_int = sed.integrate( bp );
      ASSERT( spec_int == spec_int, "Produced NaN for integration of SED and bandpass filter." );
      real_type bp_int = bp.integral();
      return apparent_magnitude( spec_int, bp_int, area );
   }

   template< class Spline >
   real_type
   absolute_magnitude( const tao::sed<Spline>& sed,
                       const bandpass& bp )
   {
      return apparent_magnitude( sed, bp, calc_abs_area() );
   }

}

#endif
