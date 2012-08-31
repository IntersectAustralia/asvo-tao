#ifndef tao_modules_filter_hh
#define tao_modules_filter_hh

#include "tao/base/module.hh"

namespace tao {

   ///
   ///
   ///
   class filter
      : public module
   {
   public:

      typedef double real_type;

   public:

      filter();

      ~filter();

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
      initialise( hpc::options::dictionary& dict,
                  const char* prefix );

      ///
      /// Run the module.
      ///
      void
      run();

      ///
      ///
      ///
      real_type
      process_galaxy( const soci::row& galaxy,
                      hpc::vector<real_type>::view spectra );

   protected:

      void
      _read_options( const hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      void
      _load_filter( const hpc::string& filename );

   protected:

      hpc::vector<hpc::vector<real_type>> _filters;
   };
}

#endif
