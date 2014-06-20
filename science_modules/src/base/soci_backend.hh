#ifndef tao_base_soci_backend_hh
#define tao_base_soci_backend_hh

#include <stdint.h>
#include <string>
#include <boost/optional.hpp>
#include <boost/lexical_cast.hpp>
#include "soci_base_backend.hh"
#ifdef HAVE_POSTGRESQL
#include <soci/postgresql/soci-postgresql.h>
#endif
#ifdef HAVE_SQLITE3
#include <soci/sqlite3/soci-sqlite3.h>
#endif
#include "xml_dict.hh"
#include "types.hh"

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

         soci( const simulation* sim = NULL )
            : super_type( sim ),
              _my_sql( false ),
              _sql( 0 )
         {
         }

         void
         disconnect()
         {
            LOGILN( "Disconnecting from database." );
            if( _my_sql )
               delete _sql;
            _my_sql = false;
            _sql = 0;
         }

         void
         connect( const std::string& dbname,
                  boost::optional<const std::string&> user = boost::optional<const std::string&>(),
                  boost::optional<const std::string&> passwd = boost::optional<const std::string&>(),
                  boost::optional<const std::string&> host = boost::optional<const std::string&>(),
                  boost::optional<uint16_t> port = boost::optional<uint16_t>() )
         {
            disconnect();

            // Connect to the database.
            LOGILN( "Connecting to database via SOCI.", setindent( 2 ) );
#ifndef NLOG
            if( host )
               LOGILN( "Host: ", *host );
            if( port )
               LOGILN( "Port: ", *port );
#endif
            LOGILN( "Database: ", dbname );
            std::string conn = boost::str( boost::format( "dbname=%1%" ) % dbname );
            if( user )
               conn += " user=" + *user;
            if( passwd )
               conn += " password='" + *passwd + "'";
            if( host )
               conn += " host=" + *host;
            if( port )
               conn += " port=" + boost::lexical_cast<std::string>( *port );

            // Create a session.
            _my_sql = true;
            {
               auto db_timer = this->db_timer().start();

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
            }
            this->_con = true;
            LOGILN( "Done.", setindent( -2 ) );

            // Check for update.
            this->_initialise();
         }

         void
         connect( const xml_dict& global_dict )
         {
            ASSERT( 0, "Not implemented yet." );
         }

         void
         connect( ::soci::session& sql )
         {
            disconnect();

            LOGILN( "Connecting to database via SOCI.", setindent( 2 ) );
            LOGILN( "Aliasing existing session." );
            _my_sql = false;
            _sql = &sql;
            this->_con = true;
            this->_initialise();
            LOGILN( "Done." );
         }

         void
         reconnect()
         {
            LOGILN( "Reconnecting to database via SOCI.", setindent( 2 ) );
            {
               auto db_timer = this->db_timer().start();
               session().reconnect();
            }
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
         session( const std::string& table )
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
