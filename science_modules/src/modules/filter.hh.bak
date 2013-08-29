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
      factory( const string& name,
	       pugi::xml_node base );

   public:

      filter( const string& name = string(),
	      pugi::xml_node base = pugi::xml_node() );

      ~filter();



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

      ///
      ///
      ///
      void
      process_galaxy( const tao::galaxy& galaxy,
                      const fibre<real_type>& total_spectra,
                      const fibre<real_type>& disk_spectra,
                      const fibre<real_type>& bulge_spectra );

      ///
      ///
      ///
      const vector<real_type>::view
      magnitudes() const;

   protected:

      void
      _process_spectra( const vector<real_type>::view& spectra,
                        real_type area,
			real_type& luminosity,
			fibre<real_type>& apparent_mags,
			fibre<real_type>& absolute_mags,
			unsigned gal_idx );

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
      _read_options( const options::xml_dict& global_dict );

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
      vector<string> _filter_names;

      fibre<real_type> _total_app_mags, _total_abs_mags;
      fibre<real_type> _disk_app_mags, _disk_abs_mags;
      fibre<real_type> _bulge_app_mags, _bulge_abs_mags;
      vector<real_type> _total_lum, _disk_lum, _bulge_lum;
   };
}

#endif
