#ifndef tao_base_sfh_hh
#define tao_base_sfh_hh

// Forward declaration of test suites to allow direct access.
class sfh_suite;

namespace tao {
   using namespace hpc;

   ///
   /// Star-formation History. Responsible for rebinning star-formation
   /// history data into appropriate time bins.
   ///
   template< class T >
   class sfh
   {
      friend class ::sfh_suite;

   public:

      typedef T real_type;

   public:

      sfh()
         : _timer( NULL ),
           _db_timer( NULL )
      {
      }

      void
      set_timer( profile::timer* timer )
      {
         _timer = timer;
      }

      void
      set_db_timer( profile::timer* timer )
      {
         _db_timer = timer;
      }

      void
      clear_tree_data()
      {
         _descs.deallocate();
         _snaps.deallocate();
         _sfrs.deallocate();
         _bulge_sfrs.deallocate();
         _cold_gas.deallocate();
         _metals.deallocate();
      }

      void
      set_snapshot_ages( const age_line& snap_ages )
      {
         _snap_ages = snap_ages;
      }

      void
      set_bin_ages( const age_line& bin_ages )
      {
         _bin_ages = bin_ages;
      }

      template< class T >
      void
      set_tree_data( vector<int> descs,
                     vector<int> snaps,
                     vector<real_type> sfrs,
                     vector<real_type> bulge_sfrs,
                     vector<real_type> cold_gas,
                     vector<real_type> metals )
      {
         // All arrays must be of the same size.
         ASSERT( descs.size() == snaps.size() &&
                 descs.size() == sfrs.size() &&
                 descs.size() == bulge_sfrs.size() &&
                 descs.size() == cold_gas.size() &&
                 descs.size() == metals.size(),
                 "Tree data sizes must match." );

         // Clear all existing tree data.
         clear_tree_data();

         // Take array data.
         _descs.swap( descs );
         _snaps.swap( snaps );
         _sfrs.swap( sfrs );
         _bulge_sfrs.swap( bulge_sfrs );
         _cold_gas.swap( cold_gas );
         _metals.swap( metals );

         // Calculate parents.
         _calc_parents();
      }

      void
      load_tree_data( soci::session& sql,
                      const string& table_name,
                      unsigned long long tree_id )
      {
         _timer_start( _timer );
         LOGILN( "Loading tree with global ID ", tree_id, " from table ", table_name, setindent( 2 ) );

         // Clear away any existing tree data.
         clear_tree_data();

         // Extract number of records in this tree.
         unsigned tree_size;
         _timer_start( _db_timer );
         sql << "SELECT COUNT(*) FROM " + table + " WHERE globaltreeid = :id",
            soci::into( tree_size ), soci::use( tree_id );
         _timer_stop( _db_timer );
         LOGDLN( "Tree size: ", tree_size );

         // If the tree size is greater than the threshold we should use a cumulative
         // method to form the history.
         if( tree_size >= _thresh )
         {
            _accum = true;
         }
         else
         {
            _accum = false;

            // Resize data arrays.
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
            _timer_start( _db_timer );
            sql << query, soci::into( (std::vector<int>&)_descs ),
               soci::into( (std::vector<double>&)_metals ), soci::into( (std::vector<double>&)_cold_gas ),
               soci::into( (std::vector<double>&)_sfrs ), soci::into( (std::vector<double>&)_bulge_sfrs ),
               soci::into( (std::vector<int>&)_snaps ),
               soci::use( tree_id );
            _timer_stop( _db_timer );
            LOGTLN( "Descendant: ", _descs );
            LOGTLN( "Star formation rates: ", _sfrs );
            LOGTLN( "Bulge star formation rates: ", _bulge_sfrs );
            LOGTLN( "Metals cold gas: ", _metals );
            LOGTLN( "Cold gas: ", _cold_gas );
            LOGTLN( "Snapshots: ", _snaps );

            // Build the parents for each galaxy.
            _calc_parents();
         }

         // Set the current table/tree information.
         _cur_table = table_name;
         _cur_tree_id = tree_id;

         LOGI( setindent( -2 ) );
         _timer_stop( _timer );
      }

