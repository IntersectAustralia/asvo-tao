#include <cstdlib>
#include <iostream>
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>
#include <soci/soci.h>
#include <soci/postgresql/soci-postgresql.h>
#include <libhpc/libhpc.hh>

using namespace hpc;
using namespace soci;

// Global SQL strings.
const string sql_connect = "dbname=millennium host=localhost port=3305 user=taoadmin password='ta0admin.'";
const string sql_insert = "INSERT INTO snapshot_redshift VALUES("
   ":snap, "
   ":redshift"
   ")";

void
file_loop( session& sql )
{
   std::ifstream file( "millennium.a_list" );
   ASSERT( file );
   unsigned snap = 0;
   double age, redshift;
   while( (file >> age, !file.eof()) )
   {
      redshift = 1.0/age - 1.0;
      LOGDLN( "Inserting entry: ", snap, " -> ", redshift );
      sql << sql_insert, soci::use( snap ), soci::use( redshift );
      ++snap;
   }
}

void
create_table( session& sql )
{
   int exists;
   sql << "SELECT COUNT(table_name) FROM information_schema.tables"
      " WHERE table_schema='public' AND table_name='snapshot_redshift'",
      into( exists );
   if( exists )
   {
      LOGDLN( "Table exists, removing." );
      sql << "DROP TABLE snapshot_redshifts";
   }

   // Create the snapshot to redshift table.
   LOGDLN( "Creating redshift table." );
   sql << "CREATE TABLE snapshot_redshift("
      "snapshot INTEGER, "
      "redshift DOUBLE PRECISION"
      ")";
}

int
main( int argc,
      char* argv[] )
{
   // ASSERT( argc > 1 );
   // LOG_CONSOLE();
   // LOG_PUSH( new logging::omp::file( "taoimport.log." ) );

  // Open database session.
  session sql( postgresql, sql_connect );

  // Try to create the galaxies table.
  create_table( sql );

  // Enter the file loop.
  file_loop( sql );

   return EXIT_SUCCESS;
}
