#include <cstdio>
#include <cmath>
#include <fstream>
#include <boost/algorithm/string/trim.hpp>
#include <boost/tokenizer.hpp>
#include "skymaker.hh"

using namespace hpc;
namespace fs = boost::filesystem;

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

   skymaker::image::image()
   {
   }

   skymaker::image::image( unsigned index,
			   int sub_cone,
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
      setup( index, sub_cone, format, mag_field, min_mag, z_min, z_max,
	     origin_ra, origin_dec, fov_ra, fov_dec, width, height );
   }

   ///
   /// Setup an image.
   ///
   void
   skymaker::image::setup( unsigned index,
			   int sub_cone,
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
      _idx = index;
      _sub_cone = sub_cone;
      _format = format;
      _mag_field = mag_field;
      _min_mag = min_mag;
      _z_min = z_min;
      _z_max = z_max;
      _origin_ra = to_radians( origin_ra );
      _origin_dec = to_radians( origin_dec );
      _fov_ra = to_radians( fov_ra );
      _fov_dec = to_radians( fov_dec );
      _width = width;
      _height = height;
      _cnt = 0;

      // Calculate the required scale factors.
      _scale_x = 0.5*_width/tan( 0.5*_fov_ra );
      _scale_y = 0.5*_height/tan( 0.5*_fov_dec );
   }

   void
   skymaker::image::add_galaxy( const tao::galaxy& gal,
				unsigned idx )
   {
      // Read magnitude and redshift from galaxy.
      real_type mag = gal.values<real_type>( _mag_field )[idx];
      real_type redshift = gal.values<real_type>( "redshift_cosmological" )[idx];

      // Only process if within magnitude and redshift limits.
      if( mag >= _min_mag &&
	  redshift >= _z_min && redshift <= _z_max )
      {
         // Convert the cartesian coordiantes to right-ascension and
         // declination.
         real_type ra, dec;
         numerics::cartesian_to_ecs( gal.values<real_type>( "pos_x" )[idx],
                                     gal.values<real_type>( "pos_y" )[idx],
                                     gal.values<real_type>( "pos_z" )[idx],
                                     ra,
                                     dec );
         LOGDLN( "Converted to (", ra, ", ", dec, ")" );

	 // Filter out any RA or DEC outside our FoV.
	 if( fabs( ra - _origin_ra ) <= 0.5*_fov_ra && fabs( dec - _origin_dec ) <= 0.5*_fov_dec )
	 {
	    // Now convert to pixel coordinates.
	    real_type x, y;
	    numerics::gnomonic_projection( ra, dec,
					   _origin_ra, _origin_dec,
					   x, y );
	    LOGDLN( "Now to (", x, ", ", y, ")" );

	    // To convert to pixel coordinates use the scaling factor
	    // in each dimension and offset by half image size.
	    x = x*_scale_x + 0.5*_width;
	    y = y*_scale_y + 0.5*_height;
	    // ASSERT( x >= 0.0 && x <= _width, "Bad X pixel calculation." );
	    // ASSERT( y >= 0.0 && y <= _height, "Bad Y pixel calculation." );
	    LOGDLN( "Pixel coordinates: ", x, ", ", y );

            _list_file << "200 " << x << " " << y << " " << mag;

            // // Try and extract some more values.
            // real_type disk_scale_radius = gal.values<real_type>( "diskscaleradius" )[idx];
            // real_type total_lum = gal.values<real_type>( "total_luminosity" )[idx];
            // real_type bulge_lum = gal.values<real_type>( "bulge_luminosity" )[idx];

            // // Do some calculations.
            // real_type ang_diam_dist = numerics::redshift_to_angular_diameter_distance( gal.values<real_type>( "redshift" )[idx] );
            // real_type bulge_to_total = bulge_lum/total_lum;
            // real_type bulge_equiv_radius = atan( 0.5*bulge_to_total*disk_scale_radius/ang_diam_dist )*206264.806;
            // real_type disk_scale_length = atan( disk_scale_radius/ang_diam_dist )*206264.806;

	    // // std::cout << ang_diam_dist << ", " << disk_scale_radius << ", " << disk_scale_length << "\n";

            // _list_file << " " << bulge_to_total;
            // _list_file << " " << bulge_equiv_radius;
            // _list_file << " 0.8";
	    // _list_file << " " << generate_uniform<real_type>( 0, 360 ) << " ";
            // _list_file << " " << disk_scale_length;
            // _list_file << " 0.2";
	    // _list_file << " " << generate_uniform<real_type>( 0, 360 );
	    _list_file << "\n";

            ++_cnt;
         }
      }
   }

   void
   skymaker::image::render( const fs::path& output_dir,
			    bool keep_files )
   {
      // Close the list file.
      _list_file.close();

      // Merge list files.
      string master_filename;
      if( mpi::comm::world.rank() == 0 )
      {
	 master_filename = "tao_sky.master." + index_string( _idx ) + ".list";
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

	 // Rename the output file.
	 fs::path target = "image." + index_string( _sub_cone ) + "." + index_string( _idx ) + ".fits";
	 target = output_dir/target;
	 fs::rename( "sky.fits", target );
      }
      mpi::comm::world.barrier();

      // Delete the files we used.
      if( !keep_files )
      {
	 ::remove( master_filename.c_str() );
	 ::remove( _list_filename.c_str() );
	 ::remove( _conf_filename.c_str() );
      }
   }

   void
   skymaker::image::setup_list()
   {
      _list_filename = "tao_sky." + index_string( _idx ) + "." + mpi::rank_string() + ".list";
      LOGDLN( "Opening parameter file: ", _list_filename );
      _list_file.open( _list_filename, std::ios::out );
   }

   void
   skymaker::image::setup_conf()
   {
      _conf_filename ="tao_sky." + index_string( _idx ) + "." + mpi::rank_string() + ".conf";
      LOGDLN( "Opening config file: ", _conf_filename );
      std::ofstream file( _conf_filename, std::ios::out );
      file << "IMAGE_SIZE " << _width << "," << _height << "\n";
      file << "STARCOUNT_ZP 0.0\n";  // no auto stars
      file << "MAG_LIMITS 0.1 49.0\n"; // wider magnitude limits
      file << "ARM_COUNT 4\n";
      file << "ARM_THICKNESS 40\n";
      file << "ARM_POSANGLE 30\n";
   }

   ///
   /// Initialise the module.
   ///
   void
   skymaker::initialise( const options::xml_dict& global_dict )
   {
      LOG_ENTER();

      _read_options( global_dict );

      // Reset counter of each image.
      for( auto& img : _imgs )
      {
	 img.setup_list();
	 img.setup_conf();
      }

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
         process_galaxy( gal, ii );

      LOG_EXIT();
      _timer.stop();
   }

   void
   skymaker::finalise()
   {
      _timer.start();

      for( auto& img : _imgs )
	 img.render( _output_dir, _keep_files );

      _timer.stop();
   }

   void
   skymaker::process_galaxy( const tao::galaxy& galaxy,
                             unsigned idx )
   {
      _timer.start();

      for( auto& img : _imgs )
         img.add_galaxy( galaxy, idx );

      _timer.stop();
   }

   void
   skymaker::_read_options( const options::xml_dict& global_dict )
   {
      // Cache the dictionary.
      const options::xml_dict& dict = _dict;

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

         // Construct a new image with the contents.
	 if( exe )
	 {
	    _imgs.emplace_back(
	       ii++,
	       global_dict.get<int>( "subjobindex" ), sub.get<string>( "format", "FITS" ),
	       sub.get<string>( "mag_field" ), sub.get<real_type>( "min_mag", 7 ),
	       sub.get<real_type>( "z_min", 0 ), sub.get<real_type>( "z_max", 127 ),
	       sub.get<real_type>( "origin_ra" ), sub.get<real_type>( "origin_dec" ),
	       sub.get<real_type>( "fov_ra" ), sub.get<real_type>( "fov_dec" ),
	       sub.get<unsigned>( "width", 1024 ), sub.get<unsigned>( "height", 1024 )
	       );
	 }
      }

      // Flags.
      _keep_files = dict.get<bool>( "keep-files",false );
   }

}
