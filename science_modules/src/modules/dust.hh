#ifndef tao_dust_dust_hh
#define tao_dust_dust_hh

#include "tao/base/module.hh"

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
         initialise( const options::xml_dict& global_dict )
         {
            // Don't initialise if we're already doing so.
            if( this->_init )
               return;
            module_type::initialise( global_dict );

            auto timer = this->timer_start();
            LOGILN( "Initialising dust module.", setindent( 2 ) );

            // Cache dictionary.
            const options::xml_dict& dict = this->_dict;

            // Extract things from the galaxy object.
            ASSERT( this->parents().size() == 1, "Must have at least one parent defined." );
            tao::batch<real_type>& bat = this->parents().front()->batch();
            _total_spectra = &bat.vector<real_type>( "total_spectra" );
            _disk_spectra = &bat.vector<real_type>( "disk_spectra" );
            _bulge_spectra = &bat.vector<real_type>( "bulge_spectra" );
            _sfrs = bat.scalar<real_type>( "sfr" );

            // Find the wavelengths from my parents.
            _waves = this->template attribute<const vector<real_type>::view>( "wavelengths" );

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
            for( unsigned ii = 0; ii < bat.size(); ++ii )
            {
               process_spectra( _sfrs[ii], (*_total_spectra)[ii] );
               process_spectra( _sfrs[ii], (*_disk_spectra)[ii] );
               process_spectra( _sfrs[ii], (*_bulge_spectra)[ii] );
            }
         }

         void
         process_spectra( real_type sfr,
                          vector<real_type>::view spectra )
         {
            static const real_type M_E_CU = M_E*M_E*M_E;
            static const real_type ALPHA  = M_E_CU - 1.0/M_E/M_E;

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
            // LOGDLN( "adust: ", adust );

            // K-band unchanged by dust with this value (?).
            real_type rdust = 3.675;
            // LOGDLN( "rdust: ", rdust );
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
               // LOGDLN( "kdust: ", kdust );

               real_type expdust;
               if( adust >= 0.0 )
                  expdust = kdust*adust/rdust;
               else
                  expdust = 0.0;
               // LOGDLN( "expdust: ", expdust );

               // Stomp on spectra.
               spectra[ii] = spectra[ii]*pow( 10.0, -0.4*expdust );
            }
         }

      protected:

         fibre<real_type>* _total_spectra;
         fibre<real_type>* _disk_spectra;
         fibre<real_type>* _bulge_spectra;
         vector<real_type>::view _sfrs;
         vector<real_type>::view _waves;
      };

   }
}

#endif
