#ifndef tao_base_sfh_hh
#define tao_base_sfh_hh

#include <unordered_set>
#include <unordered_map>
#include <map>
#include <vector>
#include <boost/algorithm/string/trim.hpp>
#include <boost/lexical_cast.hpp>
#include <libhpc/system/deallocate.hh>
#include "age_line.hh"
#include "stellar_population.hh"

namespace tao {
   using boost::format;
   using boost::str;

   ///
   /// Star-formation History. Responsible for rebinning star-formation
   /// history data into appropriate time bins.
   ///
   template< class T >
   class sfh
   {
   public:

      typedef T real_type;

   public:

      sfh()
         : _snap_ages( NULL ),
           _bin_ages( NULL ),
           _cur_tree_id( std::numeric_limits<unsigned long long>::max() )
      {
      }

      sfh( age_line<real_type> const* snap_ages,
	   age_line<real_type> const* bin_ages,
	   fs::path const& path )
      {
	 set_snapshot_ages( snap_ages );
	 set_bin_ages( bin_ages );
	 load( path );
      }

      void
      clear_tree_data()
      {
         hpc::deallocate( _descs );
         hpc::deallocate( _snaps );
	 hpc::deallocate( _descs );
	 hpc::deallocate( _lids );
         hpc::deallocate( _disk_sfrs );
         hpc::deallocate( _bulge_sfrs );
         hpc::deallocate( _cold_gas );
         hpc::deallocate( _masses );
         hpc::deallocate( _metals );
      }

      void
      set_snapshot_ages( const age_line<real_type>* snap_ages )
      {
         _snap_ages = snap_ages;
      }

      age_line<real_type> const*
      snapshot_ages() const
      {
         return _snap_ages;
      }

      void
      set_bin_ages( const age_line<real_type>* bin_ages )
      {
         _bin_ages = bin_ages;
      }

      age_line<real_type> const*
      bin_ages() const
      {
         return _bin_ages;
      }

      void
      load( fs::path const& path )
      {
	 LOGBLOCKI( "Loading merger tree from: ", path );

	 // Open the file.
	 std::ifstream file( path.c_str() );
	 EXCEPT( file.is_open(), "Couldn't find merger tree file: ", path );

	 // First element is the number of galaxies.
	 unsigned num_gals;
	 file >> num_gals;

	 // Read snapshot array.
	 _snaps.resize( num_gals );
	 for( unsigned ii = 0; ii < num_gals; ++ii )
	    file >> _snaps[ii];

	 // Read SFR array.
	 _disk_sfrs.resize( num_gals );
	 for( unsigned ii = 0; ii < num_gals; ++ii )
	    file >> _disk_sfrs[ii];

	 // Read bulge SFR array.
	 _bulge_sfrs.resize( num_gals );
	 for( unsigned ii = 0; ii < num_gals; ++ii )
	    file >> _bulge_sfrs[ii];

	 // Read metallicity array.
	 _metals.resize( num_gals );
	 for( unsigned ii = 0; ii < num_gals; ++ii )
	    file >> _metals[ii];

	 // Read cold gas array.
	 _cold_gas.resize( num_gals );
	 for( unsigned ii = 0; ii < num_gals; ++ii )
	    file >> _cold_gas[ii];

	 // The oldest snapshot is the first one in the list.
	 _old_snap = _snaps[0];

	 EXCEPT( file.good(), "Error reading merger tree file." );
      }

