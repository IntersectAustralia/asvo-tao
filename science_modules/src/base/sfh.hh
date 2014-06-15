#ifndef tao_base_sfh_hh
#define tao_base_sfh_hh

#include <unordered_set>
#include <unordered_map>
#include <map>
#include <vector>
#include <libhpc/system/deallocate.hh>
#include <libhpc/system/math.hh>
#include <libhpc/system/filesystem.hh>
#include "types.hh"
#include "age_line.hh"
#include "stellar_population.hh"

namespace tao {

#ifndef NDEBUG
   struct rebin_stats_type
   {
      unsigned n_gals;
      unsigned n_mergers;
      unsigned n_major;
      unsigned n_minor;
      unsigned n_disrupt;
      unsigned n_ics;
   };
#endif

   ///
   /// Star-formation History. Responsible for rebinning star-formation
   /// history data into appropriate time bins.
   ///
   class sfh
   {
   public:

      sfh();

      sfh( age_line<real_type> const* snap_ages,
	   hpc::fs::path const& path );

      void
      clear_tree_data();

      void
      set_snapshot_ages( age_line<real_type> const* snap_ages );

      age_line<real_type> const*
      snapshot_ages() const;

      void
      load( hpc::fs::path const& path );

      void
      load_tree_data( soci::session& sql,
                      std::string const& table_name,
		      unsigned long long tree_id,
                      unsigned long long global_index );

      unsigned long long
      tree_id() const;

      unsigned long long
      root_galaxy_id() const;

      unsigned
      root_galaxy_index() const;

      unsigned
      size() const;

      std::vector<int> const&
      descendants() const;

      std::vector<int> const&
      snapshots() const;

      std::vector<int> const&
      local_galaxy_ids() const;

      std::vector<real_type> const&
      disk_sfrs() const;

      std::vector<real_type> const&
      bulge_sfrs() const;

      std::vector<real_type> const&
      disk_metallicities() const;

      std::vector<real_type> const&
      bulge_metallicities() const;

      std::vector<real_type> const&
      masses() const;

      hpc::view<std::vector<unsigned> const>
      parents( unsigned gal_id ) const;

      unsigned
      lid_to_index( unsigned lid ) const;

      unsigned
      snapshot( unsigned gal_id ) const;

      unsigned
      closest_snapshot() const;

      real_type
      disk_sfr( unsigned gal_id ) const;

      std::vector<real_type>
      ages() const;

      std::vector<real_type>
      calculated_masses() const;

      template< class DiskVec,
		class BulgeVec = DiskVec >
#ifndef NDEBUG
      rebin_stats_type
#else
      unsigned
#endif
      rebin( typename hpc::type_traits<DiskVec>::reference disk_age_masses,
             typename hpc::type_traits<BulgeVec>::reference bulge_age_masses,
             stellar_population const& ssp )
      {
         // Must have ages available.
         ASSERT( _snap_ages, "Snapshot ages have not been set." );

         // Array sizes must match the number of bins.
         ASSERT( ssp.age_masses_size() == disk_age_masses.size() &&
                 ssp.age_masses_size() == bulge_age_masses.size(),
                 "Rebinning arrays must have the same size as the age bins." );

         // Clear out values.
         std::fill( disk_age_masses.begin(), disk_age_masses.end(), 0.0 );
         std::fill( bulge_age_masses.begin(), bulge_age_masses.end(), 0.0 );

         // _rebin_linear_thibault<DiskVec,BulgeVec>( (*_snap_ages)[_old_snap],
	 //                                           disk_age_masses, bulge_age_masses, ssp );
#ifndef NDEBUG
         rebin_stats_type stats = { 0 };
#endif
         _rebin_recurse<DiskVec,BulgeVec>( (*_snap_ages)[_old_snap], _root, false,
					   disk_age_masses, bulge_age_masses,
#ifndef NDEBUG
                                           stats,
#endif
                                           ssp );
#ifndef NDEBUG
         return stats;
#endif
      }

   protected:

      void
      _calc_parents();

