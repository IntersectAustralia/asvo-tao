#include <soci/sqlite3/soci-sqlite3.h>
#include <soci/postgresql/soci-postgresql.h>
#include "module.hh"

using namespace hpc;

namespace tao {

   module::module()
      : _connected( false )
   {
   }

   void
   module::_db_connect( soci::session& sql )
   {
      LOG_ENTER();

      LOGDLN( "Connecting to ", _dbtype, " database \"", _dbname, "\"" );
      try
      {
         if( _dbtype == "sqlite" )
            sql.open( soci::sqlite3, _dbname );
         else
         {
	    string connect = "dbname=" + _dbname;
	    connect += " host=" + _dbhost;
	    connect += " port=" + _dbport;
	    connect += " user=" + _dbuser;
	    connect += " password='" + _dbpass + "'";
	    LOGDLN( "Connect string: ", connect );
	    sql.open( soci::postgresql, connect );
         }
      }
      catch( const std::exception& ex )
      {
         // TODO: Handle database errors.
         LOGDLN( "Error opening database connection: ", ex.what() );
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
         LOGDLN( "Disconnecting from database." );
         _sql.close();
         _connected = false;
      }
   }
}
