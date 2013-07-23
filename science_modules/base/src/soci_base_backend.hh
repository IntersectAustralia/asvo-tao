#ifndef tao_base_soci_base_backend_hh
#define tao_base_soci_base_backend_hh

#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <soci/soci.h>
#include "rdb_backend.hh"
#include "tile_table_iterator.hh"
#include "batch.hh"

namespace tao {
   namespace backends {

      template< class T,
                class TableIter >
      class soci_galaxy_iterator;

      template< class T >
      class soci_table_iterator;

      template< class T >
      class soci_base
         : public rdb<T>
      {
         friend class soci_table_iterator<T>;

      public:

         typedef T real_type;
         typedef rdb<real_type> super_type;
         typedef tao::query<real_type> query_type;
         typedef soci_table_iterator<real_type> table_iterator;
         typedef backends::tile_table_iterator<soci_base> tile_table_iterator;
         typedef soci_galaxy_iterator<real_type,table_iterator> galaxy_iterator;
         typedef soci_galaxy_iterator<real_type,tile_table_iterator> tile_galaxy_iterator;

      public:

         soci_base( const simulation<real_type>* sim )
            : super_type( sim )
         {
         }

         virtual
         ::soci::session&
         session() = 0;

         virtual
         ::soci::session&
         session( const string& table ) = 0;

         tile_galaxy_iterator
         galaxy_begin( query_type& query,
                       const tile<real_type>& tile )
         {
            string qs = this->make_tile_query_string( tile, query );
            return tile_galaxy_iterator( *this, query, qs, table_begin( tile ), table_end( tile ) );
         }

         tile_galaxy_iterator
         galaxy_end( query_type& query,
                     const tile<real_type>& tile )
         {
            return tile_galaxy_iterator( *this, query, "", table_end( tile ), table_end( tile ), true );
         }

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

         virtual
         void
         _initialise()
         {
            ASSERT( this->_sim, "No simulation set." );
            ASSERT( this->_con, "Not connected to database." );

            // Always load table information in one go.
            _load_table_info();

            // Gotta get the types for all the fields.
            _load_field_types();

            // Create temporary snapshot range table.
            LOGILN( "Making redshift range table.", setindent( 2 ) );
            session() << this->make_snap_rng_query_string( *this->_sim );
            LOGILN( "Done.", setindent( -2 ) );
         }

         void
         _load_table_info()
         {
            LOGILN( "Loading tree table information.", setindent( 2 ) );

            // Extract the size and allocate.
            int size;
            session() << "SELECT COUNT(*) FROM summary", soci::into( size );
            _minx.resize( size );
            _miny.resize( size );
            _minz.resize( size );
            _maxx.resize( size );
            _maxy.resize( size );
            _maxz.resize( size );
            _tbls.resize( size );
            LOGILN( "Number of tables: ", size );

            // Now extract table info.
            session() << "SELECT minx, miny, minz, maxx, maxy, maxz, tablename FROM summary",
               soci::into( _minx ), soci::into( _miny ), soci::into( _minz ),
               soci::into( _maxx ), soci::into( _maxy ), soci::into( _maxz ),
               soci::into( _tbls );

            LOGILN( "Done.", setindent( -2 ) );
         }

         void
         _load_field_types()
         {
            LOGILN( "Extracting field types.", setindent( 2 ) );
            soci::rowset<soci::row> rs = session( _tbls[0] ).prepare << "SELECT column_name, data_type FROM information_schema.columns"
               " WHERE table_name = '" + _tbls[0] + "'";
            this->_field_types.clear();
            for( soci::rowset<soci::row>::const_iterator it = rs.begin(); it != rs.end(); ++it )
            {
               typename batch<real_type>::field_value_type type;
               string type_str = it->get<std::string>( 1 );
               LOGILN( it->get<std::string>( 0 ), ": ", type_str );
               if( type_str == "string" )
                  type = batch<real_type>::STRING;
               else if( type_str == "integer" )
                  type = batch<real_type>::INTEGER;
               else if( type_str == "bigint" )
                  type = batch<real_type>::LONG_LONG;
               else if( type_str == "real" )
                  type = batch<real_type>::DOUBLE;
#ifndef NDEBUG
               else
                  ASSERT( 0, "Unknown field type." );
#endif

               // Insert into field types.
               this->_field_types.insert( it->get<std::string>( 0 ), type );

               // Prepare default mapping.
               this->_field_map[it->get<std::string>( 0 )] = it->get<std::string>( 0 );
            }

            // Before finishing, insert the known mapping conversions.
            // TODO: Generalise.
            this->_field_map["pos_x"] = "posx";
            this->_field_map["pos_y"] = "posy";
            this->_field_map["pos_z"] = "posz";
            this->_field_map["snapshot"] = "snapnum";
            this->_field_map["global_tree_id"] = "globaltreeid";
            this->_field_map["local_galaxy_id"] = "localgalaxyid";

            LOGILN( "Done.", setindent( -2 ) );
         }

      protected:

         std::vector<double> _minx, _miny, _minz;
         std::vector<double> _maxx, _maxy, _maxz;
         std::vector<std::string> _tbls;
      };

