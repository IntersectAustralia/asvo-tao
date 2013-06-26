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

      class image {

         image();

         image( int sub_cone,
                const string& format,
                const string& mag_field,
                real_type min_mag,
                real_type z_min,
                real_type z_max,
                real_type origin_ra,
                real_type origin_dec,
                real_type fov_ra,
                real_type fov_dec,
                unsigned width,
                unsigned height );

         void
         process_galaxy( const tao::galaxy& galaxy,
                         unsigned idx,
                         real_type magnitude );

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
      };

      static
      module*
      factory( const string& name,
	       pugi::xml_node base );

   public:

      skymaker( const string& name = string(),
		pugi::xml_node base = pugi::xml_node() );

      ~skymaker();



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

      virtual
      void
      finalise();

      void
      process_galaxy( const tao::galaxy& galaxy,
                      unsigned idx,
		      real_type magnitude );

   protected:

      void
      _read_options( const options::xml_dict& global_dict );

      void
      _setup_list();

      void
      _setup_conf();

   protected:

      list<image> _imgs;
      bool _keep_files;
   };
}

#endif
