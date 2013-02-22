#include "modules.hh"

namespace tao {

   void
   register_modules()
   {
      factory.register_module( "empty", empty::factory );
      factory.register_module( "light-cone", lightcone::factory );
      factory.register_module( "sed", sed::factory );
   }

}
