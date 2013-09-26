#ifndef tao_base_soci_base_backend_hh
#define tao_base_soci_base_backend_hh

#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <soci/soci.h>
#include "rdb_backend.hh"
#include "tile_table_iterator.hh"
#include "box_table_iterator.hh"
#include "lightcone_galaxy_iterator.hh"
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
         typedef backends::box_table_iterator<soci_base> box_table_iterator;
         typedef soci_galaxy_iterator<real_type,tile_table_iterator> tile_galaxy_iterator;
         typedef soci_galaxy_iterator<real_type,box_table_iterator> box_galaxy_iterator;
         typedef tao::lightcone_galaxy_iterator<soci_base<real_type>> lightcone_galaxy_iterator;

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

         real_type
         box_size()
         {
            real_type size;
            session() << this->make_box_size_query_string(),
               soci::into( size );
            return size;
         }

         void
         snapshot_redshifts( vector<real_type>& snap_zs )
         {
            unsigned size;
            session() << "SELECT COUNT(*) FROM snap_redshift",
               soci::into( size );
            snap_zs.resize( size );
            session() << "SELECT redshift FROM snap_redshift ORDER BY " + this->_field_map.at( "snapshot" ),
               soci::into( (std::vector<real_type>&)snap_zs );
         }

         tile_galaxy_iterator
         galaxy_begin( query_type& query,
                       tile<real_type> const& tile,
                       tao::batch<real_type>* bat = 0,
                       filter const* filt = 0 )
         {
            string qs = this->make_tile_query_string( tile, query, filt );
            return tile_galaxy_iterator( *this, query, qs, table_begin( tile ), table_end( tile ), tile.lightcone(), bat );
         }

         tile_galaxy_iterator
         galaxy_end( query_type& query,
                     const tile<real_type>& tile )
         {
            return tile_galaxy_iterator();
         }

         box_galaxy_iterator
         galaxy_begin( query_type& query,
                       const box<real_type>& box,
                       tao::batch<real_type>* bat = 0,
                       filter const* filt = 0 )
         {
            string qs = this->make_box_query_string( box, query, filt );
            return box_galaxy_iterator( *this, query, qs, table_begin( box ), table_end( box ), 0, bat );
         }

         box_galaxy_iterator
         galaxy_end( query_type& query,
                     const box<real_type>& box )
         {
            return box_galaxy_iterator();
         }

         lightcone_galaxy_iterator
         galaxy_begin( query_type& query,
                       const lightcone<real_type>& lc,
                       tao::batch<real_type>* bat = 0,
                       filter const* filt = 0 )
         {
            return lightcone_galaxy_iterator( lc, *this, query, bat, filt );
         }

         lightcone_galaxy_iterator
         galaxy_end( query_type& query,
                     const lightcone<real_type>& lc )
         {
            return lightcone_galaxy_iterator();
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
            return tile_table_iterator();
         }

         box_table_iterator
         table_begin( const box<real_type>& box ) const
         {
            return box_table_iterator( &box, this );
         }

         box_table_iterator
         table_end( const box<real_type>& box ) const
         {
            return box_table_iterator();
         }

      protected:

         virtual
         void
         _initialise()
         {
            ASSERT( this->_con, "Not connected to database." );

            // Load tables if not already done.
            if( _tbls.empty() )
               _load_table_info();

            // Gotta get the types for all the fields.
            if( this->_field_map.empty() )
               _load_field_types();

            // Create temporary snapshot range table if simulation
            // is set.
            if( this->_sim )
            {
               LOGILN( "Making redshift range table.", setindent( 2 ) );

               // Try and drop the redshift range table.
               try
               {
                  session() << this->make_drop_snap_rng_query_string();
               }
               catch( const ::soci::soci_error& ex )
               {
               }

               auto queries = this->make_snap_rng_query_string( *this->_sim );
               for( const auto& query : queries )
                  session() << query;
               LOGILN( "Done.", setindent( -2 ) );
            }
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

            // Perform the correct query.
            auto& sql = session( _tbls[0] );
            string be_name = sql.get_backend_name();
            soci::rowset<soci::row>* rs;
            if( be_name == "sqlite3" )
               rs = new soci::rowset<soci::row>( sql.prepare << "PRAGMA TABLE_INFO(" + _tbls[0] + ")" );
            else
            {
               rs = new soci::rowset<soci::row>( sql.prepare << "SELECT column_name, data_type FROM information_schema.columns"
                  " WHERE table_name = '" + _tbls[0] + "'" );
            }

            // Buld field types.
            this->_field_types.clear();
            for( soci::rowset<soci::row>::const_iterator it = rs->begin(); it != rs->end(); ++it )
            {
               typename batch<real_type>::field_value_type type;
               string type_str = ((be_name == "sqlite3") ? it->get<std::string>( 2 ) : it->get<std::string>( 1 ));
               to_lower( type_str );
               string field_str = ((be_name == "sqlite3") ? it->get<std::string>( 1 ) : it->get<std::string>( 0 ));
               LOGILN( field_str, ": ", type_str );
               if( type_str == "string" || type_str == "varchar" )
                  type = batch<real_type>::STRING;
               else if( type_str == "integer" )
                  type = batch<real_type>::INTEGER;
               else if( type_str == "bigint" )
                  type = batch<real_type>::LONG_LONG;
               else if( type_str == "real" || type_str == "double precision" )
                  type = batch<real_type>::DOUBLE;
               else
                  EXCEPT( 0, "Unknown field type for field '", field_str, "': ", type_str );

               // Insert into field types.
               this->_field_types.insert( field_str, type );

               // Prepare default mapping.
               this->_field_map[field_str] = field_str;
            }

            // Destroy the rowset.
            delete rs;

            // Before finishing, insert the known mapping conversions.
            // TODO: Generalise.
            this->_field_map["pos_x"] = "posx";
            this->_field_map["pos_y"] = "posy";
            this->_field_map["pos_z"] = "posz";
            this->_field_map["vel_x"] = "velx";
            this->_field_map["vel_y"] = "vely";
            this->_field_map["vel_z"] = "velz";
            this->_field_map["snapshot"] = "snapnum";
            this->_field_map["global_index"] = "globalindex";
            this->_field_map["global_tree_id"] = "globaltreeid";
            this->_field_map["local_galaxy_id"] = "localgalaxyid";

            // Make sure we have all the essential fields available. Do this by
            // checking that all the mapped fields exist in the field types.
            for( const auto& item : this->_field_map )
               EXCEPT( this->_field_types.has( item.second ), "Database is missing essential field: ", item.second );

            LOGILN( "Done.", setindent( -2 ) );
         }

      protected:

         std::vector<double> _minx, _miny, _minz;
         std::vector<double> _maxx, _maxy, _maxz;
         std::vector<std::string> _tbls;
      };

      ///
      ///
      ///
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

         soci_galaxy_iterator()
            : _be( NULL ),
              _query( NULL ),
              _my_bat( false ),
              _done( true )
         {
         }

         soci_galaxy_iterator( soci_base<real_type>& be,
                               query_type& query,
                               const string& query_str,
                               const table_iterator& table_start,
                               const table_iterator& table_finish,
                               const lightcone<real_type>* lc = 0,
                               tao::batch<real_type>* bat = 0 )
            : _be( &be ),
              _query( &query ),
              _query_str( query_str ),
              _table_pos( table_start ),
              _table_end( table_finish ),
              _lc( lc ),
              _st( NULL ),
              _done( false ),
              _my_bat( false ),
              _bat( bat )
         {
            if( _table_pos != _table_end )
            {
               // Prepare the batch object.
               if( !_bat )
               {
                  _my_bat = true;
                  _bat = new tao::batch<real_type>();
               }
               be.init_batch( *_bat, *_query );

               // Need to get to first position.
               _prepare( _table_pos->name() );
               increment();
            }
            else
               _done = true;
         }

         soci_galaxy_iterator( const soci_galaxy_iterator& src )
            : _be( src._be ),
              _query( src._query ),
              _query_str( src._query_str ),
              _table_pos( src._table_pos ),
              _table_end( src._table_end ),
              _lc( src._lc ),
              _st( src._st ),
              _done( src._done )
         {
            if( src._my_bat )
            {
               _my_bat = true;
               _bat = new tao::batch<real_type>( *src._bat );
            }
            else
            {
               _my_bat = false;
               _bat = src._bat;
            }
         }

         soci_galaxy_iterator( soci_galaxy_iterator&& src )
            : _be( src._be ),
              _query( src._query ),
              _query_str( src._query_str ),
              _table_pos( src._table_pos ),
              _table_end( src._table_end ),
              _lc( src._lc ),
              _st( src._st ),
              _done( src._done ),
              _my_bat( src._my_bat ),
              _bat( src._bat )
         {
            src._my_bat = false;
            src._bat = 0;
         }

         ~soci_galaxy_iterator()
         {
            // Delete the batch object if we own it.
            if( _my_bat && _bat )
            {
               delete _bat;
               _bat = 0;
            }
         }

         reference_type
         operator*()
         {
            return *_bat;
         }

         bool
         done() const
         {
            return _done;
         }

         soci_galaxy_iterator&
         operator=( const soci_galaxy_iterator& op )
         {
            _be = op._be;
            _query = op._query;
            _query_str = op._query_str;
            _table_pos = op._table_pos;
            _table_end = op._table_end;
            _lc = op._lc;
            _st = op._st;
            _done = op._done;

            if( op._my_bat )
            {
               _my_bat = true;
               _bat = new tao::batch<real_type>( *op._bat );
            }
            else
            {
               _my_bat = false;
               _bat = op._bat;
            }
         }

         soci_galaxy_iterator&
         operator=( soci_galaxy_iterator&& op )
         {
            _be = op._be;
            _query = op._query;
            _query_str = op._query_str;
            _table_pos = op._table_pos;
            _table_end = op._table_end;
            _lc = op._lc;
            _st = op._st;
            _done = op._done;
            _my_bat = op._my_bat;
            _bat = op._bat;

            op._my_bat = false;
            op._bat = 0;
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
            return *_bat;
         }

         void
         _prepare( const string& table )
         {
            LOGILN( "Querying table: ", table );
            LOGDLN( "Preparing query for table: ", table, setindent( 2 ) );

            // Delete any existing statement.
            if( _st )
               delete _st;

            string qs = boost::algorithm::replace_all_copy( _query_str, "-table-", table );
            LOGDLN( "Query string: ", qs );
            auto prep = _be->session( table ).prepare << qs;
            for( unsigned ii = 0; ii < _query->output_fields().size(); ++ii )
            {
               const auto& field = _bat->field( _query->output_fields()[ii] );
               const auto& type = std::get<2>( field );
               switch( type )
               {
                  case batch<real_type>::STRING:
                     boost::any_cast<vector<string>*>( std::get<0>( field ) )->resize( _bat->max_size() );
                     prep = prep, soci::into( *(std::vector<std::string>*)boost::any_cast<vector<string>*>( std::get<0>( field ) ) );
                     break;
                  case batch<real_type>::DOUBLE:
                     boost::any_cast<vector<double>*>( std::get<0>( field ) )->resize( _bat->max_size() );
                     prep = prep, soci::into( *(std::vector<double>*)boost::any_cast<vector<double>*>( std::get<0>( field ) ) );
                     break;
                  case batch<real_type>::INTEGER:
                     boost::any_cast<vector<int>*>( std::get<0>( field ) )->resize( _bat->max_size() );
                     prep = prep, soci::into( *(std::vector<int>*)boost::any_cast<vector<int>*>( std::get<0>( field ) ) );
                     break;
                  case batch<real_type>::LONG_LONG:
                     boost::any_cast<vector<long long>*>( std::get<0>( field ) )->resize( _bat->max_size() );
                     prep = prep, soci::into( *(std::vector<long long>*)boost::any_cast<vector<long long>*>( std::get<0>( field ) ) );
                     break;
                  case batch<real_type>::UNSIGNED_LONG_LONG:
                     boost::any_cast<vector<unsigned long long>*>( std::get<0>( field ) )->resize( _bat->max_size() );
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
            _bat->set_attribute( "table", table );

            LOGDLN( "Done.", setindent( -2 ) );
         }

         bool
         _fetch()
         {
            LOGDLN( "Fetching rows.", setindent( 2 ) );
            ASSERT( _st, "No statement available on galaxy iterator." );

            // Actually perform the fetch.
            bool rows_exist = _st->fetch();
            _bat->update_size();
            LOGDLN( "Fetched ", _bat->size(), " rows." );

            // If we found some rows perform any calculated field updates.
            if( rows_exist )
              _calc_fields();

            // Return whether we got any rows.
            LOGDLN( "Done.", setindent( -2 ) );
            return rows_exist;
         }

        void
        _calc_fields()
        {
           auto pos_x = _bat->template scalar<real_type>( "pos_x" );
           auto pos_y = _bat->template scalar<real_type>( "pos_y" );
           auto pos_z = _bat->template scalar<real_type>( "pos_z" );
           auto vel_x = _bat->template scalar<real_type>( "vel_x" );
           auto vel_y = _bat->template scalar<real_type>( "vel_y" );
           auto vel_z = _bat->template scalar<real_type>( "vel_z" );
           auto z_cos = _bat->template scalar<real_type>( "redshift_cosmological" );
           auto z_obs = _bat->template scalar<real_type>( "redshift_observed" );
           auto ra = _bat->template scalar<real_type>( "ra" );
           auto dec = _bat->template scalar<real_type>( "dec" );
           auto dist = _bat->template scalar<real_type>( "distance" );
           for( unsigned ii = 0; ii < _bat->size(); ++ii )
           {
              if( _lc )
              {
                 real_type h0 = _lc->simulation()->hubble();

                 // Compute distance.
                 dist[ii] = sqrt( pos_x[ii]*pos_x[ii] + pos_y[ii]*pos_y[ii] + pos_z[ii]*pos_z[ii] );

                 // Compute cosmological redshift.
                 z_cos[ii] = _lc->distance_to_redshift( dist[ii] );

                 // Compute RA and DEC.
                 numerics::cartesian_to_ecs( pos_x[ii], pos_y[ii], pos_z[ii], ra[ii], dec[ii] );
                 ra[ii] = to_degrees( ra[ii] );
                 dec[ii] = to_degrees( dec[ii] );

                 // Calculate observed redshift.
                 if( dist[ii] > 0.0 )
                 {
                    array<real_type,3> rad_vec{ { pos_x[ii]/dist[ii], pos_y[ii]/dist[ii], pos_z[ii]/dist[ii] } };
                    real_type dist_z = dist[ii] + ((rad_vec[0]*vel_x[ii] + rad_vec[1]*vel_y[ii] + rad_vec[2]*vel_z[ii])/h0)*(h0/100.0);
                    z_obs[ii] = _lc->distance_to_redshift( dist_z );
                 }
                 else
                    z_obs[ii] = 0.0;
              }
           }
        }

      protected:

         soci_base<real_type>* _be;
         const lightcone<real_type>* _lc;
         query_type* _query;
         string _query_str;
         table_iterator _table_pos, _table_end;
         soci::statement* _st;
         bool _my_bat;
         batch<real_type>* _bat;
         bool _done;
      };

      ///
      ///
      ///
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