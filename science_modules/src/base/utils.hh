#ifndef tao_base_utils_hh
#define tao_base_utils_hh

#include <boost/filesystem.hpp>
#include <gsl/gsl_math.h>
#include <gsl/gsl_integration.h>
#include <libhpc/system/varray.hh>
#include <libhpc/numerics/constants.hh>
#include "types.hh"

namespace tao {

   class lightcone;

   template< class T >
   struct cosmology
   {
      T hubble;
      T omega_m;
      T omega_l;
      T omega_k;
      T omega_r;
   };

   template< class T >
   T
   expansion_to_redshift( T ef )
   {
      return 1.0/ef - 1.0;
   }

   template< class T >
   T
   redshift_to_age_func( double x,
                         void* param )
   {
      cosmology<T>* cosmo = (cosmology<T>*)param;
      return 1.0/sqrt( cosmo->omega_k +
                       cosmo->omega_m/x +
                       cosmo->omega_r/(x*x) +
                       cosmo->omega_l*x*x );
   }

   template< class T >
   T
   redshift_to_age( T redshift,
                    T hubble = 73.0,
                    T omega_m = 0.25,
                    T omega_l = 0.75 )
   {
      // Prepare the GSL function.
      cosmology<T> cosmo;
      cosmo.hubble = hubble;
      cosmo.omega_m = omega_m;
      cosmo.omega_l = omega_l;
      cosmo.omega_r = 4.165e-5/((hubble/100.0)*(hubble/100.0));
      cosmo.omega_k = 1.0 - cosmo.omega_m - cosmo.omega_l - cosmo.omega_r;
      gsl_function func;
      func.function = &redshift_to_age_func<T>;
      func.params = &cosmo;

      // Create some work space.
      gsl_integration_workspace* work = gsl_integration_workspace_alloc( 1000 );

      // Perform the integration.
      T res, abserr;
      T upp = 1.0/(1.0 + redshift);
      gsl_integration_qag( &func, 0.0, upp, 1e-5, 1e-8, 1000, GSL_INTEG_GAUSS21, work, &res, &abserr );
      res *= (977.8/hubble); // convert to Gyrs

      // Don't forget to free work space.
      gsl_integration_workspace_free( work );

      return res;
   }

   real_type
   observed_redshift( real_type z,
                      hpc::varray<real_type,3> const& pos,
                      hpc::varray<real_type,3> const& vel,
                      real_type h0,
                      real_type c = hpc::constant::c_km_s );

   real_type
   approx_observed_redshift( lightcone const& lc,
                             hpc::varray<real_type,3> const& pos,
                             hpc::varray<real_type,3> const& vel );

   boost::filesystem::path
   data_prefix();

}

#endif
