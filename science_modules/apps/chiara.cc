#include <cstdlib>
#include <iostream>
#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <libhpc/libhpc.hh>

using namespace hpc;

int
main( int argc,
      char* argv[] )
{
   ASSERT( argc > 2 );
   std::ifstream input( argv[1] );

   // Open database session.
   soci::session sql( soci::sqlite3, argv[2] );

   // Create some tables for snapshots.
   sql << "create table snapshot_000 (Pos1 double precision, Pos2 double precision, Pos3 double precision, id integer)";
   sql << "create table snapshot_001 (Pos1 double precision, Pos2 double precision, Pos3 double precision, id integer)";

   // Now some tables for star formation information.
   sql << "create table disk_star_formation (galaxy_id integer, mass double precision, "
      "metal double precision, age double precision)";
   sql << "create table bulge_star_formation (galaxy_id integer, mass double precision, "
      "metal double precision, age double precision)";

   // Need some constants and variables for adding objects to
   // the database.
   unsigned num_ages = 67;
   unsigned gal_id = 0;
   double age = 0.0;
   double sfrd, sfrb;
   std::vector<double> sfhd( num_ages ), sfhb( num_ages );
   std::vector<double> metd( num_ages ), metb( num_ages );
   std::vector<unsigned> gal_ids( num_ages ), ages( num_ages );

   // Prepare some sql statements.
   soci::statement sfhd_st = (sql.prepare << "insert into disk_star_formation values(:id, :mass, :metal, :age)",
                              soci::use( gal_ids ), soci::use( sfhd ), soci::use( metd ), soci::use( ages ));
   soci::statement sfhb_st = (sql.prepare << "insert into bulge_star_formation values(:id, :mass, :metal, :age)",
                              soci::use( gal_ids ), soci::use( sfhb ), soci::use( metb ), soci::use( ages ));

   // Begin looping on the file.
   while( !input.eof() )
   {
      // Read the disk and bulge star formation rates. Note that
      // if we hit the EOF here, we're still okay, just means there
      // was some whitespace.
      input >> sfrd >> sfrb;
      if( input.eof() )
         break;

      // Create a transaction to speed this asshole up.
      soci::transaction trn( sql );

      std::cout << "Galaxy " << gal_id << "... ";

      // Read the disk star formation history.
      for( unsigned ii = 0; ii < num_ages; ++ii )
         input >> sfhd[ii];

      // Read the disk metallicities.
      for( unsigned ii = 0; ii < num_ages; ++ii )
         input >> metd[ii];

      // Read the bulge star formation history.
      for( unsigned ii = 0; ii < num_ages; ++ii )
         input >> sfhb[ii];

      // Read the bulge metallicities.
      for( unsigned ii = 0; ii < num_ages; ++ii )
         input >> metb[ii];

      // Set the ages and ids vectors.
      std::fill( gal_ids.begin(), gal_ids.end(), gal_id );
      std::fill( ages.begin(), ages.end(), age );

      // Generate some randomized coordinates.
      double x = generate_uniform<double>( 5.0, 20.0 );
      double y = generate_uniform<double>( 5.0, 20.0 );
      double z = generate_uniform<double>( 5.0, 20.0 );

      // Insert galaxy object position information.
      sql << "insert into snapshot_000 values(:x, :y, :z, :id)",
         soci::use( x ), soci::use( y ), soci::use( z ), soci::use( gal_id );
      sql << "insert into snapshot_001 values(:x, :y, :z, :id)",
         soci::use( x ), soci::use( y ), soci::use( z ), soci::use( gal_id );

      // Insert star formation histories.
      sfhd_st.execute( true );
      sfhb_st.execute( true );

      // Commit the transaction now.
      trn.commit();

      // Move forward.
      ++gal_id;
      age += 1.0;

      std::cout << "done\n";
   }

   return EXIT_SUCCESS;
}
