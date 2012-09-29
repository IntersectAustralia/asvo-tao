#include <cstdlib>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>

using namespace hpc;
using namespace tao;

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );

   ASSERT( argc > 1 );
   LOG_CONSOLE();

   // Setup the filenames.
   string filename = string( argv[1] );
   string flat_filename = string( argv[1] ) + ".flat.0";

   // Open database session.
   soci::session sql( soci::mysql, "db=random unix_socket='/var/lib/mysql/mysql.sock' user=root pass='la di da'" );

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
   double min_disk_metal = 0.0, max_disk_metal = 0.06;
   double min_bulge_metal = 0.0, max_bulge_metal = 0.06;

   // Create the metadata table.
   LOGLN( "Creating metadata table..." );
   sql << "DROP TABLE IF EXISTS meta";
   sql << "CREATE TABLE meta (snap_table INTEGER, redshift DOUBLE PRECISION, box_size DOUBLE PRECISION)";
   for( unsigned ii = 0; ii < num_snapshots; ++ii )
   {
      sql << "INSERT INTO meta VALUES(:table, :z, :box)",
         use( ii ), use( start_z + (num_snapshots - ii - 1)*dz ),
         use( box_size );
   }
   LOGLN( "done." );

   // Create some tables for snapshots.
   LOGLN( "Creating snapshots tables..." );
   for( unsigned ii = 0; ii < num_snapshots; ++ii )
   {
      sql << (string("DROP TABLE IF EXISTS ") + table_name( ii ));
      string query = "CREATE TABLE ";
      query += table_name( ii );
      query += " (x DOUBLE PRECISION, y DOUBLE PRECISION, z DOUBLE PRECISION, id INTEGER, "
         "disk_mass DOUBLE PRECISION, bulge_mass DOUBLE PRECISION, "
         "disk_rate DOUBLE PRECISION, bulge_rate DOUBLE PRECISION, "
         "disk_metal DOUBLE PRECISION, bulge_metal DOUBLE PRECISION, "
         "flat_file INTEGER, flat_offset INTEGER, flat_length INTEGER)";
      sql << query;
   }
   LOGLN( "done." );

   // Need some constants and variables for adding objects to
   // the database.
   unsigned gal_id = 0;
   unsigned chunk_size = 1000;
   std::vector<double> sfhd( chunk_size ), sfhb( chunk_size );
   std::vector<double> metd( chunk_size ), metb( chunk_size );
   std::vector<unsigned> gal_ids( chunk_size );
   unsigned flat_offs = 0, flat_file = 0;

   // Produce as many galaxies as requested.
   LOGLN( "Generating galaxies...", setindent( 2 ) );
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

         // Insert galaxy object position information.
         for( unsigned jj = num_snapshots; jj > 0; --jj )
         {
            string query = "INSERT INTO ";
            query += table_name( jj - 1 );
            query += " VALUES(:x, :y, :z, :id, :dm, :bm, "
               ":dr, :br, :dme, :bme, :ff, :fi, :fl)";
            sql << query,
               use( x ), use( y ), use( z ), use( gal_id ),
               use( dmass ), use( bmass ),
               use( drate ), use( brate ),
               use( dmetal ), use( bmetal ),
               use( flat_file ), use( flat_offs++ ), use( jj );
         }

         // Update.
         LOGLN( "Wrote galaxy ", gal_id, " at ", x, ", ", y, ", ", z );

         // Move forward.
         ++gal_id;
      }
      LOGLN( setindent( -2 ), "done." );

      // Commit the transaction now.
      trn.commit();
   }

   // Now that the database in order, dump the flat file.
   write_flat_file( sql, flat_filename );

   mpi::finalise();
   return EXIT_SUCCESS;
}
