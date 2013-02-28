#include <cstdio>
#include <cmath>
#include <fstream>
#include <boost/algorithm/string/trim.hpp>
#include <boost/tokenizer.hpp>
#include "skymaker.hh"

using namespace hpc;

namespace tao {

   // Factory function used to create a new skymaker module.
   module*
   skymaker::factory( const string& name )
   {
      return new skymaker( name );
   }

   skymaker::skymaker( const string& name )
      : module( name )
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
      dict.add_option( new options::string( "magnitude-field" ), prefix );
      dict.add_option( new options::string( "bulge-magnitude-field" ), prefix );
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

   void
   skymaker::execute()
   {
      _timer.start();
      LOG_ENTER();
      ASSERT( parents().size() == 1 );

      // Grab the galaxy from the parent object.
      tao::galaxy& gal = parents().front()->galaxy();

      // Read magnitude from galaxy.
      real_type mag = gal.value<real_type>( _mag_field );

      // Perform the processing.
      process_galaxy( gal, mag );

      LOG_EXIT();
      _timer.stop();
   }

   void
   skymaker::finalise()
   {
      _timer.start();

      // Close the list file.
      _list_file.close();

      // Launch the external command, but only if we are rank zero.
      // TODO: Need a library call.
      if( mpi::comm::world.rank() == 0 )
      {
         string cmd = string( "sky " ) + _list_filename + string( " -c " ) + _conf_filename;
         cmd += " > /dev/null";
         LOGDLN( "Running: ", cmd );
         ::system( cmd.c_str() );
      }
      mpi::comm::world.barrier();

      // Delete the files we used.
      ::remove( _list_filename.c_str() );
      ::remove( _conf_filename.c_str() );

      _timer.stop();
   }

   void
   skymaker::process_galaxy( const tao::galaxy& galaxy,
                             real_type magnitude )
   {
      _timer.start();

      // Only process if within magnitude limits.
      if( magnitude >= _min_mag && magnitude <= _max_mag )
      {
         // Convert the cartesian coordiantes to right-ascension and
         // declination.
         real_type ra, dec;
         numerics::cartesian_to_ecs( galaxy.x(), galaxy.y(), galaxy.z(), ra, dec );
         LOGDLN( "Converted to (", ra, ", ", dec, ")" );

         // Now convert to pixel coordinates.
         real_type x, y;
         numerics::gnomonic_projection( ra, dec,
                                        _ra0, _dec0,
                                        x, y );
         LOGDLN( "Now to (", x, ", ", y, ")" );

         // Now, convert to pixel coordinates.
         // TODO: Do this properly.
         x = _foc_x*x/_pix_w + _img_x;
         y = _foc_y*y/_pix_h + _img_y;
         LOGDLN( "Pixel coordinates: ", x, ", ", y );

         // If not outside image bounds, write to file.
         if( x >= 0.0 && x <= (real_type)_img_w &&
             y >= 0.0 && y <= (real_type)_img_h )
         {
            _list_file << "200 " << x << " " << y << " " << magnitude;

            // Try and extract some more values.
            real_type bulge_magnitude = galaxy.value<real_type>( _bulge_mag_field );
            real_type disc_scale_radius = galaxy.value<real_type>( "discscaleradius" )/0.71; // divided by h
            real_type stellar_mass = galaxy.value<real_type>( "stellarmass" )*1e10/0.71;
            real_type bulge_mass = galaxy.value<real_type>( "bulgemass" )*1e10/0.71;

            // Do some calculations.
            real_type ang_diam_dist = numerics::redshift_to_angular_diameter_distance( galaxy.redshift() );
            real_type bulge_to_total = bulge_magnitude/magnitude;
            real_type bulge_equiv_radius = atan( 0.5*(bulge_mass/stellar_mass)*disc_scale_radius/ang_diam_dist )*206264.806;
            real_type disc_scale_length = atan( disc_scale_radius/ang_diam_dist )*206264.806;

            std::cout << bulge_to_total << ", " << bulge_equiv_radius << ", " << disc_scale_length << "\n";

            _list_file << " " << bulge_magnitude/magnitude;
            _list_file << " " << bulge_equiv_radius;
            _list_file << " 0.8";
	    _list_file << generate_uniform<real_type>( 0, 360 ) << " ";
            _list_file << " " << disc_scale_length;
            _list_file << " 0.2";
	    _list_file << generate_uniform<real_type>( 0, 360 ) << "\n";

            ++_cnt;
         }

         // TODO: Include all the disk/bulge information.
      }

      _timer.stop();
   }

   void
   skymaker::_read_options( const options::dictionary& dict,
                            optional<const string&> prefix )
   {
      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      // What magnitude name are we interested in?
      _mag_field = sub.get<string>( "magnitude-field" );
      _bulge_mag_field = sub.get<string>( "bulge-magnitude-field" );

      // Get image dimensions.
      _img_w = sub.get<unsigned>( "image_width" );
      _img_h = sub.get<unsigned>( "image_height" );
      LOGDLN( "Image dimensions: ", _img_w, "x", _img_h );

      // Get origin ra,dec.
      _ra0 = sub.get<unsigned>( "origin_ra" );
      _dec0 = sub.get<unsigned>( "origin_dec" );
      LOGDLN( "Origin: ", _ra0, ", ", _dec0 );

      // Get focal scale.
      _foc_x = sub.get<real_type>( "focal_x" );
      _foc_y = sub.get<real_type>( "focal_y" );
      LOGDLN( "Image offset: ", _foc_x, ", ", _foc_y );

      // Get image offset.
      _img_x = sub.get<real_type>( "image_offset_x" );
      _img_y = sub.get<real_type>( "image_offset_y" );
      LOGDLN( "Image offset: ", _img_x, ", ", _img_y );

      // Get pixel dimensions.
      _pix_w = sub.get<real_type>( "pixel_width" );
      _pix_h = sub.get<real_type>( "pixel_height" );
      LOGDLN( "Pixel dimensions: ", _pix_w, "x", _pix_h );

      // Get magnitude limits.
      _min_mag = sub.get<real_type>( "min_mag" );
      _max_mag = sub.get<real_type>( "max_mag" );
      LOGDLN( "Magnitude limits: ", _min_mag, ", ", _max_mag );
   }

   void
   skymaker::_setup_list()
   {
      _list_filename = tmpnam( NULL );
      LOGDLN( "Opening parameter file: ", _list_filename );
      _list_file.open( _list_filename, std::ios::out );
   }

   void
   skymaker::_setup_conf()
   {
      _conf_filename = tmpnam( NULL );
      LOGDLN( "Opening config file: ", _conf_filename );
      std::ofstream file( _conf_filename, std::ios::out );
      file << "IMAGE_SIZE " << _img_w << "," << _img_h << "\n";
      file << "STARCOUNT_ZP 0.0\n";  // no auto stars
      file << "MAG_LIMITS 0.1 49.0"; // wider magnitude limits
   }
}
