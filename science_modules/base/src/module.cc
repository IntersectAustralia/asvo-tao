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
   module::_read_db_options( const options::dictionary& dict )
   {
      LOG_ENTER();

      // Extract database details.
      _dbtype = dict.get<string>( "settings:database:type" );
      _dbname = dict.get<string>( "database" );
      if( _dbtype != "sqlite" )
      {
         _dbhost = dict.get<string>( "settings:database:host" );
         _dbport = dict.get<string>( "settings:database:port" );
         _dbuser = dict.get<string>( "settings:database:user" );
         _dbpass = dict.get<string>( "settings:database:password" );
      }
      _tree_pre = dict.get<string>( "settings:database:treetableprefix" );

      LOG_EXIT();
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
