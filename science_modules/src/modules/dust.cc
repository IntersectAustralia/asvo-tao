#include <math.h>
#include <boost/algorithm/string/trim.hpp>
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

      _read_options( global_dict );
      _read_wavelengths( _waves_filename );

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

      // Extract things from the galaxy object.
      fibre<real_type>& total_spectra = gal.vector_values<real_type>( "total_spectra" );
      fibre<real_type>& disk_spectra = gal.vector_values<real_type>( "disk_spectra" );
      fibre<real_type>& bulge_spectra = gal.vector_values<real_type>( "bulge_spectra" );

      // Perform the processing.
      process_galaxy( gal, total_spectra, disk_spectra, bulge_spectra );

      LOG_EXIT();
      _timer.stop();
   }

   void
   dust::process_galaxy( tao::galaxy& galaxy,
			 fibre<real_type>& total_spectra,
			 fibre<real_type>& disk_spectra,
			 fibre<real_type>& bulge_spectra )
   {
      auto ids = galaxy.values<int>( "localgalaxyid" );
      auto sfrs = galaxy.values<real_type>( "sfr" );
      for( unsigned ii = 0; ii < galaxy.batch_size(); ++ii )
      {
	 process_spectra( galaxy, ids[ii], sfrs[ii], total_spectra[ii] );
	 process_spectra( galaxy, ids[ii], sfrs[ii], disk_spectra[ii] );
	 process_spectra( galaxy, ids[ii], sfrs[ii], bulge_spectra[ii] );
      }
   }

   void
   dust::process_spectra( tao::galaxy& galaxy,
			  unsigned gal_idx,
			  real_type& sfr,
			  vector<real_type>::view spectra )
   {
      ASSERT( _waves.size() == spectra.size() );
      LOGDLN( "Adding dust to specific spectra of galaxy: ", gal_idx, setindent( 2 ) );
      LOGDLN( "SFR: ", sfr );

      // Calculate "adust", whatever that is...
      real_type adust;
      if( sfr > 0.05 )
      {
         // TODO: Explain the shit out of this.
         // TODO: Needs thorough checking.
         adust = 3.675*1.0/ALPHA*pow( sfr/1.479, 0.4 );
         adust += -1.0/ALPHA/M_E/M_E + 0.06;
      }
      else
         adust = 0.0;
      LOGDLN( "adust: ", adust );

      // K-band unchanged by dust with this value (?).
      real_type rdust = 3.675;
      LOGDLN( "rdust: ", rdust );
      ASSERT( adust/rdust >= 0.0, "Some dust problem... ?" );

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
	 LOGDLN( "kdust: ", kdust );

         real_type expdust;
         if( adust >= 0.0 )
            expdust = kdust*adust/rdust;
         else
            expdust = 0.0;
	 LOGDLN( "expdust: ", expdust );

         // Stomp on spectra.
         spectra[ii] = spectra[ii]*pow( 10.0, -0.4*expdust );
      }

      LOGD( setindent( -2 ) );
   }

   void
   dust::_read_wavelengths( const string& filename )
   {
      LOG_ENTER();

      // Open the file.
      std::ifstream file( filename );
      ASSERT( file.is_open() );

      // Need to get number of lines in file first.
      unsigned num_waves = 0;
      {
         string line;
         while( !file.eof() )
         {
            std::getline( file, line );
            if( boost::trim_copy( line ).length() )
               ++num_waves;
         }
      }

      // Allocate. Note that the ordering goes time,spectra,metals.
      _waves.reallocate( num_waves );

      // Read in the file in one big go.
      file.clear();
      file.seekg( 0 );
      for( unsigned ii = 0; ii < _waves.size(); ++ii )
         file >> _waves[ii];

      LOG_EXIT();
   }

   void
   dust::_read_options( const options::xml_dict& global_dict )
   {
      // Get the wavelengths filename.
      _waves_filename = _dict.get<string>( "wavelengths", "wavelengths.dat" );
      LOGLN( "Using wavelengths filename \"", _waves_filename, "\"" );
   }
}
