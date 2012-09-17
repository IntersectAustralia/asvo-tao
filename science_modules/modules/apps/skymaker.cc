#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include <tao/modules/lightcone.hh>
#include <tao/modules/sed.hh>
#include <tao/modules/filter.hh>
#include <tao/modules/skymaker.hh>

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
         const galaxy gal = *lc;
         LOGLN( "Processing galaxy: ", gal.id(), setindent( 2 ) );

         // Calculate the SED and cache results.
         sed.process_galaxy( gal );
         vector<real_type>::view spectra = sed.total_spectra();

         // Perform filtering and cache the particular
         // band we're interested in.
         filter.process_galaxy( gal, lc.redshift(), spectra );
         real_type v_mag = filter.magnitudes()[1]; // V band
         std::cout << "Adding galaxy: " << v_mag << "\n";

         // Add to the skymaker object list.
         skymaker.add_galaxy( gal, v_mag );

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