      template< class T,
                class TableIter >
      class soci_galaxy_iterator
         : public boost::iterator_facade< soci_galaxy_iterator<T,TableIter>,
                                          batch<T>&,
                                          std::forward_iterator_tag,
                                          batch<T>& >
      {
         friend class boost::iterator_core_access;

      public:

         typedef T real_type;
         typedef tao::query<real_type> query_type;
         typedef TableIter table_iterator;
         typedef batch<real_type>& value_type;
         typedef value_type reference_type;

      public:

         soci_galaxy_iterator( soci_base<real_type>& be,
                               query_type& query,
                               const string& query_str,
                               const table_iterator& table_start,
                               const table_iterator& table_finish,
                               bool done = false )
            : _be( be ),
              _query( query ),
              _query_str( query_str ),
              _table_pos( table_start ),
              _table_end( table_finish ),
              _st( NULL ),
              _done( done )
         {
            if( !_done )
            {
               if( _table_pos != _table_end )
               {
                  // Prepare the batch object.
                  be.init_batch( _bat, _query );

                  // Need to get to first position.
                  _prepare( _table_pos->name() );
                  increment();
               }
            }
         }

         soci_galaxy_iterator( const soci_galaxy_iterator& src )
            : _be( src._be ),
              _query( src._query ),
              _table_pos( src._table_pos ),
              _table_end( src._table_end )
         {
            ASSERT( 0, "Shouldn't be copying this iterator." );
         }

         soci_galaxy_iterator( soci_galaxy_iterator&& src )
            : _be( src._be ),
              _query( src._query ),
              _table_pos( src._table_pos ),
              _table_end( src._table_end )
         {
            ASSERT( 0, "Shouldn't be moving this iterator." );
         }

         reference_type
         operator*()
         {
            return _bat;
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
               {
                  _done = true;
                  break;
               }

               // If we're not done yet, prepare the next statement.
               _prepare( _table_pos->name() );
            }
         }

         bool
         equal( const soci_galaxy_iterator& op ) const
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
            LOGILN( "Preparing query for table: ", table, setindent( 2 ) );

            // Delete any existing statement.
            if( _st )
               delete _st;

            string qs = boost::algorithm::replace_all_copy( _query_str, "-table-", table );
            LOGDLN( "Query string: ", qs );
            auto prep = _be.session( table ).prepare << qs;
            for( unsigned ii = 0; ii < _query.output_fields().size(); ++ii )
            {
               const auto& field = _bat.field( _query.output_fields()[ii] );
               const auto& type = std::get<2>( field );
               switch( type )
               {
                  case batch<real_type>::STRING:
                     boost::any_cast<vector<string>*>( std::get<0>( field ) )->resize( _bat.max_size() );
                     prep = prep, soci::into( *(std::vector<std::string>*)boost::any_cast<vector<string>*>( std::get<0>( field ) ) );
                     break;
                  case batch<real_type>::DOUBLE:
                     boost::any_cast<vector<double>*>( std::get<0>( field ) )->resize( _bat.max_size() );
                     prep = prep, soci::into( *(std::vector<double>*)boost::any_cast<vector<double>*>( std::get<0>( field ) ) );
                     break;
                  case batch<real_type>::INTEGER:
                     boost::any_cast<vector<int>*>( std::get<0>( field ) )->resize( _bat.max_size() );
                     prep = prep, soci::into( *(std::vector<int>*)boost::any_cast<vector<int>*>( std::get<0>( field ) ) );
                     break;
                  case batch<real_type>::LONG_LONG:
                     boost::any_cast<vector<long long>*>( std::get<0>( field ) )->resize( _bat.max_size() );
                     prep = prep, soci::into( *(std::vector<long long>*)boost::any_cast<vector<long long>*>( std::get<0>( field ) ) );
                     break;
                  case batch<real_type>::UNSIGNED_LONG_LONG:
                     boost::any_cast<vector<unsigned long long>*>( std::get<0>( field ) )->resize( _bat.max_size() );
                     prep = prep, soci::into( *(std::vector<unsigned long long>*)boost::any_cast<vector<unsigned long long>*>( std::get<0>( field ) ) );
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

            LOGILN( "Done.", setindent( -2 ) );
         }

         bool
         _fetch()
         {
            LOGDLN( "Fetching rows.", setindent( 2 ) );
            ASSERT( _st, "No statement available on galaxy iterator." );

            // Actually perform the fetch.
            bool rows_exist = _st->fetch();
            _bat.update_size();
            LOGDLN( "Fetched ", _bat.size(), " rows." );

            // Return whether we got any rows.
            LOGDLN( "Done.", setindent( -2 ) );
            return rows_exist;
         }

      protected:

         soci_base<real_type>& _be;
         query_type& _query;
         string _query_str;
         table_iterator _table_pos, _table_end;
         soci::statement* _st;
         batch<real_type> _bat;
         bool _done;
      };

      template< class T >
      class soci_table_iterator
         : public boost::iterator_facade< soci_table_iterator<T>,
                                          typename rdb<T>::table_type,
                                          std::forward_iterator_tag,
                                          typename rdb<T>::table_type >
      {
         friend class boost::iterator_core_access;

      public:

         typedef T real_type;
         typedef typename rdb<real_type>::table_type value_type;
         typedef value_type reference_type;

      public:

         soci_table_iterator( const soci_base<real_type>& be,
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
         equal( const soci_table_iterator& op ) const
         {
            return _idx == op._idx;
         }

         reference_type
         dereference() const
         {
            return typename rdb<real_type>::table_type( _be._tbls[_idx],
                                                        _be._minx[_idx], _be._miny[_idx], _be._minz[_idx],
                                                        _be._maxx[_idx], _be._maxy[_idx], _be._maxz[_idx] );
         }

      protected:

         const soci_base<real_type>& _be;
         unsigned _idx;
      };

   }
}

#endif
