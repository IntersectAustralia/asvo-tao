#ifndef tao_modules_filter_hh
#define tao_modules_filter_hh

#include "tao/base/base.hh"

class filter_suite;

namespace tao {

   ///
   ///
   ///
   class filter
      : public module
   {
      friend class ::filter_suite;

   public:

      typedef double real_type;

   public:

      filter( const string& name = string() );

      ~filter();

      ///
      ///
      ///
      virtual
      void
      setup_options( hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      ///
      /// Initialise the module.
      ///
      virtual
      void
      initialise( const hpc::options::dictionary& dict,
                  hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

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
      const hpc::vector<real_type>::view
      magnitudes() const;

   protected:

      real_type
      _apparant_magnitude( real_type spectra,
                           real_type filter,
                           real_type vega,
                           real_type distance );

      void
      _prepare_spectra( const hpc::vector<real_type>::view& spectra,
                        hpc::numerics::spline<real_type>& spline );

      real_type
      _integrate( const hpc::numerics::spline<real_type>& filter,
                  const hpc::numerics::spline<real_type>& spectra );

      real_type
      _integrate( const hpc::numerics::spline<real_type>& spectra );

      void
      _gauss_quad( hpc::vector<real_type>::view crds,
                   hpc::vector<real_type>::view weights );

      void
      _read_options( const hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      void
      _read_wavelengths( const hpc::string& filename );

      void
      _load_filter( const hpc::string& filename );

      void
      _process_vega( const hpc::string& filename );

   protected:

      hpc::vector<real_type> _waves;
      hpc::vector<real_type>::view _spec;
      hpc::vector<hpc::numerics::spline<real_type>> _filters;
      hpc::vector<real_type> _filt_int;
      hpc::vector<real_type> _vega_int;
      hpc::vector<real_type> _vega_mag;
      hpc::vector<real_type> _mags;
   };
}

#endif
