#include <cstdlib>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <libhpc/libhpc.hh>

using namespace hpc;
using soci::use;
using soci::into;

string
table_name( unsigned idx )
{
   return boost::str( boost::format( "snapshot_%1$03d" ) % idx );
}

///
/// @param[in]  num_cur_galaxies  Number of galaxies on current level.
/// @returns                      Number of galaxies on next level.
///
unsigned
step_down( unsigned num_cur_galaxies )
{
}

void
write_flat_file( soci::session& sql,
                 const string& filename )
{
   // Open the file.
   std::ofstream file( filename, std::ios::out );
   ASSERT( file.good() );

   // Need to create two datatypes, one for memory and the other for file.
   h5::datatype mem_type, file_type;
   make_flat_types<double>( mem_type, file_type );

   // Create new file for writing.
   h5::file( filename, H5F_ACC_TRUNC );

   // How many galaxies are in all the snapshots?
   unsigned net_gals = 0;
   for( unsigned ii = 0; ii < num_snaps; ++ii )
   {
      string query = string( "SELECT count(*) FROM " ) + table_name( ii );
      unsigned num_in_this;
      sql << query, into( num_in_this );
      net_gals += num_in_this;
   }

   // Create a file dataset of the appropriate size.
   h5::dataspace file_space;
   file_space.create( num_flat_gals );
   h5::dataset file_set;
   flat_set.create( file, "flat_trees", file_type, file_space );

   // Create a memory space of a single elements size.
   h5::dataspace mem_space;
   mem_space.create( 1 );

   // Iterate over all flat objects, in order, to write them.
   unsigned cur_gal = 0;
   soci::rowset<soci::row> rowset( (sql.prepare << string( "SELECT * FROM " ) + snapshot) );
   vector<hsize_t> count( 1 ), start( 1 );
   for( soci::rowset<soci::row>::const_iterator it = rowset.begin(); it != rowset.end(); ++it )
   {
      // Prepare the data.
      flat_info<double> info;
      info.disk_mass = row.get<double>( "disk_mass" );
      info.bulge_mass = row.get<double>( "bulge_mass" );
      info.disk_rate = row.get<double>( "disk_rate" );
      info.bulge_rate = row.get<double>( "bulge_rate" );
      info.disk_metal = row.get<double>( "disk_metal" );
      info.bulge_metal = row.get<double>( "bulge_metal" );
      info.redshift = redshift;

      // Select the appropriate element in the file based on the row. Note that
      // we only write this particular galaxy.
      start[0] = row.get<int>( "flat_offset" );
      count[0] = 1;
      file_space.select_hyperslab( H5S_SELECT_SET, count, start );

      // Transfer each element, in order, to the file.
      file_set.write( &info, mem_type, mem_space, file_space );
   }
}

int
main( int argc,
      char* argv[] )
{
   ASSERT( argc > 1 );
   LOG_CONSOLE();

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
   LOGLN( "Creating metadata table..." );
   sql << "CREATE TABLE meta (snap_table TEXT, redshift DOUBLE PRECISION, box_size DOUBLE PRECISION)";
   for( unsigned ii = 0; ii < num_snapshots; ++ii )
   {
      sql << "INSERT INTO meta VALUES(:table, :z, :box)",
         use( table_name( ii ) ), use( start_z + ii*dz ),
         use( box_size );
   }
   LOGLN( "done." );

   // Create some tables for snapshots.
   LOGLN( "Creating snapshots tables..." );
   for( unsigned ii = 0; ii < num_snapshots; ++ii )
   {
      string query = "CREATE TABLE ";
      query += table_name( ii );
      query += " (x DOUBLE PRECISION, y DOUBLE PRECISION, z DOUBLE PRECISION, id INTEGER, "
         "disk_mass DOUBLE PRECISION, bulge_mass DOUBLE PRECISION, "
         "disk_rate DOUBLE PRECISION, bulge_rate DOUBLE PRECISION, "
         "disk_metal DOUBLE PRECISION, bulge_metal DOUBLE PRECISION, "
         "flat_offset INTEGER, flat_length INTEGER)";
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
   unsigned flat = 0;

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

         // Generate a zero-depth hierarchy.
         unsigned flat_offset = flat++, flat_length = 1;

         // Insert galaxy object position information.
         for( unsigned jj = 0; jj < num_snapshots; ++jj )
         {
            string query = "INSERT INTO ";
            query += table_name( jj );
            query += " VALUES(:x, :y, :z, :id, :dm, :bm, "
               ":dr, :br, :dme, :bme, :fi, :fl)";
            sql << query,
               use( x ), use( y ), use( z ), use( gal_id ),
               use( dmass ), use( bmass ),
               use( drate ), use( brate ),
               use( dmetal ), use( bmetal ),
               use( flat_offset ), use( flat_length );
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

   return EXIT_SUCCESS;
}
