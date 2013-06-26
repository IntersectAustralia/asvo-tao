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
   skymaker::factory( const string& name,
		      pugi::xml_node base )
   {
      return new skymaker( name, base );
   }

   skymaker::skymaker( const string& name,
		       pugi::xml_node base )
      : module( name, base )
   {
   }

   skymaker::~skymaker()
   {
   }

   ///
   /// Setup an image.
   ///
   skymaker::image::setup( int sub_cone,
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
                           unsigned height )
   {
      _sub_cone = sub_cone;
      _format = format;
      _mag_field = mag_field;
      _min_mag = min_mag;
      _z_min = z_min;
      _z_max = z_max;
      _origin_ra = origin_ra*0.25*M_PI;
      _origin_dec = origin_dec*0.25*M_PI;
      _fov_ra = fov_ra*0.25*M_PI;
      _fov_dec = fov_dec*0.25*M_PI;
      _width = width;
      _height = height;
   }

   void
   skymaker::image::process_galaxy( const tao::galaxy& galaxy,
                                    unsigned idx,
                                    real_type magnitude )
   {
      // Only process if within magnitude limits.
      if( magnitude >= _min_mag )
      {
         // Convert the cartesian coordiantes to right-ascension and
         // declination.
         real_type ra, dec;
         numerics::cartesian_to_ecs( galaxy.values<real_type>( "pos_x" )[idx],
                                     galaxy.values<real_type>( "pos_y" )[idx],
                                     galaxy.values<real_type>( "pos_z" )[idx],
                                     ra,
                                     dec );
         LOGDLN( "Converted to (", ra, ", ", dec, ")" );

         // Now convert to pixel coordinates.
         real_type x, y;
         numerics::gnomonic_projection( ra, dec,
                                        _origin_ra, _origin_dec,
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
            real_type bulge_magnitude = galaxy.values<real_type>( _bulge_mag_field )[idx];
            real_type disk_scale_radius = galaxy.values<real_type>( "diskscaleradius" )[idx];
            real_type total_lum = galaxy.values<real_type>( "total_luminosity" )[idx];
            real_type bulge_lum = galaxy.values<real_type>( "bulge_luminosity" )[idx];

            // Do some calculations.
            real_type ang_diam_dist = numerics::redshift_to_angular_diameter_distance( galaxy.values<real_type>( "redshift" )[idx] );
            real_type bulge_to_total = bulge_lum/total_lum;
            real_type bulge_equiv_radius = atan( 0.5*bulge_to_total*disk_scale_radius/ang_diam_dist )*206264.806;
            real_type disk_scale_length = atan( disk_scale_radius/ang_diam_dist )*206264.806;

	    // std::cout << ang_diam_dist << ", " << disk_scale_radius << ", " << disk_scale_length << "\n";

            _list_file << " " << bulge_to_total;
            _list_file << " " << bulge_equiv_radius;
            _list_file << " 0.8";
	    _list_file << " " << generate_uniform<real_type>( 0, 360 ) << " ";
            _list_file << " " << disk_scale_length;
            _list_file << " 0.2";
	    _list_file << " " << generate_uniform<real_type>( 0, 360 ) << "\n";

            ++_cnt;
         }
      }
   }

   ///
   /// Initialise the module.
   ///
   void
   skymaker::initialise( const options::xml_dict& global_dict )
   {
      LOG_ENTER();

      _read_options( global_dict );
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

      // Walk over galaxies here.
      for( unsigned ii = 0; ii < gal.batch_size(); ++ii )
      {
         // Read magnitude from galaxy.
         real_type mag = gal.values<real_type>( _mag_field )[ii];

         // Perform the processing.
         process_galaxy( gal, ii, mag );
      }

      LOG_EXIT();
      _timer.stop();
   }

   void
   skymaker::finalise()
   {
      _timer.start();

      // Close the list file.
      _list_file.close();

      // Merge list files.
      string master_filename;
      if( mpi::comm::world.rank() == 0 )
      {
	 master_filename = "master_sky.list"; //tmpnam( NULL );
         ::remove( master_filename.c_str() );
      }
      mpi::comm::world.bcast( master_filename, 0 );
      LOGDLN( "Skymaker master filename: ", master_filename );
      mpi::comm::world.chain_recv<int>(); // wait for previous ranks to finish.
      std::ofstream master_file( master_filename, std::ofstream::out | std::ofstream::app );
      std::ifstream list_file( _list_filename );
      char ch;
      while( list_file.get( ch ) )
         master_file.put( ch );
      ASSERT( list_file.eof() );
      list_file.close();
      master_file.close();
      mpi::comm::world.chain_send<int>( 0 ); // flag next rank

      // Launch the external command, but only if we are rank zero.
      // TODO: Need a library call.
      if( mpi::comm::world.rank() == 0 )
      {
         string cmd = string( "sky " ) + master_filename + string( " -c " ) + _conf_filename;
         cmd += " > /dev/null";
         LOGDLN( "Running: ", cmd );
         ::system( cmd.c_str() );
      }
      mpi::comm::world.barrier();

      // Delete the files we used.
      ::remove( master_filename.c_str() );
      if( !_keep_files )
      {
	 ::remove( _list_filename.c_str() );
	 ::remove( _conf_filename.c_str() );
      }

      _timer.stop();
   }

   void
   skymaker::process_galaxy( const tao::galaxy& galaxy,
                             unsigned idx,
                             real_type magnitude )
   {
      _timer.start();

      for( auto& img : _imgs )
         img.process_galaxy( galaxy, idx, magnitude );

      _timer.stop();
   }

   void
   skymaker::_read_options( const options::xml_dict& global_dict )
   {
      // Cache the dictionary.
      const options::xml_dict& dict = _dict;

      // Get image list.
      auto imgs = dict.get_nodes( "images" );
      for( const auto& img : imgs )
      {
         // Create a sub XML dict.
         xml_dict sub( img.node() );

         // Construct a new image with the contents.
         _imgs.emplace_back(
            sub.get<int>( "sub_cone" ), sub.get<string>( "format" ),
            sub.get<string>( "mag_field" ), sub.get<real_type>( "min_mag" ),
            sub.get<real_type>( "z_min" ), sub.get<real_type>( "z_max" ),
            sub.get<real_type>( "origin_ra" ), sub.get<real_type>( "origin_dec" ),
            sub.get<real_type>( "fov_ra" ), sub.get<real_type>( "fov_dec" ),
            sub.get<unsigned>( "width" ), sub.get<unsigned>( "height" )
            );
      }

      // Flags.
      _keep_files = dict.get<bool>( "keep-files",false );
   }

   void
   skymaker::_setup_list()
   {
      std::stringstream filename;
      filename << "my_sky.list." << std::setfill( '0' ) << std::setw( 5 ) << mpi::comm::world.rank();
      _list_filename = _keep_files ? filename.str() : tmpnam( NULL );
      LOGDLN( "Opening parameter file: ", _list_filename );
      _list_file.open( _list_filename, std::ios::out );
   }

   void
   skymaker::_setup_conf()
   {
      // Only rank 0 sets up the configuration.
      if( mpi::comm::world.rank() == 0 )
      {
         _conf_filename = _keep_files ? "my_sky.conf" : tmpnam( NULL );
         LOGDLN( "Opening config file: ", _conf_filename );
         std::ofstream file( _conf_filename, std::ios::out );
         file << "IMAGE_SIZE " << _img_w << "," << _img_h << "\n";
         file << "STARCOUNT_ZP 0.0\n";  // no auto stars
         file << "MAG_LIMITS 0.1 49.0"; // wider magnitude limits
      }
   }
}