      void
      load_tree_data( soci::session& sql,
                      std::string const& table_name,
		      unsigned long long tree_id,
                      unsigned long long global_index )
      {
	 LOGBLOCKD( "Loading tree data from table ", table_name, " for tree with index ", tree_id, " rooted at galaxy with global index ", global_index );

	 // Clear away any existing tree data.
	 clear_tree_data();

	 // Load the basic object information.
	 unsigned long long dfo, subsize;
	 sql << "SELECT depthfirst_traversalorder, subtree_count, snapnum FROM " + table_name + " WHERE globalindex=:gid",
	    soci::into( dfo ), soci::into( subsize ), soci::into( _old_snap ),
	    soci::use( global_index );

	 // Resize data arrays.
	 _disk_sfrs.resize( subsize );
	 _bulge_sfrs.resize( subsize );
	 _cold_gas.resize( subsize );
	 _masses.resize( subsize );
	 _metals.resize( subsize );
	 _snaps.resize( subsize );
	 _descs.resize( subsize );
	 _lids.resize( subsize );
         _inv_lids.clear();

	 // Extract the sub tree.
	 int dfo_first = dfo;
	 int dfo_last = dfo + subsize;
	 std::string query = "SELECT sfrdiskz, sfrbulgez, "
	    "sfrdisk, sfrbulge, snapnum, descendant, localgalaxyid, stellarmass FROM " + table_name +
	    " WHERE globaltreeid = :treeid"
	    " AND depthfirst_traversalorder >= :first AND depthfirst_traversalorder < :last";
         sql << query,
            soci::into( _disk_sfr_z ), soci::into( _bulge_sfr_z ),
            soci::into( _disk_sfrs ), soci::into( _bulge_sfrs ),
            soci::into( _snaps ), soci::into( _descs ),
            soci::into( _lids ), soci::into( _masses ),
            soci::use( tree_id ), soci::use( dfo_first ), soci::use( dfo_last );

         // Build inverse mapping, from local ids to indices.
         for( unsigned ii = 0; ii < _lids.size(); ++ii )
            _inv_lids.emplace( _lids[ii], ii );

#ifndef NDEBUG
	 // Do a check to confirm the tree has been loaded correctly.
	 // Look for any galaxy that has a descendant not in the set.
	 {
	    std::vector<int> descs( subsize + 10 ); // add ten to check size is right
	    std::vector<int> local_ids( subsize + 10 ), global_idxs( subsize + 10 );
	    sql << "SELECT descendant, localgalaxyid, globalindex FROM " + table_name + " WHERE globaltreeid = :treeid"
	       " AND depthfirst_traversalorder >= :first AND depthfirst_traversalorder < :last",
	       soci::into( descs ), soci::into( local_ids ), soci::into( global_idxs ),
	       soci::use( tree_id ), soci::use( dfo_first ), soci::use( dfo_last );
	    ASSERT( descs.size() == subsize, "Subtree size in database is wrong." );

	    // Need a fast lookup for local IDs.
	    std::unordered_set<int> local_lookup( local_ids.begin(), local_ids.end() );

	    // Check all descendants match except for the root.
	    unsigned num_roots = 0;
	    for( unsigned ii = 0; ii < descs.size(); ++ii )
	    {
	       if( descs[ii] != -1 && global_idxs[ii] != global_index )
	       {
		  ASSERT( local_lookup.count( descs[ii] ),
			  "Depth first ordering is not returning correct subtree." );
	       }
	       else
		  ++num_roots;
	    }
	    ASSERT( num_roots == 1, "Found multiple roots to subtree." );
	 }
#endif

	 // Set the current table/tree information.
	 _cur_table = table_name;
	 _cur_tree_id = tree_id;
	 _cur_gid = global_index;

	 // Calculate parent maps.
	 _calc_parents();
      }

      template< class DiskVec,
		class BulgeVec >
      void
      rebin( typename hpc::type_traits<DiskVec>::reference disk_age_masses,
             typename hpc::type_traits<BulgeVec>::reference bulge_age_masses,
             stellar_population const& ssp )
      {
         rebin_thibault<DiskVec,BulgeVec>( disk_age_masses, bulge_age_masses, ssp );
      }

      template< class DiskVec,
		class BulgeVec >
      void
      rebin_thibault( typename hpc::type_traits<DiskVec>::reference disk_age_masses,
		      typename hpc::type_traits<BulgeVec>::reference bulge_age_masses,
                      stellar_population const& ssp )

