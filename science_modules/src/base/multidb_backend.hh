#ifndef tao_base_multidb_backend_hh
#define tao_base_multidb_backend_hh

#include <stdint.h>
#include <string>
#include <boost/optional.hpp>
#include <boost/lexical_cast.hpp>
#include "soci_base_backend.hh"
#include "multidb.hh"
#include "xml_dict.hh"

namespace tao {
   namespace backends {

      template< class T >
      class multidb
         : public soci_base<T>
      {
      public:

         struct server_type
         {
            std::string dbname;
            std::string user;
            std::string passwd;
            boost::optional<std::string> host;
            boost::optional<uint16_t> port;
         };

         typedef T real_type;
         typedef soci_base<real_type> super_type;

      public:

         multidb( const simulation* sim = NULL )
            : super_type( sim )
         {
         }

         void
         connect( const xml_dict& global_dict )
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
            LOGBLOCKI( "Connecting to database via multidb." );

            // Process each server.
            while( start != finish )
            {
               LOGBLOCKI( "Adding server:" );
#ifndef NLOG
               if( start->host )
                  LOGILN( "Host: ", *start->host );
               if( start->port )
                  LOGILN( "Port: ", *start->port );
#endif
               const auto& serv = *start++;
               _mdb.AddNewServer( serv.dbname, *serv.host, serv.user, serv.passwd, boost::lexical_cast<std::string>( *serv.port ) );
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
            LOGBLOCKI( "Reconnecting to database via multidb." );
            // _mdb.reconnect();
         }

         virtual
         ::soci::session&
         session()
         {
            return _mdb["tree_0"];
         }

         virtual
         ::soci::session&
         session( const std::string& table )
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

            if( this->_init_tbls )
            {
               // Create temporary snapshot range table.
               if( this->_sim )
               {
                  LOGBLOCKI( "Making redshift range tables." );
                  for( auto& pair : _mdb.CurrentServers )
                  {
                     pair.second->OpenConnection();

                     // Try and drop the redshift range table.
                     try
                     {
                        pair.second->Connection << this->make_drop_snap_rng_query_string();
                     }
                     catch( const ::soci::soci_error& ex )
                     {
                     }

                     auto queries = this->make_snap_rng_query_string( *this->_sim );
                     for( const auto& query : queries )
                        pair.second->Connection << query;
                  }
               }
            }
         }

      protected:

         tao::multidb _mdb;
      };

   }
}

#endif
