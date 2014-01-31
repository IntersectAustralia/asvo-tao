#include "backend.hh"

namespace tao {

   backend::backend( tao::simulation const* sim )
      : _sim( sim )
   {
   }

   void
   backend::set_simulation( tao::simulation const* sim )
   {
      _sim = sim;
   }

   tao::simulation const*
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
