#ifndef tao_modules_skymaker_hh
#define tao_modules_skymaker_hh

#include <boost/filesystem.hpp>
#include "tao/base/base.hh"

namespace tao {
   namespace modules {
      using namespace hpc;
      namespace fs = boost::filesystem;

      class skymaker_image
      {
      public:

         static double const default_back_magnitude;
         static double const default_exposure_time;

      public:

         skymaker_image();

         skymaker_image( unsigned index,
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
                         unsigned height,
                         double back_mag = default_back_magnitude,
                         double exp_time = default_exposure_time );

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
                unsigned height,
                double back_mag = default_back_magnitude,
                double exp_time = default_exposure_time );

         void
         setup_list();

         void
         setup_conf();

         void
         add_galaxy( const tao::batch<real_type>& bat,
                     unsigned idx );

         void
         render( const fs::path& output_dir,
                 bool keep_files );

         const string&
         mag_field() const;

	 bool
	 okay() const;

      protected:

         unsigned _idx;
         string _list_filename;
         string _conf_filename;
         string _sky_filename;
         string _sky_list_filename;
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
         double _back_mag; // background magnitude
         double _exp_time; // exposure time in seconds
         unsigned _cnt;
	 bool _okay;
      };

      template< class Backend >
      class skymaker
         : public module<Backend>
      {
      public:

         typedef Backend backend_type;
         typedef module<backend_type> module_type;
         typedef skymaker_image image_type;

         static
         module_type*
         factory( const string& name,
                  pugi::xml_node base )
         {
            return new skymaker( name, base );
         }

      public:

         skymaker( const string& name = string(),
                   pugi::xml_node base = pugi::xml_node() )
            : module_type( name, base )
         {
         }

         virtual
         ~skymaker()
         {
         }

         ///
         /// Initialise the module.
         ///
         virtual
         void
         initialise( const options::xml_dict& global_dict )
         {
            // Don't initialise if we're already doing so.
            if( this->_init )
               return;
            module_type::initialise( global_dict );

            auto timer = this->timer_start();
            LOGILN( "Initialising skymaker module.", setindent( 2 ) );

            // Read options and create images.
            _read_options( global_dict );

            // Prepare each image.
            for( auto& img : _imgs )
            {
               img.setup_list();
               img.setup_conf();
            }
	    LOGILN( "Found ", _imgs.size(), " images." );

            LOGILN( "Done.", setindent( -2 ) );
         }

         ///
         /// Run the module.
         ///
         virtual
         void
         execute()
         {
            auto timer = this->timer_start();

            // Grab the batch from the parent object.
            tao::batch<real_type>& bat = this->parents().front()->batch();

            // Walk over galaxies here.
            for( unsigned ii = 0; ii < bat.size(); ++ii )
               process_galaxy( bat, ii );
         }

         virtual
         void
         finalise()
         {
            auto timer = this->timer_start();
            LOGILN( "Rendering skymaker images.", setindent( 2 ) );

	    bool okay = true;
            for( auto& img : _imgs )
	    {
               img.render( _output_dir, _keep_files );
	       if( !img.okay() )
		  okay = false;
	    }

	    // Check for any failures and write a report to output.
	    if( !okay )
	    {
	       std::ofstream outf( (_output_dir/"image_errors.txt").string() );
	       outf << "There were errors generating one or more images, ";
	       outf << "some images may be missing or corrupted.\n";
	    }

            LOGILN( "Done.", setindent( -2 ) );
         }

         void
         process_galaxy( const tao::batch<real_type>& bat,
                         unsigned idx )
         {
            auto timer = this->timer_start();
            for( auto& img : _imgs )
               img.add_galaxy( bat, idx );
         }

      protected:

         void
         _read_options( const options::xml_dict& global_dict )
         {
            // Cache the dictionary.
            const options::xml_dict& dict = this->_dict;

            // Get the output path.
            _output_dir = global_dict.get<string>( "outputdir" );

            // Get image list.
            auto imgs = dict.get_nodes( "images/item" );
            unsigned ii = 0;
            for( const auto& img : imgs )
            {
               // Create a sub XML dict.
               options::xml_dict sub( img.node() );

               // Sub-cone can be an integer or "ALL".
               string sc = sub.get<string>( "sub_cone", "ALL" );
               bool exe = false;
               if( sc == "ALL" )
                  exe = true;
               else
               {
                  int sc_val = boost::lexical_cast<int>( sc );
                  if( sc_val == global_dict.get<int>( "subjobindex" ) )
                     exe = true;
               }

               // Minimum magnitude can be "none" or a real value.
               optional<real_type> min_mag = none;
               {
                  string val_str = sub.get<string>( "min_mag", "None" );
                  if( val_str != "None" )
                     min_mag = boost::lexical_cast<real_type>( val_str );
               }

               // Construct a new image with the contents.
               if( exe )
               {
                  _imgs.emplace_back(
                     ii++,
                     global_dict.get<int>( "subjobindex" ), sub.get<string>( "format", "FITS" ),
                     sub.get<string>( "mag_field" ), min_mag,
                     sub.get<real_type>( "z_min", 0 ), sub.get<real_type>( "z_max", 127 ),
                     sub.get<real_type>( "origin_ra" ), sub.get<real_type>( "origin_dec" ),
                     sub.get<real_type>( "fov_ra" ), sub.get<real_type>( "fov_dec" ),
                     sub.get<unsigned>( "width", 1024 ), sub.get<unsigned>( "height", 1024 ),
                     sub.get<double>( "back_mag", image_type::default_back_magnitude ),
                     sub.get<double>( "exp_time", image_type::default_exposure_time )
                     );
                  LOGILN( "Added image for magnitude field: ", _imgs.back().mag_field() );
               }
            }

            // Flags.
            _keep_files = dict.get<bool>( "keep-files",false );
         }

      protected:

         list<image_type> _imgs;
         fs::path _output_dir;
         bool _keep_files;
      };

   }
}

#endif
