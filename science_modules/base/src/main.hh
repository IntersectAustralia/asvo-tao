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
   hpc::mpi::initialise( argc, argv );
   LOG_PUSH( new hpc::mpi::logger( "tao.log." ) );
   tao::application<pipeline> app( argc, argv );
   app.run();
   hpc::mpi::finalise();
   return EXIT_SUCCESS;
}

#endif
