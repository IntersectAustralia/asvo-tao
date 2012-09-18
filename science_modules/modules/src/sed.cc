#include <fstream>
#include <boost/algorithm/string/trim.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/tokenizer.hpp>
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
      // dict.add_option( new options::string( "database_type" ), prefix );
      // dict.add_option( new options::string( "database_name" ), prefix );
      // dict.add_option( new options::string( "database_host", string() ), prefix );
      // dict.add_option( new options::string( "database_user", string() ), prefix );
      // dict.add_option( new options::string( "database_pass", string() ), prefix );
      dict.add_option( new options::string( "ssp_filename" ), prefix );
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
      make_hdf5_types<real_type>( _flat_mem_type, _flat_file_type );

      _read_options( dict, prefix );

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
      _rebin_info( galaxy.flat_file(), galaxy.flat_offset(), galaxy.flat_length() );

      // Clear disk and bulge output spectrums.
      std::fill( _disk_spectra.begin(), _disk_spectra.end(), 0.0 );
      std::fill( _bulge_spectra.begin(), _bulge_spectra.end(), 0.0 );

      // Process each time.
      for( mpi::lindex ii = 0; ii < _ages.size(); ++ii )
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

      _sum_spectra( time_idx, _disk_age_metals[time_idx], _disk_age_masses[time_idx], _disk_spectra );
      _sum_spectra( time_idx, _bulge_age_metals[time_idx], _bulge_age_masses[time_idx], _bulge_spectra );

      LOG_EXIT();
   }

   void
   sed::_sum_spectra( mpi::lindex time_idx,
                      real_type metal,
                      real_type age_mass,
                      vector<real_type>::view galaxy_spectra )
   {
      LOG_ENTER();

      // Interpolate the metallicity to an index.
      unsigned metal_idx = _interp_metal( metal );
      ASSERT( metal_idx < _num_metals );
      LOGLN( "Found metal index ", metal_idx, " from metallicity of ", metal );

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
      LOG_ENTER();

      // Be sure we have the correct flat information available.
      _update_flat_info( flat_file );

      // If there is only one item to rebin, don't try to build the cubic splines.
      if( flat_length > 1 )
      {
         LOGLN( "Flat length greater than one." );

         // Create the knots for disk/bulge star formation rates.
         fibre<real_type> dmassknots( 2, flat_length ), bmassknots( 2, flat_length );
         fibre<real_type> dmetknots( 2, flat_length ), bmetknots( 2, flat_length );
         for( unsigned ii = 0; ii < flat_length; ++ii )
         {
            dmassknots(ii,0) = _flat_data[flat_offset + ii].redshift;
            bmassknots(ii,0) = _flat_data[flat_offset + ii].redshift;
            dmetknots(ii,0) = _flat_data[flat_offset + ii].redshift;
            bmetknots(ii,0) = _flat_data[flat_offset + ii].redshift;
            dmassknots(ii,1) = _flat_data[flat_offset + ii].disk_rate;
            bmassknots(ii,1) = _flat_data[flat_offset + ii].bulge_rate;
            dmetknots(ii,1) = _flat_data[flat_offset + ii].disk_metal;
            bmetknots(ii,1) = _flat_data[flat_offset + ii].bulge_metal;
         }
         LOGLN( "Disk knots: ", dmassknots );
         LOGLN( "Bulge knots: ", bmassknots );

         // Prepare splines.
         numerics::spline<real_type> dmassspline, bmassspline;
         numerics::spline<real_type> dmetspline, bmetspline;
         dmassspline.set_knots( dmassknots );
         bmassspline.set_knots( bmassknots );
         dmetspline.set_knots( dmetknots );
         bmetspline.set_knots( bmetknots );

         // Clear out values.
         std::fill( _disk_age_masses.begin(), _disk_age_masses.end(), 0.0 );
         std::fill( _bulge_age_masses.begin(), _bulge_age_masses.end(), 0.0 );
         std::fill( _disk_age_metals.begin(), _disk_age_metals.end(), 0.0 );
         std::fill( _bulge_age_metals.begin(), _bulge_age_metals.end(), 0.0 );

         // Integrate.
         typedef vector<real_type>::view array_type;
         element<array_type> take_first( 0 );
         range<real_type> old_rng( dmassspline.knots().front()[0], dmassspline.knots().back()[0] );
         range<real_type> new_rng( _ages.front(), _ages.back() );
         LOGLN( "Age range: ", new_rng );
         LOGLN( "Galaxy redshift range: ", old_rng );
         real_type low = old_rng.start();
         real_type upp = old_rng.finish();
         auto it = make_interp_iterator(
            boost::make_transform_iterator( dmassspline.knots().begin(), take_first ),
            boost::make_transform_iterator( dmassspline.knots().end(), take_first ),
            _ages.begin(),
            _ages.end(),
            1e-7
            );
         while( !num::approx( *it, low, 1e-7 ) )
            ++it;
         vector<real_type> crds( 4 ), weights( 4 );
         _gauss_quad( crds, weights );
         while( !num::approx( *it++, upp, 1e-7 ) )
         {
            LOGLN( "Integrating range: (", low, ", ", *it, ")" );
            real_type w = *it - low;
            real_type jac_det = 0.5*w;
            unsigned old_poly = it.indices()[0] - 1;
            unsigned new_poly = it.indices()[1] - 1;
            LOGLN( "Galaxy/age indices: ", old_poly, ", ", new_poly );
            for( unsigned ii = 0; ii < 4; ++ii )
            {
               real_type x = low + w*0.5*(1.0 + crds[ii]);

               // This integral looks like this because of a change of variable
               // frome wavelength to frequency. Do the math!
               _disk_age_masses[new_poly] += jac_det*weights[ii]*dmassspline( x, old_poly )*1e10;
               _bulge_age_masses[new_poly] += jac_det*weights[ii]*bmassspline( x, old_poly )*1e10;
            }

            // Interpolate metallicity.
            _disk_age_metals[new_poly] = dmetspline( low, old_poly );
            _bulge_age_metals[new_poly] = bmetspline( low, old_poly );

            // Advance.
            low = *it;
         }
      }
      else
      {
         LOGLN( "Flat length equal to one." );

         // Locate the correct bin.
         auto it = std::lower_bound( _ages.begin(), _ages.end(), _flat_data[flat_offset].redshift );
         unsigned bin;
         if( it == _ages.end() )
            bin = _ages.size() - 1;
         else
            bin = *it;
         LOGLN( "Redshift ", _flat_data[flat_offset].redshift, " correlates to bin ", bin );
         _disk_age_masses[bin] = _flat_data[flat_offset].disk_mass;
         _bulge_age_masses[bin] = _flat_data[flat_offset].bulge_mass;
         _disk_age_metals[bin] = _flat_data[flat_offset].disk_metal;
         _bulge_age_metals[bin] = _flat_data[flat_offset].bulge_metal;
      }

      LOGLN( "Disk masses: ", _disk_age_masses );
      LOGLN( "Bulge masses: ", _bulge_age_masses );
      LOGLN( "Disk metals: ", _disk_age_metals );
      LOGLN( "Bulge metals: ", _bulge_age_metals );
      LOG_EXIT();
   }

   void
   sed::_gauss_quad( vector<real_type>::view crds,
                     vector<real_type>::view weights )
   {
      real_type v0 = sqrt( (3.0 - 2.0*sqrt( 6.0/5.0 ))/7.0 );
      real_type v1 = sqrt( (3.0 + 2.0*sqrt( 6.0/5.0 ))/7.0 );
      crds[0] = -v1;
      crds[1] = -v0;
      crds[2] = v0;
      crds[3] = v1;
      weights[0] = (18.0 - sqrt( 30.0 ))/36.0;
      weights[1] = (18.0 + sqrt( 30.0 ))/36.0;
      weights[2] = (18.0 + sqrt( 30.0 ))/36.0;
      weights[3] = (18.0 - sqrt( 30.0 ))/36.0;
   }

   void
   sed::_update_flat_info( unsigned flat_file )
   {
      LOG_ENTER();

      if( flat_file != _cur_flat_file )
      {
         LOGLN( "Need to change flat file." );

         // For now I force continually increasing flat files. This may
         // change in the future.
         ASSERT( (int)flat_file > _cur_flat_file );

         _read_flat_file( "trees", flat_file );
         _cur_flat_file = flat_file;
      }

      LOG_EXIT();
   }

   void
   sed::_read_options( const options::dictionary& dict,
                       optional<const string&> prefix )
   {
      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      // // Extract database details.
      // _dbtype = sub.get<string>( "database_type" );
      // _dbname = sub.get<string>( "database_name" );
      // _dbhost = sub.get<string>( "database_host" );
      // _dbuser = sub.get<string>( "database_user" );
      // _dbpass = sub.get<string>( "database_pass" );
      // _db_connect( _sql, _dbtype, _dbname );

      // Extract the counts.
      _num_spectra = sub.get<unsigned>( "num_spectra" );
      _num_metals = sub.get<unsigned>( "num_metals" );
      LOGLN( "Number of times: ", _ages.size() );
      LOGLN( "Number of spectra: ", _num_spectra );
      LOGLN( "Number of metals: ", _num_metals );

      // Get the SSP filename.
      _read_ssp( sub.get<string>( "ssp_filename" ) );
   }

   void
   sed::_read_ssp( const string& filename )
   {
      LOG_ENTER();

      // The SSP file contains the age grid information first.
      std::ifstream file( filename, std::ios::in );
      unsigned num_ages;
      file >> num_ages;
      ASSERT( file.good() );
      _ages.reallocate( num_ages );
      _disk_age_masses.reallocate( num_ages );
      _bulge_age_masses.reallocate( num_ages );
      _disk_age_metals.reallocate( num_ages );
      _bulge_age_metals.reallocate( num_ages );
      for( unsigned ii = 0; ii < num_ages; ++ii )
      {
         file >> _ages[ii];
         ASSERT( file.good() );
      }

      // Must be ordered.
      std::sort( _ages.begin(), _ages.end() );

      // Take the dual.
      for( unsigned ii = 0; ii < _ages.size() - 1; ++ii )
         _ages[ii] = 0.5*(_ages[ii] + _ages[ii + 1]);
      _ages.resize( _ages.size() - 1 );

      // Allocate. Note that the ordering goes time,spectra,metals.
      _ssp.reallocate( _ages.size()*_num_spectra*_num_metals );
      LOGLN( "Reallocated SSP array to ", _ssp.size() );

      // Read in the file in one big go.
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
      h5::file file( filename, H5F_ACC_RDONLY );
      _flat_data.reallocate( file.read_data_size( "flat_trees" ) );
      file.read<flat_info<real_type>>( "flat_trees", _flat_mem_type, _flat_data );
   }
}
