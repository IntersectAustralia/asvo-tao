#include <cstdlib>
#include <iostream>
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>
#include <soci/soci.h>
#include <soci/postgresql/soci-postgresql.h>
#include <libhpc/libhpc.hh>

using namespace hpc;
using namespace soci;

// Parameters.
unsigned num_threads = 10;

struct galaxy_type
{
   int   type;
   long long   GalaxyIndex;
   int   HaloIndex;
   int   fof_idx;
   int   tree_idx;

   // LUKE: See struct GALAXY.
   long long  global_index;
   int        descendant;
   long long  global_descendant;

   int   snap;
   int   central_gal;
   float CentralMvir;

   // properties of subhalo at the last time this galaxy was a central galaaxy 
   float Pos[3];
   float Vel[3];
   float Spin[3];
   int   Len;   
   float Mvir;
   float Rvir;
   float Vvir;
   float Vmax;
   float VelDisp;

   // baryonic reservoirs 
   float ColdGas;
   float StellarMass;
   float BulgeMass;
   float HotGas;
   float EjectedMass;
   float BlackHoleMass;
   float ICS;

   // metals
   float MetalsColdGas;
   float MetalsStellarMass;
   float MetalsBulgeMass;
   float MetalsHotGas;
   float MetalsEjectedMass;
   float MetalsICS;

   // misc 
   float Sfr;
   float SfrBulge;
   float SfrICS;
   float DiskScaleRadius;
   float Cooling;
   float Heating;
};

// Global SQL strings.
const string sql_connect = "dbname=millennium host=localhost port=3305 user=taoadmin password='ta0admin.'";
const string sql_insert = "INSERT INTO galaxies VALUES("
   ":type, "
   ":global_index, :global_descendant, "
   ":tree_local_index, :tree_local_descendant, "
   ":tree, "
   ":snapshot, "
   ":central_mvir, "
   ":pos_x, :pos_y, :pos_z, "
   ":vel_x, :vel_y, :vel_z, "
   ":spin_x, :spin_y, :spin_z, "
   ":length, "
   ":mvir, "
   ":rvir, "
   ":vvir, "
   ":vmax, "
   ":vel_disp, "
   ":cold_gas, "
   ":stellar_mass, "
   ":bulge_mass, "
   ":hot_gas, "
   ":ejected_mass, "
   ":black_hole_mass, "
   ":ics, "
   ":metals_cold_gas, "
   ":metals_stellar_mass, "
   ":metals_bulge_mass, "
   ":metals_hot_gas, "
   ":metals_ejected_mass, "
   ":metals_ics, "
   ":sfr, "
   ":bulge_sfr, "
   ":ics_sfr, "
   ":disk_scale_radius, "
   ":cooling, "
   ":heating"
   ")";

