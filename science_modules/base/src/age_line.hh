#ifndef tao_base_age_line_hh
#define tao_base_age_line_hh

#include <libhpc/logging/logging.hh>
#include "timed.hh"
#include "utils.hh"

// Forward declaration of test suites to allow direct access.
class age_line_suite;

namespace tao {
   using namespace hpc;

   ///
   /// Star-formation History. Responsible for rebinning star-formation
   /// history data into appropriate time bins.
   ///
   template< class T >
   class age_line
      : public timed
   {
      friend class ::age_line_suite;

   public:

      typedef T real_type;

   public:

      age_line()
         : timed()
      {
      }

      age_line( vector<real_type> ages )
      {
         set_ages( ages );
      }

      age_line( soci::session& sql )
      {
         load_ages( sql );
      }

      void
      clear()
      {
         _ages.deallocate();
         _dual.deallocate();
      }

      unsigned
      size() const
      {
         return _ages.size();
      }

      real_type
      dual( unsigned idx ) const
      {
         return _dual[idx];
      }

      ///
      /// Set age values. Ages must be given as giga-years from the beginning
      /// of the universe.
      ///
      void
      set_ages( vector<real_type> ages )
      {
         timer_start();
         LOGTLN( "Setting ages on age line.", setindent( 2 ) );

         // Clear existing values.
         clear();

         // Don't do anything if we have no ages.
         if( ages.size() )
         {
            // Take age values.
            _ages.swap( ages );
            LOGTLN( "Ages: ", _ages );

            // Must be sure ages are sorted correctly.
#ifndef NDEBUG
            for( unsigned ii = 1; ii < _ages.size(); ++ii )
               ASSERT( _ages[ii] >= _ages[ii - 1], "Ages must be sorted in ascending order." );
#endif

            // Calculate dual.
            _calc_dual();
         }

         LOGT( setindent( -2 ) );
         timer_stop();
      }

      ///
      /// Load ages from database. Attempts to load ages from a connected
      /// database under the table name "snap_redshift".
      ///
      void
      load_ages( soci::session& sql,
                 real_type hubble = 73.0,
                 real_type omega_m = 0.25,
                 real_type omega_l = 0.75 )
      {
         timer_start();
         LOGDLN( "Loading ages from database.", setindent( 2 ) );

         // Clear existing values.
         clear();

         // Find number of snapshots and resize the containers.
         unsigned num_snaps;
         db_timer_start();
         sql << "SELECT COUNT(*) FROM snap_redshift", soci::into( num_snaps );
         db_timer_stop();
         LOGDLN( "Number of snapshots: ", num_snaps );

         // Need space to store the snapshots.
         _ages.reallocate( num_snaps );

         // Read meta data.
         db_timer_start();
         sql << "SELECT redshift FROM snap_redshift ORDER BY snapnum",
            soci::into( (std::vector<real_type>&)_ages );
         db_timer_stop();
         LOGTLN( "Redshifts: ", _ages );

         // Convert to ages.
         for( unsigned ii = 0; ii < _ages.size(); ++ii )
            _ages[ii] = redshift_to_age<real_type>( _ages[ii], hubble, omega_m, omega_l );
         LOGDLN( "Snapshot ages: ", _ages );

         // Calculate the dual.
         _calc_dual();

         LOGD( setindent( -2 ) );
         timer_stop();
      }

      unsigned
      find_bin( real_type age ) const
      {
         LOGTLN( "Searching for bin using age: ", age, setindent( 2 ) );
         unsigned bin;
         {
            // Use binary search to find first element greater.
            auto it = std::lower_bound( _dual.begin(), _dual.end(), age );
            if( it == _dual.end() )
               bin = _dual.size();
            else
               bin = it - _dual.begin();
         }
         LOGTLN( "Found bin ", bin, " with age of ", _ages[bin], ".", setindent( -2 ) );
         return bin;
      }

      real_type
      operator[]( unsigned idx ) const
      {
         return _ages[idx];
      }

   protected:

      void
      _calc_dual()
      {
         if( _ages.size() )
         {
            _dual.resize( _ages.size() - 1 );
            for( unsigned ii = 1; ii < _ages.size(); ++ii )
               _dual[ii - 1] = 0.5*(_ages[ii] + _ages[ii - 1]);
         }
         else
            _dual.deallocate();
         LOGTLN( "Dual: ", _dual );
      }

   protected:

      vector<real_type> _ages, _dual;
   };
}

#endif
