#ifndef tao_base_integration_hh
#define tao_base_integration_hh

#include <libhpc/numerics/spline_integrator.hh>
#include "types.hh"

#define M_C 2.99792458e18 // angstrom/s

namespace tao {
   using namespace hpc;

   template< class Spline >
   real_type
   integrate( const numerics::spline_integrator<real_type>& integ,
              const Spline& sp )
   {
      return integ(
         sp,
         []( double x, double val )
         {
            return val*M_C/(x*x);
         }
         );
   }

   template< class Spline >
   real_type
   integrate( const Spline& sp )
   {
      numerics::spline_integrator<real_type> integ;
      return integrate( integ, sp );
   }

   template< class Spline0,
             class Spline1 >
   real_type
   integrate( const numerics::spline_spline_integrator<real_type>& integ,
              const Spline0& sp0,
              const Spline1& sp1 )
   {
      return integ(
         sp0, sp1,
         []( double x, double val0, double val1 )
         {
            return val0*val1;
         }
         );
   }

   template< class Spline0,
             class Spline1 >
   real_type
   integrate( const Spline0& sp0,
              const Spline1& sp1 )
   {
      numerics::spline_spline_integrator<real_type> integ;
      return integrate( integ, sp0, sp1 );
   }

}

#endif