      // template< class DiskVec,
      // 		class BulgeVec >
      // void
      // _rebin_linear_thibault( real_type oldest_age,
      // 			      typename hpc::type_traits<DiskVec>::reference disk_age_masses,
      // 			      typename hpc::type_traits<BulgeVec>::reference bulge_age_masses,
      //                         stellar_population const& ssp )
      // {
      // 	 // Iterate over all objects.
      // 	 for( unsigned ii = 0; ii < _disk_sfrs.size(); ++ii )
      // 	 {
      // 	    // Don't try to calculate anything if the SFR is zero. I do
      // 	    // this not only for efficiency but also because some simulations
      // 	    // don't always supply a snapshot - 1. Also, don't try this
      // 	    // at snapshot 0 for the same reason.
      // 	    real_type disk_sfr = _disk_sfrs[ii];
      // 	    real_type bulge_sfr = _bulge_sfrs[ii];
      //       LOGDLN( "Disk SFR: ", disk_sfr );
      //       LOGDLN( "Bulge SFR: ", bulge_sfr );
      // 	    int snap = _snaps[ii];
      // 	    if( snap > 0 && (disk_sfr > 0.0 || bulge_sfr > 0.0) )
      // 	    {
      // 	       // Calculate the starting age based on the average age
      // 	       // of my parent galaxies.
      // 	       real_type parent_age = 0.0;
      // 	       real_type prev_mass = 0.0;
      // 	       {
      //             auto pars = parents( ii );
      // 		  unsigned cnt = 0;
      //             for( unsigned jj = 0; jj < pars.size(); ++jj )
      // 		  {
      // 		     auto par_idx = pars[jj];
      //                int par_snap = _snaps[par_idx];
      //                if( par_snap < snap )
      //                {
      //                   parent_age += (*_snap_ages)[par_snap];
      //                   ++cnt;
      //                }
      //                else
      //                   std::cout << "WARNING: Found badly connected parents.\n";
      // 		     prev_mass += _masses[par_idx];
      // 		  }
      // 		  if( cnt > 0 )
      // 		     parent_age /= (real_type)cnt;
      // 		  else
      // 		  {
      // 		     ASSERT( _snaps[ii] > 0, "Don't have a previous snapshot." );

      // 		     // // Use the amount of stellar mass on the object to determine
      // 		     // // the age.
      // 		     // if( _sfrs[ii] > 0.0 )
      // 		     // {
      // 		     // 	parent_age = (*_snap_ages)[_snaps[ii]] - 10.0*(_masses[ii]/0.43)/_sfrs[ii];
      // 		     // 	ASSERT( parent_age > 0.0, "Bad age calculation." );
      // 		     // }
      // 		     // else
      // 		     parent_age = (*_snap_ages)[_snaps[ii] - 1];
      // 		  }
      // 	       }

      // 	       // Calculate the age of material created at the beginning of
      // 	       // this timestep and at the end. Be careful! This age I speak
      // 	       // of is how old the material will be when we get to the
      // 	       // time of the final galaxy.
      // 	       // ASSERT( snap > 0, "Must have a previous snapshot." );
      //          LOGDLN( "Current snapsnot: ", snap );
      // 	       LOGDLN( "Oldest snapshot age: ", oldest_age );
      // 	       LOGDLN( "Current snapshot age (from start of time): ", (*_snap_ages)[snap] );
      // 	       LOGDLN( "Parent snapshot age (from start of time): ", parent_age );
      // 	       real_type first_age = oldest_age - parent_age;
      // 	       real_type last_age = oldest_age - (*_snap_ages)[snap];
      // 	       real_type age_size = first_age - last_age;
      //          LOGDLN( "Material start age: ", first_age );
      //          LOGDLN( "Material finish age: ", last_age );

