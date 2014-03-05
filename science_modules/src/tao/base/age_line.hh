#ifndef tao_base_age_line_hh
#define tao_base_age_line_hh

#include <boost/filesystem/path.hpp>
#include <soci.h>
#include <libhpc/logging/logging.hh>
#include "timed.hh"
#include "utils.hh"
#include "simulation.hh"

namespace tao {
   namespace fs = boost::filesystem;
   using namespace hpc;

   ///
   /// Star-formation History. Responsible for rebinning star-formation
   /// history data into appropriate time bins.
   ///
   template< class T >
   class age_line
      : public timed
   {
   public:

      typedef T real_type;

   public:

      age_line()
         : timed()
      {
      }

      template< class Seq >
      age_line( Seq&& ages )
      {
         set_ages( std::forward<Seq>( ages ) );
      }

      age_line( soci::session& sql,
		real_type hubble = 73.0,
		real_type omega_m = 0.25,
		real_type omega_l = 0.75 )
      {
         load_ages( sql, hubble, omega_m, omega_l );
      }

      age_line( fs::path const& path )
      {
	 load( path );
      }

      age_line( soci::session& sql,
		const simulation& sim )
      {
         load_ages( sql, sim.hubble(), sim.omega_m(), sim.omega_l() );
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

      typename view<vector<real_type>>::type const
      dual() const
      {
	 return _dual;
      }

      typename view<vector<real_type>>::type const
      ages() const
      {
	 return _ages;
      }

      ///
      /// Set age values. Ages must be given as giga-years from the beginning
      /// of the universe.
      ///
      template< class Seq >
      void
      set_ages( Seq&& ages )
      {
         auto timer = timer_start();
         LOGTLN( "Setting ages on age line.", setindent( 2 ) );

         // Clear existing values.
         clear();

         // Don't do anything if we have no ages.
         if( ages.size() )
         {
            // Assign age values.
            hpc::assign( _ages, std::forward<Seq>( ages ) );

            // Must be sure ages are sorted correctly.
#ifndef NDEBUG
            for( unsigned ii = 1; ii < _ages.size(); ++ii )
               ASSERT( _ages[ii] >= _ages[ii - 1], "Ages must be sorted in ascending order." );
#endif

            // Calculate dual.
            _calc_dual();
         }

         LOGT( setindent( -2 ) );
      }

      void
      load( fs::path const& path )
      {
	 LOGBLOCKI( "Loading ages from: ", path );

	 // Open the file.
	 std::ifstream file( path.c_str() );
	 EXCEPT( file.is_open(), "Couldn't find ages file: ", path );

	 // Read the number of ages.
	 unsigned num_ages;
	 file >> num_ages;
	 EXCEPT( file.good(), "Error reading ages file." );
	 LOGILN( "Number of ages: ", num_ages );

	 // Read the ages.
	 vector<real_type> bin_ages( num_ages );
	 for( unsigned ii = 0; ii < num_ages; ++ii )
	    file >> bin_ages[ii];
	 EXCEPT( file.good(), "Error reading ages file." );

	 // Setup the bin ages.
	 set_ages( bin_ages );
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
         auto timer = timer_start();
         LOGBLOCKD( "Loading ages from database." );

         // Clear existing values.
         clear();

         // Find number of snapshots and resize the containers.
         unsigned num_snaps;
         {
            auto db_timer = db_timer_start();
            sql << "SELECT COUNT(*) FROM snap_redshift", soci::into( num_snaps );
         }
         LOGDLN( "Number of snapshots: ", num_snaps );

         // Need space to store the snapshots.
         _ages.reallocate( num_snaps );

         // Read meta data.
         {
            auto db_timer = db_timer_start();
            sql << "SELECT redshift FROM snap_redshift ORDER BY snapnum",
               soci::into( (std::vector<real_type>&)_ages );
         }
         LOGTLN( "Redshifts: ", _ages );

         // Convert to ages.
         for( unsigned ii = 0; ii < _ages.size(); ++ii )
            _ages[ii] = redshift_to_age<real_type>( _ages[ii], hubble, omega_m, omega_l );
         LOGDLN( "Snapshot ages: ", _ages );

         // Calculate the dual.
         _calc_dual();
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