      template< class T >
      void
      rebin( soci::session& sql,
             unsigned galaxy_id,
             typename vector<T>::view age_masses,
             typename vector<T>::view bulge_age_masses,
             typename vector<T>::view age_metals )
      {
         LOGDLN( "Rebinning galaxy with local ID ", galaxy_id, " in tree with ID ", _cur_tree, " in table ", _cur_table, "." );

         // Array sizes must match the number of bins.
         ASSERT( _bin_ages.size() == age_masses.size() &&
                 _bin_ages.size() == bulge_age_masses.size() &&
                 _bin_ages.size() == age_metals.size(),
                 "Rebinning arrays must have the same size as the age bins." );

         // Clear out values.
         std::fill( age_masses.begin(), age_masses.end(), 0.0 );
         std::fill( bulge_age_masses.begin(), bulge_age_masses.end(), 0.0 );
         std::fill( age_metals.begin(), age_metals.end(), 0.0 );

         // Rebin everything from this galaxy. Check if we are supposed to
         // be using a cumulative method.
         if( _accum )
         {
            // Extract the snapshot so we can get the age.
            unsigned snap;
            sql << "SELECT snapnum FROM " + _cur_table + " WHERE globaltreeid = :tid AND localgalaxyid = :gid",
               soci::into( snap ), soci::use( _cur_tree ), soci::use( galaxy_id );

            // Begin processing parents.
            _iter_parents( sql, id, _snap_ages[snap] );
         }
         else
         {
            _rebin_recurse( sql, id, _sfrs[id], _bulge_sfrs[id], _cold_gas[id], _metals[id], _snap_ages[_snaps[id]] );
         }
      }

   protected:

      void
      _calc_parents()
      {
         // Clear existing parents.
         _parents.clear();

         // Build the parents for each galaxy.
         for( unsigned ii = 0; ii < _descs.size(); ++ii )
         {
            if( _descs[ii] != -1 )
               _parents.insert( _descs[ii], ii );
         }
      }

      void
      sed::_rebin_recurse( soci::session& sql,
                           unsigned id,
                           real_type sfr,
                           real_type bulge_sfr,
                           real_type cold_gas,
                           real_type metal,
                           real_type oldest_age )
      {
         LOGDLN( "Rebinning masses/metals at galaxy: ", id, setindent( 2 ) );

         // Recurse parents, rebinning each of them.
         if( _accum )
         {
            _iter_parents( sql, id, oldest_age );
         }
         else
         {
            auto rng = _parents.equal_range( id );
            while( rng.first != rng.second )
            {
               unsigned par = (*rng.first++).second;
               _rebin_recurse( sql, par, _sfrs[par], _bulge_sfrs[par], _cold_gas[par], _metals[par], oldest_age );
            }
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

         // Use the star formation rates to compute the new mass
         // produced. Bear in mind the rates we expect from the
         // database will be solar masses per year.
         real_type new_mass = sfr*age_size*1e9;
         real_type new_bulge_mass = bulge_sfr*age_size*1e9;
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
                   frac*new_mass*(metal/cold_gas))/
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

      void
      sed::_iter_parents( soci::session& sql,
                          unsigned id,
                          real_type oldest_age )
      {
         LOGDLN( "Accumulating tree with id: ", id );

         // Must query the database to get parents.
         string query = str( format( "SELECT local_idx, sfr, bulge_sfr, coldgas, metalscoldgas FROM %1% WHERE descendant=%2% AND tree_idx=%3%" ) % _cur_table % id % _cur_tree_id );
         _timer_start( _db_timer );
         soci::rowset<soci::row> rs = sql.prepare << query;
         _timer_stop( _db_timer );

         // Now process each parent directly.
         for( soci::rowset<soci::row>::const_iterator it = rs.begin(); it != rs.end(); ++it )
         {
            _timer_start( _db_timer );
            int pid = it->get<int>( 0 );
            double psfr = it->get<double>( 1 );
            double pbulge_sfr = it->get<double>( 2 );
            double pcold_gas = it->get<double>( 3 );
            double pmetal = it->get<double>( 4 );
            _timer_stop( _db_timer );
            _rebin_recurse( sql, pid, psfr, pbulge_sfr, pcold_gas, pmetal, oldest_age );
         }
      }

      void
      _timer_start( profile::timer* timer )
      {
         if( timer )
            timer->start();
      }

      void
      _timer_stop( profile::timer* timer )
      {
         if( timer )
            timer->stop();
      }

   protected:

      age_list* _snap_ages;
      age_list* _bin_ages;
      vector<int> _descs, _snaps;
      vector<real_type> _sfrs, _bulge_sfrs, _cold_gas, _metals;
      multimap<unsigned,unsigned> _parents;
      string _cur_tree;
      unsigned long long _cur_tree_id;

      profile::timer* _db_timer;
      profile::timer* _timer;
   };

}

#endif
