#ifndef tao_base_backend_hh
#define tao_base_backend_hh

#include <libhpc/profile/timer.hh>
#include "simulation.hh"

namespace tao {

   template< class T >
   class backend
   {
   public:

      typedef T real_type;

   public:

      backend( const simulation<real_type>* sim = NULL )
         : _sim( sim )
      {
      }

      virtual
      void
      set_simulation( const simulation<real_type>* sim )
      {
         _sim = sim;
      }

      virtual
      simulation<real_type> const*
      load_simulation() = 0;

      profile::timer&
      timer()
      {
         return _timer;
      }

   protected:

      const simulation<real_type>* _sim;
      profile::timer _timer;
   };

}

#endif
