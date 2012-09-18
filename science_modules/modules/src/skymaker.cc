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
      dict.add_option( new options::real( "origin_ra", 0.25*M_PI ), prefix );
      dict.add_option( new options::real( "origin_dec", 0.25*M_PI ), prefix );
      dict.add_option( new options::real( "focal_x", 1.0 ), prefix );
      dict.add_option( new options::real( "focal_y", 1.0 ), prefix );
      dict.add_option( new options::real( "image_offset_x", 0.0 ), prefix );
      dict.add_option( new options::real( "image_offset_y", 0.0 ), prefix );
      dict.add_option( new options::real( "pixel_width", 1.0 ), prefix );
      dict.add_option( new options::real( "pixel_height", 1.0 ), prefix );
      dict.add_option( new options::real( "min_mag", 7.0 ), prefix );
      dict.add_option( new options::real( "max_mag", 50.0 ), prefix );
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

      // Reset counter.
      _cnt = 0;

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

      // Launch the external command, but only if we are rank zero.
      // TODO: Need a library call.
      if( mpi::comm::world.rank() == 0 )
      {
         string cmd = string( "sky " ) + _list_filename + string( " -c " ) + _conf_filename;
         cmd += " > /dev/null";
         LOGLN( "Running: ", cmd );
         ::system( cmd.c_str() );
      }
      mpi::comm::world.barrier();

      // Delete the files we used.
      ::remove( _list_filename.c_str() );
      ::remove( _conf_filename.c_str() );
   }

   void
   skymaker::add_galaxy( const tao::galaxy& galaxy,
                         real_type magnitude )
   {
      // Only process if within magnitude limits.
      if( magnitude >= _min_mag && magnitude <= _max_mag )
      {
         // Convert the cartesian coordiantes to right-ascension and
         // declination.
         real_type ra, dec;
         numerics::cartesian_to_ecs( galaxy.x(), galaxy.y(), galaxy.z(), ra, dec );
         LOGLN( "Converted to (", ra, ", ", dec, ")" );

         // Now convert to pixel coordinates.
         real_type x, y;
         numerics::gnomonic_projection( ra, dec,
                                        _ra0, _dec0,
                                        x, y );
         LOGLN( "Now to (", x, ", ", y, ")" );

         // Now, convert to pixel coordinates.
         // TODO: Do this properly.
         x = _foc_x*x/_pix_w + _img_x;
         y = _foc_y*y/_pix_h + _img_y;
         LOGLN( "Pixel coordinates: ", x, ", ", y );

         // If not outside image bounds, write to file.
         if( x >= 0.0 && x <= (real_type)_img_w &&
             y >= 0.0 && y <= (real_type)_img_h )
         {
            _list_file << "200 " << x << " " << y << " " << magnitude << "\n";
            ++_cnt;
         }

         // TODO: Include all the disk/bulge information.
      }
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

      // Get origin ra,dec.
      _ra0 = sub.get<unsigned>( "origin_ra" );
      _dec0 = sub.get<unsigned>( "origin_dec" );
      LOGLN( "Origin: ", _ra0, ", ", _dec0 );

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

      // Get magnitude limits.
      _min_mag = sub.get<real_type>( "min_mag" );
      _max_mag = sub.get<real_type>( "max_mag" );
      LOGLN( "Magnitude limits: ", _min_mag, ", ", _max_mag );
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