      {
         // Must have ages available.
         ASSERT( _snap_ages, "Snapshot ages have not been set." );
         ASSERT( _bin_ages, "Bin ages have not been set." );

         // Array sizes must match the number of bins.
         ASSERT( _bin_ages->size()*ssp.num_metal_bins() == disk_age_masses.size() &&
                 _bin_ages->size()*ssp.num_metal_bins() == bulge_age_masses.size(),
                 "Rebinning arrays must have the same size as the age bins." );

         // Clear out values.
         std::fill( disk_age_masses.begin(), disk_age_masses.end(), 0.0 );
         std::fill( bulge_age_masses.begin(), bulge_age_masses.end(), 0.0 );

         _rebin_linear_thibault<DiskVec,BulgeVec>( (*_snap_ages)[_old_snap], disk_age_masses, bulge_age_masses, ssp );
      }

      // template< class U >
      // void
      // rebin_chiara( typename vector<U>::view age_masses,
      //               typename vector<U>::view bulge_age_masses,
      //               typename vector<U>::view age_metals )

      // {
      //    // LOGBLOCKD( "Rebinning galaxy with local ID ", galaxy_id, " in tree with ID ", _cur_tree_id, " in table ", _cur_table, "." );

      //    // Must have ages available.
      //    ASSERT( _snap_ages, "Snapshot ages have not been set." );
      //    ASSERT( _bin_ages, "Bin ages have not been set." );

      //    // Array sizes must match the number of bins.
      //    ASSERT( _bin_ages->size() == age_masses.size() &&
      //            _bin_ages->size() == bulge_age_masses.size() &&
      //            _bin_ages->size() == age_metals.size(),
      //            "Rebinning arrays must have the same size as the age bins." );

      //    // Clear out values.
      //    std::fill( age_masses.begin(), age_masses.end(), 0.0 );
      //    std::fill( bulge_age_masses.begin(), bulge_age_masses.end(), 0.0 );
      //    std::fill( age_metals.begin(), age_metals.end(), 0.0 );

      //    // // Rebin everything from this galaxy. Check if we are supposed to
      //    // // be using a cumulative method.
      // 	 // if( _accum )
      // 	 // {
      // 	 //    ASSERT( 0 );
      // 	 //    // // Process each chunk.
      // 	 //    // while( _load_chunk() )
      // 	 //    //    _rebin_linear<U>( (*_snap_ages)[snap], age_masses, bulge_age_masses, age_metals );
      // 	 // }
      // 	 // else
      // 	 // {
      // 	    _rebin_linear_chiara<U>( (*_snap_ages)[_old_snap], age_masses, bulge_age_masses, age_metals );
      // 	    // _rebin_reurse<U>( sql, galaxy_id, _sfrs[galaxy_id], _bulge_sfrs[galaxy_id], _cold_gas[galaxy_id],
      // 	    // 		       _metals[galaxy_id], _snaps[galaxy_id], (*_snap_ages)[_snaps[galaxy_id]],
      // 	    // 		       age_masses, bulge_age_masses, age_metals );
      // 	 // }
      // }

      unsigned
      size() const
      {
         return _disk_sfrs.size();
      }

      std::pair<std::multimap<unsigned,unsigned>::const_iterator,
                std::multimap<unsigned,unsigned>::const_iterator>
      parents( unsigned gal_id ) const
      {
      	 return _parents.equal_range( gal_id );
      }

      unsigned
      lid_to_index( unsigned lid ) const
      {
         return _inv_lids.at( lid );
      }

      std::vector<int> const&
      snapshots() const
      {
	 return _snaps;
      }

      unsigned
      snapshot( unsigned gal_id ) const
      {
	 return _snaps[gal_id];
      }

      unsigned
      closest_snapshot() const
      {
	 return _old_snap; // Why the shit did I call it "old_snap"?
      }

      std::vector<real_type> const&
      disk_sfrs() const
      {
	 return _disk_sfrs;
      }

      real_type
      disk_sfr( unsigned gal_id ) const
      {
	 return _disk_sfrs[gal_id];
      }

      std::vector<real_type> const&
      bulge_sfrs() const
      {
         return _bulge_sfrs;
      }

      std::vector<real_type> const&
      cold_gas_masses() const
      {
         return _cold_gas;
      }

      std::vector<real_type> const&
      metallicities() const
      {
         return _metals;
      }

