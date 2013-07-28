#include "magnitudes.hh"

namespace tao {

   real_type
   calc_area( real_type redshift )
   {
      real_type dist = numerics::redshift_to_luminosity_distance( redshift, 1000 );
      if( dist < 1e-5 )  // Be careful! If dist is zero (which it can be) then resort to absolute
         dist = 1e-5;    // magnitudes.
      return log10( 4.0*M_PI ) + 2.0*log10( dist*3.08568025e24 ); // result in cm^2
   }

   real_type
   calc_abs_area()
   {
      return calc_area( 10.0/1e6 );
   }

   real_type
   apparent_magnitude( const tao::sed& sed,
                       const bandpass& bp,
                       real_type area )
   {
      real_type spec_int = sed.integrate( bp );
      real_type bp_int = bp.integral();
      return apparent( spec_int, bp_int, area );
   }

   real_type
   apparent_magnitude( real_type spec_int,
                       real_type bp_int,
                       real_type area )
   {
      return -2.5*(log10( spec_int ) - area - log10( bp_int )) - 48.6;
   }

   real_type
   absolute_magnitude( const tao::sed& sed,
                       const bandpass& bp )
   {
      return apparent( sed, bp, calc_abs_area() );
   }

}
