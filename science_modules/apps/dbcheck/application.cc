#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
#include <libhpc/logging/logging.hh>
#include <libhpc/h5/h5.hh>
#include <libhpc/containers/num.hh>
#include <tao/base/multidb_backend.hh>
#include "application.hh"

template< class T >
T
perc_diff( T x,
	   T y )
{
   T div = x;
   if( div == 0.0 )
      div = std::numeric_limits<T>::epsilon();
   return fabs( y - x )/div;
}

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

   void
   make_hdf5_types( hpc::h5::datatype& mem_type,
		    hpc::h5::datatype& file_type )
   {
      // Create memory type.
      mem_type.compound( sizeof(galaxy) );
      mem_type.insert( hpc::h5::datatype::native_int, "type", HOFFSET( galaxy, type ) );
      mem_type.insert( hpc::h5::datatype::native_llong, "galaxy index", HOFFSET( galaxy, galaxy_idx ) );
      mem_type.insert( hpc::h5::datatype::native_int, "halo index", HOFFSET( galaxy, halo_idx ) );
      mem_type.insert( hpc::h5::datatype::native_int, "friends-of-friends index", HOFFSET( galaxy, fof_halo_idx ) );
      mem_type.insert( hpc::h5::datatype::native_int, "tree index", HOFFSET( galaxy, tree_idx ) );
      mem_type.insert( hpc::h5::datatype::native_llong, "gobal galaxy index", HOFFSET( galaxy, global_index ) );
      mem_type.insert( hpc::h5::datatype::native_int, "descendant", HOFFSET( galaxy, descendant ) );
      mem_type.insert( hpc::h5::datatype::native_llong, "global descendant", HOFFSET( galaxy, global_descendant ) );
      mem_type.insert( hpc::h5::datatype::native_int, "snapshot", HOFFSET( galaxy, snapshot ) );
      mem_type.insert( hpc::h5::datatype::native_int, "central galaxy", HOFFSET( galaxy, central_gal ) );
      mem_type.insert( hpc::h5::datatype::native_float, "central galaxy virial mass", HOFFSET( galaxy, central_mvir ) );
      mem_type.insert( hpc::h5::datatype::native_float, "x position", HOFFSET( galaxy, pos[0] ) );
      mem_type.insert( hpc::h5::datatype::native_float, "y position", HOFFSET( galaxy, pos[1] ) );
      mem_type.insert( hpc::h5::datatype::native_float, "z position", HOFFSET( galaxy, pos[2] ) );
      mem_type.insert( hpc::h5::datatype::native_float, "x velocity", HOFFSET( galaxy, vel[0] ) );
      mem_type.insert( hpc::h5::datatype::native_float, "y velocity", HOFFSET( galaxy, vel[1] ) );
      mem_type.insert( hpc::h5::datatype::native_float, "z velocity", HOFFSET( galaxy, vel[2] ) );
      mem_type.insert( hpc::h5::datatype::native_float, "x spin", HOFFSET( galaxy, spin[0] ) );
      mem_type.insert( hpc::h5::datatype::native_float, "y spin", HOFFSET( galaxy, spin[1] ) );
      mem_type.insert( hpc::h5::datatype::native_float, "z spin", HOFFSET( galaxy, spin[2] ) );
      mem_type.insert( hpc::h5::datatype::native_int, "number of darkmatter particles", HOFFSET( galaxy, num_particles ) );
      mem_type.insert( hpc::h5::datatype::native_float, "virial mass", HOFFSET( galaxy, mvir ) );
      mem_type.insert( hpc::h5::datatype::native_float, "virial radius", HOFFSET( galaxy, rvir ) );
      mem_type.insert( hpc::h5::datatype::native_float, "virial velocity (?)", HOFFSET( galaxy, vvir ) );
      mem_type.insert( hpc::h5::datatype::native_float, "maximum velocity", HOFFSET( galaxy, vmax ) );
      mem_type.insert( hpc::h5::datatype::native_float, "velocity dispersion (?)", HOFFSET( galaxy, vel_disp ) );
      mem_type.insert( hpc::h5::datatype::native_float, "cold gas", HOFFSET( galaxy, cold_gas ) );
      mem_type.insert( hpc::h5::datatype::native_float, "stellar mass", HOFFSET( galaxy, stellar_mass ) );
      mem_type.insert( hpc::h5::datatype::native_float, "bulge mass", HOFFSET( galaxy, bulge_mass ) );
      mem_type.insert( hpc::h5::datatype::native_float, "hot gas", HOFFSET( galaxy, hot_gas ) );
      mem_type.insert( hpc::h5::datatype::native_float, "ejected mass", HOFFSET( galaxy, ejected_mass ) );
      mem_type.insert( hpc::h5::datatype::native_float, "blackhole mass", HOFFSET( galaxy, blackhole_mass ) );
      mem_type.insert( hpc::h5::datatype::native_float, "ics", HOFFSET( galaxy, ics ) );
      mem_type.insert( hpc::h5::datatype::native_float, "metals cold gas", HOFFSET( galaxy, metals_cold_gas ) );
      mem_type.insert( hpc::h5::datatype::native_float, "metals stellar mass", HOFFSET( galaxy, metals_stellar_mass ) );
      mem_type.insert( hpc::h5::datatype::native_float, "metals bulge mass", HOFFSET( galaxy, metals_bulge_mass ) );
      mem_type.insert( hpc::h5::datatype::native_float, "metals hot gas", HOFFSET( galaxy, metals_hot_gas ) );
      mem_type.insert( hpc::h5::datatype::native_float, "metals ejected mass", HOFFSET( galaxy, metals_ejected_mass ) );
      mem_type.insert( hpc::h5::datatype::native_float, "metals ics", HOFFSET( galaxy, metals_ics ) );
      mem_type.insert( hpc::h5::datatype::native_float, "star formation rate", HOFFSET( galaxy, sfr ) );
      mem_type.insert( hpc::h5::datatype::native_float, "bulge star formation rate", HOFFSET( galaxy, sfr_bulge ) );
      mem_type.insert( hpc::h5::datatype::native_float, "ics star formation rate", HOFFSET( galaxy, sfr_ics ) );
      mem_type.insert( hpc::h5::datatype::native_float, "disk scale radius", HOFFSET( galaxy, disk_scale_radius ) );
      mem_type.insert( hpc::h5::datatype::native_float, "cooling", HOFFSET( galaxy, cooling ) );
      mem_type.insert( hpc::h5::datatype::native_float, "heating", HOFFSET( galaxy, heating ) );
      mem_type.insert( hpc::h5::datatype::native_float, "last major merger", HOFFSET( galaxy, last_major_merger ) );
      mem_type.insert( hpc::h5::datatype::native_float, "outflow rate", HOFFSET( galaxy, outflow_rate ) );

      // Create file type.
      file_type.compound( 200 );
      file_type.insert( hpc::h5::datatype::std_i32be, "type", 0 );
      file_type.insert( hpc::h5::datatype::std_i64be, "galaxy index", 4 );
      file_type.insert( hpc::h5::datatype::std_i32be, "halo index", 12 );
      file_type.insert( hpc::h5::datatype::std_i32be, "friends-of-friends index", 16 );
      file_type.insert( hpc::h5::datatype::std_i32be, "tree index", 20 );
      file_type.insert( hpc::h5::datatype::std_i64be, "gobal galaxy index", 24 );
      file_type.insert( hpc::h5::datatype::std_i32be, "descendant", 32 );
      file_type.insert( hpc::h5::datatype::std_i64be, "global descendant", 36 );
      file_type.insert( hpc::h5::datatype::std_i32be, "snapshot", 44 );
      file_type.insert( hpc::h5::datatype::std_i32be, "central galaxy", 48 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "central galaxy virial mass", 52 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "x position", 56 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "y position", 60 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "z position", 64 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "x velocity", 68 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "y velocity", 72 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "z velocity", 76 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "x spin", 80 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "y spin", 84 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "z spin", 88 );
      file_type.insert( hpc::h5::datatype::std_i32be, "number of darkmatter particles", 92 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "virial mass", 96 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "virial radius", 100 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "virial velocity (?)", 104 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "maximum velocity", 108 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "velocity dispersion (?)", 112 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "cold gas", 116 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "stellar mass", 120 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "bulge mass", 124 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "hot gas", 128 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "ejected mass", 132 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "blackhole mass", 136 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "ics", 140 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "metals cold gas", 144 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "metals stellar mass", 148 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "metals bulge mass", 152 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "metals hot gas", 156 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "metals ejected mass", 160 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "metals ics", 164 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "star formation rate", 168 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "bulge star formation rate", 172 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "ics star formation rate", 176 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "disk scale radius", 180 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "cooling", 184 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "heating", 188 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "last major merger", 192 );
      file_type.insert( hpc::h5::datatype::ieee_f32be, "outflow rate", 196 );
   }

}