      std::vector<real_type>
      ages() const
      {
	 std::vector<real_type> ages( _disk_sfrs.size() );
	 for( unsigned ii = 0; ii < _disk_sfrs.size(); ++ii )
	 {
	    // Calculate the starting age based on the average age
	    // of my parent galaxies.
	    real_type parent_age = 0.0;
	    {
	       auto rng = _parents.equal_range( ii );
	       unsigned cnt = 0;
	       while( rng.first != rng.second )
	       {
		  parent_age += (*_snap_ages)[_snaps[rng.first->second]];
		  ++rng.first;
		  ++cnt;
	       }
	       if( cnt > 0 )
		  parent_age /= (real_type)cnt;
	       else
	       {
		  ASSERT( _snaps[ii] > 0, "Don't have a previous snapshot." );

		  // Use the amount of stellar mass on the object to determine
		  // the age.
		  // TODO: Don't bother with this for now.
		  // if( _sfrs[ii] > 0.0 )
		  // {
		  //    parent_age = (*_snap_ages)[_snaps[ii]] - 10.0*(_masses[ii]/0.43)/_sfrs[ii];
		  //    ASSERT( parent_age > 0.0, "Bad age calculation." );
		  // }
		  // else
		  parent_age = (*_snap_ages)[_snaps[ii] - 1];
	       }
	    }
	    real_type first_age = (*_snap_ages)[_old_snap] - parent_age;
	    real_type last_age = (*_snap_ages)[_old_snap] - (*_snap_ages)[_snaps[ii]];
	    ages[ii] = first_age - last_age;
	 }
	 return ages;
      }

      std::vector<real_type>
      masses() const
      {
	 std::vector<real_type> ages = this->ages();
	 std::vector<real_type> masses( _disk_sfrs.size() );
	 for( unsigned ii = 0; ii < _disk_sfrs.size(); ++ii )
	    masses[ii] = _disk_sfrs[ii]*ages[ii]*1e9; //*(1.0 - 0.43);
	 return masses;
      }

   protected:

      void
      _calc_parents()
      {
      	 // Clear existing parents.
      	 _parents.clear();

	 // Invert the local index mapping.
	 int max_lid = std::max(
	    *std::max_element( _lids.begin(), _lids.end() ),
	    *std::max_element( _descs.begin(), _descs.end() )
	    );
	 std::vector<int> inv_lids( max_lid + 1 );
	 std::fill( inv_lids.begin(), inv_lids.end(), -1 );
	 for( unsigned ii = 0; ii < _lids.size(); ++ii )
	    inv_lids[_lids[ii]] = ii;

      	 // Build the parents for each galaxy.
      	 for( unsigned ii = 0; ii < _descs.size(); ++ii )
      	 {
      	    if( _descs[ii] != -1 && inv_lids[_descs[ii]] != -1 )
      	       _parents.insert( std::make_pair( inv_lids[_descs[ii]], inv_lids[_lids[ii]] ) );
      	 }
      }

