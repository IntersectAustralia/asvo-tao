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
      lc.setup_options( dict, "workflow:light-cone" );
   }

   ///
   /// Persistent initialisation.
   ///
   void
   initialise( const hpc::options::dictionary& dict )
   {
      lc.initialise( dict, "workflow:light-cone" );
      dump.initialise( dict, lc );
      dump.set_filename( dict.get<string>( "outputdir" ) + "/tao.output" );
      dump.open();
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

   void
   log_timings()
   {
      LOGILN( "Time breakdown:", setindent( 2 ) );
      LOGILN( "Lightcone: ", lc.time() );
   }

   lightcone lc;
   csv dump;
};

// Need to include this last to have a complete pipeline type.
#include <tao/base/main.hh>
