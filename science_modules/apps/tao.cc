#include <cstdlib>
#include <iostream>
#include <tao/base/base.hh>
#include <tao/modules/modules.hh>
#include "application.hh"

int
main( int argc,
      char* argv[] )
{
   hpc::mpi::initialise( argc, argv );
   tao::application app( argc, argv );
   app.run();
   hpc::mpi::finalise();
   return EXIT_SUCCESS;
}
