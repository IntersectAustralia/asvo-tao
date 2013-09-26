#ifndef tao_base_rdb_backend_hh
#define tao_base_rdb_backend_hh

#include <unordered_map>
#include <libhpc/containers/set.hh>
#include <libhpc/containers/string.hh>
#include "backend.hh"
#include "query.hh"
#include "tile.hh"
#include "batch.hh"
#include "filter.hh"

namespace tao {
   namespace backends {

      template< class T >
      class rdb_table;

      template< class T >
      class rdb
         : public backend<T>
      {
      public:

         typedef T real_type;
         typedef backend<real_type> super_type;
         typedef rdb_table<real_type> table_type;

      public:

         rdb( const simulation<real_type>* sim )
            : super_type( sim ),
              _con( false )
         {
         }

         ///
         /// Set the simulation. Overloaded to allow for loading table
         /// information from the database when we have both a connection
         /// and simulation available.
         ///
         virtual
         void
         set_simulation( const simulation<real_type>* sim )
         {
            super_type::set_simulation( sim );
            if( sim && _con )
               _initialise();
         }

         void
         init_batch( batch<real_type>& bat,
                     tao::query<real_type>& query ) const
         {
            for( const auto& field : query.output_fields() )
            {
               // Check that the field actually exists. Due to calculated fields
               // it may not actually be on the database.
               if( this->_field_map.find( field ) != this->_field_map.end() )
                  bat.set_scalar( field, _field_types.at( this->_field_map.at( field ) ) );
            }

            // Add fields that will need to be calculated.
            bat.template set_scalar<real_type>( "redshift_cosmological" );
            bat.template set_scalar<real_type>( "redshift_observed" );
            bat.template set_scalar<real_type>( "ra" );
            bat.template set_scalar<real_type>( "dec" );
            bat.template set_scalar<real_type>( "distance" );
         }

         string
         make_box_query_string( const box<real_type>& box,
                                tao::query<real_type>& qry ) const
         {
            // boost::format fmt( "SELECT %1% FROM -table- "
            //                    "WHERE %2% = %3% AND "         // snapshot
            //                    "%4% > %5% AND %4% < %6% AND " // x position
            //                    "%7% > %8% AND %7% < %9% AND " // y position
            //                    "%10% > %11% AND %10% < %12%" ); // z position
            // std::unordered_map<string,string> map;
            // make_field_map( map, qry, tile );
            // fmt % make_output_field_query_string( qry, map );
            // fmt % _field_map["snapshot"] % box.snapshot();
            // fmt % _field_map.at( "pos_x" ) % box.min_pos()[0] % box.max_pos()[0];
            // fmt % _field_map.at( "pos_y" ) % box.min_pos()[1] % box.max_pos()[1];
            // fmt % _field_map.at( "pos_z" ) % box.min_pos()[2] % box.max_pos()[2];
            // return fmt.str();
            return "";
         }

         string
         make_tile_query_string( const tile<real_type>& tile,
                                 tao::query<real_type>& query,
                                 filter const* filt = 0 ) const
         {
            boost::format fmt(
               "SELECT %1% FROM -table- "
               "INNER JOIN redshift_ranges ON (-table-.%2% = redshift_ranges.snapshot) "
               "WHERE "
               "(POW(%3%,2) + POW(%4%,2) + POW(%5%,2)) >= redshift_ranges.min AND "
               "(POW(%3%,2) + POW(%4%,2) + POW(%5%,2)) < redshift_ranges.max AND "
               "(%3%)/(SQRT(POW(%3%,2) + POW(%4%,2))) >= %6% AND "
               "(%3%)/(SQRT(POW(%3%,2) + POW(%4%,2))) < %7% AND "
               "SQRT(POW(%3%,2) + POW(%4%,2))/(SQRT(POW(%3%,2) + POW(%4%,2) + POW(%5%,2))) >= %8% AND "
               "SQRT(POW(%3%,2) + POW(%4%,2))/(SQRT(POW(%3%,2) + POW(%4%,2) + POW(%5%,2))) < %9% AND "
               "(POW(%3%,2) + POW(%4%,2) + POW(%5%,2)) >= %10% AND "
               "(POW(%3%,2) + POW(%4%,2) + POW(%5%,2)) < %11%"
               "%12%" // filter
               );
            std::unordered_map<string,string> map;
            make_field_map( map, query, tile );
            map["redshift"] = "redshift_ranges.redshift";
            fmt % make_output_field_query_string( query, map );
            fmt % _field_map.at( "snapshot" );
            fmt % map["pos_x"] % map["pos_y"] % map["pos_z"];
            fmt % cos( tile.lightcone()->max_ra() ) % cos( tile.lightcone()->min_ra() );
            fmt % cos( tile.lightcone()->max_dec() ) % cos( tile.lightcone()->min_dec() );
            fmt % pow( tile.lightcone()->min_dist(), 2 ) % pow( tile.lightcone()->max_dist(), 2 );
            string filt_str = make_filter_query_string( filt );
            if( !filt_str.empty() )
               filt_str = " AND " + filt_str; 
            fmt % filt_str;
            return fmt.str();
         }

         string
         make_drop_snap_rng_query_string() const
         {
            return "DROP TABLE redshift_ranges";
         }

         list<string>
         make_snap_rng_query_string( const simulation<real_type>& sim ) const
         {
            ASSERT( sim.num_snapshots() >= 2, "Must be at least two snapshots." );

            // Store in a list each command.
            list<string> queries;

            // Create a temporary table to hold values.
            queries.emplace_back( "CREATE TEMPORARY TABLE redshift_ranges "
                                  "(snapshot INTEGER, redshift DOUBLE PRECISION, min DOUBLE PRECISION, max DOUBLE PRECISION);" );

            // Insert all ranges.
            for( unsigned ii = 0; ii < sim.num_snapshots() - 1; ++ii )
            {
               boost::format fmt( "\nINSERT INTO redshift_ranges VALUES(%1%, %2%, %3%, %4%);" );
               real_type max = numerics::redshift_to_comoving_distance( sim.redshift( ii ), 1000, sim.hubble(), sim.omega_l(), sim.omega_m() )*sim.h();
               real_type min = numerics::redshift_to_comoving_distance( sim.redshift( ii + 1 ), 1000, sim.hubble(), sim.omega_l(), sim.omega_m() )*sim.h();
               LOGDLN( "Inserting range for snapshot ", ii + 1, ": [", min*min, ", ", max*max, ")" );
               fmt % (ii + 1) % sim.redshift( ii + 1 ) % (min*min) % (max*max);
               queries.emplace_back( fmt.str() );
            }

            return queries;
         }

         string
         make_output_field_query_string( tao::query<real_type>& query,
                                         const std::unordered_map<string,string>& map ) const
         {
            string qs;
            for( string of : query.output_fields() )
            {
               // // Skip anything which is thought to be calculated later.
               // if( query.calc_fields().find( of ) == query.calc_fields().end() )
               // {

               if( !qs.empty() )
                  qs += ", ";
               qs += map.at( of ) + " AS " + of;

               // }
            }
            return qs;
         }

         string
         make_box_size_query_string() const
         {
            return "SELECT metavalue FROM metadata WHERE metakey='boxsize'";
         }

         string
         make_filter_query_string( filter const* filt ) const
         {
            string qry;
            if( filt &&
                !filt->field_name().empty() &&
                _field_map.find( filt->field_name() ) != _field_map.end() && // must have this field in DB
                (filt->minimum<real_type>() || filt->maximum<real_type>()) )
            {
               string fn = _field_map.at( filt->field_name() );
               if( filt->minimum<real_type>() )
                  qry += boost::str( boost::format( "%1% >= %2%" ) % fn % *filt->minimum<real_type>() );
               if( filt->maximum<real_type>() )
               {
                  if( filt->minimum<real_type>() )
                     qry += " AND ";
                  qry += boost::str( boost::format( "%1% < %2%" ) % fn % *filt->maximum<real_type>() );
               }
            }
            return qry;
         }

         void
         make_field_map( std::unordered_map<string,string>& map,
                         tao::query<real_type>& query,
                         optional<const tao::tile<real_type>&> tile = optional<const tao::tile<real_type>&>() ) const
         {
            map.clear();
            for( string of : query.output_fields() )
            {
               // Only proceed if the field exists on the database.
               if( _field_map.find( of ) != _field_map.end() )
               {
                  // Positions need to be handled specially to take care of translation.
                  if( tile && (of == "pos_x" || of == "pos_y" || of == "pos_z") )
                  {
                     string mapped[3] = { "pos_x", "pos_y", "pos_z" };
                     real_type box_size = (*tile).lightcone()->simulation()->box_size();
                     string repl = "CASE WHEN %1% + %2% < %3% THEN %1% + %2% ELSE %1% + %2% - %3% END + %4%";
                     string field;
                     if( of == "pos_x" )
                     {
                        of = mapped[(*tile).rotation()[0]];
                        if( (*tile).random() )
                        {
                           field = boost::str( boost::format( repl ) % _field_map.at( of ) % (*tile).translation()[0] %
                                               box_size % (*tile).min()[0] );
                        }
                        else
                           field = _field_map.at( of );
                     }
                     else if( of == "pos_y" )
                     {
                        of = mapped[(*tile).rotation()[1]];
                        if( (*tile).random() )
                        {
                           field = boost::str( boost::format( repl ) % _field_map.at( of ) % (*tile).translation()[1] %
                                               box_size % (*tile).min()[1] );
                        }
                        else
                           field = _field_map.at( of );
                     }
                     else
                     {
                        if( (*tile).random() )
                        {
                           of = mapped[(*tile).rotation()[2]];
                           field = boost::str( boost::format( repl ) % _field_map.at( of ) % (*tile).translation()[2] %
                                               box_size % (*tile).min()[2] );
                        }
                        else
                           field = _field_map.at( of );
                     }

                     // Add to map.
                     map[of] = field;
                  }
                  else
                  {
                     // Velocity.
                     if( tile && (of == "velx" || of == "vely" || of == "velz") )
                     {
                        string mapped[3] = { "velx", "vely", "velz" };
                        if( of == "velx" )
                           of = mapped[(*tile).rotation()[0]];
                        else if( of == "vely" )
                           of = mapped[(*tile).rotation()[1]];
                        else
                           of = mapped[(*tile).rotation()[2]];
                     }

                     // Spin.
                     else if( tile && (of == "spinx" || of == "spiny" || of == "spinz") )
                     {
                        string mapped[3] = { "spinx", "spiny", "spinz" };
                        if( of == "spinx" )
                           of = mapped[(*tile).rotation()[0]];
                        else if( of == "spiny" )
                           of = mapped[(*tile).rotation()[1]];
                        else
                           of = mapped[(*tile).rotation()[2]];
                     }

                     // Add to the map.
                     map[of] = _field_map.at( of );
                  }
               }
               else
               {
                  // Warn the user if the database field does not exist in the
                  // mapping.
                  LOGWLN( "WARNING: Database does not have a mapped field for the name: ", of );

                  // // Add the field to the set of fields we know are being calculated.
                  // query.add_calc_field( of );
               }
            }
         }

      protected:

         virtual
         void
         _initialise() = 0;

      protected:

         std::unordered_map<string,string> _field_map;
         map<string,typename batch<real_type>::field_value_type> _field_types;
         bool _con;
      };

