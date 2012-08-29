#include <soci/sqlite3/soci-sqlite3.h>
#include "module.hh"

using namespace hpc;

namespace tao {

   void
   module::_db_connect( soci::session& sql,
                        const string& type,
                        const string& name )
   {
      LOG_ENTER();

      LOGLN( "Connecting to ", type, " database: ", name );
      try
      {
         if( type == "sqlite" )
            sql.open( soci::sqlite3, name );
         else
         {
            ASSERT( 0 );
            // sql.open( soci::mysql, str( format( "host=%1% db=%2% user=%3% password='%4'" ) % _dbhost % _dbname % _dbuser % _dbpass ) );
         }
      }
      catch( const std::exception& ex )
      {
         // TODO: Handle database errors.
         LOGLN( "Error opening database connection: ", ex.what() );
         ASSERT( 0 );
      }

      LOG_EXIT();
   }
}