      // 	       // Use the star formation rates to compute the new mass
      // 	       // produced. Bear in mind the rates we expect from the
      // 	       // database will be solar masses per year.
      // 	       real_type new_disk_mass = disk_sfr*age_size*1e9;
      // 	       real_type new_bulge_mass = bulge_sfr*age_size*1e9;
      // 	       LOGDLN( "New mass: ", new_disk_mass );
      // 	       LOGDLN( "New bulge mass: ", new_bulge_mass );
      // 	       ASSERT( new_disk_mass >= 0.0 && new_bulge_mass >= 0.0, "Mass has been lost during rebinning." );
      // 	       ASSERT( new_disk_mass == new_disk_mass, "Have NaN for new total mass during rebinning." );
      // 	       ASSERT( new_bulge_mass == new_bulge_mass, "Have NaN for new bulge mass during rebinning." );
      // 	       // ASSERT( hpc::num::approx( new_mass, _masses[ii] - prev_mass, 1e4 ) );

      // 	       // Cache metallicity bin indices.
      // 	       unsigned disk_met_bin = ssp.find_metal_bin( _disk_sfr_z[ii] );
      // 	       unsigned bulge_met_bin = ssp.find_metal_bin( _bulge_sfr_z[ii] );

      // 	       // Add the new mass to the appropriate bins. Find the first bin
      // 	       // that has overlap with this age range.
      // 	       unsigned first_age_bin = ssp.bin_ages().find_bin( last_age );
      // 	       unsigned last_age_bin = ssp.bin_ages().find_bin( first_age ) + 1;
      // 	       while( first_age_bin != last_age_bin )
      // 	       {
      // 		  // Find the fraction we will use to contribute to this
      // 		  // bin.
      // 		  real_type upp;
      // 		  if( first_age_bin < last_age_bin - 1 )
      // 		     upp = std::min( ssp.bin_ages().dual( first_age_bin ), first_age );
      // 		  else
      // 		     upp = first_age;
      // 		  real_type frac = (upp - last_age)/age_size;
      // 		  LOGDLN( "Have sub-range: [", last_age, "-", upp, ")" );
      // 		  LOGDLN( "Updating bin ", first_age_bin, " with fraction of ", frac, "." );

      //             // Calcualte bin indices.
      //             unsigned disk_bin_idx = first_age_bin*ssp.n_metal_bins() + disk_met_bin;
      //             unsigned bulge_bin_idx = first_age_bin*ssp.n_metal_bins() + bulge_met_bin;

      // 		  // Cache the current bin mass for later.
      // 		  real_type cur_disk_bin_mass = disk_age_masses[disk_bin_idx];
      // 		  real_type cur_bugle_bin_mass = bulge_age_masses[bulge_bin_idx];

      // 		  // Update the mass bins.
      // 		  disk_age_masses[disk_bin_idx] += frac*new_disk_mass;
      // 		  bulge_age_masses[bulge_bin_idx] += frac*new_bulge_mass;
      // 		  ASSERT( disk_age_masses[disk_bin_idx] == disk_age_masses[disk_bin_idx],
      // 			  "Have NaN for rebinned total masses for bin: ", disk_bin_idx );
      // 		  ASSERT( bulge_age_masses[bulge_bin_idx] == bulge_age_masses[bulge_bin_idx],
      // 			  "Have NaN for rebinned bulge masses for bin: ", bulge_bin_idx );
      // 		  ASSERT( disk_age_masses[disk_bin_idx] >= 0.0,
      // 			  "Produced negative value for rebinned total masses for bin: ", disk_bin_idx );
      // 		  ASSERT( bulge_age_masses[bulge_bin_idx] >= 0.0,
      // 			  "Produced negative value for rebinned bulge masses for bin: ", bulge_bin_idx );

      // 		  // Move to the next bin.
      // 		  if( first_age_bin < ssp.bin_ages().size() - 1 )
      // 		     last_age = ssp.bin_ages().dual( first_age_bin );
      // 		  ++first_age_bin;
      // 	       }
      // 	    }
      // 	 }
      // }

