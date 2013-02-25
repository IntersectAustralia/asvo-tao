#include <fstream>
#include <boost/algorithm/string/trim.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/tokenizer.hpp>
#include "sed.hh"

using namespace hpc;
using boost::format;
using boost::str;

namespace tao {

   double
   calc_age_func( double x,
		  void* param )
   {
      // return 1.0/sqrt( omega/x + (1.0 - omega - omega_lambda) + omega_lambda*x*x );
      return 1.0/sqrt( 0.25/x + (1.0 - 0.25 - 0.75) + 0.75*x*x );
   }

   // Factory function used to create a new SED.
   module*
   sed::factory( const string& name )
   {
      return new sed( name );
   }

   sed::sed( const string& name )
      : module( name ),
        _cur_tree_id( -1 ),
	_omega( 0.25 ),
	_omega_lambda( 0.75 ),
	_h( 0.73 )
   {
      // Prepare the workspace for integrating and the
      // function.
      _work = gsl_integration_workspace_alloc( 1000 );
      _func.function = &calc_age_func;
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
      dict.add_option( new options::string( "single-stellar-population-model" ), prefix );
      dict.add_option( new options::integer( "num-spectra", 1221 ), prefix );
      dict.add_option( new options::integer( "num-metals", 7 ), prefix );
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
   /// Run the module.
   ///
   void
   sed::execute()
   {
      LOG_ENTER();
      ASSERT( parents().size() == 1 );

      // Grab the galaxy from the parent object.
      tao::galaxy& gal = parents().front()->galaxy();

      // Perform the processing.
      process_galaxy( gal );

      // Add spectra to the galaxy object.
      gal.set_vector_field<real_type>( "disk_spectra", _disk_spectra );
      gal.set_vector_field<real_type>( "bulge_spectra", _bulge_spectra );
      gal.set_vector_field<real_type>( "total_spectra", _total_spectra );

      LOG_EXIT();
   }

   void
   sed::process_galaxy( const tao::galaxy& galaxy )
   {
      LOG_ENTER();

      // Cache the galaxy ID.
      unsigned gal_id = galaxy.id();
      LOGDLN( "Processing galaxy with ID ", gal_id );

      // Do we need to load a fresh table?
      if( galaxy.tree_id() != _cur_tree_id )
	 _load_table( galaxy.tree_id(), galaxy.table() );

      // Read the star-formation histories for this galaxy.
      _rebin_info( galaxy );

      // Clear disk and bulge output spectrums.
      std::fill( _disk_spectra.begin(), _disk_spectra.end(), 0.0 );
      std::fill( _bulge_spectra.begin(), _bulge_spectra.end(), 0.0 );

      // Process each time.
      for( mpi::lindex ii = 0; ii < _bin_ages.size(); ++ii )
         _process_time( ii );

      // Create total spectra.
      for( unsigned ii = 0; ii < _num_spectra; ++ii )
         _total_spectra[ii] = _disk_spectra[ii] + _bulge_spectra[ii];

      LOGDLN( "Disk: ", _disk_spectra );
      LOGDLN( "Bulge: ", _bulge_spectra );
      LOGDLN( "Total: ", _total_spectra );
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
      LOGDLN( "Processing time ", time_idx );

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

      LOG_EXIT();
   }

   void
   sed::_rebin_parents( unsigned id,
			unsigned root_id )
   {
      LOG_ENTER();
      LOGDLN( "Rebinning the parents of ", id, "." );

      // Find the bin for the galaxy.
      real_type last_age = _snap_ages[_snaps[id]] - _snap_ages[_snaps[root_id]];
      unsigned last_bin = _find_bin( last_age );
      LOGDLN( "Oldest bin and age of ", id, " is ", last_bin, ", ", last_age, "." );

      // Get the range of parents.
      auto rng = _parents.equal_range( id );
      while( rng.first != rng.second )
      {
   	 // Cache the parent.
   	 unsigned par = (*rng.first++).second;
	 LOGDLN( "Looking at parent ", par, "." );

	 // Find the bin for this parent.
	 real_type first_age = _snap_ages[_snaps[par]] - _snap_ages[_snaps[root_id]];
	 unsigned first_bin = _find_bin( first_age );
	 LOGDLN( "Newest bin and age of ", par, " is ", first_bin, ", ", first_age, "." );

	 // Is this real time section contained entirely within
	 // one bin?
	 if( first_bin == last_bin )
	 {
	    LOGDLN( "Contained in one bin." );
	    _update_bin( first_bin, par, first_age - last_age );
	 }

	 // Split across multiple bins.
	 else
	 {
	    LOGDLN( "Spread over multiple bins." );

	    // Start at last age.
	    LOGDLN( "Section: ", last_age, ", ", _dual_ages[last_bin], "." );
	    _update_bin( last_bin, par, _dual_ages[last_bin] - last_age );

	    // Update any full intermediate bins.
	    while( last_bin < first_bin - 1 )
	    {
	       LOGDLN( "Section: ", _dual_ages[last_bin], ", ", _dual_ages[last_bin + 1], "." );
	       _update_bin( last_bin + 1, par, _dual_ages[last_bin + 1] - _dual_ages[last_bin] );
	       ++last_bin;
	    }

	    // Update the last bin portion.
	    LOGDLN( "Section: ", _dual_ages[first_bin - 1], ", ", first_age, "." );
	    _update_bin( first_bin, par, first_age - _dual_ages[first_bin - 1] );
	 }

	 // Recursively process parents.
	 _rebin_parents( par, root_id );
      }

      LOG_EXIT();
   }

   void
   sed::_update_bin( unsigned bin,
		     unsigned id,
		     real_type dt )
   {
      LOG_ENTER();
      LOGDLN( "Updating bin ", bin, " using timestep of ", dt, "." );

      real_type add_dm = (_sfrs[id] - _bulge_sfrs[id])*dt*_h;
      real_type add_bm = _bulge_sfrs[id]*dt*_h;
      real_type new_dm = _disk_age_masses[bin] + add_dm;
      real_type new_bm = _bulge_age_masses[bin] + add_bm;
      if( new_dm > 0.0 )
      {
	 _disk_age_metals[bin] = (_disk_age_masses[bin]*_disk_age_metals[bin] + 
                                  add_dm*_metals[id])/new_dm;
      }
      if( new_bm > 0.0 )
      {
	 _bulge_age_metals[bin] = (_bulge_age_masses[bin]*_bulge_age_metals[bin] + 
                                   add_bm*_metals[id])/new_bm;
      }
      _disk_age_masses[bin] = new_dm;
      _bulge_age_masses[bin] = new_bm;
      LOGDLN( "Added ", add_dm, " disk mass." );
      LOGDLN( "Added ", add_bm, " bulge mass." );
      LOGDLN( "New disk mass: ", _disk_age_masses[bin] );
      LOGDLN( "New bulge mass: ", _bulge_age_masses[bin] );
      LOGDLN( "New disk metallicity: ", _disk_age_metals[bin] );
      LOGDLN( "New bulge metallicity: ", _bulge_age_metals[bin] );

      LOG_EXIT();
   }

   unsigned
   sed::_find_bin( real_type age )
   {
      LOG_ENTER();

      // Which bin should this parent belong in?
      unsigned bin;
      {
	 auto it = std::lower_bound( _dual_ages.begin(), _dual_ages.end(), age );
	 if( it == _dual_ages.end() )
	    bin = _dual_ages.size();
	 else
	    bin = it - _dual_ages.begin();
      }
      LOGDLN( "Found bin ", bin, " with age of ", _bin_ages[bin], "." );

      LOG_EXIT();
      return bin;
   }

   sed::real_type
   sed::_calc_age( real_type z0,
		   real_type z1 )
   {
      LOG_ENTER();
      real_type z = z1 - z0;
      real_type res, abserr;
      gsl_integration_qag( &_func, 1.0/(z + 1.0), 1.0, 1.0/_h, 1e-8,
			   1000, GSL_INTEG_GAUSS21, _work, &res, &abserr );
      res = (1.0/_h)*res;
      LOGDLN( "Calculated age as ", res, "." );
      LOG_EXIT();
      return res;
   }

   void
   sed::_read_options( const options::dictionary& dict,
                       optional<const string&> prefix )
   {
      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      // Extract database details.
      _read_db_options( dict );

      // Connect to the database.
      _db_connect();

      // Try to read H0 (and hence h) from the lightcone module.
      _h = dict.get<real_type>( "workflow:light-cone:H0" )/100.0;
      LOGDLN( "Read h as: ", _h );

      // Extract the counts.
      _num_spectra = sub.get<unsigned>( "num-spectra" );
      _num_metals = sub.get<unsigned>( "num-metals" );
      LOGDLN( "Number of times: ", _bin_ages.size() );
      LOGDLN( "Number of spectra: ", _num_spectra );
      LOGDLN( "Number of metals: ", _num_metals );

      // Get the SSP filename.
      _read_ssp( sub.get<string>( "single-stellar-population-model" ) );

      // Prepare the snapshot ages.
      _setup_snap_ages();
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
      _bin_ages.reallocate( num_ages );
      _disk_age_masses.reallocate( num_ages );
      _bulge_age_masses.reallocate( num_ages );
      _disk_age_metals.reallocate( num_ages );
      _bulge_age_metals.reallocate( num_ages );
      for( unsigned ii = 0; ii < num_ages; ++ii )
      {
         file >> _bin_ages[ii];
         ASSERT( file.good() );
      }

#ifndef NDEBUG
      // Must be ordered.
      for( unsigned ii = 1; ii < _bin_ages.size(); ++ii )
	 ASSERT( _bin_ages[ii] >= _bin_ages[ii - 1] );
#endif
      LOGDLN( "Bin ages: ", _bin_ages );

      // Take the dual to form age bins.
      _dual_ages.reallocate( _bin_ages.size() - 1 );
      for( unsigned ii = 0; ii < _bin_ages.size() - 1; ++ii )
         _dual_ages[ii] = 0.5*(_bin_ages[ii] + _bin_ages[ii + 1]);
      LOGDLN( "Dual bin ages: ", _dual_ages );

      // Allocate. Note that the ordering goes time,spectra,metals.
      _ssp.reallocate( _bin_ages.size()*_num_spectra*_num_metals );
      LOGDLN( "Reallocated SSP array to ", _ssp.size() );

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
   sed::_setup_snap_ages()
   {
      LOG_ENTER();

      // Find number of snapshots and resize the containers.
      unsigned num_snaps;
      _sql << "SELECT COUNT(*) FROM snap_redshift", soci::into( num_snaps );
      LOGDLN( num_snaps, " snapshots." );
      _snap_ages.reallocate( num_snaps );

      // Read meta data.
      _sql << "SELECT redshift FROM snap_redshift ORDER BY snapnum",
         soci::into( (std::vector<real_type>&)_snap_ages );
      LOGDLN( "Redshifts: ", _snap_ages );

      // Convert to ages.
      for( unsigned ii = 0; ii < _snap_ages.size(); ++ii )
	 _snap_ages[ii] = _calc_age( 0.0, _snap_ages[ii] );
      LOGDLN( "Snapshot ages: ", _snap_ages );

      LOG_EXIT();
   }

   void
   sed::_load_table( long long tree_id,
		     const string& table )
   {
      LOG_ENTER();
      LOGDLN( "Loading table ", table, " and tree ID ", tree_id );

      // Clear away any existing data.
      _descs.deallocate();
      _sfrs.deallocate();
      _bulge_sfrs.deallocate();
      _metals.deallocate();
      _snaps.deallocate();
      _parents.clear();

      // Extract number of records in this tree.
      unsigned tree_size;
      _sql << "SELECT COUNT(*) FROM " + table + " WHERE globaltreeid = :id",
   	 soci::into( tree_size ), soci::use( tree_id );
      LOGDLN( "Have ", tree_size, " galaxies to load." );

      // Resize all our arrays.
      _descs.resize( tree_size );
      _sfrs.resize( tree_size );
      _bulge_sfrs.resize( tree_size );
      _metals.resize( tree_size );
      _snaps.resize( tree_size );

      // Extract the table.
      string query = "SELECT descendant, metalscoldgas, "
	"sfr, sfrbulge, snapnum FROM  " + table + 
	 " WHERE globaltreeid = :id"
	 " ORDER BY localgalaxyid";
      _sql << query, soci::into( (std::vector<int>&)_descs ),
	 soci::into( (std::vector<double>&)_metals ),
	 soci::into( (std::vector<double>&)_sfrs ), soci::into( (std::vector<double>&)_bulge_sfrs ),
	 soci::into( (std::vector<int>&)_snaps ),
	 soci::use( tree_id );
      LOGDLN( "Descendant: ", _descs );
      LOGDLN( "Star formation rates: ", _sfrs );
      LOGDLN( "Bulge star formation rates: ", _bulge_sfrs );
      LOGDLN( "Metals: ", _metals );
      LOGDLN( "Snapshots: ", _snaps );

      // Build the parents for each galaxy.
      for( unsigned ii = 0; ii < _descs.size(); ++ii )
      {
	 if( _descs[ii] != -1 )
	    _parents.insert( _descs[ii], ii );
      }
      LOGDLN( "Parents table for tree: ", _parents );

      // Set the current table.
      _cur_tree_id = tree_id;

      LOG_EXIT();
   }
}
