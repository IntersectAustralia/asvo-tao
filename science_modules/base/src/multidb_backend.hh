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
            ::soci::backend_factory factory;
            string dbname;
            string user;
            string passwd;
            optional<string> host;
            optional<uint16> port;
         };

         typedef T real_type;
         typedef soci_base<real_type> super_type;

      public:

         multidb( const simulation<real_type>* sim )
            : super_type( sim )
         {
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
               // _mdb.add_server( *start++ );
            }
            _con = true;

            // Check for update.
            if( _sim && _con )
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
            ASSERT( this->_sim, "No simulation set." );
            ASSERT( this->_con, "Not connected to database." );

            _load_table_info();
            _load_field_types();

            // Create temporary snapshot range table.
            LOGILN( "Making redshift range tables.", setindent( 2 ) );
            for( auto& pair : _db->CurrentServers )
               pair.second->Connection << this->make_snap_rng_query_string( sim );
            LOGILN( "Done.", setindent( -2 ) );
         }

      protected:

         multidb _mdb;
      };

   }
}

#endif
