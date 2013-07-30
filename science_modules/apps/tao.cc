#include <cstdlib>
#include <iostream>
#include <tao/base/base.hh>
#include <tao/modules/modules.hh>
#include "application.hh"
#include <string>

using namespace std;

int
main( int argc,
      char* argv[] )
{
   hpc::mpi::initialise( argc, argv );
   string XMLFile=argv[1];
   int index=XMLFile.find(".xml");
   XMLFile.replace(index,4,"_tao.debug.log");
   LOG_PUSH( new hpc::mpi::logger( XMLFile, hpc::logging::debug ) );
#ifdef PREPROCESSING
   XMLFile=argv[1];
   index=XMLFile.find(".xml");
   XMLFile.replace(index,4,"_tao.Profile.log");
   LOG_PUSH( new hpc::mpi::logger( XMLFile,100 ) );
#endif

   LOG_PUSH( new hpc::logging::stdout( hpc::logging::info ) );
   tao::application app( argc, argv );
   app.run();
   hpc::mpi::finalise();
   return EXIT_SUCCESS;
}
