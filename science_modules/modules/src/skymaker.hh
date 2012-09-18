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
      add_galaxy( const tao::galaxy& galaxy,
                  real_type magnitude );

   protected:

      void
      _read_options( const hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix );

      void
      _setup_list();

      void
      _setup_conf();

   protected:

      hpc::string _list_filename, _conf_filename;
      std::ofstream _list_file;
      unsigned _img_w, _img_h;
      real_type _ra0, _dec0;
      real_type _pix_w, _pix_h;
      real_type _img_x, _img_y;
      real_type _foc_x, _foc_y;
      real_type _min_mag, _max_mag;
      unsigned _cnt;
   };
}

#endif
