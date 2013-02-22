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
   tao::register_modules();

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
   LOG_ENTER();

   // Keep looping over modules until all report being complete.
   bool complete;
   unsigned long long it = 1;
   do
   {
      LOGDLN( "Beginning iteration: ", it, hpc::setindent( 2 ) );

      // Reset the complete flag.
      complete = true;

      // Loop over the modules.
      for( auto module : tao::factory )
      {
         module->process( it );
         if( !module->complete() )
            complete = false;
      }

      // Advance the counter.
      ++it;

      LOGD( hpc::setindent( -2 ) );
   }
   while( !complete );

   LOG_EXIT();
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
   application();
   hpc::mpi::finalise();
   return EXIT_SUCCESS;
}
