#include <fstream>
#include <boost/lexical_cast.hpp>
#include "sed.hh"

using namespace hpc;
using boost::format;
using boost::str;

namespace tao {

   sed::sed()
      : _cur_flat_file( -1 )
   {
   }

   ///
   ///
   ///
   sed::~sed()
   {
   }

   ///
   ///
   ///
   void
   sed::setup_options( options::dictionary& dict,
                       optional<const string&> prefix )
   {
      dict.add_option( new options::string( "database_type" ), prefix );
      dict.add_option( new options::string( "database_name" ), prefix );
      dict.add_option( new options::string( "database_host", string() ), prefix );
      dict.add_option( new options::string( "database_user", string() ), prefix );
      dict.add_option( new options::string( "database_pass", string() ), prefix );
      dict.add_option( new options::string( "ssp_filename" ), prefix );
      dict.add_option( new options::integer( "num_times" ), prefix );
      dict.add_option( new options::integer( "num_spectra" ), prefix );
      dict.add_option( new options::integer( "num_metals" ), prefix );
   }

   ///
   ///
   ///
   void
   sed::setup_options( hpc::options::dictionary& dict,
                       const char* prefix )
   {
      setup_options( dict, string( prefix ) );
   }

   ///
   /// Initialise the module.
   ///
   void
   sed::initialise( const options::dictionary& dict,
                    optional<const string&> prefix )
   {
      LOG_ENTER();

      // Create flat HDF5 types.
      make_hdf5_types( _flat_mem_type, _flat_file_type );

      _read_options( dict, prefix );

      // Allocate for storing star-formation histories and
      // metallicities.
      _disk_sfh.resize( _num_times );
      _disk_metals.resize( _num_times );
      _bulge_sfh.resize( _num_times );
      _bulge_metals.resize( _num_times );

      // Allocate for output spectra.
      _disk_spectra.reallocate( _num_spectra );
      _bulge_spectra.reallocate( _num_spectra );
      _total_spectra.reallocate( _num_spectra );

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   sed::initialise( const hpc::options::dictionary& dict,
                    const char* prefix )
   {
      initialise( dict, string( prefix ) );
   }

   ///
   /// Run the module.
   ///
   void
   sed::run()
   {
      LOG_ENTER();

      // for( mpi::lindex ii = 0; ii < _num_galaxies; ++ii )
      //    _process_galaxy();

      LOG_EXIT();
   }

   void
   sed::process_galaxy( const tao::galaxy& galaxy )
   {
      LOG_ENTER();

      // Cache the galaxy ID.
      unsigned gal_id = galaxy.id();
      LOGLN( "Processing galaxy with ID ", gal_id );

      // Read the star-formation histories for this galaxy.


      _sql << "select mass, metal from disk_star_formation where galaxy_id=:id order by -age",
         soci::into( (std::vector<real_type>&)_disk_sfh ), soci::into( (std::vector<real_type>&)_disk_metals ), soci::use( gal_id );
      _sql << "select mass, metal from bulge_star_formation where galaxy_id=:id order by -age",
         soci::into( (std::vector<real_type>&)_bulge_sfh ), soci::into( (std::vector<real_type>&)_bulge_metals ), soci::use( gal_id );
      LOGLN( "Disk SFH: ", _disk_sfh );
      LOGLN( "Disk metals: ", _disk_metals );
      LOGLN( "Bulge SFH: ", _bulge_sfh );
      LOGLN( "Bulge metals: ", _bulge_metals );

      // Clear disk and bulge output spectrums.
      std::fill( _disk_spectra.begin(), _disk_spectra.end(), 0.0 );
      std::fill( _bulge_spectra.begin(), _bulge_spectra.end(), 0.0 );

      // Process each time.
      for( mpi::lindex ii = 0; ii < _num_times; ++ii )
         _process_time( ii );

      // Create total spectra.
      for( unsigned ii = 0; ii < _num_spectra; ++ii )
         _total_spectra[ii] = _disk_spectra[ii] + _bulge_spectra[ii];

      LOGLN( "Disk: ", _disk_spectra );
      LOGLN( "Bulge: ", _bulge_spectra );
      LOGLN( "Total: ", _total_spectra );
      LOG_EXIT();
   }

   vector<sed::real_type>::view
   sed::disk_spectra()
   {
      return _disk_spectra;
   }

   vector<sed::real_type>::view
   sed::bulge_spectra()
   {
      return _bulge_spectra;
   }

   vector<sed::real_type>::view
   sed::total_spectra()
   {
      return _total_spectra;
   }

   void
   sed::_process_time( mpi::lindex time_idx )
   {
      LOG_ENTER();
      LOGLN( "Processing time ", time_idx );

      _sum_spectra( time_idx, _disk_metals[time_idx], _disk_sfh[time_idx], _disk_spectra );
      _sum_spectra( time_idx, _bulge_metals[time_idx], _bulge_sfh[time_idx], _bulge_spectra );

      LOG_EXIT();
   }

   void
   sed::_sum_spectra( mpi::lindex time_idx,
                      real_type metal,
                      real_type sfh,
                      vector<real_type>::view galaxy_spectra )
   {
      LOG_ENTER();

      // Interpolate the metallicity to an index.
      unsigned metal_idx = _interp_metal( metal );
      ASSERT( metal_idx < _num_metals );
      LOGLN( "Found metal index: ", metal_idx );

      // Calculate the base index for the ssp table.
      size_t base = time_idx*_num_spectra*_num_metals + metal_idx;

      for( unsigned ii = 0; ii < _num_spectra; ++ii )
      {
         // The star formation histories read from the file are in
         // solar masses/1e10. The values in SSP are luminosity densities
         // in erg/s/angstrom, and they're really big. Scale them down
         // by 1e10 to make it more manageable.
         galaxy_spectra[ii] += _ssp[base + ii*_num_metals]*sfh;
      }

      LOG_EXIT();
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
   sed::_rebin_info( unsigned flat_file,
                     unsigned flat_offset,
                     unsigned flat_length )
   {
      // Be sure we have the correct flat information available.
      _update_flat_info( flat_file );

      // Create the knots for disk/bulge star formation rates.
      fibre<real_type> dknots( 2, flat_length ), bknots( 2, flat_length );
      for( unsigned ii = 0; ii < flat_length; ++ii )
      {
         dknots(ii,0) = _flat_data[flat_offset + ii].redshift;
         bknots(ii,0) = _flat_data[flat_offset + ii].redshift;
         dknots(ii,1) = _flat_data[flat_offset + ii].disk_rate;
         bknots(ii,1) = _flat_data[flat_offset + ii].bulge_rate;
      }

      // Prepare splines.
      numerics::spline dspline, bspline;
      dspline.set_knots( dknots );
      bspline.set_knots( bknots );

      // Integrate

      // Iterate over new time points, interpolating.
      for( unsigned ii = 0; ii < _age_points; ++ii )
      {
         _disk_sfr[ii] = dspline( _age_points[ii] );
         _bulge_sfr[ii] = bspline( _age_points[ii] );
      }
   }

   void
   sed::_update_flat_info( unsigned flat_file )
   {
      if( flat_file != _flat_file )
      {
         // For now I force continually increasing flat files. This may
         // change in the future.
         ASSERT( flat_file > _flat_file );

         _read_flat_file( "trees", flat_file );
      }
   }

   void
   sed::_read_options( const options::dictionary& dict,
                       optional<const string&> prefix )
   {
      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      // Extract database details.
      _dbtype = sub.get<string>( "database_type" );
      _dbname = sub.get<string>( "database_name" );
      _dbhost = sub.get<string>( "database_host" );
      _dbuser = sub.get<string>( "database_user" );
      _dbpass = sub.get<string>( "database_pass" );
      _db_connect( _sql, _dbtype, _dbname );

      // Extract the counts.
      _num_times = sub.get<unsigned>( "num_times" );
      _num_spectra = sub.get<unsigned>( "num_spectra" );
      _num_metals = sub.get<unsigned>( "num_metals" );
      LOGLN( "Number of times: ", _num_times );
      LOGLN( "Number of spectra: ", _num_spectra );
      LOGLN( "Number of metals: ", _num_metals );

      // Get the SSP filename.
      _read_ssp( sub.get<string>( "ssp_filename" ) );
   }

   void
   sed::_read_ssp( const string& filename )
   {
      LOG_ENTER();

      // Allocate. Note that the ordering goes time,spectra,metals.
      _ssp.reallocate( _num_times*_num_spectra*_num_metals );
      LOGLN( "Reallocated SSP array to ", _ssp.size() );

      // Read in the file in one big go.
      std::ifstream file( filename, std::ios::in );
      for( unsigned ii = 0; ii < _ssp.size(); ++ii )
      {
         // These values are luminosity densities, in erg/s/angstrom.
         file >> _ssp[ii];
         ASSERT( file.good() );
      }

      LOG_EXIT();
   }

   void
   sed::_read_flat_file( const string& base_filename,
                         unsigned flat_file )
   {
      string filename = base_filename + string( ".flat." ) + to_string( flat_file );
      h5::file file( filename, H5_ACC_RONLY );
      _flat_data.reallocate( file.read_data_size( "flat_trees" ) );
      file.read( "flat_trees", _flat_mem_type, _flat_data, _flat_file_type );
   }
}
