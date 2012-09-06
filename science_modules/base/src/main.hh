#ifndef tao_base_main_hh
#define tao_base_main_hh

#include <cstdio>
#include <libhpc/logging/logging.hh>
#include "application.hh"

// Forward declare the pipeline.
struct pipeline;

///
/// Main entry point.
///
int
main( int argc,
      char* argv[] )
{
   LOG_PUSH( new hpc::logging::file( "tao.log", hpc::logging::info ) );
   tao::application<pipeline> app( argc, argv );
   app.run();
   return EXIT_SUCCESS;
}

#endif
