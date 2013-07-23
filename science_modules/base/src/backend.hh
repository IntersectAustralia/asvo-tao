#ifndef tao_base_backend_hh
#define tao_base_backend_hh

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

   protected:

      const simulation<real_type>* _sim;
   };

}

#endif
