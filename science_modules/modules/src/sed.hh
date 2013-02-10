#ifndef tao_sed_sed_hh
#define tao_sed_sed_hh

#include <gsl/gsl_math.h>
#include <gsl/gsl_integration.h>
#include "tao/base/module.hh"

// Forward declaration of test suites to allow direct
// access to the lightcone module.
class sed_suite;
class filter_suite;

namespace tao {
   using namespace hpc;

   ///
   /// SED science module.
   ///
   /// The SED module is responsible for calculating the
   /// energy spectra of each galaxy.
   ///
   class sed
      : public module
   {
      friend class ::sed_suite;
      friend class ::filter_suite;

   public:

      typedef double real_type;

      sed();

      ~sed();

      ///
      ///
      ///
      void
      setup_options( options::dictionary& dict,
                     optional<const string&> prefix=optional<const string&>() );

      ///
      ///
      ///
      void
      setup_options( options::dictionary& dict,
                     const char* prefix );

      ///
      /// Initialise the module.
      ///
      void
      initialise( const options::dictionary& dict,
                  optional<const string&> prefix=optional<const string&>() );

      ///
      ///
      ///
      void
      initialise( const options::dictionary& dict,
                  const char* prefix );

      ///
      /// Run the module.
      ///
      void
      run();

      void
      process_galaxy( const tao::galaxy& galaxy );

      vector<real_type>::view
      disk_spectra();

      vector<real_type>::view
      bulge_spectra();

      vector<real_type>::view
      total_spectra();

   protected:

      void
      _process_time( mpi::lindex time_idx );

      void
      _sum_spectra( mpi::lindex time_idx,
                    real_type metal,
                    real_type sfh,
                    vector<real_type>::view galaxy_spectra );

      unsigned
      _interp_metal( real_type metal );

      void
      _rebin_info( const tao::galaxy& galaxy );

      void
      _rebin_parents( unsigned id,
		      unsigned root_id );

      void
      _update_bin( unsigned bin,
		   unsigned id,
		   real_type dt );

      unsigned
      _find_bin( real_type age );

      real_type
      _calc_age( real_type z0,
		 real_type z1 );

      void
      _read_ssp( const string& filename );

      void
      _setup_snap_ages();

      void
      _read_options( const options::dictionary& dict,
                     optional<const string&> prefix=optional<const string&>() );

      void
      _load_table( long long tree_id,
		   const string& table );

   protected:

      vector<real_type> _snap_ages, _bin_ages, _dual_ages;
      vector<real_type> _disk_age_masses, _bulge_age_masses;
      vector<real_type> _disk_age_metals, _bulge_age_metals;
      mpi::lindex _num_spectra, _num_metals;
      vector<real_type> _disk_spectra, _bulge_spectra, _total_spectra;
      vector<real_type> _ssp;

      long long _cur_tree_id;
      multimap<unsigned,unsigned> _parents;
      vector<int> _descs, _snaps;
      vector<real_type> _sfrs, _bulge_sfrs, _metals, _bulge_metals;

      gsl_integration_workspace* _work;
      gsl_function _func;
      real_type _omega, _omega_lambda, _h0;
   };
}

#endif
