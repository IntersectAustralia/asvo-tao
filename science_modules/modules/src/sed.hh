#ifndef tao_sed_sed_hh
#define tao_sed_sed_hh

#include "tao/base/module.hh"

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
      _find_bin( unsigned parent );

      real_type
      _calc_age( unsigned id,
		 unsigned root_id );

      void
      _read_ssp( const string& filename );

      void
      _read_options( const options::dictionary& dict,
                     optional<const string&> prefix=optional<const string&>() );

      void
      _load_table( const string& table );

   protected:

      vector<real_type> _ages, _dual_ages;
      vector<real_type> _disk_age_masses, _bulge_age_masses;
      vector<real_type> _disk_age_metals, _bulge_age_metals;
      mpi::lindex _num_spectra, _num_metals;
      vector<real_type> _disk_spectra, _bulge_spectra, _total_spectra;
      vector<real_type> _ssp;

      multimap<unsigned,unsigned> _parents;
      vector<int> _descs;
      vector<real_type> _sfrs, _bulge_sfrs, _metals, _bulge_metals, _redshifts;
   };
}

#endif