      template< class DiskVec,
		class BulgeVec >
      void
      _rebin_linear_thibault( real_type oldest_age,
			      typename hpc::type_traits<DiskVec>::reference disk_age_masses,
			      typename hpc::type_traits<BulgeVec>::reference bulge_age_masses,
                              stellar_population const& ssp )
      {
	 // Iterate over all objects.
	 for( unsigned ii = 0; ii < _disk_sfrs.size(); ++ii )
	 {
	    // Don't try to calculate anything if the SFR is zero. I do
	    // this not only for efficiency but also because some simulations
	    // don't always supply a snapshot - 1. Also, don't try this
	    // at snapshot 0 for the same reason.
	    real_type disk_sfr = _disk_sfrs[ii];
	    real_type bulge_sfr = _bulge_sfrs[ii];
	    int snap = _snaps[ii];
	    if( snap > 0 && (disk_sfr > 0.0 || bulge_sfr > 0.0) )
	    {
	       // Calculate the starting age based on the average age
	       // of my parent galaxies.
	       real_type parent_age = 0.0;
	       real_type prev_mass = 0.0;
	       {
		  auto rng = _parents.equal_range( ii );
		  unsigned cnt = 0;
		  while( rng.first != rng.second )
		  {
		     auto par_idx = rng.first->second;
                     int par_snap = _snaps[par_idx];
                     if( par_snap < snap )
                     {
                        parent_age += (*_snap_ages)[par_snap];
                        ++cnt;
                     }
                     else
                        std::cout << "WARNING: Found badly connected parents.\n";
		     prev_mass += _masses[par_idx];
                     ++rng.first;
		  }
		  if( cnt > 0 )
		     parent_age /= (real_type)cnt;
		  else
		  {
		     ASSERT( _snaps[ii] > 0, "Don't have a previous snapshot." );

		     // // Use the amount of stellar mass on the object to determine
		     // // the age.
		     // if( _sfrs[ii] > 0.0 )
		     // {
		     // 	parent_age = (*_snap_ages)[_snaps[ii]] - 10.0*(_masses[ii]/0.43)/_sfrs[ii];
		     // 	ASSERT( parent_age > 0.0, "Bad age calculation." );
		     // }
		     // else
		     parent_age = (*_snap_ages)[_snaps[ii] - 1];
		  }
	       }

	       // Calculate the age of material created at the beginning of
	       // this timestep and at the end. Be careful! This age I speak
	       // of is how old the material will be when we get to the
	       // time of the final galaxy.
	       // ASSERT( snap > 0, "Must have a previous snapshot." );
	       LOGDLN( "Oldest age in tree: ", oldest_age );
	       LOGDLN( "Age of current galaxy: ", (*_snap_ages)[snap] );
	       LOGDLN( "Age of parents: ", parent_age );
	       real_type first_age = oldest_age - parent_age;
	       real_type last_age = oldest_age - (*_snap_ages)[snap];
	       real_type age_size = first_age - last_age;
	       LOGDLN( "Age range: [", first_age, "-", last_age, ")" );
	       LOGDLN( "Age size: ", age_size );

	       // Use the star formation rates to compute the new mass
	       // produced. Bear in mind the rates we expect from the
	       // database will be solar masses per year.
	       real_type new_disk_mass = disk_sfr*age_size*1e9;
	       real_type new_bulge_mass = bulge_sfr*age_size*1e9;
	       LOGDLN( "New mass: ", new_disk_mass );
	       LOGDLN( "New bulge mass: ", new_bulge_mass );
	       ASSERT( new_disk_mass >= 0.0 && new_bulge_mass >= 0.0, "Mass has been lost during rebinning." );
	       ASSERT( new_disk_mass == new_disk_mass, "Have NaN for new total mass during rebinning." );
	       ASSERT( new_bulge_mass == new_bulge_mass, "Have NaN for new bulge mass during rebinning." );
	       // ASSERT( hpc::num::approx( new_mass, _masses[ii] - prev_mass, 1e4 ) );

	       // Cache metallicity bin indices.
	       unsigned disk_met_bin = ssp.find_metal_bin( _disk_sfr_z[ii] );
	       unsigned bulge_met_bin = ssp.find_metal_bin( _bulge_sfr_z[ii] );

	       // Add the new mass to the appropriate bins. Find the first bin
	       // that has overlap with this age range.
	       unsigned first_bin = _bin_ages->find_bin( last_age );
	       unsigned last_bin = _bin_ages->find_bin( first_age ) + 1;
	       while( first_bin != last_bin )
	       {
		  // Find the fraction we will use to contribute to this
		  // bin.
		  real_type upp;
		  if( first_bin < last_bin - 1 )
		     upp = std::min( _bin_ages->dual( first_bin ), first_age );
		  else
		     upp = first_age;
		  real_type frac = (upp - last_age)/age_size;
		  LOGDLN( "Have sub-range: [", last_age, "-", upp, ")" );
		  LOGDLN( "Updating bin ", first_bin, " with fraction of ", frac, "." );

		  // Cache the current bin mass for later.
		  real_type cur_disk_bin_mass = disk_age_masses[first_bin];
		  real_type cur_bugle_bin_mass = bulge_age_masses[first_bin];

		  // Update the mass bins.
                  unsigned disk_bin_idx = first_bin*ssp.num_metal_bins() + disk_met_bin;
                  unsigned bulge_bin_idx = first_bin*ssp.num_metal_bins() + bulge_met_bin;
		  disk_age_masses[disk_bin_idx] += frac*new_disk_mass;
		  bulge_age_masses[bulge_bin_idx] += frac*new_bulge_mass;
		  ASSERT( disk_age_masses[disk_bin_idx] == disk_age_masses[disk_bin_idx],
			  "Have NaN for rebinned total masses for bin: ", disk_bin_idx );
		  ASSERT( bulge_age_masses[bulge_bin_idx] == bulge_age_masses[bulge_bin_idx],
			  "Have NaN for rebinned bulge masses for bin: ", bulge_bin_idx );
		  ASSERT( disk_age_masses[disk_bin_idx] >= 0.0,
			  "Produced negative value for rebinned total masses for bin: ", disk_bin_idx );
		  ASSERT( bulge_age_masses[bulge_bin_idx] >= 0.0,
			  "Produced negative value for rebinned bulge masses for bin: ", bulge_bin_idx );

		  // Move to the next bin.
		  if( first_bin < _bin_ages->size() - 1 )
		     last_age = _bin_ages->dual( first_bin );
		  ++first_bin;
	       }
	    }
	 }
      }

