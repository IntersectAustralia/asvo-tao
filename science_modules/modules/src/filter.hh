#ifndef tao_modules_filter_hh
#define tao_modules_filter_hh

#include "tao/base/base.hh"

class filter_suite;

namespace tao {
   using namespace hpc;

   ///
   ///
   ///
   class filter
      : public module
   {
      friend class ::filter_suite;

   public:

      typedef double real_type;

      static
      module*
      factory( const string& name );

   public:

      filter( const string& name = string() );

      ~filter();

      ///
      ///
      ///
      virtual
      void
      setup_options( options::dictionary& dict,
                     optional<const string&> prefix=optional<const string&>() );

      ///
      /// Initialise the module.
      ///
      virtual
      void
      initialise( const options::dictionary& dict,
                  optional<const string&> prefix=optional<const string&>() );

      ///
      /// Run the module.
      ///
      virtual
      void
      execute();

      ///
      ///
      ///
      void
      process_galaxy( const tao::galaxy& galaxy,
                      const vector<real_type>& spectra );

      ///
      ///
      ///
      const vector<real_type>::view
      magnitudes() const;

   protected:

      real_type
      _apparant_magnitude( real_type spectra,
                           real_type filter,
                           real_type vega,
                           real_type distance );

      void
      _prepare_spectra( const vector<real_type>::view& spectra,
                        numerics::spline<real_type>& spline );

      real_type
      _integrate( const numerics::spline<real_type>& filter,
                  const numerics::spline<real_type>& spectra );

      real_type
      _integrate( const numerics::spline<real_type>& spectra );

      void
      _gauss_quad( vector<real_type>::view crds,
                   vector<real_type>::view weights );

      void
      _read_options( const options::dictionary& dict,
                     optional<const string&> prefix=optional<const string&>() );

      void
      _read_wavelengths( const string& filename );

      void
      _load_filter( const string& filename );

      void
      _process_vega( const string& filename );

   protected:

      vector<real_type> _waves;
      vector<real_type>::view _spec;
      vector<numerics::spline<real_type>> _filters;
      vector<real_type> _filt_int;
      vector<real_type> _vega_int;
      vector<real_type> _vega_mag;
      vector<real_type> _app_mags;
      vector<real_type> _abs_mags;
      vector<string> _filter_names;
   };
}

#endif
