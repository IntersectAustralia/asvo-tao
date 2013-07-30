#ifndef tao_base_multidb_backend_hh
#define tao_base_multidb_backend_hh

#include "soci_base_backend.hh"
#include "multidb.hh"

namespace tao {
   namespace backends {

      template< class T >
      class multidb
         : public soci_base<T>
      {
      public:

         struct server_type
         {
            string dbname;
            string user;
            string passwd;
            optional<string> host;
            optional<uint16> port;
         };

         typedef T real_type;
         typedef soci_base<real_type> super_type;

      public:

         multidb( const simulation<real_type>* sim = NULL )
            : super_type( sim )
         {
         }

         void
         connect( const options::xml_dict& global_dict )
         {
            _mdb.Connect( global_dict );
            this->_con = true;
            this->_initialise();
         }

         template< class Iterator >
         void
         connect( Iterator start,
                  const Iterator& finish )
         {
            LOGILN( "Connecting to database via multidb.", setindent( 2 ) );

            // Process each server.
            while( start != finish )
            {
               LOGILN( "Adding server:", setindent( 2 ) );
#ifndef NLOG
               if( start->host )
                  LOGILN( "Host: ", *start->host );
               if( start->port )
                  LOGILN( "Port: ", *start->port );
#endif
               const auto& serv = *start++;
               _mdb.AddNewServer( serv.dbname, *serv.host, serv.user, serv.passwd, to_string( *serv.port ) );
               LOGILN( "Done.", setindent( -2 ) );
            }

            // Open all the connections and mark as ready.
            _mdb.OpenAllConnections();
            this->_con = true;

            // Check for update.
            _initialise();
         }

         void
         reconnect()
         {
            LOGILN( "Reconnecting to database via multidb.", setindent( 2 ) );
            // _mdb.reconnect();
            LOGILN( "Done.", setindent( -2 ) );
         }

         virtual
         ::soci::session&
         session()
         {
            return _mdb["tree_1"];
         }

         virtual
         ::soci::session&
         session( const string& table )
         {
            return _mdb[table];
         }

      protected:

         virtual
         void
         _initialise()
         {
            ASSERT( this->_con, "Not connected to database." );

            if( this->_tbls.empty() )
               this->_load_table_info();

            if( this->_field_map.empty() )
               this->_load_field_types();

            // Create temporary snapshot range table.
            if( this->_sim )
            {
               LOGILN( "Making redshift range tables.", setindent( 2 ) );
               for( auto& pair : _mdb.CurrentServers )
               {
                  pair.second->OpenConnection();
                  pair.second->Connection << this->make_snap_rng_query_string( *this->_sim );
               }
               LOGILN( "Done.", setindent( -2 ) );
            }
         }

      protected:

         tao::multidb _mdb;
      };

   }
}

#endif
