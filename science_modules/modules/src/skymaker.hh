#ifndef tao_modules_skymaker_hh
#define tao_modules_skymaker_hh

#include "tao/base/module.hh"

class skymaker_suite;

namespace tao {

   ///
   ///
   ///
   class skymaker
      : public module
   {
      friend class ::skymaker_suite;

   public:

      typedef double real_type;

   public:

      skymaker();

      ~skymaker();

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

      void
      add_galaxy( soci::row& galaxy,
                  real_type magnitude );

   protected:

      void
      _read_options( const hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix );

      void
      _setup_params();

   protected:

      hpc::string _params_filename;
      std::ofstream _params_file;
   };
}

#endif
