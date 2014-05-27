#include <boost/format.hpp>
#include <libhpc/algorithm/counts.hh>
#include "sfh.hh"

namespace tao {
   using boost::format;
   using boost::str;

   sfh::sfh()
      : _snap_ages( 0 ),
        _old_snap( std::numeric_limits<int>::max() ),
        _cur_tree_id( std::numeric_limits<unsigned long long>::max() ),
        _cur_gid( std::numeric_limits<unsigned long long>::max() ),
	_root( std::numeric_limits<unsigned>::max() )
   {
   }

   sfh::sfh( age_line<real_type> const* snap_ages,
             hpc::fs::path const& path )
   {
      set_snapshot_ages( snap_ages );
      load( path );
   }

   void
   sfh::clear_tree_data()
   {
      hpc::deallocate( _descs );
      hpc::deallocate( _snaps );
      hpc::deallocate( _lids );
      hpc::deallocate( _disk_sfrs );
      hpc::deallocate( _bulge_sfrs );
      hpc::deallocate( _disk_sfr_z );
      hpc::deallocate( _bulge_sfr_z );
      hpc::deallocate( _masses );
      hpc::deallocate( _inv_lids );
      hpc::deallocate( _par_displs );
   }

   void
   sfh::set_snapshot_ages( age_line<real_type> const* snap_ages )
   {
      _snap_ages = snap_ages;
   }

   age_line<real_type> const*
   sfh::snapshot_ages() const
   {
      return _snap_ages;
   }

   void
   sfh::load( hpc::fs::path const& path )
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

      // The oldest snapshot is the first one in the list.
      _old_snap = _snaps[0];

