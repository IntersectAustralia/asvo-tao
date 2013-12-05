#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <soci/soci.h>
#include <soci/postgresql/soci-postgresql.h>
#include <libhpc/logging/logging.hh>
#include <libhpc/h5/h5.hh>
#include <libhpc/containers/num.hh>
#include "application.hh"

namespace sage {

   struct galaxy
   {
      int       type;
      long long galaxy_idx;
      int       halo_idx;
      int       fof_halo_idx;
      int       tree_idx;

      // LUKE: See struct GALAXY.
      long long global_index;
      int       descendant;
      long long global_descendant;

      int       snapshot;
      int       central_gal;
      float     central_mvir;

      // properties of subhalo at the last time this galaxy was a central galaaxy 
      float pos[3];
      float vel[3];
      float spin[3];
      int   num_particles;
      float mvir;
      float rvir;
      float vvir;
      float vmax;
      float vel_disp;

      // baryonic reservoirs 
      float cold_gas;
      float stellar_mass;
      float bulge_mass;
      float hot_gas;
      float ejected_mass;
      float blackhole_mass;
      float ics;

      // metals
      float metals_cold_gas;
      float metals_stellar_mass;
      float metals_bulge_mass;
      float metals_hot_gas;
      float metals_ejected_mass;
      float metals_ics;

      // misc 
      float sfr;
      float sfr_bulge;
      float sfr_ics;
      float disk_scale_radius;
      float cooling;
      float heating;

      float last_major_merger;
      float outflow_rate;
   };

}

namespace tao {
   namespace dbcheck {

      application::application( int argc,
				char* argv[] )
	 : hpc::mpi::application( argc, argv )
      {
         LOG_PUSH( new hpc::logging::stdout( 0 ) );
         EXCEPT( argc >= 7, "Insufficient arguments." );
         _host = argv[1];
         _port = boost::lexical_cast<uint16_t>( argv[2] );
         _dbname = argv[3];
         _user = argv[4];
         _passwd = argv[5];
         _sage_fn = argv[6];
      }

      void
      application::operator()()
      {
         // Declare some values.
         unsigned batch_size = 100;

         // Connect to the database.
         soci::session sql(
            boost::str(
               boost::format( "host=%1% port=%2% dbname=%3% user=%4% passwd=%5%")
               % _host % _port % _dbname % _user % _passwd
               )
            );

         // Get a list of all tables.
         std::vector<std::string> tables;
         {
            unsigned size;
            sql << "SELECT COUNT(*) FROM summary", soci::into( size );
            tables.resize( size );
            sql << "SELECT tablename FROM summary", soci::into( tables );
         }
         LOGILN( "Tables: ", tables );

         // Open the HDF5 file.
         hpc::h5::file file( _sage_fn, H5F_ACC_RDONLY );
         hpc::h5::dataset gal_dset( file, "galaxies" );

         // Need storage for all values.
         std::vector<unsigned long long> gids( batch_size );
         std::vector<double> posx( batch_size ), posy( batch_size ), posz( batch_size ), mass( batch_size );
         std::vector<sage::galaxy> gals( batch_size );

         // Process each table.
         for( auto const& tbl : tables )
         {
            LOGBLOCKI( "Processing table: ", tbl );

            // Process batches of galaxies at a time.
            std::string query = "SELECT * FROM " + tbl;
            sql << query,
               soci::into( gids ),
               soci::into( posx ), soci::into( posy ), soci::into( posz ),
               soci::into( mass );

            // Load elements from the galaxy dataset.
            gal_dset.read<sage::galaxy>( gals, gids );

            // Compare each entry.
            for( unsigned ii = 0; ii < gids.size(); ++ii )
            {
               EXCEPT( hpc::num::approx<double>( posx[ii], gals[ii].pos[0], 1e-4 ),
                       "X positions don't match: ", posx[ii], gals[ii].pos[0] );
               EXCEPT( hpc::num::approx<double>( posy[ii], gals[ii].pos[1], 1e-4 ),
                       "Y positions don't match: ", posy[ii], gals[ii].pos[1] );
               EXCEPT( hpc::num::approx<double>( posz[ii], gals[ii].pos[2], 1e-4 ),
                       "Z positions don't match: ", posz[ii], gals[ii].pos[2] );

               EXCEPT( hpc::num::approx<double>( mass[ii], gals[ii].stellar_mass, 1e-4 ),
                       "Stellar masses don't match: ", mass[ii], gals[ii].stellar_mass );
            }
         }
      }

   }
}
