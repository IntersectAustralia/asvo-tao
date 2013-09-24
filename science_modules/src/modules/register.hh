#ifndef tao_modules_register_hh
#define tao_modules_register_hh

#include "tao/base/factory.hh"
#include "modules.hh"

namespace tao {

   template< class Backend >
   void
   register_modules( tao::factory<Backend>& fact )
   {
      fact.register_module( "light-cone", tao::modules::lightcone<Backend>::factory );
      fact.register_module( "sed", modules::sed<Backend>::factory );
      // fact.register_module( "dust", dust::factory );
      fact.register_module( "filter", modules::filter<Backend>::factory );
      fact.register_module( "skymaker", modules::skymaker<Backend>::factory );
      fact.register_module( "csv", modules::csv<Backend>::factory );
      // fact.register_module( "hdf5", hdf5::factory );
      // fact.register_module( "votable", votable::factory );
      // fact.register_module( "fits", fits::factory );
   }

}

#endif
