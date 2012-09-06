#ifndef tao_dust_dust_hh
#define tao_dust_dust_hh

#include "tao/base/module.hh"

namespace tao {

   ///
   ///
   ///
   class dust
      : public module
   {
   public:

      typedef double real_type;

   public:

      dust();

      ~dust();

      ///
      ///
      ///
      void
      setup_options( hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      ///
      ///
      ///
      void
      setup_options( hpc::options::dictionary& dict,
                     const char* prefix );

      ///
      /// Initialise the module.
      ///
      void
      initialise( const hpc::options::dictionary& dict,
                  hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      ///
      ///
      ///
      void
      initialise( const hpc::options::dictionary& dict,
                  const char* prefix );

      ///
      /// Run the module.
      ///
      void
      run();

      ///
      ///
      ///
      void
      process_galaxy( const soci::row& galaxy,
                      hpc::vector<real_type>::view spectra );

   protected:

      void
      _read_wavelengths();

      void
      _read_options( const hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

   protected:

      hpc::string _waves_filename;
      unsigned _num_spectra;
      hpc::vector<real_type> _waves; // the wavelengths of each spectral band
   };
}

#endif
