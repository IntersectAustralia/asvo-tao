#include <cstdio>
#include <cmath>
#include <fstream>
#include <boost/algorithm/string/trim.hpp>
#include <boost/tokenizer.hpp>
// #include <boost/process.hpp>
#include "skymaker.hh"

using namespace hpc;
namespace fs = boost::filesystem;

namespace tao {
   namespace modules {

      double const skymaker_image::default_back_magnitude = 20.0;
      double const skymaker_image::default_exposure_time = 300.0;

      skymaker_image::skymaker_image()
      {
      }

      skymaker_image::skymaker_image( unsigned index,
                                      int sub_cone,
                                      const string& format,
                                      const string& mag_field,
                                      optional<real_type> min_mag,
                                      optional<real_type> max_mag,
                                      real_type z_min,
                                      real_type z_max,
                                      real_type origin_ra,
                                      real_type origin_dec,
                                      real_type fov_ra,
                                      real_type fov_dec,
                                      unsigned width,
                                      unsigned height,
                                      double back_mag,
                                      double exposure_time )
      {
         setup( index, sub_cone, format, mag_field, min_mag, max_mag, z_min, z_max,
                origin_ra, origin_dec, fov_ra, fov_dec, width, height,
                back_mag, exposure_time );
      }

      ///
      /// Setup an image.
      ///
      void
      skymaker_image::setup( unsigned index,
                             int sub_cone,
                             const string& format,
                             const string& mag_field,
                             optional<real_type> min_mag,
                             optional<real_type> max_mag,
                             real_type z_min,
                             real_type z_max,
                             real_type origin_ra,
                             real_type origin_dec,
                             real_type fov_ra,
                             real_type fov_dec,
                             unsigned width,
                             unsigned height,
                             double back_mag,
                             double exposure_time )
      {
         LOGILN( "Setting up Skykmaker image.", setindent( 2 ) );

         _idx = index;
         _sub_cone = sub_cone;
         _format = format;
         _mag_field = mag_field;
         _min_mag = min_mag;
         _max_mag = max_mag;
         _z_min = z_min;
         _z_max = z_max;
         _origin_ra = to_radians( origin_ra );
         _origin_dec = to_radians( origin_dec );
         _fov_ra = to_radians( fov_ra );
         _fov_dec = to_radians( fov_dec );
         _width = width;
         _height = height;
         _back_mag = back_mag;
         _exp_time = exposure_time;
         _cnt = 0;

         // Calculate the required scale factors.
         _scale_x = 0.5*_width/tan( 0.5*_fov_ra );
         _scale_y = 0.5*_height/tan( 0.5*_fov_dec );

         LOGILN( "Magnitude field: ", _mag_field );
         LOGILN( "Background magnitude: ", _back_mag );
         LOGILN( "Exposure time: ", _exp_time );
         LOGILN( "Done.", setindent( -2 ) );
      }

      void
      skymaker_image::add_galaxy( const tao::batch<real_type>& bat,
                                  unsigned idx )
      {
         // Read magnitude and redshift from galaxy.
         real_type mag = bat.scalar<real_type>( _mag_field )[idx];
         real_type redshift = bat.scalar<real_type>( "redshift_cosmological" )[idx];

         // Only process if within magnitude and redshift limits.
         if( (!_min_mag || mag >= *_min_mag) &&
	     (!_max_mag || mag < *_max_mag) &&
             redshift >= _z_min && redshift <= _z_max )
         {
            // Convert the cartesian coordiantes to right-ascension and
            // declination.
            real_type ra, dec;
            numerics::cartesian_to_ecs( bat.scalar<real_type>( "posx" )[idx],
                                        bat.scalar<real_type>( "posy" )[idx],
                                        bat.scalar<real_type>( "posz" )[idx],
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
      skymaker_image::render( const fs::path& output_dir,
                              bool keep_files )
      {
         LOGILN( "Rendering image.", setindent( 2 ) );

         // Close the list file.
         _list_file.close();

         // Merge list files.
         string master_filename;
         if( mpi::comm::world.rank() == 0 )
         {
            master_filename = "tao_sky.master." + index_string( _sub_cone ) + "." + index_string( _idx ) + ".list";
	    if( fs::exists( master_filename ) )
	       fs::remove( master_filename );
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
            // Be sure the destination filename does not already exist.
	    if( fs::exists( _sky_filename ) )
	       fs::remove( _sky_filename );

            // Run Skymaker.
            string cmd = string( "sky " ) + master_filename + string( " -c " ) + _conf_filename;
            cmd += " > /dev/null";
            LOGDLN( "Running: ", cmd );
	    ::system( cmd.c_str() );

	    if( fs::exists( _sky_filename ) )
	    {
	       // Rename the output file.
	       fs::path target = "image." + index_string( _sub_cone ) + "." + index_string( _idx ) + ".fits";
	       target = output_dir/target;
	       fs::rename( _sky_filename, target );
	       _okay = true;
	    }
	    else
	    {
	       LOGILN( "There was an error running Skymaker on this system. Please \n"
		       "make sure the 'sky' binary is available in your path." );
	       _okay = false;
	    }
         }
         mpi::comm::world.barrier();

         // Delete the files we used.
         if( !keep_files )
         {
	    if( mpi::comm::world.rank() == 0 )
	       fs::remove( master_filename );
            fs::remove( _list_filename );
            fs::remove( _conf_filename );
            fs::remove( _sky_list_filename );
         }

         LOGILN( "Done.", setindent( -2 ) );
      }

      const string&
      skymaker_image::mag_field() const
      {
         return _mag_field;
      }

      bool
      skymaker_image::okay() const
      {
	 return _okay;
      }

      void
      skymaker_image::setup_list()
      {
         _list_filename = "tao_sky." + index_string( _sub_cone ) + "." + index_string( _idx ) + "." + mpi::rank_string() + ".list";
         LOGDLN( "Opening parameter file: ", _list_filename );
         _list_file.open( _list_filename, std::ios::out );
      }

      void
      skymaker_image::setup_conf()
      {
         if( mpi::comm::world.rank() == 0 )
         {
            _conf_filename ="tao_sky." + index_string( _sub_cone ) + "." + index_string( _idx ) + ".conf";
            _sky_filename = "tao_sky." + index_string( _sub_cone ) + "." + index_string( _idx ) + ".fits";
            _sky_list_filename = "tao_sky." + index_string( _sub_cone ) + "." + index_string( _idx ) + ".list";
            LOGDLN( "Opening config file: ", _conf_filename );
            std::ofstream file( _conf_filename, std::ios::out );
            file << "IMAGE_NAME " << _sky_filename << "\n";
            file << "IMAGE_SIZE " << _width << "," << _height << "\n";
            file << "STARCOUNT_ZP 0.0\n";  // no auto stars
            file << "MAG_LIMITS 0.1 49.0\n"; // wider magnitude limits
            file << "ARM_COUNT 4\n";
            file << "ARM_THICKNESS 40\n";
            file << "ARM_POSANGLE 30\n";
            file << "BACK_MAG " << _back_mag << "\n";
            file << "EXPOSURE_TIME " << _exp_time << "\n";
         }
      }

   }
}
