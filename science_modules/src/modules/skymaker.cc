#include <cstdio>
#include <cmath>
#include <fstream>
#include <boost/algorithm/string/trim.hpp>
#include <boost/tokenizer.hpp>
#include <libhpc/mpi/helpers.hh>
#include <libhpc/numerics/coords.hh>
#include "skymaker.hh"

#define AUTO_BACK_MAG std::numeric_limits<double>::infinity()

namespace tao {
   namespace modules {

      namespace mpi = hpc::mpi;

      double const skymaker_image::default_back_magnitude = AUTO_BACK_MAG;
      double const skymaker_image::default_exposure_time = 300.0;

      skymaker_image::skymaker_image()
         : _okay( true )
      {
      }

      skymaker_image::skymaker_image( unsigned index,
                                      int sub_cone,
                                      const std::string& format,
                                      const std::string& mag_field,
                                      boost::optional<real_type> min_mag,
                                      boost::optional<real_type> max_mag,
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
         : _okay( true )
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
                             const std::string& format,
                             const std::string& mag_field,
                             boost::optional<real_type> min_mag,
                             boost::optional<real_type> max_mag,
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
	 hpc::to_lower( (std::string&)_mag_field );
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
         if( back_mag == AUTO_BACK_MAG )
         {
            _auto_back_mag = true;
            _back_mag = 0.0;
         }
         else
         {
            _auto_back_mag = false;
            _back_mag = back_mag;
         }
	 _back_mag_cnt = 0.0;
         _exp_time = exposure_time;
         _cnt = 0;

         // Calculate the required scale factors.
         _scale_x = 0.5*_width/tan( 0.5*_fov_ra );
         _scale_y = 0.5*_height/tan( 0.5*_fov_dec );

	 LOGILN( "Magnitude field: ", _mag_field );
	 LOGILN( "Minimum magnitude: ", (_min_mag ? boost::lexical_cast<std::string>( *_min_mag ) : "none") );
	 LOGILN( "Maximum magnitude: ", (_max_mag ? boost::lexical_cast<std::string>( *_max_mag ) : "none") );
	 LOGILN( "Minimum redshift: ", _z_min );
	 LOGILN( "Maximum redshift: ", _z_max );
         LOGILN( "Magnitude field: ", _mag_field );
#ifndef NLOG
         LOGI( "Background magnitude: " );
         if( _auto_back_mag )
            LOGILN( "auto" );
         else
            LOGILN( _back_mag );
#endif
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
	    real_type ra = to_radians( bat.scalar<real_type>( "ra" )[idx] );
            real_type dec = to_radians( bat.scalar<real_type>( "dec" )[idx] );

            // Filter out any RA or DEC outside our FoV.
            if( fabs( ra - _origin_ra ) <= 0.5*_fov_ra && fabs( dec - _origin_dec ) <= 0.5*_fov_dec )
            {
               // Now convert to pixel coordinates.
               real_type x, y;
               hpc::num::gnomonic_projection( ra, dec,
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

               // Update the back magnitude if requested.
               if( _auto_back_mag && mag < 50.0 )
	       {
		  _back_mag += mag;
		  _back_mag_cnt += 1.0;
	       }

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

         // If automatic, combine average magnitudes.
         if( _auto_back_mag )
	 {
            _back_mag = mpi::comm::world.all_reduce( _back_mag );
	    _back_mag_cnt = mpi::comm::world.all_reduce( _back_mag_cnt );
	    _back_mag /= (double)_back_mag_cnt;
	    LOGILN( "Average background magnitdue: ", _back_mag );
	 }

         // Merge list files.
         std::string master_filename;
         if( mpi::comm::world.rank() == 0 )
         {
            master_filename = "tao_sky.master." + hpc::index_string( _sub_cone ) + "." + hpc::index_string( _idx ) + ".list";
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

            // Prepare the configuration file.
            setup_conf();

            // Run Skymaker.
            std::string cmd = std::string( "sky " ) + master_filename + std::string( " -c " ) + _conf_filename;
            cmd += " > /dev/null";
            LOGDLN( "Running: ", cmd );
	    ::system( cmd.c_str() );

	    if( fs::exists( _sky_filename ) )
	    {
	       // Rename the output file.
	       fs::path target = "image." + hpc::index_string( _sub_cone ) + "." + hpc::index_string( _idx ) + ".fits";
	       target = output_dir/target;
	       fs::rename( _sky_filename, target );
	       _okay = true;
	    }
	    else
	    {
	       LOGILN( "There was an error running Skymaker." );
	       _okay = false;
	    }
         }
         mpi::comm::world.barrier();
         mpi::comm::world.bcast( _okay, 0 );

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

      const std::string&
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
         _list_filename = "tao_sky." + hpc::index_string( _sub_cone ) + "." + hpc::index_string( _idx ) + "." + mpi::rank_string() + ".list";
         LOGDLN( "Opening parameter file: ", _list_filename );
         _list_file.open( _list_filename, std::ios::out );
      }

      void
      skymaker_image::setup_conf()
      {
         if( mpi::comm::world.rank() == 0 )
         {
            _conf_filename ="tao_sky." + hpc::index_string( _sub_cone ) + "." + hpc::index_string( _idx ) + ".conf";
            _sky_filename = "tao_sky." + hpc::index_string( _sub_cone ) + "." + hpc::index_string( _idx ) + ".fits";
            _sky_list_filename = "tao_sky." + hpc::index_string( _sub_cone ) + "." + hpc::index_string( _idx ) + ".list";
            LOGDLN( "Opening config file: ", _conf_filename );
            std::ofstream file( _conf_filename, std::ios::out );
            file << "IMAGE_NAME " << _sky_filename << "\n";
            file << "IMAGE_SIZE " << _width << "," << _height << "\n";
            file << "SEEING_TYPE NONE\n";
            file << "AUREOLE_RADIUS 0\n";
            file << "STARCOUNT_ZP 0.0\n";  // no auto stars
            file << "MAG_LIMITS 0.1 49.0\n"; // wider magnitude limits
            file << "ARM_COUNT 0\n";
            file << "ARM_THICKNESS 40\n";
            file << "ARM_POSANGLE 30\n";
            file << "BACK_MAG " << _back_mag << "\n";
            file << "EXPOSURE_TIME " << _exp_time << "\n";
         }
      }

   }
}