      // template< class U >
      // void
      // _rebin_linear_chiara( real_type oldest_age,
      //                       typename vector<U>::view age_masses,
      //                       typename vector<U>::view bulge_age_masses,
      //                       typename vector<U>::view age_metals )
      // {
      // 	 // Iterate over all objects.
      // 	 for( unsigned ii = 0; ii < _sfrs.size(); ++ii )
      // 	 {
      // 	    // Don't try to calculate anything if the SFR is zero. I do
      // 	    // this not only for efficiency but also because some simulations
      // 	    // don't always supply a snapshot - 1. Also, don't try this
      // 	    // at snapshot 0 for the same reason.
      // 	    real_type sfr = _sfrs[ii];
      // 	    real_type bulge_sfr = _bulge_sfrs[ii];
      // 	    int snap = _snaps[ii];
      // 	    if( snap > 0 && (sfr > 0.0 || bulge_sfr > 0.0) )
      // 	    {
      // 	       // Cache some stuff.
      // 	       real_type metal = _metals[ii];
      // 	       real_type cold_gas = _cold_gas[ii];

      // 	       // Calculate the age of material created at the beginning of
      // 	       // this timestep and at the end. Be careful! This age I speak
      // 	       // of is how old the material will be when we get to the
      // 	       // time of the final galaxy.
      // 	       ASSERT( snap > 0, "Must have a previous snapshot." );
      // 	       LOGDLN( "Oldest age in tree: ", oldest_age );
      // 	       LOGDLN( "Age of current galaxy: ", (*_snap_ages)[snap] );
      // 	       LOGDLN( "Age of previous snapshot: ", (*_snap_ages)[snap - 1] );
      // 	       real_type first_age = oldest_age - (*_snap_ages)[snap - 1];
      // 	       real_type last_age = oldest_age - (*_snap_ages)[snap];
      // 	       real_type age_size = first_age - last_age;
      // 	       LOGDLN( "Age range: [", first_age, "-", last_age, ")" );
      // 	       LOGDLN( "Age size: ", age_size );

      // 	       // Use the star formation rates to compute the new mass
      // 	       // produced. Bear in mind the rates we expect from the
      // 	       // database will be solar masses per year.
      // 	       real_type new_mass = sfr*age_size*1e9; //*(1.0 - 0.43);
      // 	       real_type new_bulge_mass = bulge_sfr*age_size*1e9; //*(1.0 - 0.43);
      // 	       LOGDLN( "New mass: ", new_mass );
      // 	       LOGDLN( "New bulge mass: ", new_bulge_mass );
      // 	       ASSERT( new_mass >= 0.0 && new_bulge_mass >= 0.0, "Mass has been lost during rebinning." );
      // 	       ASSERT( new_mass == new_mass, "Have NaN for new total mass during rebinning." );
      // 	       ASSERT( new_bulge_mass == new_bulge_mass, "Have NaN for new bulge mass during rebinning." );