      template< class T >
      class rdb_table
      {
      public:

         typedef T real_type;

      public:

         rdb_table()
         {
         }

         rdb_table( const std::string& name,
                    real_type minx,
                    real_type miny,
                    real_type minz,
                    real_type maxx,
                    real_type maxy,
                    real_type maxz )
            : _name( name )
         {
            _min[0] = minx; _min[1] = miny; _min[2] = minz;
            _max[0] = maxx; _max[1] = maxy; _max[2] = maxz;
         }

         // rdb_table( const rdb_table& src )
         //    : name( src._name ),
         //      minx( src._minx ),
         //      miny( src._miny ),
         //      minz( src._minz ),
         //      maxx( src._maxx ),
         //      maxy( src._maxy ),
         //      maxz( src._maxz )
         // {
         // }

         const std::string&
         name() const
         {
            return _name;
         }

         const array<real_type,3>&
         min() const
         {
            return _min;
         }

         const array<real_type,3>&
         max() const
         {
            return _max;
         }

         // Define this to allow for storing tables in a set
         // to eliminate duplicates.
         bool
         operator<( const rdb_table& op ) const
         {
            return _name < op._name;
         }

         bool
         operator==( const rdb_table& op ) const
         {
            return _name == op._name && _min == op._min && _max == op._max;
         }

         friend
         std::ostream&
         operator<<( std::ostream& strm,
                     const rdb_table& obj )
         {
            strm << "rdb_table(" << obj._name << ", " << obj._min << ", " << obj._max << ")";
            return strm;
         }

      protected:

         string _name;
         array<real_type,3> _min, _max;
      };

   }
}

#endif
