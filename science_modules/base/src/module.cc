#include <soci/sqlite3/soci-sqlite3.h>
#include <soci/postgresql/soci-postgresql.h>
#include "module.hh"

using namespace hpc;

namespace tao {

   module::module()
      : _connected( false ),
	_num_restart_its( 10 ),
	_cur_restart_it( 0 )
   {
   }

   double
   module::time() const
   {
      return _timer.total();
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
   module::_db_connect()
   {
      LOG_ENTER();

      LOGDLN( "Connecting to ", _dbtype, " database \"", _dbname, "\"" );
      try
      {
         if( _dbtype == "sqlite" )
            _sql.open( soci::sqlite3, _dbname );
         else
         {
	    string connect = "dbname=" + _dbname;
	    connect += " host=" + _dbhost;
	    connect += " port=" + _dbport;
	    connect += " user=" + _dbuser;
	    connect += " password='" + _dbpass + "'";
	    LOGDLN( "Connect string: ", connect );
	    _sql.open( soci::postgresql, connect );
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

   bool
   module::_db_cycle()
   {
      if( ++_cur_restart_it == _num_restart_its )
      {
	 LOGDLN( "Reconnecting to database." );
	 _cur_restart_it = 0;
	 _db_disconnect();
	 _db_connect();
	 return true;
      }
      else
	 return false;
   }
}
