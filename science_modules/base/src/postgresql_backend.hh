#ifndef tao_base_postgresql_backend_hh
#define tao_base_postgresql_backend_hh

#include <boost/format.hpp>
#include <soci/soci.h>
#include <soci/postgresql/soci-postgresql.h>
#include "rdb_backend.hh"
#include "tile_table_iterator.hh"

namespace tao {
   namespace backends {

      template< class T >
      class postgresql_galaxy_iterator;

      template< class T >
      class postgresql_table_iterator;

      template< class T >
      class postgresql
         : public backends::rdb<T>
      {
         friend class postgresql_table_iterator<T>;

      public:

         typedef T real_type;
         typedef postgresql_galaxy_iterator<real_type> galaxy_iterator;
         typedef postgresql_table_iterator<real_type> table_iterator;
         typedef backends::tile_table_iterator<postgresql> tile_table_iterator;

      public:

         postgresql()
         {
         }

         void
         connect( const string& dbname,
                  const string& user,
                  const string& passwd,
                  optional<const string&> host = optional<const string&>(),
                  optional<uint16> port = optional<uint16>() )
         {
            // Connect to the table.
            LOGILN( "Connecting to postgresql database.", setindent( 2 ) );
#ifndef NLOG
            if( host )
               LOGILN( "Host: ", *host );
            if( port )
               LOGILN( "Port: ", *port );
#endif
            LOGILN( "Database: ", dbname );
            LOGILN( "User: ", user );
            string conn = boost::str(boost::format( "dbname=%1% user=%2% password='%3%'" ) % dbname % user % passwd);
            if( host )
               conn += " host=" + *host;
            if( port )
               conn += " port=" + to_string( *port );
            _sql.open( soci::postgresql, conn );
            LOGILN( "Done.", setindent( -2 ) );

            // Always load table information in one go.
            _load_table_info();
         }

         void
         reconnect()
         {
            LOGILN( "Reconnecting to PostgresQL database.", setindent( 2 ) );
            _sql.reconnect();
            LOGILN( "Done.", setindent( -2 ) );
         }

         // galaxy_iterator
         // galaxy_begin( const box<real_type>& box )
         // {
         //    string qs = make_box_query_string();
         //    table_iterator ti = make_table_iterator();
         //    return galaxy_iterator( qs, ti );
         // }

         // galaxy_iterator
         // galaxy_begin( const tile<real_type>& tile )
         // {
         //    return galaxy_iterator();
         // }

         // galaxy_iterator
         // galaxy_end() const
         // {
         //    return galaxy_iterator();
         // }

         table_iterator
         table_begin() const
         {
            return table_iterator( *this, 0 );
         }

         table_iterator
         table_end() const
         {
            return table_iterator( *this, _tbls.size() );
         }

         tile_table_iterator
         table_begin( const tile<real_type>& tile ) const
         {
            return tile_table_iterator( tile, *this );
         }

         tile_table_iterator
         table_end( const tile<real_type>& tile ) const
         {
            return tile_table_iterator( tile, *this, true );
         }

      protected:

         void
         _load_table_info()
         {
            LOGILN( "Loading tree table information.", setindent( 2 ) );

            // Extract the size and allocate.
            int size;
            _sql << "SELECT COUNT(*) FROM summary", soci::into( size );
            _minx.resize( size );
            _miny.resize( size );
            _minz.resize( size );
            _maxx.resize( size );
            _maxy.resize( size );
            _maxz.resize( size );
            _tbls.resize( size );
            LOGILN( "Number of tables: ", size );

            // Now extract table info.
            _sql << "SELECT minx, miny, minz, maxx, maxy, maxz, tablename FROM summary",
               soci::into( _minx ), soci::into( _miny ), soci::into( _minz ),
               soci::into( _maxx ), soci::into( _maxy ), soci::into( _maxz ),
               soci::into( _tbls );

            LOGILN( "Done.", setindent( -2 ) );
         }

      protected:

         soci::session _sql;
         std::vector<double> _minx, _miny, _minz;
         std::vector<double> _maxx, _maxy, _maxz;
         std::vector<std::string> _tbls;
      };

      // template< class T >
      // class postgresql_galaxy_iterator
      //    : public boost::iterator_facade< postgresql_galaxy_iterator<T>,
      //                                     galaxy<T>&,
      //                                     std::forward_iterator_tag,
      //                                     galaxy<T>& >
      // {
      //    friend class boost::iterator_core_access;