void
file_loop( session& sql )
{
   // Data containers and sizes.
   unsigned data_size = 1000000;
   unsigned pos = 0;
   vector<int> data_type( data_size );
   vector<long long> data_global_index( data_size ), data_global_descendant( data_size );
   vector<int> data_tree_local_index( data_size ), data_tree_local_descendant( data_size );
   vector<int> data_tree( data_size );
   vector<int> data_snapshot( data_size );
   vector<double> data_central_mvir( data_size ), data_pos_x( data_size ), data_pos_y( data_size ), data_pos_z( data_size ),
      data_vel_x( data_size ), data_vel_y( data_size ), data_vel_z( data_size ),
      data_spin_x( data_size ), data_spin_y( data_size ), data_spin_z( data_size );
   vector<int> data_length( data_size );
   vector<double> data_mvir( data_size ), data_rvir( data_size ), data_vvir( data_size ), data_vmax( data_size ),
      data_vel_disp( data_size ), data_cold_gas( data_size ), data_stellar_mass( data_size ),
      data_bulge_mass( data_size ), data_hot_gas( data_size ), data_ejected_mass( data_size ),
      data_black_hole_mass( data_size ), data_ics( data_size ), data_metals_cold_gas( data_size ), 
      data_metals_stellar_mass( data_size ), data_metals_bulge_mass( data_size ), 
      data_metals_hot_gas( data_size ), data_metals_ejected_mass( data_size ), 
      data_metals_ics( data_size ), data_sfr( data_size ), data_bulge_sfr( data_size ), data_ics_sfr( data_size ), 
      data_disk_scale_radius( data_size ), data_cooling( data_size ), data_heating( data_size );

   // Distribute the files over the threads.
   unsigned num_files = 512;
   unsigned first_file = (num_files*OMP_TID)/num_threads;
   unsigned last_file = (num_files*(OMP_TID + 1))/num_threads;
   LOGILN( "Processing from file ", first_file, " to ", last_file, "." );

   // Keep processing files from 0 onwards until we cannot open a file.
   unsigned file_idx = first_file, chunk_idx = 0;
   while( file_idx != last_file )
   {
      // Try and open the file with current chunk index.
      string filename = boost::str( boost::format( "model_%1%_%2%" ) % file_idx % chunk_idx );
      LOGILN( "Trying to open file \"", filename, "\"" );
      std::ifstream file( filename, std::ios::in | std::ios::binary );
      if( !file )
      {
         // Try with advanced file index and reset chunk index.
         if( ++file_idx < last_file )
	 {
	    chunk_idx = 0;
	    filename = boost::str( boost::format( "model_%1%_%2%" ) % file_idx % chunk_idx );
	    LOGILN( "Trying to open file \"", filename, "\"" );
	    file.open( filename, std::ios::in | std::ios::binary );
	 }
         if( !file )
         {
            LOGILN( "Failed, terminating loop." );
            break;
         }
      }
      LOGILN( "Success." );

      // Read counts.
      int num_forests, net_galaxies;
      file.read( (char*)&num_forests, sizeof(num_forests) );
      file.read( (char*)&net_galaxies, sizeof(num_forests) );
      vector<int> num_forest_gals( num_forests );
      file.read( (char*)num_forest_gals.data(), sizeof(int)*num_forests );
      ASSERT( !file.fail() );
      LOGDLN( num_forests, " forests in file." );
      LOGDLN( net_galaxies, " galaxies in file." );

      // Iterate over trees.
      vector<galaxy_type> galaxies;
      for( unsigned ii = 0; ii < num_forests; ++ii )
      {
	 LOGDLN( "Reading tree ", ii, ".", setindent( 2 ) );
	 galaxies.resize( num_forest_gals[ii] );
	 file.read( (char*)galaxies.data(), galaxies.size()*sizeof(galaxy_type) );
	 ASSERT( !file.fail() );

	 // Iterate over each galaxy.
	 LOGDLN( "Inserting tree." );
	 for( unsigned jj = 0; jj < galaxies.size(); ++jj )
	 {
	    data_type[pos] = galaxies[jj].type;
	    data_global_index[pos] = galaxies[jj].global_index;
	    data_global_descendant[pos] = galaxies[jj].global_descendant;
	    data_tree_local_index[pos] = jj;
	    data_tree_local_descendant[pos] = galaxies[jj].descendant;
	    data_tree[pos] = galaxies[jj].tree_idx;
	    data_snapshot[pos] = galaxies[jj].snap;
	    data_central_mvir[pos] = galaxies[jj].CentralMvir;
	    data_pos_x[pos] = galaxies[jj].Pos[0];
	    data_pos_y[pos] = galaxies[jj].Pos[1];
	    data_pos_z[pos] = galaxies[jj].Pos[2];
	    data_vel_x[pos] = galaxies[jj].Vel[0];
	    data_vel_y[pos] = galaxies[jj].Vel[1];
	    data_vel_z[pos] = galaxies[jj].Vel[2];
	    data_spin_x[pos] = galaxies[jj].Spin[0];
	    data_spin_y[pos] = galaxies[jj].Spin[1];
	    data_spin_z[pos] = galaxies[jj].Spin[2];
	    data_length[pos] = galaxies[jj].Len;
	    data_mvir[pos] = galaxies[jj].Mvir;
	    data_rvir[pos] = galaxies[jj].Rvir;
	    data_vvir[pos] = galaxies[jj].Vvir;
	    data_vmax[pos] = galaxies[jj].Vmax;
	    data_vel_disp[pos] = galaxies[jj].VelDisp;
	    data_cold_gas[pos] = galaxies[jj].ColdGas;
	    data_stellar_mass[pos] = galaxies[jj].StellarMass;
	    data_bulge_mass[pos] = galaxies[jj].BulgeMass;
	    data_hot_gas[pos] = galaxies[jj].HotGas;
	    data_ejected_mass[pos] = galaxies[jj].EjectedMass;
	    data_black_hole_mass[pos] = galaxies[jj].BlackHoleMass;
	    data_ics[pos] = galaxies[jj].ICS;
	    data_metals_cold_gas[pos] = galaxies[jj].MetalsColdGas;
	    data_metals_stellar_mass[pos] = galaxies[jj].MetalsStellarMass;
	    data_metals_bulge_mass[pos] = galaxies[jj].MetalsBulgeMass;
	    data_metals_hot_gas[pos] = galaxies[jj].MetalsHotGas;
	    data_metals_ejected_mass[pos] = galaxies[jj].MetalsEjectedMass;
	    data_metals_ics[pos] = galaxies[jj].MetalsICS;
	    data_sfr[pos] = galaxies[jj].Sfr;
	    data_bulge_sfr[pos] = galaxies[jj].SfrBulge;
	    data_ics_sfr[pos] = galaxies[jj].SfrICS;
	    data_disk_scale_radius[pos] = galaxies[jj].DiskScaleRadius;
	    data_cooling[pos] = galaxies[jj].Cooling;
	    data_heating[pos] = galaxies[jj].Heating;

	    if( ++pos == data_size )
	    {
	       LOGDLN( "Hit data size limit, inserting." );
	       sql << sql_insert,
		  use( (std::vector<int>&)data_type ),
		  use( (std::vector<long long>&)data_global_index ), use( (std::vector<long long>&)data_global_descendant ),
		  use( (std::vector<int>&)data_tree_local_index ), use( (std::vector<int>&)data_tree_local_descendant ),
		  use( (std::vector<int>&)data_tree ),
		  use( (std::vector<int>&)data_snapshot ),
		  use( (std::vector<double>&)data_central_mvir ),
		  use( (std::vector<double>&)data_pos_x ), use( (std::vector<double>&)data_pos_y ), use( (std::vector<double>&)data_pos_z ),
		  use( (std::vector<double>&)data_vel_x ), use( (std::vector<double>&)data_vel_y ), use( (std::vector<double>&)data_vel_z ),
		  use( (std::vector<double>&)data_spin_x ), use( (std::vector<double>&)data_spin_y ), use( (std::vector<double>&)data_spin_z ),
		  use( (std::vector<int>&)data_length ),
		  use( (std::vector<double>&)data_mvir ),
		  use( (std::vector<double>&)data_rvir ),
		  use( (std::vector<double>&)data_vvir ),
		  use( (std::vector<double>&)data_vmax ),
		  use( (std::vector<double>&)data_vel_disp ),
		  use( (std::vector<double>&)data_cold_gas ),
		  use( (std::vector<double>&)data_stellar_mass ),
		  use( (std::vector<double>&)data_bulge_mass ),
		  use( (std::vector<double>&)data_hot_gas ),
		  use( (std::vector<double>&)data_ejected_mass ),
		  use( (std::vector<double>&)data_black_hole_mass ),
		  use( (std::vector<double>&)data_ics ),
		  use( (std::vector<double>&)data_metals_cold_gas ),
		  use( (std::vector<double>&)data_metals_stellar_mass ),
		  use( (std::vector<double>&)data_metals_bulge_mass ),
		  use( (std::vector<double>&)data_metals_hot_gas ),
		  use( (std::vector<double>&)data_metals_ejected_mass ),
		  use( (std::vector<double>&)data_metals_ics ),
		  use( (std::vector<double>&)data_sfr ),
		  use( (std::vector<double>&)data_bulge_sfr ),
		  use( (std::vector<double>&)data_ics_sfr ),
		  use( (std::vector<double>&)data_disk_scale_radius ),
		  use( (std::vector<double>&)data_cooling ),
		  use( (std::vector<double>&)data_heating );
	       pos = 0;
	       LOGDLN( "Done." );
	    }
	 }
	 LOGDLN( "Done." );

	 LOGD( setindent( -2 ) );
      }

      // Advance the chunk and table.
      ++chunk_idx;
   }
}

