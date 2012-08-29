#include "dust.hh"

#define M_E 2.71828183
#define M_E_CU (M_E*M_E*M_E)
#define ALPHA (M_E_CU - 1.0/M_E/M_E)

namespace tao {

   void
   dust::run()
   {
      // real_type sfr = disk_sfr[galaxy_idx] + bulge_sfr[galaxy_idx];
      // if( sfr > 0.05 )
      // {
      //    // TODO: Explain the shit out of this.
      //    // TODO: Needs thorough checking.
      //    adust = pow( 3.675*1/ALPHA*(sfr/1.479), 0.4 );
      //    adust += -1.0/ALPHA/M_E/M_E + 0.06;
      // }
      // else
      //    adust = 0.0;
      // rdust = 3.675;

      // for( mpi::lindex ii = 0; ii < num_spectra; ++ii )
      // {
      //    real_type wl = wavelengths[ii];
      //    if( wavelengths[ii] <= 6300.0 )
      //    {
      //       kdust[ii] = 2.659*(-2.156 + 1.5098*1e4/wl - 0.198*1e8/wl/wl + 
      //          0.011*1e12/wl/wl/wl) + rdust;
      //    }
      //    else
      //    {
      //       kdust[ii] = 2.659*(-1.857 + 1.040*1e4/wl[ii]) + rdust;
      //    }
      //    if( adust >= 0.0 )
      //       expdust[ii] = kdust[ii]*adust/rdust;
      //    else
      //       expdust[ii] = 0.0;
      
      //    flux[ii] = pow( fluxtemp[ii]*10.0, -0.4*expdust[ii] );
      // }
   }

   void
   dust::_read_wavelengths()
   {
   }
}
