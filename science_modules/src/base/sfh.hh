#ifndef tao_base_sfh_hh
#define tao_base_sfh_hh

#include <boost/algorithm/string/trim.hpp>
#include <boost/lexical_cast.hpp>
#include "timed.hh"
#include "age_line.hh"

// Forward declaration of test suites to allow direct access.
class sfh_suite;

namespace tao {
   using namespace hpc;
   using boost::format;
   using boost::str;

   ///
   /// Star-formation History. Responsible for rebinning star-formation
   /// history data into appropriate time bins.
   ///
   template< class T >
   class sfh
      : public timed
   {
      friend class ::sfh_suite;

   public:

      typedef T real_type;

   public:

      sfh()
         : timed(),
           _snap_ages( NULL ),
           _bin_ages( NULL ),
           _thresh( 100000000 ),
           _accum( false ),
           _cur_tree_id( std::numeric_limits<unsigned long long>::max() )
      {
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
      set_snapshot_ages( const age_line<real_type>* snap_ages )
      {
         _snap_ages = snap_ages;
      }

      void
      set_bin_ages( const age_line<real_type>* bin_ages )
      {
         _bin_ages = bin_ages;
      }

      void
      set_tree_data( vector<int>& descs,
                     vector<int>& snaps,
                     vector<real_type>& sfrs,
                     vector<real_type>& bulge_sfrs,
                     vector<real_type>& cold_gas,
                     vector<real_type>& metals )
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
         auto timer = timer_start();

         // We only want to reload if this isn't the same tree.
         if( _cur_tree_id != tree_id )
         {
            LOGILN( "Loading tree with global ID ", tree_id, " from table ", table_name, setindent( 2 ) );

            // Clear away any existing tree data.
            clear_tree_data();

            // Extract number of records in this tree.
            unsigned tree_size;
            {
               auto db_timer = db_timer_start();
               sql << "SELECT galaxycount FROM treesummary WHERE globaltreeid=:id",
                  soci::into( tree_size ), soci::use( tree_id );
            }
            LOGILN( "Tree size: ", tree_size );

            // If the tree size is greater than the threshold we should use a cumulative
            // method to form the history.
            // if( tree_size >= _thresh )
            // {
            //    _accum = true;
            // }
            // else
            // {
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
                  "sfr, sfrbulge, snapnum FROM  " + table_name +
                  " WHERE globaltreeid = :id"
                  " ORDER BY localgalaxyid";
               {
                  auto db_timer = db_timer_start();
                  sql << query, soci::into( (std::vector<int>&)_descs ),
                     soci::into( (std::vector<double>&)_metals ), soci::into( (std::vector<double>&)_cold_gas ),
                     soci::into( (std::vector<double>&)_sfrs ), soci::into( (std::vector<double>&)_bulge_sfrs ),
                     soci::into( (std::vector<int>&)_snaps ),
                     soci::use( tree_id );
               }
               LOGTLN( "Descendant: ", _descs );
               LOGTLN( "Star formation rates: ", _sfrs );
               LOGTLN( "Bulge star formation rates: ", _bulge_sfrs );
               LOGTLN( "Metals cold gas: ", _metals );
               LOGTLN( "Cold gas: ", _cold_gas );
               LOGTLN( "Snapshots: ", _snaps );

               // Build the parents for each galaxy.
               _calc_parents();
            // }

            // Set the current table/tree information.
            _cur_table = table_name;
            _cur_tree_id = tree_id;

            LOGILN( "Done.", setindent( -2 ) );
         }
      }

      template< class U >
      void
      rebin( soci::session& sql,
             unsigned galaxy_id,
             typename vector<U>::view age_masses,
             typename vector<U>::view bulge_age_masses,
             typename vector<U>::view age_metals )

      {
         LOGDLN( "Rebinning galaxy with local ID ", galaxy_id, " in tree with ID ", _cur_tree_id, " in table ", _cur_table, ".", setindent( 2 ) );

         // Must have ages available.
         ASSERT( _snap_ages, "Snapshot ages have not been set." );
         ASSERT( _bin_ages, "Bin ages have not been set." );

         // Array sizes must match the number of bins.
         ASSERT( _bin_ages->size() == age_masses.size() &&
                 _bin_ages->size() == bulge_age_masses.size() &&
                 _bin_ages->size() == age_metals.size(),
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
               soci::into( snap ), soci::use( _cur_tree_id ), soci::use( galaxy_id );

            // Begin processing parents.
            _iter_parents<U>( sql, galaxy_id, (*_snap_ages)[snap], age_masses, bulge_age_masses, age_metals );
         }
         else
         {
            _rebin_recurse<U>( sql, galaxy_id, _sfrs[galaxy_id], _bulge_sfrs[galaxy_id], _cold_gas[galaxy_id],
                               _metals[galaxy_id], _snaps[galaxy_id], (*_snap_ages)[_snaps[galaxy_id]],
                               age_masses, bulge_age_masses, age_metals );
         }

         LOGD( setindent( -2 ) );
      }

      unsigned
      size() const
      {
         return _descs.size();
      }

      std::pair< multimap<unsigned,unsigned>::const_iterator,
                 multimap<unsigned,unsigned>::const_iterator >
      parents( unsigned gal_id ) const
      {
         return _parents.equal_range( gal_id );
      }

      unsigned
      snapshot( unsigned gal_id ) const
      {
         return _snaps[gal_id];
      }

      real_type
      sfr( unsigned gal_id ) const
      {
         return _sfrs[gal_id];
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

      template< class U >
      void
      _rebin_recurse( soci::session& sql,
                      unsigned id,
                      real_type sfr,
                      real_type bulge_sfr,
                      real_type cold_gas,
                      real_type metal,
                      unsigned snap,
                      real_type oldest_age,
                      typename vector<U>::view age_masses,
                      typename vector<U>::view bulge_age_masses,
                      typename vector<U>::view age_metals )
      {
         LOGDLN( "Rebinning masses/metals at galaxy: ", id, setindent( 2 ) );

         // Recurse parents, rebinning each of them.
         if( _accum )
         {
            _iter_parents<U>( sql, id, oldest_age, age_masses, bulge_age_masses, age_metals );
         }
         else
         {
            auto rng = _parents.equal_range( id );
            while( rng.first != rng.second )
            {
               unsigned par = (*rng.first++).second;
               _rebin_recurse<U>( sql, par, _sfrs[par], _bulge_sfrs[par], _cold_gas[par], _metals[par], _snaps[par],
                                  oldest_age, age_masses, bulge_age_masses, age_metals );
            }
         }

         // Calculate the age of material created at the beginning of
         // this timestep and at the end. Be careful! This age I speak
         // of is how old the material will be when we get to the
         // time of the final galaxy.
         ASSERT( snap > 0, "Must have a previous snapshot." );
         LOGDLN( "Oldest age in tree: ", oldest_age );
         LOGDLN( "Age of current galaxy: ", (*_snap_ages)[snap] );
         LOGDLN( "Age of previous snapshot: ", (*_snap_ages)[snap - 1] );
         real_type first_age = oldest_age - (*_snap_ages)[snap - 1];
         real_type last_age = oldest_age - (*_snap_ages)[snap];
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
            real_type cur_bin_mass = age_masses[first_bin];

            // Update the mass bins.
            LOGD( "Mass from ", age_masses[first_bin], " to " );
            age_masses[first_bin] += frac*new_mass;
            LOGDLN( age_masses[first_bin], "." );
            LOGD( "Bulge mass from ", bulge_age_masses[first_bin], " to " );
            bulge_age_masses[first_bin] += frac*new_bulge_mass;
            LOGDLN( bulge_age_masses[first_bin], "." );

            // Update the metal bins. This is impossible when no masses
            // have been added to the bin at all.
            if( age_masses[first_bin] > 0.0 )
            {
               LOGD( "Metals from ", age_metals[first_bin], " to " );
               age_metals[first_bin] =
                  (cur_bin_mass*age_metals[first_bin] +
                   frac*new_mass*(metal/cold_gas))/
                  age_masses[first_bin];
               LOGDLN( age_metals[first_bin], "." );
            }

            // Move to the next bin.
            if( first_bin < _bin_ages->size() - 1 )
               last_age = _bin_ages->dual( first_bin );
            ++first_bin;
         }

         LOGD( setindent( -2 ) );
      }

      template< class U >
      void
      _iter_parents( soci::session& sql,
                     unsigned id,
                     real_type oldest_age,
                     typename vector<U>::view age_masses,
                     typename vector<U>::view bulge_age_masses,
                     typename vector<U>::view age_metals )
      {
         LOGDLN( "Accumulating tree with galaxy ID: ", id, setindent( 2 ) );

         // Must query the database to get parents.
         string query = str( format( "SELECT localgalaxyid, sfr, sfrbulge, coldgas, metalscoldgas, snapnum "
                                     "FROM %1% WHERE descendant=%2% AND globaltreeid=%3%" ) % _cur_table % id % _cur_tree_id );
         // auto db_timer = db_timer_start();
         soci::rowset<soci::row> rs = sql.prepare << query;

         // Now process each parent directly.
         for( soci::rowset<soci::row>::const_iterator it = rs.begin(); it != rs.end(); ++it )
         {
            int pid;
            double psfr, pbulge_sfr, pcold_gas, pmetal, psnap;
            {
               auto db_timer = db_timer_start();
               pid = it->get<int>( 0 );
               psfr = it->get<double>( 1 );
               pbulge_sfr = it->get<double>( 2 );
               pcold_gas = it->get<double>( 3 );
               pmetal = it->get<double>( 4 );
               psnap = it->get<int>( 5 );
            }
            _rebin_recurse<U>( sql, pid, psfr, pbulge_sfr, pcold_gas, pmetal, psnap,
                               oldest_age, age_masses, bulge_age_masses, age_metals );
         }

         LOGD( setindent( -2 ) );
      }

   protected:

      const age_line<real_type>* _snap_ages;
      const age_line<real_type>* _bin_ages;
      unsigned _thresh;
      bool _accum;
      vector<int> _descs, _snaps;
      vector<real_type> _sfrs, _bulge_sfrs, _cold_gas, _metals;
      multimap<unsigned,unsigned> _parents;
      string _cur_table;
      unsigned long long _cur_tree_id;
   };

}

#endif
