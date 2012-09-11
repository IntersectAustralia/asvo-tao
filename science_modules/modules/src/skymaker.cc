#include <cstdio>
#include <cmath>
#include <fstream>
#include <boost/algorithm/string/trim.hpp>
#include <boost/tokenizer.hpp>
#include "skymaker.hh"

using namespace hpc;

namespace tao {

   skymaker::skymaker()
   {
   }

   skymaker::~skymaker()
   {
   }

   ///
   ///
   ///
   void
   skymaker::setup_options( options::dictionary& dict,
                            optional<const string&> prefix )
   {
      dict.add_option( new options::integer( "image_width", 1024 ), prefix );
      dict.add_option( new options::integer( "image_height", 1024 ), prefix );
      dict.add_option( new options::real( "focal_x", 1.0 ), prefix );
      dict.add_option( new options::real( "focal_y", 1.0 ), prefix );
      dict.add_option( new options::real( "image_offset_x", 0.0 ), prefix );
      dict.add_option( new options::real( "image_offset_y", 0.0 ), prefix );
      dict.add_option( new options::real( "pixel_width", 1.0 ), prefix );
      dict.add_option( new options::real( "pixel_height", 1.0 ), prefix );
   }

   ///
   ///
   ///
   void
   skymaker::setup_options( hpc::options::dictionary& dict,
                            const char* prefix )
   {
      setup_options( dict, string( prefix ) );
   }

   ///
   /// Initialise the module.
   ///
   void
   skymaker::initialise( const options::dictionary& dict,
                         optional<const string&> prefix )
   {
      LOG_ENTER();

      _read_options( dict, prefix );
      _setup_list();
      _setup_conf();

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   skymaker::initialise( const hpc::options::dictionary& dict,
                         const char* prefix )
   {
      initialise( dict, string( prefix ) );
   }

   void
   skymaker::run()
   {
      // Close the list file.
      _list_file.close();

      // Launch the external command.
      // TODO: Need a library call.
      string cmd = string( "sky " ) + _list_filename + string( " -c " ) + _conf_filename;
      cmd += " > /dev/null";
      LOGLN( "Running: ", cmd );
      ::system( cmd.c_str() );

      // Delete the files we used.
      ::remove( _list_filename.c_str() );
      ::remove( _conf_filename.c_str() );
   }

   void
   skymaker::add_galaxy( const tao::galaxy& galaxy,
                         real_type magnitude )
   {
      _list_file << "200" << " "; // 100 = star, 200 = galaxy

      // Convert the cartesian coordiantes to right-ascension and
      // declination.
      real_type ra, dec;
      numerics::cartesian_to_ecs( galaxy.x(), galaxy.y(), galaxy.z(), ra, dec );
      LOGLN( "Converted to (", ra, ", ", dec, ")" );

      // Now convert to pixel coordinates.
      real_type x, y;
      numerics::gnomonic_projection( ra, dec,
                                     0.25*M_PI, 0.0,
                                     x, y );
      LOGLN( "Now to (", x, ", ", y, ")" );

      // Now, convert to pixel coordinates.
      // TODO: Do this properly.
      x = _foc_x*x/_pix_w + _img_x;
      y = _foc_y*y/_pix_h + _img_y;
      LOGLN( "Pixel coordinates: ", x, ", ", y );

      // Write to file.
      _list_file << x << " " << y << " " << magnitude << "\n";

      // TODO: Include all the disk/bulge information.
   }

   void
   skymaker::_read_options( const options::dictionary& dict,
                            optional<const string&> prefix )
   {
      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      // Get image dimensions.
      _img_w = sub.get<unsigned>( "image_width" );
      _img_h = sub.get<unsigned>( "image_height" );
      LOGLN( "Image dimensions: ", _img_w, "x", _img_h );

      // Get focal scale.
      _foc_x = sub.get<real_type>( "focal_x" );
      _foc_y = sub.get<real_type>( "focal_y" );
      LOGLN( "Image offset: ", _foc_x, ", ", _foc_y );

      // Get image offset.
      _img_x = sub.get<real_type>( "image_offset_x" );
      _img_y = sub.get<real_type>( "image_offset_y" );
      LOGLN( "Image offset: ", _img_x, ", ", _img_y );

      // Get pixel dimensions.
      _pix_w = sub.get<real_type>( "pixel_width" );
      _pix_h = sub.get<real_type>( "pixel_height" );
      LOGLN( "Pixel dimensions: ", _pix_w, "x", _pix_h );
   }

   void
   skymaker::_setup_list()
   {
      _list_filename = tmpnam( NULL );
      LOGLN( "Opening parameter file: ", _list_filename );
      _list_file.open( _list_filename, std::ios::out );
   }

   void
   skymaker::_setup_conf()
   {
      _conf_filename = tmpnam( NULL );
      LOGLN( "Opening config file: ", _conf_filename );
      std::ofstream file( _conf_filename, std::ios::out );
      file << "IMAGE_SIZE " << _img_w << "," << _img_h << "\n";
      file << "STARCOUNT_ZP 0.0\n";  // no auto stars
      file << "MAG_LIMITS 0.1 49.0"; // wider magnitude limits
   }
}
