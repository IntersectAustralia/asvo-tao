#include <fstream>
#include <boost/filesystem.hpp>
#include <libhpc/system/exe.hh>
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
      return algorithm::bin( _metal_bins.begin(), _metal_bins.end(), metal );
      // if( metal <= 0.0005 )
      //    return 0;
      // else if( metal <= 0.0025 )
      //    return 1;
      // else if( metal <= 0.007 )
      //    return 2;
      // else if( metal <= 0.015 )
      //    return 3;
      // else if( metal <= 0.03 )
      //    return 4;
      // else if( metal <= 0.055 )
      //    return 5;
      // else
      //    return 6;
   }

   void
   sed::_read_options( const options::xml_dict& global_dict )
   {
      // Extract database details and connect.
      _read_db_options( global_dict );
      _db_connect();

      // Try to read H0, omega_m and omega_l from the lightcone module.
      {
	 std::string h_val, m_val, l_val;
#ifdef MULTIDB
	 (*_db)["tree_1"] << "SELECT metavalue FROM metadata WHERE metakey='hubble'", soci::into( h_val );
	 (*_db)["tree_1"] << "SELECT metavalue FROM metadata WHERE metakey='omega_m'", soci::into( m_val );
	 (*_db)["tree_1"] << "SELECT metavalue FROM metadata WHERE metakey='omega_l'", soci::into( l_val );
#else
	 _sql << "SELECT metavalue FROM metadata WHERE metakey='hubble'", soci::into( h_val );
	 _sql << "SELECT metavalue FROM metadata WHERE metakey='omega_m'", soci::into( m_val );
	 _sql << "SELECT metavalue FROM metadata WHERE metakey='omega_l'", soci::into( l_val );
#endif
	 _hubble = boost::lexical_cast<real_type>( h_val );
	 _omega_m = boost::lexical_cast<real_type>( m_val );
	 _omega_l = boost::lexical_cast<real_type>( l_val );
      }
      LOGILN( "SED: Hubble constant: ", _hubble );
      LOGILN( "SED: OmegaM: ", _omega_m );
      LOGILN( "SED: OmegaL: ", _omega_l );

      // Extract number of wavelengths from file.
      {
	 string filename = _dict.get<string>( "wavelengths-file", "m05/wavelengths.dat" );
	 LOGILN( "SED: Wavelengths filename: ", filename );
	 _read_waves( filename );
      }

      // Load the metallicities.
      {
	 string filename = _dict.get<string>( "metallicities-file", "m05/metallicites.dat" );
	 LOGILN( "SED: Metallicity filename: ", filename );
	 _read_metals( filename );
      }

      // Load the ages.
      {
	 string filename = _dict.get<string>( "ages-file", "m05/ages.dat" );
	 LOGILN( "SED: Ages filename: ", filename );
	 _read_ages( filename );
      }

      // Load the SSP.
      string ssp_fn = _dict.get<string>( "single-stellar-population-model", "m05/ssp.ssz" );
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
   sed::_read_ages( const string& filename )
   {
      // The SSP file contains the age grid information first.
      boost::filesystem::path fn = nix::executable_path().parent_path().parent_path()/"data/stellar_populations/"/filename;
      std::ifstream file( fn.c_str(), std::ios::in );
      unsigned num_ages;
      file >> num_ages;
      ASSERT( file.good(), "Error reading ages file." );
      {
         vector<real_type> bin_ages( num_ages );
         for( unsigned ii = 0; ii < num_ages; ++ii )
         {
            file >> bin_ages[ii];
            ASSERT( file.good(), "Error reading ages file." );
         }

#ifndef NDEBUG
         // Must be ordered.
         for( unsigned ii = 1; ii < bin_ages.size(); ++ii )
            ASSERT( bin_ages[ii] >= bin_ages[ii - 1], "Bin ages must be descending ordered." );
#endif

         // Setup the bin ages.
         _bin_ages.set_ages( bin_ages );
      }

      // Allocate history bin arrays.
      _age_masses.reallocate( _bin_ages.size() );
      _bulge_age_masses.reallocate( _bin_ages.size() );
      _age_metals.reallocate( _bin_ages.size() );
   }

   void
   sed::_read_ssp( const string& filename )
   {
      boost::filesystem::path fn = nix::executable_path().parent_path().parent_path()/"data/stellar_populations/"/filename;
      std::ifstream file( fn.c_str(), std::ios::in );

      // Allocate. Note that the ordering goes time,spectra,metals.
      _ssp.reallocate( _bin_ages.size()*_num_spectra*_num_metals );

      // Read in the file in one big go.
      for( unsigned ii = 0; ii < _ssp.size(); ++ii )
      {
         // These values are luminosity densities, in erg/s/angstrom.
         file >> _ssp[ii];
         ASSERT( file.good(), "Error reading SSP file." );
      }
   }

   void
   sed::_read_metals( const string& filename )
   {
      boost::filesystem::path fn = nix::executable_path().parent_path().parent_path()/"data/stellar_populations/"/filename;
      std::ifstream file( fn.c_str(), std::ios::in );

      // The first line can be the word "dual", indicating
      // the dual has already been taken.
      string dual;
      file >> dual;
      ASSERT( file, "Error reading metallicity file." );

      if( dual == "dual" )
      {
	 file >> _num_metals;
	 ASSERT( file, "Error reading metallicity file." );
      }
      else
	 _num_metals = boost::lexical_cast<unsigned>( dual );
      ASSERT( file, "Error reading metallicity file." );
      if( _num_metals )
      {
         vector<real_type> metals( _num_metals );
         for( unsigned ii = 0; ii < _num_metals; ++ii )
         {
            file >> metals[ii];
            ASSERT( file, "Error reading metallicity file." );
         }
	 ASSERT( std::is_sorted( metals.begin(), metals.end() ),
		 "Metallicities must be in ascending order." );

	 // Store the duals if not already in that format.
	 if( dual == "dual" )
	 {
	    _metal_bins.resize( _num_metals++ );
	    std::copy( metals.begin(), metals.end(), _metal_bins.begin() );
	 }
	 else
	 {
	    _metal_bins.resize( _num_metals - 1 );
	    algorithm::dual( metals.begin(), metals.end(), _metal_bins.begin() );
	 }
      }
   }

   void
   sed::_read_waves( const string& filename )
   {
      boost::filesystem::path fn = nix::executable_path().parent_path().parent_path()/"data/stellar_populations/"/filename;
      std::ifstream file( fn.c_str(), std::ios::in );
      ASSERT( file, "Couldn't find wavelengths file.") ;

      // Need to get number of lines in file first.
      _num_spectra = 0;
      {
         string line;
         while( !file.eof() )
         {
            std::getline( file, line );
            if( boost::trim_copy( line ).length() )
               ++_num_spectra;
         }
      }
   }
}
