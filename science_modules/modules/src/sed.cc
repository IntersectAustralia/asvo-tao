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
      dict.add_option( new options::string( "database_port", string() ), prefix );
      dict.add_option( new options::string( "database_user", string() ), prefix );
      dict.add_option( new options::string( "database_pass", string() ), prefix );
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
      _rebin_info( galaxy );

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
   sed::_rebin_info( const tao::galaxy& galaxy )
   {
      LOG_ENTER();

      // Clear out values.
      std::fill( _disk_age_masses.begin(), _disk_age_masses.end(), 0.0 );
      std::fill( _bulge_age_masses.begin(), _bulge_age_masses.end(), 0.0 );
      std::fill( _disk_age_metals.begin(), _disk_age_metals.end(), 0.0 );
      std::fill( _bulge_age_metals.begin(), _bulge_age_metals.end(), 0.0 );

      // Rebin everything from this galaxy.
      unsigned id = galaxy.local_id();
      _rebin_parents( id, id );
   }

   void
   sed::_rebin_parents( unsigned id,
			unsigned root_id )
   {
      // Find the bin for the galaxy.
      unsigned last_bin = _find_bin( id );
      real_type last_age = _calc_age( id, root_id );

      // Get the range of parents.
      auto rng = _parents.equal_range( id );
      while( rng.first != rng.second )
      {
   	 // Cache the parent.
   	 unsigned par = (*rng.first++).second;

	 // Find the bin for this parent.
	 unsigned first_bin = _find_bin( par );
	 real_type first_age = _calc_age( par, root_id );

	 // Is this real time section contained entirely within
	 // one bin?
	 if( first_bin == last_bin )
	 {
	    _update_bin( first_bin, par, last_age - first_age );
	 }

	 // Split across multiple bins.
	 else
	 {
	    // Update the first bin portion.
	    _update_bin( first_bin, par, _dual_ages[first_bin + 1] - first_age );

	    // Update any full intermediate bins.
	    while( ++first_bin < last_bin )
	       _update_bin( first_bin, par, _dual_ages[first_bin + 1] - _dual_ages[first_bin] );

	    // Update the last bin portion.
	    _update_bin( last_bin, par, _dual_ages[last_bin] - last_age );
	 }

	 // Recursively process parents.
	 _rebin_parents( par, root_id );
      }
   }

   void
   sed::_update_bin( unsigned bin,
		     unsigned id,
		     real_type dt )
   {
      real_type add_dm = (_sfrs[id] - _bulge_sfrs[id])*dt;
      real_type add_bm = _bulge_sfrs[id]*dt;
      real_type new_dm = _disk_age_masses[bin] + add_dm;
      real_type new_bm = _bulge_age_masses[bin] + add_bm;
      _disk_age_metals[bin] = (_disk_age_masses[bin]*_disk_age_metals[bin] + add_dm*(_metals[id] - _bulge_metals[id]))/new_dm;
      _bulge_age_metals[bin] = (_bulge_age_masses[bin]*_bulge_age_metals[bin] + add_bm*_bulge_metals[id])/new_bm;
      _disk_age_masses[bin] = new_dm;
      _bulge_age_masses[bin] = new_bm;
   }

   unsigned
   sed::_find_bin( unsigned parent )
   {
      // Which bin should this parent belong in?
      real_type redshift = _redshifts[parent];
      unsigned bin;
      {
	 auto it = std::lower_bound( _ages.begin(), _ages.end(), redshift );
	 ASSERT( it != _ages.end() );
	 bin = it - _ages.begin();
      }
      return bin;
   }

   sed::real_type
   sed::_calc_age( unsigned id,
		   unsigned root_id )
   {
      return 0.0;
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
      _dbport = sub.get<string>( "database_port" );
      _dbuser = sub.get<string>( "database_user" );
      _dbpass = sub.get<string>( "database_pass" );
      _db_connect( _sql );

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

      // Take the dual to form age bins.
      _dual_ages.reallocate( _ages.size() - 1 );
      for( unsigned ii = 0; ii < _ages.size() - 1; ++ii )
         _ages[ii] = 0.5*(_ages[ii] + _ages[ii + 1]);

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
   sed::_load_table( const string& table )
   {
      // Clear away any existing data.
      _descs.deallocate();
      _sfrs.deallocate();
      _bulge_sfrs.deallocate();
      _metals.deallocate();
      _bulge_metals.deallocate();
      _redshifts.deallocate();
      _parents.clear();

      // First need to pull the table's tree id.
      long long tree_id;
      _sql << "SELECT globaltreeid FROM " + table, soci::into( tree_id );

      // Extract number of records in this tree.
      unsigned tree_size;
      _sql << "SELECT galaxycount FROM treesummary WHERE globaltreeid = :id",
   	 soci::into( tree_size ), soci::use( tree_id );

      // Resize all our arrays.
      _descs.resize( tree_size );
      _sfrs.resize( tree_size );
      _bulge_sfrs.resize( tree_size );
      _metals.resize( tree_size );
      _bulge_metals.resize( tree_size );
      _redshifts.resize( tree_size );

      // Extract the table.
      string query = "SELECT globalindex, descendant, stellarmass, bulgemass, sfr, sfrbulge, "
	 "metalsstellarmass, metalsbulgemass, redshift"
   	 " INNER JOIN snap_redshift ON (" + table + ".snapnum = snap_redshift.snapnum)";
      _sql << query, soci::into( (std::vector<int>&)_descs ),
   	 soci::into( (std::vector<double>&)_sfrs ), soci::into( (std::vector<double>&)_bulge_sfrs ),
	 soci::into( (std::vector<double>&)_metals ), soci::into( (std::vector<double>&)_bulge_metals ),
	 soci::into( (std::vector<double>&)_redshifts );

      // Build the parents for each galaxy.
      for( unsigned ii = 0; ii < _descs.size(); ++ii )
   	 _parents.insert( _descs[ii], ii );
   }
}
