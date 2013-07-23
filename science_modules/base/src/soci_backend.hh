#ifndef tao_base_soci_backend_hh
#define tao_base_soci_backend_hh

#include "soci_base_backend.hh"
#include <soci/postgresql/soci-postgresql.h>

namespace tao {
   namespace backends {

      template< class T >
      class soci
         : public soci_base<T>
      {
      public:

         typedef T real_type;
         typedef soci_base<real_type> super_type;

      public:

         soci( const simulation<real_type>* sim = NULL )
            : super_type( sim )
         {
         }

         void
         connect( const string& dbname,
                  const string& user,
                  const string& passwd,
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
            string conn = boost::str(boost::format( "dbname=%1% user=%2% password='%3%'" ) % dbname % user % passwd);
            if( host )
               conn += " host=" + *host;
            if( port )
               conn += " port=" + to_string( *port );
            session().open( ::soci::postgresql, conn );
            this->_con = true;
            LOGILN( "Done.", setindent( -2 ) );

            // Check for update.
            if( this->_sim && this->_con )
               this->_initialise();
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
            return _sql;
         }

         virtual
         ::soci::session&
         session( const string& table )
         {
            return _sql;
         }

      protected:

         ::soci::session _sql;
      };

   }
}

#endif
