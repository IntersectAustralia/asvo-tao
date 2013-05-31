#include <cmath>
#include "dust.hh"

#define M_E_CU (M_E*M_E*M_E)
#define ALPHA (M_E_CU - 1.0/M_E/M_E)

using namespace hpc;

namespace tao {

   // Factory function used to create a new dust.
   module*
   dust::factory( const string& name,
		  pugi::xml_node base )
   {
      return new dust( name, base );
   }

   dust::dust( const string& name,
	       pugi::xml_node base )
      : module( name, base )
   {
   }

   dust::~dust()
   {
   }

   ///
   /// Initialise the module.
   ///
   void
   dust::initialise( const options::xml_dict& global_dict )
   {
      LOG_ENTER();

      // _read_options( dict, prefix );
      // _read_wavelengths();

      LOG_EXIT();
   }

   void
   dust::execute()
   {
      _timer.start();
      LOG_ENTER();
      ASSERT( parents().size() == 1 );

      // Grab the galaxy from the parent object.
      tao::galaxy& gal = parents().front()->galaxy();

      // // Perform the processing.
      // process_galaxy( gal );

      // // Add spectra to the galaxy object.
      // gal.set_vector_field<real_type>( "disk_spectra", _disk_spectra );
      // gal.set_vector_field<real_type>( "bulge_spectra", _bulge_spectra );
      // gal.set_vector_field<real_type>( "total_spectra", _total_spectra );

      LOG_EXIT();
      _timer.stop();
   }

   void
   dust::process_galaxy( const tao::galaxy& galaxy,
                         vector<real_type>::view spectra )
   {
      ASSERT( spectra.size() == _num_spectra );

      // Cache star formation rates.
      real_type disk_sfr = 0.0; //galaxy.get<real_type>( "disk_sfr" );
      real_type bulge_sfr = 0.0; //galaxy.get<real_type>( "bulge_sfr" );
      real_type sfr = disk_sfr + bulge_sfr;

      // Calculate "adust", whatever that is...
      real_type adust;
      if( sfr > 0.05 )
      {
         // TODO: Explain the shit out of this.
         // TODO: Needs thorough checking.
         adust = pow( 3.675*1/ALPHA*(sfr/1.479), 0.4 );
         adust += -1.0/ALPHA/M_E/M_E + 0.06;
      }
      else
         adust = 0.0;

      // K-band unchanged by dust with this value (?).
      real_type rdust = 3.675;

      for( unsigned ii = 0; ii < spectra.size(); ++ii )
      {
         real_type wl = _waves[ii];

         // Why 6300.0?
         real_type kdust;
         if( wl <= 6300.0 )
         {
            kdust = 2.659*(-2.156 + 1.5098*1e4/wl - 0.198*1e8/wl/wl + 
                           0.011*1e12/wl/wl/wl) + rdust;
         }
         else
         {
            kdust = 2.659*(-1.857 + 1.040*1e4/wl) + rdust;
         }

         real_type expdust;
         if( adust >= 0.0 )
            expdust = kdust*adust/rdust;
         else
            expdust = 0.0;

         // Stomp on spectra.
         spectra[ii] = pow( spectra[ii]*10.0, -0.4*expdust );
      }
   }

   void
   dust::_read_wavelengths()
   {
      LOG_ENTER();

      // Allocate. Note that the ordering goes time,spectra,metals.
      _waves.reallocate( _num_spectra );

      // Read in the file in one big go.
      std::ifstream file( _waves_filename, std::ios::in );
      for( unsigned ii = 0; ii < _waves.size(); ++ii )
         file >> _waves[ii];

      LOG_EXIT();
   }

   void
   dust::_read_options( const options::xml_dict& global_dict )
   {
      // // Get the sub dictionary, if it exists.
      // const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      // // Get the wavelengths filename.
      // _waves_filename = sub.get<string>( "waves_filename" );
      // LOGLN( "Using wavelengths filename \"", _waves_filename, "\"" );

      // // Get the counts.
      // _num_spectra = sub.get<unsigned>( "num_spectra" );
      // LOGLN( "Number of spectra: ", _num_spectra );
   }
}
