#include <cmath>
#include "dust.hh"

#define M_E_CU (M_E*M_E*M_E)
#define ALPHA (M_E_CU - 1.0/M_E/M_E)

using namespace hpc;

namespace tao {

   dust::dust()
   {
   }

   dust::~dust()
   {
   }

   ///
   ///
   ///
   void
   dust::setup_options( options::dictionary& dict,
                        optional<const string&> prefix )
   {
      dict.add_option( new options::string( "waves_filename" ), prefix );
      dict.add_option( new options::integer( "num_spectra" ), prefix );
   }

   ///
   ///
   ///
   void
   dust::setup_options( hpc::options::dictionary& dict,
                        const char* prefix )
   {
      setup_options( dict, string( prefix ) );
   }

   ///
   /// Initialise the module.
   ///
   void
   dust::initialise( const options::dictionary& dict,
                     optional<const string&> prefix )
   {
      LOG_ENTER();

      _read_options( dict, prefix );
      _read_wavelengths();

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   dust::initialise( const hpc::options::dictionary& dict,
                     const char* prefix )
   {
      initialise( dict, string( prefix ) );
   }

   void
   dust::run()
   {
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
   dust::_read_options( const options::dictionary& dict,
                        optional<const string&> prefix )
   {
      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      // Get the wavelengths filename.
      _waves_filename = sub.get<string>( "waves_filename" );
      LOGLN( "Using wavelengths filename \"", _waves_filename, "\"" );

      // Get the counts.
      _num_spectra = sub.get<unsigned>( "num_spectra" );
      LOGLN( "Number of spectra: ", _num_spectra );
   }
}
