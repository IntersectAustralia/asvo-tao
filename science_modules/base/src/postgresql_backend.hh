#ifndef tao_base_postgresql_backend_hh
#define tao_base_postgresql_backend_hh

#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <soci/soci.h>
#include <soci/postgresql/soci-postgresql.h>
#include "rdb_backend.hh"
#include "tile_table_iterator.hh"
#include "batch.hh"

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
         typedef tao::query<postgresql<real_type>> query_type;
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
         }

         void
         reconnect()
         {
            LOGILN( "Reconnecting to PostgresQL database.", setindent( 2 ) );
            _sql.reconnect();
            LOGILN( "Done.", setindent( -2 ) );
         }

         void
         initialise( const simulation<real_type>& sim )
         {
            // Always load table information in one go.
            _load_table_info();

            // Gotta get the types for all the fields.
            _load_field_types();

            // Create temporary snapshot range table.
            LOGILN( "Making redshift range table.", setindent( 2 ) );
            _sql << this->make_snap_rng_query_string( sim );
            LOGILN( "Done.", setindent( -2 ) );
         }

         void
         init_batch( batch<real_type>& bat,
                     tao::query<real_type>& query )
         {
            for( const auto& field : query.output_fields() )
               bat.set_scalar( field, _field_types.at( _field_map.at( field ) ) );
         }

         galaxy_iterator
         galaxy_begin( query_type& query,
                       const tile<real_type>& tile )
         {
            string qs = make_tile_query_string( tile, query );
            return galaxy_iterator( *this, query, qs, table_begin( tile ), table_end( tile ) );
         }

         // galaxy_iterator
         // galaxy_end( const tile<real_type>& tile ) const
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

         void
         _load_field_types()
         {
            LOGILN( "Extracting field types.", setindent( 2 ) );
            soci::rowset<soci::row> rs = _sql.prepare << "SELECT column_name, data_type FROM information_schema.columns"
               " WHERE table_name = " + _tbls[0];
            _field_types.clear();
            for( soci::rowset<soci::row>::const_iterator it = rs.begin(); it != rs.end(); ++it )
            {
               batch::field_value_type type;
               string type_str = it.get<std::string>( 1 );
               LOGILN( it.get<std::string>( 0 ), ": ", type_str );
               if( type_str == "string" )
                  type = batch::STRING;
               else if( type_str == "integer" )
                  type = batch::INTEGER;
               else if( type_str == "bigint" )
                  type = batch::LONG_LONG;
#ifndef NDEBUG
               else
                  ASSERT( 0, "Unknown field type." );
#endif
               _field_types.insert( it.get<std::string>( 0 ), type );
            }
            LOGILN( "Done.", setindent( -2 ) );
         }

      protected:

         soci::session _sql;
         map<string,batch<real_type>::field_value_type> _field_types;
         std::vector<double> _minx, _miny, _minz;
         std::vector<double> _maxx, _maxy, _maxz;
         std::vector<std::string> _tbls;
      };

      template< class T >
      class postgresql_galaxy_iterator
         : public boost::iterator_facade< postgresql_galaxy_iterator<T>,
                                          batch<T>&,
                                          std::forward_iterator_tag,
                                          batch<T>& >
      {
         friend class boost::iterator_core_access;

      public:

         typedef T real_type;
         typedef tao::query<postgresql<real_type>> query_type;
         typedef typename postgresql<real_type>::table_iterator table_iterator;
         typedef batch<real_type>& value_type;
         typedef value_type reference_type;

      public:

         postgresql_galaxy_iterator( postgresql<real_type>& be,
                                     query_type& query )
            : _be( be ),
              _query( query ),
              _done( true )
         {
         }

         template< class Seq >
         postgresql_galaxy_iterator( postgersql<real_type>& be,
                                     query_type& query,
                                     const string& query_str,
                                     const table_iterator& table_begin,
                                     const table_iterator& table_end )
            : _be( be ),
              _query( query ),
              _query_str( query_str ),
              _table_pos( table_begin ),
              _table_end( table_end ),
              _st( NULL ),
              _done( false )
         {
            // Prepare the batch object.
            be.init_batch( _bat, _query );

            // Need to get to first position.
            _prepare();
            increment();
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

               // If we're not done yet, prepare the next statement.
               _prepare();
            }
         }

         bool
         equal( const postgresql_galaxy_iterator& op ) const
         {
            return _done == op._done;
         }

         reference_type
         dereference() const
         {
            return _bat;
         }

         void
         _prepare( const string& table )
         {
            // Delete any existing statement.
            if( _st )
               delete _st;

            auto prep = _sql->prepare << boost::algorithm::replace_all_copy( _query_str, "-table-", table );
            for( unsigned ii = 0; ii < query.output_fields().size(); ++ii )
            {
               const auto& field = _bat.field( query.output_fields()[ii] );
               const auto& type = std::get<2>( field );
               switch( type )
               {
                  case galaxy::STRING:
                     prep = prep, soci::into( *boost::any_cast<(std::vector<std::string>*)>( std::get<0>( field ) ) );
                     break;
                  case galaxy::DOUBLE:
                     prep = prep, soci::into( *boost::any_cast<(std::vector<double>*)>( std::get<0>( field ) ) );
                     break;
                  case galaxy::INTEGER:
                     prep = prep, soci::into( *boost::any_cast<(std::vector<int>*)>( std::get<0>( field ) ) );
                     break;
                  case galaxy::LONG_LONG:
                     prep = prep, soci::into( *boost::any_cast<(std::vector<long long>*)>( std::get<0>( field ) ) );
                     break;
                  case galaxy::UNSIGNED_LONG_LONG:
                     prep = prep, soci::into( *boost::any_cast<(std::vector<unsigned long long>*)>( std::get<0>( field ) ) );
                     break;
                  default:
                     ASSERT( 0, "Unknown field type." );
               }
            }

            // Prepare and execute the query without
            // fetching anything yet.
            _st = new soci::statement( prep );
            _st->execute();

            // Store the current table on the object.
            _bat.set_attribute( "table", table );
         }

         bool
         _fetch()
         {
            ASSERT( _st, "No statement available on galaxy iterator." );

            // Actually perform the fetch.
            bool rows_exist = _st->fetch();
            _bat.update_size();

            // Return whether we got any rows.
            return rows_exist;
         }

      protected:

         query_type* _query;
         soci::session* _sql;
         string _query_str;
         table_iterator _table_pos, _table_end;
         soci::statement* _st;
         batch<real_type> _bat;
         bool _done;
      };

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
