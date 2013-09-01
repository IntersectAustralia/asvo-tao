#include <fstream>
#include "sed.hh"

using namespace hpc;

namespace tao {
   namespace modules {

      // Factory function used to create a new SED.
      module*
      sed::factory( const string& name,
                    pugi::xml_node base )
      {
         return new sed( name, base );
      }

      sed::sed( const string& name,
                pugi::xml_node base )
         : module( name, base )
      {
      }

      ///
      ///
      ///
      sed::~sed()
      {
      }

      ///
      /// Initialise the module.
      ///
      void
      sed::initialise( const options::xml_dict& global_dict )
      {
         LOGILN( "Initialising SED module.", setindent( 2 ) );

         module::initialise( global_dict );
         _read_options( global_dict );

         // // Allocate history bin arrays.
         // _age_masses.reallocate( _bin_ages.size() );
         // _bulge_age_masses.reallocate( _bin_ages.size() );
         // _age_metals.reallocate( _bin_ages.size() );

         // Prepare the batch object.
         tao::batch<real_type>& bat = parents().front()->batch();
         bat.set_vector<real_type>( "disk_spectra", _num_spectra );
         bat.set_vector<real_type>( "bulge_spectra", _num_spectra );
         bat.set_vector<real_type>( "total_spectra", _num_spectra );

         LOGILN( "Done.", setindent( -2 ) );
      }

      ///
      /// Run the module.
      ///
      void
      sed::execute()
      {
         timer_start();
         ASSERT( parents().size() == 1 );

         // Cache some information.
         soci::session& sql = _be->session();
         tao::batch<real_type>& bat = parents().front()->batch();
         const auto& table_name = bat.attribute<string>( "table" );
         const auto tree_gids = bat.scalar<long long>( "global_tree_id" );
         const auto gal_lids = bat.scalar<int>( "local_galaxy_id" );
         auto total_spectra = bat.vector<real_type>( "total_spectra" );
         auto disk_spectra = bat.vector<real_type>( "disk_spectra" );
         auto bulge_spectra = bat.vector<real_type>( "bulge_spectra" );

         // Perform the processing.
         for( unsigned ii = 0; ii < bat.size(); ++ii )
         {
            // Be sure we're on the correct tree.
            _sfh.load_tree_data( sql, table_name, tree_gids[ii] );

            // Rebin the star-formation history.
            _sfh.rebin<real_type>( sql, gal_lids[ii], _age_masses, _bulge_age_masses, _age_metals );

            // Sum contributions from the SSP.
            _ssp.sum( _age_masses.begin(), _age_metals.begin(), total_spectra[ii].begin() );
            _ssp.sum( _bulge_age_masses.begin(), _age_metals.begin(), bulge_spectra[ii].begin() );

            // Create disk spectra.
            for( unsigned jj = 0; jj < _ssp.wavelengths().size(); ++jj )
               disk_spectra[ii][jj] = total_spectra[ii][jj] - bulge_spectra[ii][jj];
         }

         timer_stop();
      }

      void
      sed::_read_options( const options::xml_dict& global_dict )
      {
         // Get the filenames for SSP information.
         string wave_fn = _dict.get<string>( "wavelengths-file" );
         string metal_fn = _dict.get<string>( "metallicities-file" );
         string ssp_fn = _dict.get<string>( "single-stellar-population-model" );

         // // Prepare the SSP.
         // _ssp.load( wave_fn, metal_fn, ssp_fn );
      }

   }
}
