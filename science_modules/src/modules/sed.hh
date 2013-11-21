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
               return boost::any( _ssp.wavelengths() );
            else
               return module_type::find_attribute( name );
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
            LOGILN( "Initialising SED module.", setindent( 2 ) );

            // Locate the backend and the simulation.
            _be = this->parents().front()->backend();
            _sim = this->template attribute<const simulation<real_type>*>( "simulation" );

            // Handle optinos.
            _read_options( global_dict );

            // Setup my SFH age line.
            _snap_ages.load_ages( _be->session(), _sim->hubble(), _sim->omega_m(), _sim->omega_l() );
            _sfh.set_snapshot_ages( &_snap_ages );
            _sfh.set_bin_ages( &_ssp.bin_ages() );

            // Allocate history bin arrays.
            _age_masses.reallocate( _ssp.bin_ages().size() );
            _bulge_age_masses.reallocate( _ssp.bin_ages().size() );
            _age_metals.reallocate( _ssp.bin_ages().size() );

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
            auto timer = this->timer_start();
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
#ifndef NLOG
	    auto gal_gids = bat.scalar<long long>( "globalindex" );
#endif

            // Perform the processing.
            for( unsigned ii = 0; ii < bat.size(); ++ii )
            {
	       LOGBLOCKI( "Calculating SED for galaxy with global index: ", gal_gids[ii] );

               // Be sure we're on the correct tree.
               {
                  auto db_timer = this->db_timer_start();
                  _sfh.load_tree_data( sql, table_name, tree_gids[ii], gal_gids[ii] );
               }
	       LOGILN( "Tree size: ", _sfh.size() );

               // Rebin the star-formation history.
	       hpc::profile::timer local_rebin_timer;
               {
                  auto rebin_timer = _rebin_timer.start();
		  auto ANON = local_rebin_timer.start();
                  _sfh.rebin<real_type>( _age_masses, _bulge_age_masses, _age_metals );
               }
	       LOGILN( "Rebinning took: ", local_rebin_timer.total(), " s" );

               // Sum contributions from the SSP.
               {
                  auto sum_timer = _sum_timer.start();
                  _ssp.sum( _age_masses.begin(), _age_metals.begin(), total_spectra[ii].begin() );
                  _ssp.sum( _bulge_age_masses.begin(), _age_metals.begin(), bulge_spectra[ii].begin() );
               }

               // Create disk spectra.
               for( unsigned jj = 0; jj < _ssp.wavelengths().size(); ++jj )
                  disk_spectra[ii][jj] = total_spectra[ii][jj] - bulge_spectra[ii][jj];

#if 0
	       // Dump stuff.
	       std::ofstream outf( boost::lexical_cast<std::string>( gal_gids[ii] ) + ".dat" );
	       outf << "MASSES: " << _age_masses << "\n";
	       outf << "METALS: " << _age_metals << "\n";
#endif
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
            LOGILN( this->_name, " rebinning time: ", _rebin_timer.total(), " (s)" );
            LOGILN( this->_name, " summation time: ", _sum_timer.total(), " (s)" );
         }

      protected:

         void
         _read_options( const options::xml_dict& global_dict )
         {
            // Cache dictionary.
            const options::xml_dict& dict = this->_dict;

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
         const simulation<real_type>* _sim;
         stellar_population _ssp;
         age_line<real_type> _snap_ages;
         sfh<real_type> _sfh;
         vector<real_type> _age_masses, _bulge_age_masses;
         vector<real_type> _age_metals;

         profile::timer _rebin_timer;
         profile::timer _sum_timer;
      };

   }
}

#endif
