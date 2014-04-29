#include <libhpc/numerics/spline.hh>
#include "dust.hh"

namespace tao {
   namespace dust {

      real_type const slab::default_sun_metallicity = 0.019;

      slab::slab()
         : _sun_metal( default_sun_metallicity )
      {
      }

      hpc::view<std::vector<real_type>>
      slab::extinction() const
      {
         return _ext;
      }

      hpc::view<std::vector<real_type>>
      slab::albedo() const
      {
         return _alb;
      }

      hpc::view<std::vector<real_type>>
      slab::exponents() const
      {
         return _exp;
      }

      real_type
      slab::_calc_tau( real_type nh,
                       real_type metal,
                       real_type ext,
                       real_type alb,
                       real_type exp )
      {
         ASSERT( ext >= 0.0 );
         real_type tau = ext*nh*pow( metal/_sun_metal, exp );
         return tau*sqrt( 1.0 - alb );
      }

   }
}