      EXCEPT( file.good(), "Error reading merger tree file." );
   }

   void
   sfh::load_tree_data( soci::session& sql,
                        std::string const& table_name,
                        unsigned long long tree_id,
                        unsigned long long global_index )
   {
      LOGBLOCKD( "Loading tree data from table ", table_name, " for tree with index ", tree_id, " rooted at galaxy with global index ", global_index );

      // Clear away any existing tree data.
      clear_tree_data();

      // Load the basic object information.
      unsigned long long dfo, subsize;
      sql << "SELECT depthfirst_traversalorder, subtree_count, snapnum FROM " +
	table_name + " WHERE globalindex=:gid",
         soci::into( dfo ), soci::into( subsize ), soci::into( _old_snap ),
         soci::use( global_index );
      LOGDLN( "Starting at depth first index: ", dfo );
      LOGDLN( "Subtree size: ", subsize );
      LOGDLN( "Oldest snapshot: ", _old_snap );

      // Resize data arrays.
      _disk_sfrs.resize( subsize );
      _bulge_sfrs.resize( subsize );
      _disk_sfr_z.resize( subsize );
      _bulge_sfr_z.resize( subsize );
      _snaps.resize( subsize );
      _descs.resize( subsize );
      _lids.resize( subsize );
      _merge_types.resize( subsize );
      _masses.resize( subsize );

      // Extract the sub tree.
      int dfo_first = dfo;
      int dfo_last = dfo + subsize;
      std::string query = "SELECT sfrdiskz, sfrbulgez, mergetype, "
         "sfrdisk, sfrbulge, snapnum, descendant, localgalaxyid, stellarmass FROM " + table_name +
         " WHERE globaltreeid = :treeid"
         " AND depthfirst_traversalorder >= :first AND depthfirst_traversalorder < :last";
      sql << query,
	 soci::into( _disk_sfr_z ), soci::into( _bulge_sfr_z ), soci::into( _merge_types ),
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
         sql << "SELECT descendant, localgalaxyid, globalindex FROM " + table_name +
	    " WHERE globaltreeid = :treeid"
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

   unsigned long long
   sfh::tree_id() const
   {
      return _cur_tree_id;
   }

   unsigned long long
   sfh::root_galaxy_id() const
   {
      return _cur_gid;
   }

   unsigned
   sfh::root_galaxy_index() const
   {
      return _root;
   }

   unsigned
   sfh::size() const
   {
      return _disk_sfrs.size();
   }

   std::vector<int> const&
   sfh::descendants() const
   {
      return _descs;
   }

   std::vector<int> const&
   sfh::snapshots() const
   {
      return _snaps;
   }

   std::vector<int> const&
   sfh::local_galaxy_ids() const
   {
      return _lids;
   }

   std::vector<real_type> const&
   sfh::disk_sfrs() const
   {
      return _disk_sfrs;
   }

   std::vector<real_type> const&
   sfh::bulge_sfrs() const
   {
      return _bulge_sfrs;
   }

   std::vector<real_type> const&
   sfh::disk_metallicities() const
   {
      return _disk_sfr_z;
   }

   std::vector<real_type> const&
   sfh::bulge_metallicities() const
   {
      return _bulge_sfr_z;
   }

   std::vector<real_type> const&
   sfh::masses() const
   {
      return _masses;
   }

   hpc::view<std::vector<unsigned> const>
   sfh::parents( unsigned idx ) const
   {
      ASSERT( idx + 1 < _par_displs.size(), "Invalid galaxy index." );
      auto displ = _par_displs[idx];
      return hpc::view<std::vector<unsigned> const>( _pars, _par_displs[idx + 1] - displ, displ );
   }

   unsigned
   sfh::lid_to_index( unsigned lid ) const
   {
      return _inv_lids.at( lid );
   }

   unsigned
   sfh::snapshot( unsigned gal_id ) const
   {
      return _snaps[gal_id];
   }

   unsigned
   sfh::closest_snapshot() const
   {
      return _old_snap; // Why the shit did I call it "old_snap"?
   }

   real_type
   sfh::disk_sfr( unsigned gal_id ) const
   {
      return _disk_sfrs[gal_id];
   }

   std::vector<real_type>
   sfh::ages() const
   {
      std::vector<real_type> ages( _disk_sfrs.size() );
      for( unsigned ii = 0; ii < _disk_sfrs.size(); ++ii )
      {
         // Calculate the starting age based on the average age
         // of my parent galaxies.
         real_type parent_age = 0.0;
         {
            auto pars = parents( ii );
            unsigned cnt = 0;
            for( unsigned jj = 0; jj < pars.size(); ++jj )
            {
               parent_age += (*_snap_ages)[_snaps[jj]];
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
   sfh::calculated_masses() const
   {
      std::vector<real_type> ages = this->ages();
      std::vector<real_type> masses( _disk_sfrs.size() );
      for( unsigned ii = 0; ii < _disk_sfrs.size(); ++ii )
         masses[ii] = _disk_sfrs[ii]*ages[ii]*1e9; //*(1.0 - 0.43);
      return masses;
   }

   void
   sfh::_calc_parents()
   {
      // Invert the local index mapping.
      int max_lid = std::max(
         *std::max_element( _lids.begin(), _lids.end() ),
         *std::max_element( _descs.begin(), _descs.end() )
         );
      std::vector<int> inv_lids( max_lid + 1 );
      std::fill( inv_lids.begin(), inv_lids.end(), -1 );
      for( unsigned ii = 0; ii < _lids.size(); ++ii )
         inv_lids[_lids[ii]] = ii;

      // Count the number of parents each galaxy has.
      _par_displs.resize( _lids.size() + 1 );
      std::fill( _par_displs.begin(), _par_displs.end(), 0 );
#ifndef NDEBUG
      _root = std::numeric_limits<unsigned>::max();
#endif
      for( size_t ii = 0; ii < _descs.size(); ++ii )
      {
	 // All galaxies should have a descendant except for
	 // the root.
         if( _descs[ii] != -1 && inv_lids[_descs[ii]] != -1 )
            ++_par_displs[inv_lids[_descs[ii]]];
	 else
	 {
	    ASSERT( _root == std::numeric_limits<unsigned>::max(), "Found more than one "
		    "galaxy with no descendants in merger subtree." );
	    _root = ii;
	 }
      }
      hpc::counts_to_displs<std::vector<unsigned>>( _par_displs );

      // Build the parents for each galaxy.
      _pars.resize( _par_displs[_lids.size()] );
      for( unsigned ii = 0; ii < _descs.size(); ++ii )
      {
         if( _descs[ii] != -1 && inv_lids[_descs[ii]] != -1 )
         {
            unsigned ch = inv_lids[_descs[ii]], pa = inv_lids[_lids[ii]];
            _pars[_par_displs[ch]++] = pa;
         }
      }
      hpc::correct_displs<std::vector<unsigned>>( _par_displs );

      // Map descendants to indices.
      for( unsigned ii = 0; ii < _descs.size(); ++ii )
      {
         if( _descs[ii] != -1 )
            _descs[ii] = inv_lids[_descs[ii]];
      }
   }

}
