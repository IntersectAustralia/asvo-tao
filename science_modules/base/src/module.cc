#include <soci/sqlite3/soci-sqlite3.h>
#include "module.hh"

using namespace hpc;

namespace tao {

   module::module()
      : _connected( false )
   {
   }

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

      // Flag as connected.
      _connected = true;

      LOG_EXIT();
   }

   void
   module::_db_disconnect()
   {
      if( _connected )
      {
         LOGLN( "Disconnecting from database." );
         _sql.close();
         _connected = false;
      }
   }
}
