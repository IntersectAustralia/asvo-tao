#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include <tao/modules/lightcone.hh>
#include <tao/modules/sed.hh>
#include <tao/modules/filter.hh>

using namespace tao;
using namespace hpc;

///
/// Filter pipeline.
///
struct pipeline
{
   // Cache any frequently used types.
   typedef tao::lightcone::real_type real_type;

   ///
   /// Add options to dictionary.
   ///
   void
   setup_options( options::dictionary& dict )
   {
      lc.setup_options( dict, "lightcone" );
      sed.setup_options( dict, "sed" );
      filter.setup_options( dict, "filter" );
   }

   ///
   /// Persistent initialisation.
   ///
   void
   initialise( const options::dictionary& dict )
   {
      lc.initialise( dict, "lightcone" );
      sed.initialise( dict, "sed" );
      filter.initialise( dict, "filter" );
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
         filter.process_galaxy( gal, lc.redshift(), spectra );

         // Dump?

         LOG( setindent( -2 ) );
      }
   }

   tao::lightcone lc;
   tao::sed sed;
   tao::filter filter;
};

// Need to include this last to have a complete pipeline type.
#include <tao/base/main.hh>
