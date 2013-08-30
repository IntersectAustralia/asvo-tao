#ifndef tao_base_soci_backend_hh
#define tao_base_soci_backend_hh

#include "soci_base_backend.hh"
#ifdef HAVE_POSTGRESQL
#include <soci/postgresql/soci-postgresql.h>
#endif
#ifdef HAVE_SQLITE3
#include <soci/sqlite3/soci-sqlite3.h>
#endif

namespace tao {
   namespace backends {

      template< class T >
      class soci
         : public soci_base<T>
      {
      public:

         enum database_type {
#ifdef HAVE_POSTGRESQL
            POSTGRESQL
#ifdef HAVE_SQLITE3
            ,
#endif
#endif
#ifdef HAVE_SQLITE3
            SQLITE3
#endif
         };

         typedef T real_type;
         typedef soci_base<real_type> super_type;

      public:

         soci( const simulation<real_type>* sim = NULL )
            : super_type( sim ),
              _my_sql( false ),
              _sql( 0 )
         {
         }

         void
         disconnect()
         {
            LOGILN( "Disconnecting from database.\n" );
            if( _my_sql )
               delete _sql;
            _my_sql = false;
            _sql = 0;
         }

         void
         connect( const string& dbname,
                  optional<const string&> user = optional<const string&>(),
                  optional<const string&> passwd = optional<const string&>(),
                  optional<const string&> host = optional<const string&>(),
                  optional<uint16> port = optional<uint16>() )
         {
            // Connect to the database.
            LOGILN( "Connecting to database via SOCI.", setindent( 2 ) );
#ifndef NLOG
            if( host )
               LOGILN( "Host: ", *host );
            if( port )
               LOGILN( "Port: ", *port );
#endif
            LOGILN( "Database: ", dbname );
            string conn = boost::str( boost::format( "dbname=%1%" ) % dbname );
            if( user )
               conn += " user=" + *user;
            if( passwd )
               conn += " password='" + *passwd + "'";
            if( host )
               conn += " host=" + *host;
            if( port )
               conn += " port=" + to_string( *port );

            // Create a session.
            disconnect();
            _my_sql = true;
            _sql = new ::soci::session;
#ifdef HAVE_POSTGRESQL
            if( user )
               session().open( ::soci::postgresql, conn );
#ifdef HAVE_SQLITE3
            else
#endif
#endif
#ifdef HAVE_SQLITE3
            if( !user )
               session().open( ::soci::sqlite3, conn );
#elif !defined( NDEBUG )
            else
               ASSERT( 0, "Could not detect database connection type." );
#endif
            this->_con = true;
            LOGILN( "Done.", setindent( -2 ) );

            // Check for update.
            this->_initialise();
         }

         void
         connect( ::soci::session& sql )
         {
            disconnect();
            _my_sql = false;
            _sql = &sql;
         }

         void
         reconnect()
         {
            LOGILN( "Reconnecting to database via SOCI.", setindent( 2 ) );
            session().reconnect();
            LOGILN( "Done.", setindent( -2 ) );
         }

         virtual
         ::soci::session&
         session()
         {
            return *_sql;
         }

         virtual
         ::soci::session&
         session( const string& table )
         {
            return *_sql;
         }

      protected:

         bool _my_sql;
         ::soci::session* _sql;
      };

   }
}

#endif