      // public:

      //    typedef T real_type;
      //    typedef galaxy<real_type>& value_type;
      //    typedef value_type reference_type;

      // public:

      //    postgresql_galaxy_iterator()
      //    {
      //    }

      //    postgresql_galaxy_iterator( const string& query,
      //                                const table_iterator& table_begin,
      //                                const table_iterator& table_end )
      //       : _query( query ),
      //         _table_pos( table_begin ),
      //         _table_end( table_end )
      //    {
      //    }

      // protected:

      //    void
      //    increment()
      //    {
      //       // Try and fetch more rows. If there are none we need to move
      //       // to the next table.
      //       while( !_fetch() )
      //       {
      //          // Move on to the next table unless we've exhausted them.
      //          ++_table_pos;
      //          if( _table_pos == _table_end )
      //             break;
      //       }
      //    }

      //    bool
      //    equal( const galaxy_iterator& op ) const
      //    {
      //       return _table_pos == op._table_pos;
      //    }

      //    reference_type
      //    dereference() const
      //    {
      //       return _gal;
      //    }

      //    void
      //    _fetch()
      //    {
      //       ASSERT( _st, "No statement available on galaxy iterator." );

      //       // Clear out the current galaxy object.
      //       _gal.clear();
      //       _gal.set_table( *_table_pos );

      //       // Actually perform the fetch.
      //       bool rows_exist = _st->fetch();
      //       if( rows_exist )
      //       {
      //          // Update the galaxy object.
      //          unsigned ii = 0;
      //          for( const string& name : _out_fields )
      //          {
      //             switch( _field_types[ii] )
      //             {
      //                case galaxy::STRING:
      //                   _gal.set_batch_size( ((vector<string>*)_field_stor[ii])->size() );
      //                   _gal.set_field<string>( name, *(vector<string>*)_field_stor[ii] );
      //                   break;

      //                case galaxy::DOUBLE:
      //                   _gal.set_batch_size( ((vector<double>*)_field_stor[ii])->size() );
      //                   _gal.set_field<double>( name, *(vector<double>*)_field_stor[ii] );
      //                   break;

      //                case galaxy::INTEGER:
      //                   _gal.set_batch_size( ((vector<int>*)_field_stor[ii])->size() );
      //                   _gal.set_field<int>( name, *(vector<int>*)_field_stor[ii] );
      //                   break;

      //                case galaxy::UNSIGNED_LONG_LONG:
      //                   _gal.set_batch_size( ((vector<unsigned long long>*)_field_stor[ii])->size() );
      //                   _gal.set_field<unsigned long long>( name, *(vector<unsigned long long>*)_field_stor[ii] );
      //                   break;

      //                case galaxy::LONG_LONG:
      //                   _gal.set_batch_size( ((vector<long long>*)_field_stor[ii])->size() );
      //                   _gal.set_field<long long>( name, *(vector<long long>*)_field_stor[ii] );
      //                   break;

      //                default:
      //                   ASSERT( 0, "Unknown field type." );
      //             }

      //             // Don't forget to advance.
      //             ++ii;
      //          }
      //       }

      //       // Return whether we got any rows.
      //       return rows_exist;
      //    }

      // protected:

      //    soci::statement* _st;
      //    galaxy<real_type> _gal;
      // };

      template< class T >
      class postgresql_table_iterator
         : public boost::iterator_facade< postgresql_table_iterator<T>,
                                          typename rdb<T>::table,
                                          std::forward_iterator_tag,
                                          typename rdb<T>::table >
      {
         friend class boost::iterator_core_access;

      public:

         typedef T real_type;
         typedef typename rdb<real_type>::table value_type;
         typedef value_type reference_type;

      public:

         postgresql_table_iterator( const postgresql<real_type>& be,
                                    unsigned idx )
            : _be( be ),
              _idx( idx )
         {
         }

      protected:

         void
         increment()
         {
            ++_idx;
         }

         bool
         equal( const postgresql_table_iterator& op ) const
         {
            return _idx == op._idx;
         }

         reference_type
         dereference() const
         {
            return typename rdb<real_type>::table( _be._tbls[_idx],
                                                   _be._minx[_idx], _be._miny[_idx], _be._minz[_idx],
                                                   _be._maxx[_idx], _be._maxy[_idx], _be._maxz[_idx] );
         }

      protected:

         const postgresql<real_type>& _be;
         unsigned _idx;
      };

   }
}

#endif
