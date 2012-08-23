#include <cstdlib>
#include <tao/base/application.hh>
#include <tao/lightcone/lightcone.hh>

///
/// Lightcone pipeline.
///
struct pipeline
{
   void
   setup_options( hpc::options::dictionary& dict )
   {
      lc.setup_options( dict );
   }

   void
   initialise( const hpc::options::dictionary& dict )
   {
      lc.initialise( dict );
   }

   void
   run()
   {
      lc.run();
   }

   tao::lightcone lc;
};

///
/// Main entry point.
///
int
main( int argc,
      char* argv[] )
{
   tao::application<pipeline> app( argc, argv );
   app.run();
   return EXIT_SUCCESS;
}
