#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include <tao/modules/lightcone.hh>

using namespace tao;

///
/// Lightcone pipeline.
///
struct pipeline
{
   ///
   /// Add options to dictionary.
   ///
   void
   setup_options( hpc::options::dictionary& dict )
   {
      lc.setup_options( dict );
   }

   ///
   /// Persistent initialisation.
   ///
   void
   initialise( const hpc::options::dictionary& dict )
   {
      lc.initialise( dict );
   }

   ///
   /// Execute the pipeline.
   ///
   void
   run()
   {
      // Iterate over the galaxies.
      for( lc.begin(); !lc.done(); ++lc )
      {
         // Just print them out for now.
         const galaxy gal = *lc;
      }
   }

   lightcone lc;
};

// Need to include this last to have a complete pipeline type.
#include <tao/base/main.hh>
