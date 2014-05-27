#ifndef tao_dust_dust_hh
#define tao_dust_dust_hh

#include "tao/base/module.hh"
#include "tao/base/dust.hh"

namespace tao {
   namespace modules {
      using namespace hpc;

      ///
      ///
      ///
      template< class Backend >
      class dust
         : public module<Backend>
      {
      public:

         typedef Backend backend_type;
         typedef module<backend_type> module_type;

         enum model_type
         {
            CALZETTI,
            SLAB
         };

         static
         module_type*
         factory( const string& name,
                  pugi::xml_node base )
         {
            return new dust( name, base );
         }

      public:

         dust( const string& name = string(),
               pugi::xml_node base = pugi::xml_node() )
            : module_type( name, base )
         {
         }

         virtual
         ~dust()
         {
         }

         ///
         /// Initialise the module.
         ///
         virtual
         void
         initialise( const xml_dict& global_dict )
         {
            // Don't initialise if we're already doing so.
            if( this->_init )
               return;
            module_type::initialise( global_dict );

            LOGILN( "Initialising dust module.", setindent( 2 ) );

            // Cache dictionary.
            const xml_dict& dict = this->_dict;

            // Extract things from the galaxy object.
            ASSERT( this->parents().size() == 1, "Must have at least one parent defined." );
            tao::batch<real_type>& bat = this->parents().front()->batch();
            _total_spectra = &bat.vector<real_type>( "total_spectra" );
            _disk_spectra = &bat.vector<real_type>( "disk_spectra" );
            _bulge_spectra = &bat.vector<real_type>( "bulge_spectra" );

            // Find the wavelengths from my parents.
            _waves = this->template attribute<hpc::view<std::vector<real_type>> const>( "wavelengths" );

            // What kind of dust are we using?
            std::string mod = boost::algorithm::to_lower_copy( dict.get<std::string>( "model" ) );
            if( mod == "calzetti" )
            {
               _mod = CALZETTI;
               _sfrs = bat.scalar<real_type>( "sfr" );
            }
            else if( mod == "slab" )
            {
               _mod = SLAB;
               _sim = this->template attribute<simulation const*>( "simulation" );
               _cold_gas = bat.scalar<real_type>( "coldgas" );
               _cold_gas_metal = bat.scalar<real_type>( "metalscoldgas" );
               _redshifts = bat.scalar<real_type>( "redshift_cosmological" );
               _disk_radius = bat.scalar<real_type>( "diskscaleradius" );
               std::vector<real_type> waves( _waves.size() );
               std::copy( _waves.begin(), _waves.end(), waves.begin() );
               _slab.load_extinction( data_prefix()/"dust/nebform.dat", waves );
            }
            else
               EXCEPT( 0, "Unknown dust model: ", mod );
            LOGILN( "Dust model: ", dict.get<std::string>( "model" ) );

	    LOGILN( "Done.", setindent( -2 ) );
         }

         ///
         /// Run the module.
         ///
         virtual
         void
         execute()
         {
            tao::batch<real_type>& bat = this->parents().front()->batch();
            switch( _mod )
            {
               case CALZETTI:
                  for( unsigned ii = 0; ii < bat.size(); ++ii )
                  {
                     process_spectra_calzetti( _sfrs[ii], (*_total_spectra)[ii] );
                     process_spectra_calzetti( _sfrs[ii], (*_disk_spectra)[ii] );
                     process_spectra_calzetti( _sfrs[ii], (*_bulge_spectra)[ii] );
                  }
                  break;

               case SLAB:
                  for( unsigned ii = 0; ii < bat.size(); ++ii )
                  {
                     process_spectra_slab( _redshifts[ii], _cold_gas[ii], _cold_gas_metal[ii], _disk_radius[ii], (*_total_spectra)[ii] );
                     process_spectra_slab( _redshifts[ii], _cold_gas[ii], _cold_gas_metal[ii], _disk_radius[ii], (*_disk_spectra)[ii] );
                     process_spectra_slab( _redshifts[ii], _cold_gas[ii], _cold_gas_metal[ii], _disk_radius[ii], (*_bulge_spectra)[ii] );
                  }
                  break;
            }
         }

         void
         process_spectra_calzetti( real_type sfr,
                                   hpc::view<std::vector<real_type>> spectra )
         {
            tao::dust::calzetti( sfr, spectra.begin(), spectra.end(), _waves.begin(), spectra.begin() );
         }

         void
         process_spectra_slab( real_type redshift,
                               real_type cold_gas_mass,
                               real_type cold_gas_metal,
                               real_type disk_radius,
                               hpc::view<std::vector<real_type>> spectra )
         {
            _slab(
               _sim->h(),
               redshift,
               cold_gas_mass,
               cold_gas_metal,
               disk_radius,
               spectra.begin(),
               spectra.end(),
               _waves.begin(),
               spectra.begin()
               );
         }

      protected:

         model_type _mod;
         tao::dust::slab _slab;
         simulation const* _sim;
         hpc::matrix<real_type>* _total_spectra;
         hpc::matrix<real_type>* _disk_spectra;
         hpc::matrix<real_type>* _bulge_spectra;
         hpc::view<std::vector<real_type>> _sfrs;
         hpc::view<std::vector<real_type>> _waves;
         hpc::view<std::vector<real_type>> _cold_gas;
         hpc::view<std::vector<real_type>> _cold_gas_metal;
         hpc::view<std::vector<real_type>> _redshifts;
         hpc::view<std::vector<real_type>> _disk_radius;
      };

   }
}

#endif
