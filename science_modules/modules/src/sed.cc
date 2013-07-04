#include <fstream>
#include "sed.hh"

using namespace hpc;

namespace tao {

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
      module::initialise( global_dict );
      _read_options( global_dict );

      // Allocate for output spectra.
      _disk_spectra.reallocate( _num_spectra, _batch_size );
      _bulge_spectra.reallocate( _num_spectra, _batch_size );
      _total_spectra.reallocate( _num_spectra, _batch_size );
   }

   ///
   /// Run the module.
   ///
   void
   sed::execute()
   {
      _timer.start();
      ASSERT( parents().size() == 1 );

      // Grab the galaxy from the parent object.
      tao::galaxy& gal = parents().front()->galaxy();

      // Perform the processing.
      process_galaxy( gal );

      // Add spectra to the galaxy object.
      gal.set_vector_field<real_type>( "disk_spectra", _disk_spectra );
      gal.set_vector_field<real_type>( "bulge_spectra", _bulge_spectra );
      gal.set_vector_field<real_type>( "total_spectra", _total_spectra );

      _timer.stop();
   }

   void
   sed::process_galaxy( const tao::galaxy& galaxy )
   {
      _timer.start();

      // Process each galaxy.
      for( unsigned ii = 0; ii < galaxy.batch_size(); ++ii )
      {
         // Cache the galaxy ID.
         long long gal_id = galaxy.values<long long>( "globalindex" )[ii];
         LOGDLN( "SED: Processing galaxy with ID: ", gal_id, setindent( 2 ) );

         // Do we need to load a fresh table?
         long long tree_id = galaxy.values<long long>( "globaltreeid" )[ii];
         const string& table = galaxy.table();
#ifdef MULTIDB
         _sfh.load_tree_data( (*_db)[table], table, tree_id );
#else
         _sfh.load_tree_data( _sql, table, tree_id );
#endif

         // Read the star-formation histories for this galaxy.
         unsigned loc_gal_id = galaxy.values<int>( "localgalaxyid" )[ii];
#ifdef MULTIDB
         _sfh.rebin<real_type>( (*_db)[table], loc_gal_id, _age_masses, _bulge_age_masses, _age_metals );
#else
         _sfh.rebin<real_type>( _sql, loc_gal_id, _age_masses, _bulge_age_masses, _age_metals );
#endif

         // Clear disk and bulge output spectrums.
         std::fill( _total_spectra[ii].begin(), _total_spectra[ii].end(), 0.0 );
         std::fill( _bulge_spectra[ii].begin(), _bulge_spectra[ii].end(), 0.0 );

         // Process each time.
         for( mpi::lindex jj = 0; jj < _bin_ages.size(); ++jj )
            _process_time( jj, ii );

         // Create disk spectra.
         for( unsigned jj = 0; jj < _num_spectra; ++jj )
            _disk_spectra[ii][jj] = _total_spectra[ii][jj] - _bulge_spectra[ii][jj];

         LOGTLN( "SED: Disk: ", _disk_spectra[ii] );
         LOGTLN( "SED: Bulge: ", _bulge_spectra[ii] );
         LOGTLN( "SED: Total: ", _total_spectra[ii] );
         LOGD( setindent( -2 ) );
      }

      _timer.stop();
   }

   void
   sed::_process_time( mpi::lindex time_idx,
                       unsigned gal_idx )
   {
      LOGDLN( "SED: Processing age: ", _bin_ages[time_idx], setindent( 2 ) );
      _sum_spectra( time_idx, _age_metals[time_idx], _age_masses[time_idx], _total_spectra[gal_idx] );
      _sum_spectra( time_idx, _age_metals[time_idx], _bulge_age_masses[time_idx], _bulge_spectra[gal_idx] );
      LOGD( setindent( -2 ) );
   }

   void
   sed::_sum_spectra( mpi::lindex time_idx,
                      real_type metal,
                      real_type age_mass,
                      vector<real_type>::view galaxy_spectra )
   {
      // Interpolate the metallicity to an index.
      unsigned metal_idx = _interp_metal( metal );
      ASSERT( metal_idx < _num_metals );
      LOGDLN( "Found metal index ", metal_idx, " from metallicity of ", metal );

      // Calculate the base index for the ssp table.
      size_t base = time_idx*_num_spectra*_num_metals + metal_idx;

      for( unsigned ii = 0; ii < _num_spectra; ++ii )
      {
         // The star formation histories read from the file are in
         // solar masses/1e10. The values in SSP are luminosity densities
         // in erg/s/angstrom, and they're really big. Scale them down
         // by 1e10 to make it more manageable.
         galaxy_spectra[ii] += _ssp[base + ii*_num_metals]*age_mass;
      }
   }

   unsigned
   sed::_interp_metal( real_type metal )
   {
      if( metal <= 0.0005 )
         return 0;
      else if( metal <= 0.0025 )
         return 1;
      else if( metal <= 0.007 )
         return 2;
      else if( metal <= 0.015 )
         return 3;
      else if( metal <= 0.03 )
         return 4;
      else if( metal <= 0.055 )
         return 5;
      else
         return 6;
   }

   void
   sed::_read_options( const options::xml_dict& global_dict )
   {
      // Extract database details and connect.
      _read_db_options( global_dict );
      _db_connect();

      // Try to read H0, omega_m and omega_l from the lightcone module.
      _hubble = global_dict.get<real_type>( "workflow:light-cone:H0", 73.0 );
      _omega_m = global_dict.get<real_type>( "workflow:light-cone:omega_m", 0.25 );
      _omega_l = global_dict.get<real_type>( "workflow:light-cone:omega_l", 0.75 );
      LOGILN( "SED: Hubble constant: ", _hubble );
      LOGILN( "SED: OmegaM: ", _omega_m );
      LOGILN( "SED: OmegaL: ", _omega_l );

      // Extract the counts.
      _num_spectra = _dict.get<unsigned>( "num-spectra", 1221 );
      _num_metals = _dict.get<unsigned>( "num-metals", 7 );
      LOGILN( "SED: Number of times: ", _bin_ages.size() );
      LOGILN( "SED: Number of spectra: ", _num_spectra );
      LOGILN( "SED: Number of metals: ", _num_metals );

      // Get the SSP filename.
      string ssp_fn = _dict.get<string>( "single-stellar-population-model" );
      LOGILN( "SED: SSP filename: ", ssp_fn );
      _read_ssp( ssp_fn );

      // Setup the snapshot ages and SFH.
#ifdef MULTIDB
      _snap_ages.load_ages( (*_db)["tree_1"], _hubble, _omega_m, _omega_l );
#else
      _snap_ages.load_ages( _sql, _hubble, _omega_m, _omega_l );
#endif
      _sfh.set_snapshot_ages( &_snap_ages );
      _sfh.set_bin_ages( &_bin_ages );
   }

   void
   sed::_read_ssp( const string& filename )
   {
      // The SSP file contains the age grid information first.
      std::ifstream file( filename, std::ios::in );
      unsigned num_ages;
      file >> num_ages;
      ASSERT( file.good(), "Error reading SSP file." );
      {
         vector<real_type> bin_ages( num_ages );
         for( unsigned ii = 0; ii < num_ages; ++ii )
         {
            file >> bin_ages[ii];
            ASSERT( file.good(), "Error reading SSP file." );
         }

#ifndef NDEBUG
         // Must be ordered.
         for( unsigned ii = 1; ii < bin_ages.size(); ++ii )
            ASSERT( bin_ages[ii] >= bin_ages[ii - 1], "Bin ages must be descending ordered." );
#endif

         // Setup the bin ages.
         _bin_ages.set_ages( bin_ages );
      }

      // Allocate. Note that the ordering goes time,spectra,metals.
      _ssp.reallocate( _bin_ages.size()*_num_spectra*_num_metals );

      // Read in the file in one big go.
      for( unsigned ii = 0; ii < _ssp.size(); ++ii )
      {
         // These values are luminosity densities, in erg/s/angstrom.
         file >> _ssp[ii];
         ASSERT( file.good(), "Error reading SSP file." );
      }

      // Allocate history bin arrays.
      _age_masses.reallocate( _bin_ages.size() );
      _bulge_age_masses.reallocate( _bin_ages.size() );
      _age_metals.reallocate( _bin_ages.size() );
   }
}
