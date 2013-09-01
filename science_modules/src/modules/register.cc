#include "modules.hh"

namespace tao {

   void
   register_modules( factory_type& factory )
   {
      factory.register_module( "empty", modules::empty::factory );
      factory.register_module( "light-cone", modules::lightcone<backends::multidb<real_type>>::factory );
      // factory.register_module( "sed", sed::factory );
      // factory.register_module( "dust", dust::factory );
      // factory.register_module( "filter", filter::factory );
      factory.register_module( "csv", modules::csv::factory );
      // factory.register_module( "hdf5", hdf5::factory );
      // factory.register_module( "skymaker", skymaker::factory );
      // factory.register_module( "votable", votable::factory );
      // factory.register_module( "fits", fits::factory );
   }

}