void
create_table( session& sql )
{
   // Check if the table already exists.
   unsigned exists;
   sql << "SELECT COUNT(table_name) FROM information_schema.tables"
      " WHERE table_schema='public' AND table_name='galaxies'",
      into( exists );
   if( exists )
   {
      std::cout << "Table already exists.\n";
      exit( 1 );
   }

   // Create the table.
   sql << "CREATE TABLE galaxies ("
      "type SMALLINT, "
      "global_index BIGINT, global_descendant BIGINT, "
      "tree_local_index INTEGER, tree_local_descendant INTEGER, "
      "tree INTEGER, "
      "snapshot INTEGER, "
      "central_mvir DOUBLE PRECISION, "
      "pos_x DOUBLE PRECISION, pos_y DOUBLE PRECISION, pos_z DOUBLE PRECISION, "
      "vel_x DOUBLE PRECISION, vel_y DOUBLE PRECISION, vel_z DOUBLE PRECISION, "
      "spin_x DOUBLE PRECISION, spin_y DOUBLE PRECISION, spin_z DOUBLE PRECISION, "
      "length INTEGER, "
      "mvir DOUBLE PRECISION, "
      "rvir DOUBLE PRECISION, "
      "vvir DOUBLE PRECISION, "
      "vmax DOUBLE PRECISION, "
      "vel_disp DOUBLE PRECISION, "
      "cold_gas DOUBLE PRECISION, "
      "stellar_mass DOUBLE PRECISION, "
      "bulge_mass DOUBLE PRECISION, "
      "hot_gas DOUBLE PRECISION, "
      "ejected_mass DOUBLE PRECISION, "
      "black_hole_mass DOUBLE PRECISION, "
      "ics DOUBLE PRECISION, "
      "metals_cold_gas DOUBLE PRECISION, "
      "metals_stellar_mass DOUBLE PRECISION, "
      "metals_bulge_mass DOUBLE PRECISION, "
      "metals_hot_gas DOUBLE PRECISION, "
      "metals_ejected_mass DOUBLE PRECISION, "
      "metals_ics DOUBLE PRECISION, "
      "sfr DOUBLE PRECISION, "
      "bulge_sfr DOUBLE PRECISION, "
      "ics_sfr DOUBLE PRECISION, "
      "disk_scale_radius DOUBLE PRECISION, "
      "cooling DOUBLE PRECISION, "
      "heating DOUBLE PRECISION"
      ")";

   // Create indices.
   sql << "CREATE INDEX ON galaxies (tree)";
   sql << "CREATE INDEX ON galaxies (snapshot)";
   sql << "CREATE INDEX ON galaxies (pos_x)";
   sql << "CREATE INDEX ON galaxies (pos_y)";
   sql << "CREATE INDEX ON galaxies (pos_z)";
}

int
main( int argc,
      char* argv[] )
{
   // ASSERT( argc > 1 );
   // LOG_CONSOLE();
   LOG_PUSH( new logging::omp::file( "taoimport.log." ) );

   // Setup the number of threads to use.
#ifdef _OPENMP
   omp_set_num_threads( num_threads );
   LOGILN( "Running with ", num_threads, " threads." );
#endif

   // Split off workers.
#pragma omp parallel
   {
      // Open database session.
      session sql( postgresql, sql_connect );

      // Try to create the galaxies table.
#pragma omp master
      create_table( sql );
#pragma omp barrier

      // Enter the file loop.
      file_loop( sql );
   }

   return EXIT_SUCCESS;
}
