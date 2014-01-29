#include "backend.hh"

namespace tao {

   backend::backend( tao::simulation<real_type> const* sim )
      : _sim( sim )
   {
   }

   void
   backend::set_simulation( tao::simulation<real_type> const* sim )
   {
      _sim = sim;
   }

   tao::simulation<real_type> const*
   backend::simulation() const
   {
      return _sim;
   }

   hpc::profile::timer&
   backend::timer()
   {
      return _timer;
   }

}
