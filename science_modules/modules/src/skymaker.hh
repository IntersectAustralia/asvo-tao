#ifndef tao_modules_skymaker_hh
#define tao_modules_skymaker_hh

#include <boost/filesystem.hpp>
#include "tao/base/module.hh"

class skymaker_suite;

namespace tao {
   using namespace hpc;
   namespace fs = boost::filesystem;

   ///
   ///
   ///
   class skymaker
      : public module
   {
      friend class ::skymaker_suite;

   public:

      typedef double real_type;

      class image
      {
	 friend class ::skymaker_suite;

      public:

         image();

	 image( unsigned index,
		int sub_cone,
                const string& format,
                const string& mag_field,
                optional<real_type> min_mag,
                real_type z_min,
                real_type z_max,
                real_type origin_ra,
                real_type origin_dec,
                real_type fov_ra,
                real_type fov_dec,
                unsigned width,
                unsigned height );

	 void
	 setup( unsigned index,
		int sub_cone,
		const string& format,
		const string& mag_field,
		optional<real_type> min_mag,
		real_type z_min,
		real_type z_max,
		real_type origin_ra,
		real_type origin_dec,
		real_type fov_ra,
		real_type fov_dec,
		unsigned width,
		unsigned height );

	 void
	 setup_list();

	 void
	 setup_conf();

         void
         add_galaxy( const tao::galaxy& galaxy,
		     unsigned idx );

	 void
	 render( const fs::path& output_dir,
		 bool keep_files );

      protected:

	 unsigned _idx;
         string _list_filename;
	 string _conf_filename;
	 string _sky_filename;
         std::ofstream _list_file;
	 unsigned _sub_cone;
	 string _format;
         string _mag_field;
         optional<real_type> _min_mag;
	 real_type _z_min, _z_max;
	 real_type _origin_ra, _origin_dec;
	 real_type _fov_ra, _fov_dec;
         unsigned _width, _height;
	 real_type _scale_x, _scale_y;
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
                      unsigned idx );

   protected:

      void
      _read_options( const options::xml_dict& global_dict );

   protected:

      list<image> _imgs;
      fs::path _output_dir;
      bool _keep_files;
   };
}

#endif
