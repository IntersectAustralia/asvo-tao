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
      tao::sed* sed = (tao::sed*)param;
      return 1.0/sqrt( sed->omega_k() +
                       sed->omega()/x +
                       sed->omega_r()/(x*x) +
                       sed->omega_lambda()*x*x );
   }

   // Factory function used to create a new SED.
   module*
   sed::factory( const string& name,
                 pugi::xml_node base )
   {
      return new sed( name, base );
   }

   sed::sed( const string& name,
             pugi::xml_node base )
      : module( name, base ),
        _cur_tree_id( -1 ),
        _omega( 0.25 ),
        _omega_lambda( 0.75 ),
        _hubble( 73.0 )
   {
      // Prepare the workspace for integrating and the
      // function.
      _work = gsl_integration_workspace_alloc( 1000 );
      _func.function = &calc_age_func;
      _func.params = this;

      // Setup some constants.
      _omega_r = 4.165e-5/((_hubble/100.0)*(_hubble/100.0));
      _omega_k = 1.0 - _omega - _omega_lambda - _omega_r;
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
      LOG_ENTER();

      module::initialise( global_dict );
      _read_options( global_dict );

      // Allocate for output spectra.
      _disk_spectra.reallocate( _num_spectra, _batch_size );
      _bulge_spectra.reallocate( _num_spectra, _batch_size );
      _total_spectra.reallocate( _num_spectra, _batch_size );

      LOG_EXIT();
   }

   ///
   /// Run the module.
   ///
   void
   sed::execute()
   {
      _timer.start();
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
      _timer.stop();
   }

   void
   sed::process_galaxy( const tao::galaxy& galaxy )
   {
      _timer.start();
      LOG_ENTER();

      // Process each galaxy.
      for( unsigned ii = 0; ii < galaxy.batch_size(); ++ii )
      {
         // Cache the galaxy ID.
         LOGDLN( "Processing galaxy with ID ", galaxy.values<long long>( "globalindex" )[ii] );

         // Do we need to load a fresh table?
         if( galaxy.values<long long>( "globaltreeid" )[ii] != _cur_tree_id )
            _load_table( galaxy.values<long long>( "globaltreeid" )[ii], galaxy.table() );

         // Read the star-formation histories for this galaxy.
         _rebin_info( galaxy, ii );

         // Clear disk and bulge output spectrums.
         std::fill( _total_spectra[ii].begin(), _total_spectra[ii].end(), 0.0 );
         std::fill( _bulge_spectra[ii].begin(), _bulge_spectra[ii].end(), 0.0 );

         // Process each time.
         for( mpi::lindex jj = 0; jj < _bin_ages.size(); ++jj )
            _process_time( jj, ii );

         // Create disk spectra.
         for( unsigned jj = 0; jj < _num_spectra; ++jj )
            _disk_spectra[ii][jj] = _total_spectra[ii][jj] - _bulge_spectra[ii][jj];

         LOGDLN( "Disk: ", _disk_spectra[ii] );
         LOGDLN( "Bulge: ", _bulge_spectra[ii] );
         LOGDLN( "Total: ", _total_spectra[ii] );
      }

      LOG_EXIT();
      _timer.stop();
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

   sed::real_type
   sed::omega() const
   {
      return _omega;
   }

   sed::real_type
   sed::omega_lambda() const
   {
      return _omega_lambda;
   }

   sed::real_type
   sed::omega_k() const
   {
      return _omega_k;
   }

   sed::real_type
   sed::omega_r() const
   {
      return _omega_r;
   }

   void
   sed::_process_time( mpi::lindex time_idx,
                       unsigned gal_idx )
   {
      LOG_ENTER();
      LOGDLN( "Processing time ", time_idx );

      _sum_spectra( time_idx, _age_metals[time_idx], _age_masses[time_idx], _total_spectra[gal_idx] );
      _sum_spectra( time_idx, _age_metals[time_idx], _bulge_age_masses[time_idx], _bulge_spectra[gal_idx] );

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
   sed::_rebin_info( const tao::galaxy& galaxy,
                     unsigned idx )
   {
      LOG_ENTER();

      // Clear out values.
      std::fill( _age_masses.begin(), _age_masses.end(), 0.0 );
      std::fill( _bulge_age_masses.begin(), _bulge_age_masses.end(), 0.0 );
      std::fill( _age_metals.begin(), _age_metals.end(), 0.0 );

      // Rebin everything from this galaxy.
      unsigned id = galaxy.values<int>( "localgalaxyid" )[idx];
      _rebin_recurse( id, _snap_ages[_snaps[id]] );

      LOG_EXIT();
   }

   void
   sed::_rebin_recurse( unsigned id,
                        real_type oldest_age )
   {
      LOGDLN( "Rebinning masses at galaxy: ", id, setindent( 2 ) );

      // Recurse parents, rebinning each of them.
      auto rng = _parents.equal_range( id );
      while( rng.first != rng.second )
      {
         unsigned par = (*rng.first++).second;
         _rebin_recurse( par, oldest_age );
      }

      // Calculate the age of material created at the beginning of
      // this timestep and at the end. Be careful! This age I speak
      // of is how old the material will be when we get to the
      // time of the final galaxy.
      ASSERT( _snaps[id] > 0, "Must have a previous snapshot." );
      real_type first_age = oldest_age - _snap_ages[_snaps[id] - 1];
      real_type last_age = oldest_age - _snap_ages[_snaps[id]];
      real_type age_size = first_age - last_age;
      LOGDLN( "Age range: [", first_age, "-", last_age, ")" );
      LOGDLN( "Age size: ", age_size );

      // // Recurse parents, summing their combined masses.
      // real_type mass = 0.0, bulge_mass = 0.0;
      // auto rng = _parents.equal_range( id );
      // while( rng.first != rng.second )
      // {
      //    unsigned par = (*rng.first++).second;
      //    auto ret_mass = _rebin_recurse( par, _snap_ages[_snaps[id]], oldest_age );
      //    mass += ret_mass.first;
      //    bulge_mass += ret_mass.second;
      // }
      // LOGDLN( "Parent mass: ", mass );
      // LOGDLN( "Parent bulge mass: ", bulge_mass );

      // Use the star formation rates to compute the new mass
      // produced. Bear in mind the rates we expect from the
      // database will be solar masses per year.
      real_type new_mass = _sfrs[id]*age_size*1e9;
      real_type new_bulge_mass = _bulge_sfrs[id]*age_size*1e9;
      LOGDLN( "New mass: ", new_mass );
      LOGDLN( "New bulge mass: ", new_bulge_mass );
      ASSERT( new_mass >= 0.0 && new_bulge_mass >= 0.0, "What does it mean to have lost mass?" );

      // Add the new mass to the appropriate bins. Find the first bin
      // that has overlap with this age range.
      unsigned first_bin = _find_bin( last_age );
      unsigned last_bin = _find_bin( first_age ) + 1;
      while( first_bin != last_bin )
      {
         // Find the fraction we will use to contribute to this
         // bin.
         real_type upp;
         if( first_bin < last_bin - 1 )
            upp = std::min( _dual_ages[first_bin], first_age );
         else
            upp = first_age;
         real_type frac = (upp - last_age)/age_size;
         LOGDLN( "Have sub-range: [", last_age, "-", upp, ")" );
         LOGDLN( "Updating bin ", first_bin, " with fraction of ", frac, "." );

         // Cache the current bin mass for later.
         real_type cur_bin_mass = _age_masses[first_bin];

         // Update the mass bins.
         LOGD( "Mass from ", _age_masses[first_bin], " to " );
         _age_masses[first_bin] += frac*new_mass;
         LOGDLN( _age_masses[first_bin], "." );
         LOGD( "Bulge mass from ", _bulge_age_masses[first_bin], " to " );
         _bulge_age_masses[first_bin] += frac*new_bulge_mass;
         LOGDLN( _bulge_age_masses[first_bin], "." );

         // Update the metal bins. This is impossible when no masses
	 // have been added to the bin at all.
	 if( _age_masses[first_bin] > 0.0 )
	 {
	    LOGD( "Metals from ", _age_metals[first_bin], " to " );
	    _age_metals[first_bin] =
	       (cur_bin_mass*_age_metals[first_bin] +
		frac*new_mass*(_metals[id]/_cold_gas[id]))/
	       _age_masses[first_bin];
	    LOGDLN( _age_metals[first_bin], "." );
	 }

         // Move to the next bin.
         if( first_bin < _dual_ages.size() )
            last_age = _dual_ages[first_bin];
         ++first_bin;
      }

      LOGD( setindent( -2 ) );
   }

   // void
   // sed::_rebin_parents( unsigned id,
   //                   unsigned root_id )
   // {
   //    LOG_ENTER();
   //    LOGDLN( "Rebinning the parents of ", id, "." );

   //    // Find the bin for the galaxy.
   //    real_type last_age = _snap_ages[_snaps[id]] - _snap_ages[_snaps[root_id]];
   //    unsigned last_bin = _find_bin( last_age );
   //    LOGDLN( "Oldest bin and age of ", id, " is ", last_bin, ", ", last_age, "." );

   //    // Get the range of parents.
   //    auto rng = _parents.equal_range( id );
   //    while( rng.first != rng.second )
   //    {
   //    // Cache the parent.
   //    unsigned par = (*rng.first++).second;
   //    LOGDLN( "Looking at parent ", par, "." );

   //    // Find the bin for this parent.
   //    real_type first_age = _snap_ages[_snaps[par]] - _snap_ages[_snaps[root_id]];
   //    unsigned first_bin = _find_bin( first_age );
   //    LOGDLN( "Newest bin and age of ", par, " is ", first_bin, ", ", first_age, "." );

   //    // Is this real time section contained entirely within
   //    // one bin?
   //    if( first_bin == last_bin )
   //    {
   //       LOGDLN( "Contained in one bin." );
   //       _update_bin( first_bin, par, first_age - last_age );
   //    }

   //    // Split across multiple bins.
   //    else
   //    {
   //       LOGDLN( "Spread over multiple bins." );

   //       // Start at last age.
   //       LOGDLN( "Section: ", last_age, ", ", _dual_ages[last_bin], "." );
   //       _update_bin( last_bin, par, _dual_ages[last_bin] - last_age );

   //       // Update any full intermediate bins.
   //       while( last_bin < first_bin - 1 )
   //       {
   //          LOGDLN( "Section: ", _dual_ages[last_bin], ", ", _dual_ages[last_bin + 1], "." );
   //          _update_bin( last_bin + 1, par, _dual_ages[last_bin + 1] - _dual_ages[last_bin] );
   //          ++last_bin;
   //       }

   //       // Update the last bin portion.
   //       LOGDLN( "Section: ", _dual_ages[first_bin - 1], ", ", first_age, "." );
   //       _update_bin( first_bin, par, first_age - _dual_ages[first_bin - 1] );
   //    }

   //    // Recursively process parents.
   //    _rebin_parents( par, root_id );
   //    }

   //    LOG_EXIT();
   // }

   // void
   // sed::_update_bin( unsigned bin,
   //                unsigned id,
   //                real_type dt )
   // {
   //    LOG_ENTER();
   //    LOGDLN( "Updating bin ", bin, " using timestep of ", dt, "." );

   //    // The numbers that come from SAGE at least, are stored in units
   //    // of 1e10*h. I need to multiply out by these units to get it
   //    // to natural units.
   //    real_type add_dm = (_sfrs[id] - _bulge_sfrs[id])*dt*1e10;
   //    real_type add_bm = _bulge_sfrs[id]*dt*1e10;
   //    real_type new_dm = _age_masses[bin] + add_dm;
   //    real_type new_bm = _bulge_age_masses[bin] + add_bm;
   //    if( new_dm > 0.0 )
   //    {
   //    _age_metals[bin] = (_age_masses[bin]*_age_metals[bin] +
   //                                add_dm*_metals[id])/new_dm;
   //    }
   //    if( new_bm > 0.0 )
   //    {
   //    _bulge_age_metals[bin] = (_bulge_age_masses[bin]*_bulge_age_metals[bin] +
   //                                 add_bm*_metals[id])/new_bm;
   //    }
   //    _age_masses[bin] = new_dm;
   //    _bulge_age_masses[bin] = new_bm;
   //    LOGDLN( "Added ", add_dm, " disk mass." );
   //    LOGDLN( "Added ", add_bm, " bulge mass." );
   //    LOGDLN( "New disk mass: ", _age_masses[bin] );
   //    LOGDLN( "New bulge mass: ", _bulge_age_masses[bin] );
   //    LOGDLN( "New disk metallicity: ", _age_metals[bin] );
   //    LOGDLN( "New bulge metallicity: ", _bulge_age_metals[bin] );

   //    LOG_EXIT();
   // }

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
   sed::_calc_age( real_type redshift )
   {
      LOG_ENTER();
      double res, abserr;
      double upp = 1.0/(1.0 + redshift);
      gsl_integration_qag( &_func, 0.0, upp, 1e-5, 1e-8,
                           1000, GSL_INTEG_GAUSS21, _work, &res, &abserr );
      res *= (977.8/_hubble); // convert to Gyrs
      LOGDLN( "Calculated age as ", res, " Gyrs." );
      LOG_EXIT();
      return res;
   }

   void
   sed::_read_options( const options::xml_dict& global_dict )
   {
      // Extract database details and connect.
      _read_db_options( global_dict );
      _db_connect();

      // Try to read H0 (and hence h) from the lightcone module.
      _hubble = global_dict.get<real_type>( "workflow:light-cone:H0", 73.0 );
      LOGDLN( "Read Hubble constant as: ", _hubble );

      // Extract the counts.
      _num_spectra = _dict.get<unsigned>( "num-spectra",1221 );
      _num_metals = _dict.get<unsigned>( "num-metals",7 );
      LOGDLN( "Number of times: ", _bin_ages.size() );
      LOGDLN( "Number of spectra: ", _num_spectra );
      LOGDLN( "Number of metals: ", _num_metals );

      // Get the SSP filename.
      _read_ssp( _dict.get<string>( "single-stellar-population-model" ) );

      // Prepare the snapshot ages.
      _setup_snap_ages();
   }

   void
   sed::_read_ssp( const string& filename )
   {
      LOG_ENTER();
      LOGDLN( "SSP File Name: ", filename );
      // The SSP file contains the age grid information first.
      std::ifstream file( filename, std::ios::in );
      unsigned num_ages;
      file >> num_ages;
      ASSERT( file.good() );
      _bin_ages.reallocate( num_ages );
      _age_masses.reallocate( num_ages );
      _bulge_age_masses.reallocate( num_ages );
      _age_metals.reallocate( num_ages );
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
      _timer.start();
      LOG_ENTER();

      // Find number of snapshots and resize the containers.
      unsigned num_snaps;
      _db_timer.start();
#ifdef MULTIDB
      (*_db)["tree_1"] << "SELECT COUNT(*) FROM snap_redshift", soci::into( num_snaps );
#else
      _sql << "SELECT COUNT(*) FROM snap_redshift", soci::into( num_snaps );
#endif
      _db_timer.stop();
      LOGDLN( num_snaps, " snapshots." );
      _snap_ages.reallocate( num_snaps );

      // Read meta data.
      _db_timer.start();
#ifdef MULTIDB
      (*_db)["tree_1"] << "SELECT redshift FROM snap_redshift ORDER BY snapnum",
         soci::into( (std::vector<real_type>&)_snap_ages );
#else
      _sql << "SELECT redshift FROM snap_redshift ORDER BY snapnum",
         soci::into( (std::vector<real_type>&)_snap_ages );
#endif
      _db_timer.stop();
      LOGDLN( "Redshifts: ", _snap_ages );

      // Convert to ages.
      for( unsigned ii = 0; ii < _snap_ages.size(); ++ii )
         _snap_ages[ii] = _calc_age( _snap_ages[ii] );
      LOGDLN( "Snapshot ages: ", _snap_ages );

      LOG_EXIT();
      _timer.stop();
   }

   void
   sed::_load_table( long long tree_id,
                     const string& table )
   {
      _timer.start();
      LOG_ENTER();
      LOGDLN( "Loading table ", table, " and tree ID ", tree_id );

      // Clear away any existing data.
      _descs.deallocate();
      _sfrs.deallocate();
      _bulge_sfrs.deallocate();
      _cold_gas.deallocate();
      _metals.deallocate();
      _snaps.deallocate();
      _parents.clear();

      // Extract number of records in this tree.
      unsigned tree_size;
      _db_timer.start();
#ifdef MULTIDB
      (*_db)[table] << "SELECT COUNT(*) FROM " + table + " WHERE globaltreeid = :id",
         soci::into( tree_size ), soci::use( tree_id );
#else
      _sql << "SELECT COUNT(*) FROM " + table + " WHERE globaltreeid = :id",
         soci::into( tree_size ), soci::use( tree_id );
#endif
      _db_timer.stop();
      LOGDLN( "Have ", tree_size, " galaxies to load." );

      // Resize all our arrays.
      _descs.resize( tree_size );
      _sfrs.resize( tree_size );
      _bulge_sfrs.resize( tree_size );
      _cold_gas.resize( tree_size );
      _metals.resize( tree_size );
      _snaps.resize( tree_size );

      // Extract the table.
      string query = "SELECT descendant, metalscoldgas, coldgas, "
        "sfr, sfrbulge, snapnum FROM  " + table +
         " WHERE globaltreeid = :id"
         " ORDER BY localgalaxyid";
      _db_timer.start();
#ifdef MULTIDB
      (*_db)[table] << query, soci::into( (std::vector<int>&)_descs ),
         soci::into( (std::vector<double>&)_metals ), soci::into( (std::vector<double>&)_cold_gas ),
         soci::into( (std::vector<double>&)_sfrs ), soci::into( (std::vector<double>&)_bulge_sfrs ),
         soci::into( (std::vector<int>&)_snaps ),
         soci::use( tree_id );
#else
      _sql << query, soci::into( (std::vector<int>&)_descs ),
         soci::into( (std::vector<double>&)_metals ), soci::into( (std::vector<double>&)_cold_gas ),
         soci::into( (std::vector<double>&)_sfrs ), soci::into( (std::vector<double>&)_bulge_sfrs ),
         soci::into( (std::vector<int>&)_snaps ),
         soci::use( tree_id );
#endif
      _db_timer.stop();
      LOGDLN( "Descendant: ", _descs );
      LOGDLN( "Star formation rates: ", _sfrs );
      LOGDLN( "Bulge star formation rates: ", _bulge_sfrs );
      LOGDLN( "Metals cold gas: ", _metals );
      LOGDLN( "Cold gas: ", _cold_gas );
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
      _timer.stop();
   }
}