      template< class DiskVec,
		class BulgeVec >
      void
      _rebin_recurse( real_type oldest_age,
		      unsigned idx,
		      bool add_to_bulge,
		      typename hpc::type_traits<DiskVec>::reference disk_age_masses,
		      typename hpc::type_traits<BulgeVec>::reference bulge_age_masses,
#ifndef NDEBUG
                      rebin_stats_type& stats,
#endif
		      stellar_population const& ssp )
      {
	 // Don't try to calculate anything if the SFR is zero. I do
	 // this not only for efficiency but also because some simulations
	 // don't always supply a snapshot - 1. Also, don't try this
	 // at snapshot 0 for the same reason.
	 int snap = _snaps[idx];
	 if( snap > 0 )
	 {
#ifndef NDEBUG
            // Increment galaxy count.
            ++stats.n_gals;
#endif

	    // Calculate the starting age based on the average age
	    // of my parent galaxies.
	    real_type parent_age = 0.0;
	    real_type prev_mass = 0.0;
	    {
	       auto pars = parents( idx );

#ifndef NDEBUG
               // Update merger stats.
               if( pars.size() )
                  stats.n_mergers += pars.size() - 1;
#endif

	       for( unsigned jj = 0; jj < pars.size(); ++jj )
	       {
		  auto par_idx = pars[jj];
		  prev_mass += _masses[par_idx];

		  // So long as I'm here, recurse into the parents and
		  // calculate their contribution.
		  if( _merge_types[par_idx] <= 1 || _merge_types[par_idx] == 3 ) // normal/minor merger || disrupt
		  {
#ifndef NDEBUG
                     if( _merge_types[par_idx] == 1 )
                        ++stats.n_minor;
                     else if( _merge_types[par_idx] == 3 )
                        ++stats.n_disrupt;
#endif

		     _rebin_recurse<DiskVec,BulgeVec>( oldest_age, par_idx, add_to_bulge,
						       disk_age_masses, bulge_age_masses,
#ifndef NDEBUG
                                                       stats,
#endif
						       ssp );
		  }
		  else if( _merge_types[par_idx] == 2 ) // major merger
		  {
#ifndef NDEBUG
                     ++stats.n_major;
#endif

		     _rebin_recurse<DiskVec,BulgeVec>( oldest_age, par_idx, true,
						       disk_age_masses, bulge_age_masses,
#ifndef NDEBUG
                                                       stats,
#endif
						       ssp );
		  }
	       }

               // Grab the parent's age. It is assumed that all parents
               // will be from the previous snapshot only.
               parent_age = (*_snap_ages)[_snaps[idx] - 1];
	    }

	    // Don't do this unless we have values to use.
	    real_type disk_sfr = _disk_sfrs[idx];
	    real_type bulge_sfr = _bulge_sfrs[idx];
	    LOGDLN( "Disk SFR: ", disk_sfr );
	    LOGDLN( "Bulge SFR: ", bulge_sfr );
	    if( disk_sfr > 0.0 || bulge_sfr > 0.0 )
	    {
	       // Calculate the age of material created at the beginning of
	       // this timestep and at the end. Be careful! This age I speak
	       // of is how old the material will be when we get to the
	       // time of the final galaxy.
	       // ASSERT( snap > 0, "Must have a previous snapshot." );
	       LOGDLN( "Current snapsnot: ", snap );
	       LOGDLN( "Oldest snapshot age: ", oldest_age );
	       LOGDLN( "Current snapshot age (from start of time): ", (*_snap_ages)[snap] );
	       LOGDLN( "Parent snapshot age (from start of time): ", parent_age );
	       real_type first_age = oldest_age - parent_age;
	       real_type last_age = oldest_age - (*_snap_ages)[snap];
	       real_type age_size = first_age - last_age;
	       LOGDLN( "Material start age: ", first_age );
	       LOGDLN( "Material finish age: ", last_age );

	       // Use the stored dt value instead of the age I calculate.
	       age_size = _dts[idx];
	       first_age = last_age + age_size;

	       // Use the star formation rates to compute the new mass
	       // produced. Bear in mind the rates we expect from the
	       // database will be solar masses per year.
	       real_type new_disk_mass = disk_sfr*age_size*1e9;
	       real_type new_bulge_mass = bulge_sfr*age_size*1e9;

	       // real_type stars = (_masses[idx]*1e10)/(1.0 - 0.43);
	       // real_type dt = stars/(disk_sfr*1e9);
	       // std::cout << dt << ", " << age_size << ", " << _dts[idx] << ", ";
	       // printf( "%.12lf\n", dt/age_size );

	       LOGDLN( "New mass: ", new_disk_mass );
	       LOGDLN( "New bulge mass: ", new_bulge_mass );
	       ASSERT( new_disk_mass >= 0.0 && new_bulge_mass >= 0.0, "Mass has been lost during rebinning." );
	       ASSERT( new_disk_mass == new_disk_mass, "Have NaN for new total mass during rebinning." );
	       ASSERT( new_bulge_mass == new_bulge_mass, "Have NaN for new bulge mass during rebinning." );
	       // ASSERT( hpc::num::approx( new_mass, _masses[idx] - prev_mass, 1e4 ) );

	       // Cache metallicity bin indices.
	       unsigned disk_met_bin = ssp.find_metal_bin( _disk_sfr_z[idx] );
	       unsigned bulge_met_bin = ssp.find_metal_bin( _bulge_sfr_z[idx] );

#ifndef NDEBUG
               // Check that we don't accidentally lose any material.
               real_type disk_added = 0.0;
               real_type bulge_added = 0.0;
#endif

	       // Add the new mass to the appropriate bins. Find the first bin
	       // that has overlap with this age range.
	       unsigned first_age_bin = ssp.bin_ages().find_bin( last_age );
	       unsigned last_age_bin = ssp.bin_ages().find_bin( first_age ) + 1;
	       while( first_age_bin != last_age_bin )
	       {
		  // Find the fraction we will use to contribute to this
		  // bin.
		  real_type upp;
		  if( first_age_bin < last_age_bin - 1 )
		     upp = std::min( ssp.bin_ages().dual( first_age_bin ), first_age );
		  else
		     upp = first_age;
		  real_type frac = (upp - last_age)/age_size;
		  LOGDLN( "Have sub-range: [", last_age, "-", upp, ")" );
		  LOGDLN( "Updating bin ", first_age_bin, " with fraction of ", frac, "." );

		  // Calcualte bin indices.
		  unsigned disk_bin_idx = first_age_bin*ssp.n_metal_bins() + disk_met_bin;
		  unsigned bulge_bin_idx = first_age_bin*ssp.n_metal_bins() + bulge_met_bin;

		  // Cache the current bin mass for later.
		  real_type cur_disk_bin_mass = disk_age_masses[disk_bin_idx];
		  real_type cur_bugle_bin_mass = bulge_age_masses[bulge_bin_idx];

		  // Update the mass bins.
		  if( add_to_bulge )
		     bulge_age_masses[bulge_bin_idx] += frac*new_disk_mass;
		  else
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

#ifndef NDEBUG
                  // Keep track of mass.
                  disk_added += frac*new_disk_mass;
                  bulge_added += frac*new_bulge_mass;
#endif

		  // Move to the next bin.
		  if( first_age_bin < ssp.bin_ages().size() - 1 )
		     last_age = ssp.bin_ages().dual( first_age_bin );
		  ++first_age_bin;
	       }

               // Check we didn't lose anything.
               ASSERT( new_disk_mass == 0.0 || hpc::approx( disk_added/new_disk_mass, 1.0, 1e-8 ), "Lost disk mass during rebin." );
               ASSERT( new_bulge_mass == 0.0 || hpc::approx( bulge_added/new_bulge_mass, 1.0, 1e-8 ), "Lost bulge mass during rebin." );
	    }
	 }
      }

   protected:

      age_line<real_type> const* _snap_ages;
      int _old_snap;
      std::vector<int> _descs, _snaps, _lids, _merge_types;
      std::vector<real_type> _dts;
      std::vector<real_type> _disk_sfr_z, _bulge_sfr_z;
      std::vector<real_type> _disk_sfrs, _bulge_sfrs, _masses;
      std::unordered_map<unsigned,unsigned> _inv_lids;
      std::vector<unsigned> _par_displs, _pars;
      std::string _cur_table;
      unsigned long long _cur_tree_id;
      unsigned long long _cur_gid;
      unsigned _root;
   };

}

#endif
