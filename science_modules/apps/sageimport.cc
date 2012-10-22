#include <cstdlib>
#include <iostream>
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>
#include <soci/soci.h>
#include <soci/postgresql/soci-postgresql.h>
#include <libhpc/libhpc.hh>

using namespace hpc;
using namespace soci;

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

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );

   // ASSERT( argc > 1 );
   // LOG_CONSOLE();
   LOG_PUSH( new logging::stdout( 0 ) );

   // Open database session.
#include "credentials.hh"
   string connect = "dbname=millennium_full host=localhost port=3308"; // user=" + user + " pass='" + password + "'";
   session sql( postgresql, connect );

   // Keep processing files from 0 onwards until we cannot open a file.
   unsigned file_idx = 0, chunk_idx = 0, table_idx = 0;
   long long tree_idx = 0;
   while( 1 )
   {
      // Try and open the file with current chunk index.
      string filename = boost::str( boost::format( "model_%1%_%2%" ) % file_idx % chunk_idx );
      LOGILN( "Trying to open file \"", filename, "\"" );
      std::ifstream file( filename, std::ios::in | std::ios::binary );
      if( !file )
      {
         // Try with advanced file index and reset chunk index.
         ++file_idx;
         chunk_idx = 0;
         filename = boost::str( boost::format( "model_%1%_%2%" ) % file_idx % chunk_idx );
         LOGILN( "Trying to open file \"", filename, "\"" );
         file.open( filename, std::ios::in | std::ios::binary );
         if( !file )
         {
            LOGILN( "Failed, terminating loop." );
            break;
         }
      }
      LOGILN( "Success." );

      // Read counts.
      int num_trees, net_halos;
      file.read( (char*)&num_trees, sizeof(num_trees) );
      file.read( (char*)&net_halos, sizeof(num_trees) );
      vector<int> num_tree_halos( num_trees );
      file.read( (char*)num_tree_halos.data(), sizeof(int)*num_trees );
      ASSERT( !file.fail() );
      LOGDLN( num_trees, " in file." );

      // Create a new table for this file.
      string table_name = "trees_" + to_string( table_idx );
      string query = "CREATE TABLE " + table_name + "(";
      query += "type SMALLINT, ";
      query += "index BIGINT, descendant BIGINT, ";
      query += "tree BIGINT, ";
      query += "snapshot SMALLINT, ";
      query += "central_mvir DOUBLE PRECISION, ";
      query += "pos_x DOUBLE PRECISION, pos_y DOUBLE PRECISION, pos_z DOUBLE PRECISION, ";
      query += "vel_x DOUBLE PRECISION, vel_y DOUBLE PRECISION, vel_z DOUBLE PRECISION, ";
      query += "spin_x DOUBLE PRECISION, spin_y DOUBLE PRECISION, spin_z DOUBLE PRECISION, ";
      query += "length INTEGER, ";
      query += "mvir DOUBLE PRECISION, ";
      query += "rvir DOUBLE PRECISION, ";
      query += "vvir DOUBLE PRECISION, ";
      query += "vmax DOUBLE PRECISION, ";
      query += "vel_disp DOUBLE PRECISION, ";
      query += "cold_gas DOUBLE PRECISION, ";
      query += "stellar_mass DOUBLE PRECISION, ";
      query += "bulge_mass DOUBLE PRECISION, ";
      query += "hot_gas DOUBLE PRECISION, ";
      query += "ejected_mass DOUBLE PRECISION, ";
      query += "black_hole_mass DOUBLE PRECISION, ";
      query += "ics DOUBLE PRECISION, ";
      query += "metals_cold_gas DOUBLE PRECISION, ";
      query += "metals_stellar_mass DOUBLE PRECISION, ";
      query += "metals_bulge_mass DOUBLE PRECISION, ";
      query += "metals_hot_gas DOUBLE PRECISION, ";
      query += "metals_ejected_mass DOUBLE PRECISION, ";
      query += "metals_ics DOUBLE PRECISION, ";
      query += "sfr DOUBLE PRECISION, ";
      query += "bulge_sfr DOUBLE PRECISION, ";
      query += "ics_sfr DOUBLE PRECISION, ";
      query += "disk_scale_radius DOUBLE PRECISION, ";
      query += "cooling DOUBLE PRECISION, ";
      query += "heating DOUBLE PRECISION";
      query += ")";
      sql << query;

      // Prepare the general insertion query.
      query = "INSERT INTO " + table_name + " VALUES(";
      query += ":type, ";
      query += ":index, :descendant, ";
      query += ":tree, ";
      query += ":snapshot, ";
      query += ":central_mvir, ";
      query += ":pos_x, :pos_y, :pos_z, ";
      query += ":vel_x, :vel_y, :vel_z, ";
      query += ":spin_x, :spin_y, :spin_z, ";
      query += ":length, ";
      query += ":mvir, ";
      query += ":rvir, ";
      query += ":vvir, ";
      query += ":vmax, ";
      query += ":vel_disp, ";
      query += ":cold_gas, ";
      query += ":stellar_mass, ";
      query += ":bulge_mass, ";
      query += ":hot_gas, ";
      query += ":ejected_mass, ";
      query += ":black_hole_mass, ";
      query += ":ics, ";
      query += ":metals_cold_gas, ";
      query += ":metals_stellar_mass, ";
      query += ":metals_bulge_mass, ";
      query += ":metals_hot_gas, ";
      query += ":metals_ejected_mass, ";
      query += ":metals_ics, ";
      query += ":sfr, ";
      query += ":bulge_sfr, ";
      query += ":ics_sfr, ";
      query += ":disk_scale_radius, ";
      query += ":cooling, ";
      query += ":heating";
      query += ")";

      // Iterate over trees.
      vector<galaxy_type> halos;
      for( unsigned ii = 0; ii < num_trees; ++ii )
      {
         LOGDLN( "Reading tree ", ii, ".", setindent( 2 ) );
         halos.resize( num_tree_halos[ii] );
         file.read( (char*)halos.data(), halos.size()*sizeof(galaxy_type) );
         ASSERT( !file.fail() );

	 // Use a transaction to speed this jerk up.
	 transaction trn( sql );

         // Iterate over each galaxy.
	 LOGDLN( "Inserting tree." );
         for( unsigned jj = 0; jj < halos.size(); ++jj )
         {
	    // LOGDLN( "Inserting galaxy ", jj, "." );
	    sql << query,
	       use( halos[jj].type ),
	       use( halos[jj].global_index ), use( halos[jj].global_descendant ),
	       use( tree_idx ),
	       use( halos[jj].snap ),
	       use( (double)halos[jj].CentralMvir ),
	       use( (double)halos[jj].Pos[0] ), use( (double)halos[jj].Pos[1] ), use( (double)halos[jj].Pos[2] ),
	       use( (double)halos[jj].Vel[0] ), use( (double)halos[jj].Vel[1] ), use( (double)halos[jj].Vel[2] ),
	       use( (double)halos[jj].Spin[0] ), use( (double)halos[jj].Spin[1] ), use( (double)halos[jj].Spin[2] ),
	       use( halos[jj].Len ),
	       use( (double)halos[jj].Mvir ),
	       use( (double)halos[jj].Rvir ),
	       use( (double)halos[jj].Vvir ),
	       use( (double)halos[jj].Vmax ),
	       use( (double)halos[jj].VelDisp ),
	       use( (double)halos[jj].ColdGas ),
	       use( (double)halos[jj].StellarMass ),
	       use( (double)halos[jj].BulgeMass ),
	       use( (double)halos[jj].HotGas ),
	       use( (double)halos[jj].EjectedMass ),
	       use( (double)halos[jj].BlackHoleMass ),
	       use( (double)halos[jj].ICS ),
	       use( (double)halos[jj].MetalsColdGas ),
	       use( (double)halos[jj].MetalsStellarMass ),
	       use( (double)halos[jj].MetalsBulgeMass ),
	       use( (double)halos[jj].MetalsHotGas ),
	       use( (double)halos[jj].MetalsEjectedMass ),
	       use( (double)halos[jj].MetalsICS ),
	       use( (double)halos[jj].Sfr ),
	       use( (double)halos[jj].SfrBulge ),
	       use( (double)halos[jj].SfrICS ),
	       use( (double)halos[jj].DiskScaleRadius ),
	       use( (double)halos[jj].Cooling ),
	       use( (double)halos[jj].Heating );
         }
	 LOGDLN( "Done." );

	 // Commit the transaction now.
	 LOGDLN( "Committing transaction." );
	 trn.commit();
	 LOGDLN( "Done." );

	 // Next tree.
	 ++tree_idx;

         LOGD( setindent( -2 ) );
      }

      // Advance the chunk and table.
      ++chunk_idx;
      ++table_idx;
   }

   mpi::finalise();
   return EXIT_SUCCESS;
}
