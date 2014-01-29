#ifndef tao_base_backend_hh
#define tao_base_backend_hh

#include <libhpc/profile/timer.hh>
#include "simulation.hh"
#include "types.hh"

namespace tao {

   class backend
   {
   public:

      backend( tao::simulation<real_type> const* sim = nullptr );

      virtual
      void
      set_simulation( tao::simulation<real_type> const* sim );

      tao::simulation<real_type> const*
      simulation() const;

      virtual
      tao::simulation<real_type> const*
      load_simulation() = 0;

      hpc::profile::timer&
      timer();

   protected:

      tao::simulation<real_type> const* _sim;
      hpc::profile::timer _timer;
   };

}

#endif
