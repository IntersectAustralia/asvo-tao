#ifndef tao_dust_dust_hh
#define tao_dust_dust_hh

#include "tao/base/module.hh"

namespace tao {
   using namespace hpc;

   ///
   ///
   ///
   class dust
      : public module
   {
   public:

      static
      module*
      factory( const string& name,
	       pugi::xml_node base );

   public:

      typedef double real_type;

   public:

     dust( const string& name = string(),
	   pugi::xml_node base = pugi::xml_node() );

      ~dust();

      ///
      /// Initialise the module.
      ///
      virtual
      void
      initialise( const options::xml_dict& global_dict );

      ///
      /// Run the module.
      ///
      void
      execute();

      ///
      ///
      ///
      void
      process_galaxy( tao::galaxy& galaxy,
		      fibre<real_type>& total_spectra,
		      fibre<real_type>& disk_spectra,
		      fibre<real_type>& bulge_spectra );

      void
      process_spectra( tao::galaxy& galaxy,
		       unsigned gal_idx,
		       real_type& sfr,
		       vector<real_type>::view spectra );

   protected:

      void
      _read_wavelengths( const string& filename );

      void
      _read_options( const options::xml_dict& global_dict );

   protected:

      string _waves_filename;
      vector<real_type> _waves; // the wavelengths of each spectral band
   };
}

#endif
