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
   /// Persistent initialisation.
   ///
   void
   initialise( const options::xml_dict& dict )
   {
      lc.initialise( dict, string( "workflow:light-cone" ) );
      sed.initialise( dict, string( "workflow:sed" ) );
      filter.initialise( dict, string( "workflow:sed" ) );
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
         // Cache the database row.
         const galaxy gal = *lc;

         // Calculate the SED and cache results.
         sed.process_galaxy( gal );
         vector<real_type>::view total_spectra = sed.total_spectra();
         vector<real_type>::view disk_spectra = sed.disk_spectra();
         vector<real_type>::view bulge_spectra = sed.bulge_spectra();

         // Perform filtering.
         filter.process_galaxy( gal, total_spectra, disk_spectra, bulge_spectra );

         // Dump?
	 dump.process_galaxy( gal );
      }
   }

   void
   log_timings()
   {
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
