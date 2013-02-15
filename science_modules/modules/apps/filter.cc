#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include <tao/modules/lightcone.hh>
#include <tao/modules/sed.hh>
#include <tao/modules/filter.hh>
#include <tao/modules/csv.hh>

using namespace tao;
using namespace hpc;

///
/// Filter pipeline.
///
struct pipeline
{
   // Cache any frequently used types.
   typedef lightcone::real_type real_type;

   ///
   /// Add options to dictionary.
   ///
   void
   setup_options( options::dictionary& dict )
   {
      lc.setup_options( dict, "workflow:light-cone" );
      sed.setup_options( dict, "workflow:sed" );
      filter.setup_options( dict, "workflow:sed" );
   }

   ///
   /// Persistent initialisation.
   ///
   void
   initialise( const options::dictionary& dict )
   {
      lc.initialise( dict, "workflow:light-cone" );
      sed.initialise( dict, "workflow:sed" );
      filter.initialise( dict, "workflow:sed" );
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
         // Cache the database row.
         const galaxy gal = *lc;
         LOGLN( "Processing galaxy: ", gal.id(), setindent( 2 ) );

         // Calculate the SED and cache results.
         sed.process_galaxy( gal );
         vector<real_type>::view spectra = sed.total_spectra();

         // Perform filtering.
         filter.process_galaxy( gal, spectra );
	 real_type app_mag = filter.magnitudes()[0];

         // Dump?
	 dump.process_galaxy( gal, app_mag );
      }

      // Once we're finished, dump out some timings.
      LOGILN( "Time breakdown:", setindent( 2 ) );
      LOGILN( "Lightcone: ", lc.time() );
      LOGILN( "SED:       ", sed.time() );
      LOGILN( "Filter:    ", filter.time() );
   }

   lightcone lc;
   tao::sed sed;
   tao::filter filter;
   csv dump;
};

// Need to include this last to have a complete pipeline type.
#include <tao/base/main.hh>
