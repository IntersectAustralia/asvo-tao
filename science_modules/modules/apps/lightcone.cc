#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include <tao/modules/lightcone.hh>
#include <tao/modules/csv.hh>

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
      lc.setup_options( dict, string( "workflow:light-cone" ) );
      dump.setup_options( dict );
   }

   ///
   /// Persistent initialisation.
   ///
   void
   initialise( const hpc::options::dictionary& dict )
   {
      lc.initialise( dict, string( "workflow:light-cone" ) );
      dump.initialise( dict );
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
	 // Cache the galaxy.
         const galaxy gal = *lc;

	 // Dump out.
	 dump.process_galaxy( gal );
      }
   }

   lightcone lc;
   csv dump;
};

// Need to include this last to have a complete pipeline type.
#include <tao/base/main.hh>