namespace tao {
   namespace dbcheck {

      application::application( int argc,
				char* argv[] )
	 : hpc::mpi::application( argc, argv )
      {
         LOG_PUSH( new hpc::mpi::logger( "dbcheck.log.", hpc::logging::info ) );
         EXCEPT( argc >= 2, "Insufficient arguments." );
         _sage_fn = argv[1];
      }

      void
      application::operator()()
      {
         // Declare some values.
         unsigned batch_size = 10000;

	 // Connect the backend.
	 tao::backends::multidb<real_type> be;
	 {
#include "credentials.hh"
	    vector<backends::multidb<real_type>::server_type> servers( 2 );
	    servers[0].dbname = "millennium_full_dist_v2";
	    servers[0].user = username;
	    servers[0].passwd = password;
	    servers[0].host = string( "tao01.hpc.swin.edu.au" );
	    servers[0].port = 3306;
	    servers[1].dbname = "millennium_full_dist_v2";
	    servers[1].user = username;
	    servers[1].passwd = password;
	    servers[1].host = string( "tao02.hpc.swin.edu.au" );
	    servers[1].port = 3306;
	    be.connect( servers.begin(), servers.end() );
	 }

	 // Setup simulation.
	 be.load_simulation();

         // Get a list of all tables.
	 unsigned num_tables = be.num_tables();

	 // Open the HDF5 file.
	 hpc::h5::file file( _sage_fn, H5F_ACC_RDONLY );
	 hpc::h5::dataset gal_dset( file, "galaxies" );
	 hpc::h5::datatype mem_type, file_type;
	 sage::make_hdf5_types( mem_type, file_type );

	 // Need storage for all values.
	 std::vector<unsigned long long> gids( batch_size );
	 std::vector<double> posx( batch_size ), posy( batch_size ), posz( batch_size ), mass( batch_size );
	 std::vector<sage::galaxy> gals( batch_size );

	 // Begin iterating over tables.
	 unsigned start = (rank()*num_tables)/this->size();
	 unsigned finish = ((rank() + 1)*num_tables)/this->size();
	 for( unsigned ii = start; ii < finish; ++ii )
	 {
	    auto tbl = be.table( ii );
	    LOGBLOCKI( "Processing table: ", tbl.name() );

	    // Repeat until we're out of galaxies in the table.
	    unsigned long long offs = 0;
	    do
	    {
	       // Process batches of galaxies at a time.
	       LOGDLN( "Querying database." );
	       gids.resize( batch_size );
	       posx.resize( batch_size );
	       posy.resize( batch_size );
	       posz.resize( batch_size );
	       mass.resize( batch_size );
	       std::string query = "SELECT globalindex, posx, posy, posz, stellarmass FROM " + tbl.name() + " LIMIT :1 OFFSET :2";
	       be.session( tbl.name() ) << query,
		  soci::use( batch_size ), soci::use( offs ),
		  soci::into( gids ),
		  soci::into( posx ), soci::into( posy ), soci::into( posz ),
		  soci::into( mass );
	       LOGDLN( "Number of galaxies in batch: ", gids.size() );

	       // Load elements from the galaxy dataset.
	       LOGDLN( "Loading from HDF5." );
	       hpc::h5::dataspace mem_space, file_space;
	       mem_space.create( gids.size() );
	       gal_dset.space( file_space );
	       file_space.select_elements2( gids );
	       gal_dset.read( gals.data(), mem_type, mem_space, file_space );

	       // Compare each entry.
	       for( unsigned ii = 0; ii < gids.size(); ++ii )
	       {
		  EXCEPT( perc_diff<double>( posx[ii], gals[ii].pos[0] ) < 1e-4,
			  "X positions don't match: ", posx[ii], " != ", gals[ii].pos[0] );
		  EXCEPT( perc_diff<double>( posy[ii], gals[ii].pos[1] ) < 1e-4,
			  "Y positions don't match: ", posy[ii], " != ", gals[ii].pos[1] );
		  EXCEPT( perc_diff<double>( posz[ii], gals[ii].pos[2] ) < 1e-4,
			  "Z positions don't match: ", posz[ii], " != ", gals[ii].pos[2] );

		  EXCEPT( perc_diff<double>( mass[ii], gals[ii].stellar_mass ) < 1e-4,
			  "Stellar masses don't match: ", mass[ii], " != ", gals[ii].stellar_mass );

		  EXCEPT( posx[ii] >= tbl.min()[0] && posx[ii] <= tbl.max()[0] &&
			  posy[ii] >= tbl.min()[1] && posy[ii] <= tbl.max()[1] &&
			  posz[ii] >= tbl.min()[2] && posz[ii] <= tbl.max()[2],
			  "Galaxy outside table boundary." );
	       }

	       // Move to the next offset.
	       offs += gids.size();
	    }
	    while( gids.size() == batch_size );
	 }
      }

   }
}
