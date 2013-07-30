#ifndef tao_base_integration_hh
#define tao_base_integration_hh

#include <libhpc/numerics/spline.hh>
#include "types.hh"

namespace tao {
   using namespace hpc;
   namespace integ {

      real_type
      integrate( const numerics::spline<real_type>& spectra,
                 const numerics::spline<real_type>& filter );

      real_type
      integrate( const numerics::spline<real_type>& spectra );

   }
}

#endif
