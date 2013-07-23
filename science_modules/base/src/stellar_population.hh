#ifndef tao_base_stellar_population_hh
#define tao_base_stellar_population_hh

#include "timed.hh"
#include "age_line.hh"
#include "types.hh"

// Forward declaration of test suites to allow direct access.
class stellar_population_suite;

namespace tao {
   using namespace hpc;

   ///
   ///
   ///
   class stellar_population
      : public timed
   {
      friend class ::stellar_population_suite;

   public:

      stellar_population();

      void
      set_num_metals( unsigned num_metals );

      void
      set_wavelengths( vector<real_type>& waves );

      void
      set_spectra( vector<real_type>& spectra );

      void
      load( const string& wave_filename,
            const string& ssp_filename );

      real_type
      at( unsigned age_idx,
          unsigned spec_idx,
          unsigned metal_idx ) const;

      const vector<real_type>::view
      wavelengths() const;

      const age_line<real_type>&
      bin_ages() const;

   protected:

      void
      _load_waves( const string& filename );

      void
      _load_ssp( const string& filename );

   protected:

      unsigned _num_metals;
      vector<real_type> _waves;
      vector<real_type> _spec;
      age_line<real_type> _age_bins;
   };

}

#endif
