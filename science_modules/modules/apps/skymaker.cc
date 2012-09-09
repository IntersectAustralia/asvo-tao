#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include <tao/modules/lightcone.hh>
#include <tao/modules/sed.hh>
#include <tao/modules/filter.hh>

using namespace tao;
using namespace hpc;

///
/// Full image pipeline using SkyMaker.
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
      skymaker.setup_options( dict, "skymaker" );
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
      skymaker.initialise( dict, "skymaker" );
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
         const lightcone::row_type& row = *lc;
         LOGLN( "Processing galaxy: ", row.get<int>( "id" ), setindent( 2 ) );

         // Calculate the SED and cache results.
         sed.process_galaxy( row );
         vector<real_type>::view spectra = sed.total_spectra();

         // Perform filtering.
         filter.process_galaxy( row, spectra );

         // Add to the skymaker object list.
         skymaker.add_galaxy( row );

         LOG( setindent( -2 ) );
      }

      // Use skymaker to produce a final image.
      skymaker.run();
   }

   tao::lightcone lc;
   tao::sed sed;
   tao::filter filter;
   tao::skymaker skymaker;
};

// Need to include this last to have a complete pipeline type.
#include <tao/base/main.hh>
