#include <cstdlib>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <libhpc/libhpc.hh>

using namespace hpc;
using soci::use;

string
table_name( unsigned idx )
{
   return boost::str( boost::format( "snapshot_%1$03d" ) % idx );
}

int
main( int argc,
      char* argv[] )
{
   ASSERT( argc > 1 );

   // Open database session.
   soci::session sql( soci::sqlite3, argv[1] );

   // Define some values.
   unsigned num_snapshots = 12;
   unsigned num_galaxies = 500;
   double start_z = 0.1;
   double dz = 0.1;
   double box_min = 100.0, box_max = 1000.0;
   double box_size = generate_uniform<double>( box_min, box_max );
   double min_distance = 10.0;
   double min_disk_mass = 1e4, max_disk_mass = 1e11;
   double min_bulge_mass = 0.0, max_bulge_mass = 1e11;
   double min_disk_rate = 0.2, max_disk_rate = 6.0;
   double min_bulge_rate = 0.0, max_bulge_rate = 8e-8;
   double min_disk_metal = 0.0, max_disk_metal = 1e-1;
   double min_bulge_metal = 0.0, max_bulge_metal = 1e-1;

   // Create the metadata table.
   sql << "CREATE TABLE meta (snap_table TEXT, redshift DOUBLE PRECISION, box_size DOUBLE PRECISION)";
   for( unsigned ii = 0; ii < num_snapshots; ++ii )
   {
      sql << "INSERT INTO meta VALUES(:table, :z, :box)",
         use( table_name( ii ) ), use( start_z + ii*dz ),
         use( box_size );
   }

   // Create some tables for snapshots.
   for( unsigned ii = 0; ii < num_snapshots; ++ii )
   {
      sql << "CREATE TABLE :table (x DOUBLE PRECISION, y DOUBLE PRECISION, z DOUBLE PRECISION, id INTEGER, "
         "disk_mass DOUBLE PRECISION, bulge_mass DOUBLE PRECISION, "
         "disk_rate DOUBLE PRECISION, bulge_rate DOUBLE PRECISION, "
         "disk_metal DOUBLE PRECISION, bulge_metal DOUBLE PRECISION, "
         "left INTEGER, right INTEGER)",
         use( table_name( ii ) );
   }

   // Need some constants and variables for adding objects to
   // the database.
   unsigned gal_id = 0;
   unsigned chunk_size = 1000;
   std::vector<double> sfhd( chunk_size ), sfhb( chunk_size );
   std::vector<double> metd( chunk_size ), metb( chunk_size );
   std::vector<unsigned> gal_ids( chunk_size );

   // Produce as many galaxies as requested.
   while( gal_id < num_galaxies )
   {
      // Use a transaction to speed this jerk up.
      soci::transaction trn( sql );

      // Build galaxies in chunks to ehance performance.
      for( unsigned ii = 0; ii < chunk_size && gal_id < num_galaxies; ++ii )
      {
         // Generate some randomized coordinates.
         double x, y, z;
         do
         {
            x = generate_uniform<double>( 0.0, box_size );
            y = generate_uniform<double>( 0.0, box_size );
            z = generate_uniform<double>( 0.0, box_size );
         }
         while( x*x + y*y + z*z < min_distance );

         // Generate some masses and things.
         double dmass, bmass, drate, brate, dmetal, bmetal;
         dmass = generate_uniform<double>( min_disk_mass, max_disk_mass );
         bmass = generate_uniform<double>( min_bulge_mass, max_bulge_mass );
         drate = generate_uniform<double>( min_disk_rate, max_disk_rate );
         brate = generate_uniform<double>( min_bulge_rate, max_bulge_rate );
         dmetal = generate_uniform<double>( min_disk_metal, max_disk_metal );
         bmetal = generate_uniform<double>( min_bulge_metal, max_bulge_metal );

         // Generate the hierarchy (how the fuck?).
         unsigned left = 0, right = 0;

         // Insert galaxy object position information.
         for( unsigned jj = 0; jj < num_snapshots; ++jj )
         {
            sql << "INSERT INTO :table VALUES(:x, :y, :z, :id, :dm, :bm, "
               ":dr, :br, :dme, :bme, :l, :r)",
               use( table_name( jj ) ),
               use( x ), use( y ), use( z ), use( gal_id ),
               use( dmass ), use( bmass ),
               use( drate ), use( brate ),
               use( dmetal ), use( bmetal ),
               use( left ), use( right );
         }

         // Update.
         std::cout << "Wrote galaxy " << gal_id << " at " << x << ", " << y << ", " << z << "\n";

         // Move forward.
         ++gal_id;
      }

      // Commit the transaction now.
      trn.commit();
   }

   return EXIT_SUCCESS;
}