      // 	       // Add the new mass to the appropriate bins. Find the first bin
      // 	       // that has overlap with this age range.
      // 	       unsigned first_bin = _bin_ages->find_bin( last_age );
      // 	       unsigned last_bin = _bin_ages->find_bin( first_age ) + 1;
      // 	       while( first_bin != last_bin )
      // 	       {
      // 		  // Find the fraction we will use to contribute to this
      // 		  // bin.
      // 		  real_type upp;
      // 		  if( first_bin < last_bin - 1 )
      // 		     upp = std::min( _bin_ages->dual( first_bin ), first_age );
      // 		  else
      // 		     upp = first_age;
      // 		  real_type frac = (upp - last_age)/age_size;
      // 		  LOGDLN( "Have sub-range: [", last_age, "-", upp, ")" );
      // 		  LOGDLN( "Updating bin ", first_bin, " with fraction of ", frac, "." );

      // 		  // Cache the current bin mass for later.
      // 		  real_type cur_bin_mass = age_masses[first_bin];

      // 		  // Update the mass bins.
      // 		  LOGD( "Mass from ", age_masses[first_bin], " to " );
      // 		  age_masses[first_bin] += frac*new_mass;
      // 		  LOGDLN( age_masses[first_bin], "." );
      // 		  LOGD( "Bulge mass from ", bulge_age_masses[first_bin], " to " );
      // 		  bulge_age_masses[first_bin] += frac*new_bulge_mass;
      // 		  LOGDLN( bulge_age_masses[first_bin], "." );
      // 		  ASSERT( age_masses[first_bin] == age_masses[first_bin],
      // 			  "Have NaN for rebinned total masses for bin: ", first_bin );
      // 		  ASSERT( bulge_age_masses[first_bin] == bulge_age_masses[first_bin],
      // 			  "Have NaN for rebinned bulge masses for bin: ", first_bin );
      // 		  ASSERT( age_masses[first_bin] >= 0.0,
      // 			  "Produced negative value for rebinned total masses for bin: ", first_bin );
      // 		  ASSERT( bulge_age_masses[first_bin] >= 0.0,
      // 			  "Produced negative value for rebinned bulge masses for bin: ", first_bin );

      // 		  // Update the metal bins. This is impossible when no masses
      // 		  // have been added to the bin at all.
      // 		  if( age_masses[first_bin] > 0.0 && cold_gas > 0.0 )
      // 		  {
      // 		     LOGD( "Metals from ", age_metals[first_bin], " to " );
      // 		     // ASSERT( cold_gas > 0.0, "Cannot have zero cold gas for metallicity rebinning." );
      // 		     age_metals[first_bin] =
      // 			(cur_bin_mass*age_metals[first_bin] +
      // 			 frac*new_mass*(metal/cold_gas))/
      // 			age_masses[first_bin];
      // 		     LOGDLN( age_metals[first_bin], "." );
      // 		     ASSERT( age_metals[first_bin] == age_metals[first_bin],
      // 			     "Have NaN for rebinned metallicities for bin: ", first_bin );
      // 		     ASSERT( age_metals[first_bin] >= 0.0,
      // 			     "Produced negative value for rebinned metallicities for bin: ", first_bin );
      // 		  }

      // 		  // Move to the next bin.
      // 		  if( first_bin < _bin_ages->size() - 1 )
      // 		     last_age = _bin_ages->dual( first_bin );
      // 		  ++first_bin;
      // 	       }
      // 	    }
      // 	 }
      // }

   protected:

      age_line<real_type> const* _snap_ages;
      age_line<real_type> const* _bin_ages;
      int _old_snap;
      std::vector<int> _descs, _snaps, _lids;
      std::vector<real_type> _disk_sfr_z, _bulge_sfr_z;
      std::vector<real_type> _cold_gas, _metals;
      std::vector<real_type> _disk_sfrs, _bulge_sfrs, _masses;
      std::unordered_map<unsigned,unsigned> _inv_lids;
      std::multimap<unsigned,unsigned> _parents;
      std::string _cur_table;
      unsigned long long _cur_tree_id;
      unsigned long long _cur_gid;
   };

}

#endif
