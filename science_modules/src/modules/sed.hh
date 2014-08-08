#ifndef tao_modules_sed_hh
#define tao_modules_sed_hh

#include <libhpc/libhpc.hh>
#include <boost/optional.hpp>
#include "tao/base/base.hh"

namespace tao {
   namespace modules {

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
         factory( std::string const& name,
                  pugi::xml_node base )
         {
            return new sed( name, base );
         }

      public:

         sed( std::string const& name = std::string(),
              pugi::xml_node base = pugi::xml_node() )
            : module_type( name, base ),
              _be( 0 ),
              _sim( 0 )
         {
         }

         virtual
         ~sed()
         {
         }

         backend_type const*
         backend() const
         {
            return _be;
         }

         tao::simulation const*
         simulation() const
         {
            return _sim;
         }

         std::vector<real_type> const&
         disk_age_masses() const
         {
            return _disk_age_masses;
         }

         std::vector<real_type> const&
         bulge_age_masses() const
         {
            return _bulge_age_masses;
         }

         virtual
         boost::optional<boost::any>
         find_attribute( std::string const& name )
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
         initialise( xml_dict const& global_dict )
         {
            // Don't initialise if we're already doing so.
            if( this->_init )
               return;
            module_type::initialise( global_dict );

            LOGBLOCKI( "Initialising SED module." );

            // Locate the backend and the simulation.
            _be = this->parents().front()->backend();
            _sim = this->template attribute<tao::simulation const*>( "simulation" );

            // Handle optinos.
            _read_options( global_dict );

            // Setup my SFH age line.
            _snap_ages.load_ages( _be->session(), _sim->hubble(), _sim->omega_m(), _sim->omega_l() );
            _sfh.set_h( _sim->h() );
            _sfh.set_snapshot_ages( &_snap_ages );

            // Allocate history bin arrays.
            hpc::reallocate( _disk_age_masses,  _ssp.age_masses_size() );
            hpc::reallocate( _bulge_age_masses, _ssp.age_masses_size() );

            // Prepare the batch object.
            tao::batch<real_type>& bat = this->parents().front()->batch();
            bat.set_vector<real_type>( "disk_spectra",  _ssp.wavelengths().size() );
            bat.set_vector<real_type>( "bulge_spectra", _ssp.wavelengths().size() );
            bat.set_vector<real_type>( "total_spectra", _ssp.wavelengths().size() );
         }

         ///
         /// Run the module for a batch object.
         ///
         virtual
         void
         execute()
         {
            ASSERT( this->parents().size() == 1, "SED module must have at least and "
                    "at most one parent." );
	    LOGBLOCKD( "Processing batch in SED module." );

            // Cache some information.
            tao::batch<real_type>& bat = this->parents().front()->batch();
            auto const& table_name = bat.attribute<std::string>( "table" );
            auto const tree_gids   = bat.scalar<long long>( "globaltreeid" );
            auto const gal_lids    = bat.scalar<int>(       "localgalaxyid" );
            auto& total_spectra    = bat.vector<real_type>( "total_spectra" );
            auto& disk_spectra     = bat.vector<real_type>( "disk_spectra" );
            auto& bulge_spectra    = bat.vector<real_type>( "bulge_spectra" );
	    auto const gal_gids    = bat.scalar<long long>( "globalindex" );
            soci::session& sql     = _be->session( table_name );

            // Perform the processing.
            for( unsigned ii = 0; ii < bat.size(); ++ii )
            {
	       LOGILN( "Calculating SED for galaxy with global index: ", gal_gids[ii] );

               // Be sure we're on the correct tree.
               _sfh.load_tree_data( sql, table_name, tree_gids[ii], gal_gids[ii] );

               // Rebin the star-formation history.
               _sfh.rebin<std::vector<real_type>,std::vector<real_type>>(
                  _disk_age_masses, _bulge_age_masses, _ssp
                  );

               // Sum contributions from the SSP.
               _ssp.sum( _disk_age_masses.begin(),  disk_spectra[ii].begin() );
               _ssp.sum( _bulge_age_masses.begin(), bulge_spectra[ii].begin() );

               // Create total spectra.
               for( unsigned jj = 0; jj < _ssp.wavelengths().size(); ++jj )
                  total_spectra[ii][jj] = disk_spectra[ii][jj] + bulge_spectra[ii][jj];
            }
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
         _read_options( xml_dict const& global_dict )
         {
            // Cache dictionary.
            xml_dict const& dict = this->_dict;

            // Get the filenames for SSP information.
            auto path = data_prefix()/"stellar_populations";
            auto ages_fn = path/dict.get<std::string>( "ages-file" );
            auto waves_fn = path/dict.get<std::string>( "wavelengths-file" );
            auto metals_fn = path/dict.get<std::string>( "metallicities-file" );
            auto ssp_fn = path/dict.get<std::string>( "single-stellar-population-model" );

            // Prepare the SSP.
            _ssp.load( ages_fn, waves_fn, metals_fn, ssp_fn );
         }

      protected:

         backend_type* _be;
         tao::simulation const* _sim;
         stellar_population _ssp;
         age_line<real_type> _snap_ages;
         sfh _sfh;
         std::vector<real_type> _disk_age_masses;
         std::vector<real_type> _bulge_age_masses;
      };

   }
}

#endif
