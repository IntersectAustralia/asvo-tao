#ifndef tao_base_postgresql_backend_hh
#define tao_base_postgresql_backend_hh

#include <soci/soci-postgresql.h>
#include "rdb_backend.hh"

namespace tao {
   namespace backends {

      template< class T >
      class postgresql
         : public rdb_backend
      {
      public:

         typedef T real_type;
         typedef postgresql_galaxy_iterator<real_type> galaxy_iterator;

      public:

         postgresql()
         {
         }

         void
         connect( const string& host,
                  uint16 port,
                  const string& dbname,
                  const string& user,
                  const string& passwd )
         {
            LOGILN( "Connecting to postgresql database.", setindent( 2 ) );
            LOGILN( "Host: ", host );
            LOGILN( "Port: ", port );
            LOGILN( "Database: ", dbname );
            LOGILN( "User: ", user );
            boost::format conn( "host=%1% port=%2% dbname=%3% user=%4% password='%5%'" );
            fmt % host % port % dbname % user % passwd;
            _sql.open( soci::postgresql, conn.str() );
         }

         void
         reconnect()
         {
            _sql.reconnect();
         }

         galaxy_iterator
         galaxy_begin( const box<real_type>& box )
         {
            string qs = make_box_query_string();
            table_iterator ti = make_table_iterator();
            return galaxy_iterator( qs, ti );
         }

         galaxy_iterator
         galaxy_begin( const tile<real_type>& tile )
         {
            return galaxy_iterator();
         }

         galaxy_iterator
         galaxy_end() const
         {
            return galaxy_iterator();
         }

      protected:

         string
         _make_box_query( const box<real_type>& box )
         {
            string query = "SELECT * F";
         }

      protected:

         soci::session _sql;
      };

      template< class T >
      class postgresql_galaxy_iterator
         : public boost::iterator_facade< postgresql_galaxy_iterator<T>,
                                          galaxy<T>&,
                                          std::forward_iterator_tag,
                                          galaxy<T>& >
      {
         friend class boost::iterator_core_access;

      public:

         typedef T real_type;
         typedef galaxy<real_type>& value_type;
         typedef value_type reference_type;

      public:

         galaxy_iterator()
         {
         }

         galaxy_iterator( const string& query,
                          const table_iterator& table_begin,
                          const table_iterator& table_end )
            : _query( query ),
              _table_pos( table_begin ),
              _table_end( table_end )
         {
         }

      protected:

         void
         increment()
         {
            // Try and fetch more rows. If there are none we need to move
            // to the next table.
            while( !_fetch() )
            {
               // Move on to the next table unless we've exhausted them.
               ++_table_pos;
               if( _table_pos == _table_end )
                  break;
            }
         }

         bool
         equal( const galaxy_iterator& op ) const
         {
            return _table_pos == op._table_pos;
         }

         reference_type
         dereference() const
         {
            return _gal;
         }

         void
         _fetch()
         {
            ASSERT( _st, "No statement available on galaxy iterator." );

            // Clear out the current galaxy object.
            _gal.clear();
            _gal.set_table( *_table_pos );

            // Actually perform the fetch.
            bool rows_exist = _st->fetch();
            if( rows_exist )
            {
               // Update the galaxy object.
               unsigned ii = 0;
               for( const string& name : _out_fields )
               {
                  switch( _field_types[ii] )
                  {
                     case galaxy::STRING:
                        _gal.set_batch_size( ((vector<string>*)_field_stor[ii])->size() );
                        _gal.set_field<string>( name, *(vector<string>*)_field_stor[ii] );
                        break;

                     case galaxy::DOUBLE:
                        _gal.set_batch_size( ((vector<double>*)_field_stor[ii])->size() );
                        _gal.set_field<double>( name, *(vector<double>*)_field_stor[ii] );
                        break;

                     case galaxy::INTEGER:
                        _gal.set_batch_size( ((vector<int>*)_field_stor[ii])->size() );
                        _gal.set_field<int>( name, *(vector<int>*)_field_stor[ii] );
                        break;

                     case galaxy::UNSIGNED_LONG_LONG:
                        _gal.set_batch_size( ((vector<unsigned long long>*)_field_stor[ii])->size() );
                        _gal.set_field<unsigned long long>( name, *(vector<unsigned long long>*)_field_stor[ii] );
                        break;

                     case galaxy::LONG_LONG:
                        _gal.set_batch_size( ((vector<long long>*)_field_stor[ii])->size() );
                        _gal.set_field<long long>( name, *(vector<long long>*)_field_stor[ii] );
                        break;

                     default:
                        ASSERT( 0, "Unknown field type." );
                  }

                  // Don't forget to advance.
                  ++ii;
               }

               // Return whether we got any rows.
               return rows_exist;
            }

           protected:

            soci::statement* _st;
            galaxy<real_type> _gal;
         };

      }
}

#endif
