#include <libhpc/numerics/coords.hh>
#include "magnitudes.hh"

namespace tao {

   real_type
   calc_area( real_type redshift,
              tao::simulation const& sim )
   {
      real_type dist = numerics::redshift_to_luminosity_distance( redshift, 1000, sim.hubble(), sim.omega_l(), sim.omega_m() );
      if( dist < 1e-5 )  // Be careful! If dist is zero (which it can be) then resort to absolute
         dist = 1e-5;    // magnitudes.
      real_type area = log10( 4.0*M_PI ) + 2.0*log10( dist*3.08568025e24 ); // result in cm^2
      ASSERT( area == area, "Produced NaN during area calculation." );
      return area;
   }

   real_type
   calc_abs_area()
   {
      real_type area = log10( 4.0*M_PI ) + 2.0*log10( (10.0/1e6)*3.08568025e24 ); // result in cm^2
      ASSERT( area == area, "Produced NaN during area calculation." );
      return area;
   }

   real_type
   apparent_magnitude( real_type spec_int,
                       real_type bp_int,
                       real_type area )
   {
      if( num::approx( spec_int, 0.0 ) || num::approx( bp_int, 0.0 ) )
         return 100.0;
      else
         return -2.5*(log10( spec_int ) - area - log10( bp_int )) - 48.6;
   }

}
