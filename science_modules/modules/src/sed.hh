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

      static
      module*
      factory( const string& name,
               pugi::xml_node base );

   public:

      typedef double real_type;

      sed( const string& name = string(),
           pugi::xml_node base = pugi::xml_node() );

      ~sed();

      ///
      /// Initialise the module.
      ///
      virtual
      void
      initialise( const options::xml_dict& global_dict );

      ///
      /// Run the module.
      ///
      virtual
      void
      execute();

      void
      process_galaxy( const tao::galaxy& galaxy );

      vector<real_type>::view
      disk_spectra();

      vector<real_type>::view
      bulge_spectra();

      vector<real_type>::view
      total_spectra();

      real_type
      omega() const;

      real_type
      omega_lambda() const;

      real_type
      omega_k() const;

      real_type
      omega_r() const;

   protected:

      void
      _process_time( mpi::lindex time_idx,
                     unsigned gal_idx );

      void
      _sum_spectra( mpi::lindex time_idx,
                    real_type metal,
                    real_type sfh,
                    vector<real_type>::view galaxy_spectra );

      unsigned
      _interp_metal( real_type metal );

      void
      _rebin_info( const tao::galaxy& galaxy,
                   unsigned idx );

      void
      _rebin_recurse( unsigned id,
                      real_type sfr,
                      real_type bulge_sfr,
                      real_type cold_gas,
                      real_type metal,
                      real_type oldest_age );

      void
      _iter_parents( unsigned id,
                     real_type oldest_age );

      unsigned
      _find_bin( real_type age );

      real_type
      _calc_age( real_type redshift );

      void
      _read_ssp( const string& filename );

      void
      _setup_snap_ages();

      void
      _read_options( const options::xml_dict& global_dict );

      void
      _load_table( long long tree_id,
                   const string& table );

   protected:

      vector<real_type> _snap_ages, _bin_ages, _dual_ages;
      vector<real_type> _age_masses, _bulge_age_masses;
      vector<real_type> _age_metals;
      mpi::lindex _num_spectra, _num_metals;
      fibre<real_type> _disk_spectra, _bulge_spectra, _total_spectra;
      vector<real_type> _ssp;

      string _cur_table;
      string _cur_tree;
      long long _cur_tree_id;
      unsigned _thresh;
      bool _accum;
      multimap<unsigned,unsigned> _parents;
      vector<int> _descs, _snaps;
      vector<real_type> _sfrs, _bulge_sfrs, _cold_gas, _metals;

      gsl_integration_workspace* _work;
      gsl_function _func;
      real_type _omega, _omega_lambda, _hubble;
      real_type _omega_r, _omega_k;
   };
}

#endif
