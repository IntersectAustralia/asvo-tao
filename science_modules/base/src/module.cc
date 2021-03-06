#include <soci/sqlite3/soci-sqlite3.h>
#include <soci/postgresql/soci-postgresql.h>
#include "module.hh"

using namespace hpc;

namespace tao {

   module::module( const string& name,
		   pugi::xml_node base )
      : _name( name ),
	_base( base ),
	_dict( base ),
	_global_dict( NULL ),
#ifdef MULTIDB
	_db( NULL ),
#endif
        _it( 0 ),
        _complete( false ),
        _connected( false ),
	_num_restart_its( 1000 ),
	_cur_restart_it( 0 )
   {
   }

   module::~module()
   {
   }

   void
   module::add_parent( module& parent )
   {
      // Check that we don't already have this guy.
      ASSERT( std::find( _parents.begin(), _parents.end(), &parent ) == _parents.end() );

      // Add it to the list.
      _parents.push_back( &parent );

      LOGDLN( "Added ", parent.name(), " to ", _name );
   }

   list<module*>&
   module::parents()
   {
      return _parents;
   }

   void
   module::process( unsigned long long iteration )
   {
      LOG_ENTER();

      // Iteration should never be lower than my current.
      ASSERT( iteration >= _it );

      // If we have not already processed this round, launch
      // the execute routine.
      if( iteration > _it )
      {
         // Should only ever be greater by one.
         ASSERT( iteration == _it + 1 );

         // Process all parents.
         bool all_complete = !_parents.empty();
         for( auto& parent : _parents )
         {
            parent->process( iteration );
            if( !parent->complete() )
               all_complete = false;
         }

         // Call the user-defined execute routine.
         if( !all_complete )
            execute();
         else
         {
            LOGDLN( "All parents are complete, marking myself as complete." );
            _complete = true;
         }

         // Update my iteration counter.
         _it = iteration;
      }

      LOG_EXIT();
   }

   void
   module::initialise( const options::xml_dict& global_dict )
   {
      // Store global dictionary.
      _global_dict = &global_dict;

      // Reset timers.
      _timer.reset();
      _db_timer.reset();
   }

   void
   module::finalise()
   {
   }

   tao::galaxy&
   module::galaxy()
   {
      // By default return the first parent.
      return _parents.front()->galaxy();
   }

   void
   module::log_metrics()
   {
      LOGILN( name(), " runtime: ", time(), " (s)" );
      LOGILN( name(), " db time: ", db_time(), " (s)" );
   }

   bool
   module::complete() const
   {
      return _complete;
   }

   const string&
   module::name() const
   {
      return _name;
   }

   const options::xml_dict&
   module::local_dict() const
   {
      return _dict;
   }

   pugi::xml_node
   module::local_xml_node()
   {
      return _base;
   }

   double
   module::time() const
   {
      return _timer.total();
   }

   double
   module::db_time() const
   {
      return _db_timer.total();
   }

   void
   module::_read_db_options( const options::xml_dict& global_dict )
   {
      LOG_ENTER();

#ifndef MULTIDB
      // Extract database details.
      _dbtype = global_dict.get<string>( "settings:database:type","postgresql" );
      _dbname = global_dict.get<string>( "database" );
      if( _dbtype != "sqlite" )
      {
         _dbhost = global_dict.get<string>( "settings:database:host" );
         _dbport = global_dict.get<string>( "settings:database:port" );
         _dbuser = global_dict.get<string>( "settings:database:user" );
         _dbpass = global_dict.get<string>( "settings:database:password" );
      }
      _tree_pre = global_dict.get<string>( "settings:database:treetableprefix", "tree_" );
#endif

      // Read the batch size from the dictinary.
      _batch_size = global_dict.get<unsigned>( "settings:database:batch-size",100 );
      LOGDLN( "Setting batch size to ", _batch_size );

      LOG_EXIT();
   }

   void
   module::_db_connect()
   {
      LOG_ENTER();

#ifdef MULTIDB
      // Fire up the multidb.
      ASSERT( _global_dict );
      _db = new multidb( *_global_dict );
      _db->OpenAllConnections();
#else
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
#endif

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
#ifdef MULTIDB
	 delete _db;
	 _db = NULL;
#else
	 _sql.close();
#endif
         _connected = false;
      }
   }

   bool
   module::_db_cycle()
   {
      LOG_ENTER();

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

      LOG_EXIT();
   }

}
