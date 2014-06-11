#ifndef tao_modules_sed_hh
#define tao_modules_sed_hh

#include <libhpc/libhpc.hh>
#include "tao/base/base.hh"

namespace tao {
   namespace modules {
      using namespace hpc;

      ///
      /// SED science module. The SED module is responsible for calculating the
      /// energy spectra of each galaxy.
      ///
      template< class Backend >
      class sed
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
            return new sed( name, base );
         }

      public:

         sed( const string& name = string(),
              pugi::xml_node base = pugi::xml_node() )
            : module_type( name, base )
         {
         }

         virtual
         ~sed()
         {
         }

         virtual
         optional<boost::any>
         find_attribute( const string& name )
         {
            if( name == "wavelengths" )
               return boost::any( hpc::view<std::vector<double> const>( _ssp.wavelengths() ) );
            else
               return module_type::find_attribute( name );
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

            LOGILN( "Initialising SED module.", setindent( 2 ) );

            // Locate the backend and the simulation.
            _be = this->parents().front()->backend();
            _sim = this->template attribute<const simulation*>( "simulation" );

            // Handle optinos.
            _read_options( global_dict );

            // Setup my SFH age line.
            _snap_ages.load_ages( _be->session(), _sim->hubble(), _sim->omega_m(), _sim->omega_l() );
            _sfh.set_snapshot_ages( &_snap_ages );

            // Allocate history bin arrays.
            hpc::reallocate( _age_masses, _ssp.age_masses_size() );
            hpc::reallocate( _bulge_age_masses, _ssp.age_masses_size() );
            // _age_metals.reallocate( _ssp.bin_ages().size() );

            // Prepare the batch object.
            tao::batch<real_type>& bat = this->parents().front()->batch();
            bat.set_vector<real_type>( "disk_spectra", _ssp.wavelengths().size() );
            bat.set_vector<real_type>( "bulge_spectra", _ssp.wavelengths().size() );
            bat.set_vector<real_type>( "total_spectra", _ssp.wavelengths().size() );

            LOGILN( "Done.", setindent( -2 ) );
         }

         ///
         /// Run the module.
         ///
         virtual
         void
         execute()
         {
            ASSERT( this->parents().size() == 1 );
	    LOGDLN( "Processing batch in SED module.", setindent( 2 ) );

            // Cache some information.
            tao::batch<real_type>& bat = this->parents().front()->batch();
            const auto& table_name = bat.attribute<string>( "table" );
            const auto tree_gids = bat.scalar<long long>( "globaltreeid" );
            const auto gal_lids = bat.scalar<int>( "localgalaxyid" );
            auto& total_spectra = bat.vector<real_type>( "total_spectra" );
            auto& disk_spectra = bat.vector<real_type>( "disk_spectra" );
            auto& bulge_spectra = bat.vector<real_type>( "bulge_spectra" );
            soci::session& sql = _be->session( table_name );
	    auto gal_gids = bat.scalar<long long>( "globalindex" );

            // Perform the processing.
            for( unsigned ii = 0; ii < bat.size(); ++ii )
            {
	       LOGILN( "Calculating SED for galaxy with global index: ", gal_gids[ii] );

               // Be sure we're on the correct tree.
               _sfh.load_tree_data( sql, table_name, tree_gids[ii], gal_gids[ii] );

               // Rebin the star-formation history.
               _sfh.rebin<std::vector<real_type>,std::vector<real_type>>( _age_masses, _bulge_age_masses, _ssp );

               // Sum contributions from the SSP.
               _ssp.sum( _age_masses.begin(), total_spectra[ii].begin() );
               _ssp.sum( _bulge_age_masses.begin(), bulge_spectra[ii].begin() );

               // Create disk spectra.
               for( unsigned jj = 0; jj < _ssp.wavelengths().size(); ++jj )
                  disk_spectra[ii][jj] = total_spectra[ii][jj] - bulge_spectra[ii][jj];
            }

	    LOGDLN( "Done.", setindent( -2 ) );
         }

         virtual
         backend_type*
         backend()
         {
            return _be;
         }

         virtual
         void
         log_metrics()
         {
            module_type::log_metrics();
            // LOGILN( this->_name, " rebinning time: ", _rebin_timer.total(), " (s)" );
            // LOGILN( this->_name, " summation time: ", _sum_timer.total(), " (s)" );
         }

      protected:

         void
         _read_options( const xml_dict& global_dict )
         {
            // Cache dictionary.
            const xml_dict& dict = this->_dict;

            // Get the filenames for SSP information.
            auto path = data_prefix()/"stellar_populations";
            auto ages_fn = path/dict.get<string>( "ages-file" );
            auto waves_fn = path/dict.get<string>( "wavelengths-file" );
            auto metals_fn = path/dict.get<string>( "metallicities-file" );
            auto ssp_fn = path/dict.get<string>( "single-stellar-population-model" );

            // Prepare the SSP.
            _ssp.load( ages_fn, waves_fn, metals_fn, ssp_fn );
         }

      protected:

         backend_type* _be;
         const simulation* _sim;
         stellar_population _ssp;
         age_line<real_type> _snap_ages;
         sfh _sfh;
         vector<real_type> _age_masses, _bulge_age_masses;
         // vector<real_type> _age_metals;
      };

   }
}

#endif