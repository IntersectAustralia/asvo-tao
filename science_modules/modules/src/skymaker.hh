#ifndef tao_modules_skymaker_hh
#define tao_modules_skymaker_hh

#include "tao/base/module.hh"

class skymaker_suite;

namespace tao {
   using namespace hpc;

   ///
   ///
   ///
   class skymaker
      : public module
   {
      friend class ::skymaker_suite;

   public:

      typedef double real_type;

      static
      module*
      factory( const string& name );

   public:

      skymaker( const string& name = string() );

      ~skymaker();



      ///
      /// Initialise the module.
      ///
      virtual
      void
      initialise( const options::xml_dict& dict,
                  optional<const string&> prefix = optional<const string&>() );

      ///
      /// Run the module.
      ///
      virtual
      void
      execute();

      virtual
      void
      finalise();

      void
      process_galaxy( const tao::galaxy& galaxy,
                      unsigned idx,
		      real_type magnitude );

   protected:

      void
      _read_options( const options::xml_dict& dict,
                     optional<const string&> prefix );

      void
      _setup_list();

      void
      _setup_conf();

   protected:

      string _mag_field, _bulge_mag_field;
      string _list_filename, _conf_filename;
      std::ofstream _list_file;
      unsigned _img_w, _img_h;
      real_type _ra0, _dec0;
      real_type _pix_w, _pix_h;
      real_type _img_x, _img_y;
      real_type _foc_x, _foc_y;
      real_type _min_mag, _max_mag;
      unsigned _cnt;
      bool _keep_files;
   };
}

#endif
