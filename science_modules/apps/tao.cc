#include <cstdlib>
#include <iostream>
#include <tao/base/base.hh>
#include <tao/modules/modules.hh>

///
///
///
void
initialise()
{
   // Call the science module registration function.


   // Setup, at minimum, a list option for the names of the
   // science modules.

   // // Iterate over the module names, creating each one.
   // for( auto name : module_names )
   //    tao::create_module( name );

   // // Now extract the parents for each module.
   // for( auto name : module_names )
   // {
   //    parents = ;
   //    for( auto parent : parents )
   //       tao::module( name ).add_parent( parent);
   // }

   tao::factory.create_module( "light-cone" );
   // tao::factory["light-cone"]->add_parent( *tao::factory["empty"] );
}

///
///
///
void
execute()
{

}

int
application()
{
   initialise();
   execute();
}

int
main( int argc,
      char* argv[] )
{
   hpc::mpi::initialise( argc, argv );
   LOG_FILE( "test.log" );
   application app;
   app.run();
   hpc::mpi::finalise();
   return EXIT_SUCCESS;
}
