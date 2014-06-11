#ifndef tao_base_rdb_backend_hh 
#define tao_base_rdb_backend_hh

#include <array>
#include <iomanip>
#include <string>
#include <unordered_map>
#include <map>
#include <boost/format.hpp>
#include <boost/optional.hpp>
#include <libhpc/numerics/coords.hh>
#include "backend.hh"
#include "query.hh"
#include "tile.hh"
#include "batch.hh"
#include "filter.hh"
#include "types.hh"

namespace tao {
   namespace backends {

      template< class T >
      class rdb_table;

      template< class T >
      class rdb
         : public backend
      {
      public:

         typedef T real_type;
         typedef backend super_type;
         typedef rdb_table<real_type> table_type;

      public:

         rdb( const tao::simulation* sim )
            : super_type( sim ),
              _con( false )
         {
         }

         void
         add_field( std::string const& name,
                    std::string const& mapped = std::string() )
         {
            _field_map[name] = mapped.empty() ? name : mapped;
         }

         ///
         /// Set the simulation. Overloaded to allow for loading table
         /// information from the database when we have both a connection
         /// and simulation available.
         ///
         virtual
         void
         set_simulation( const tao::simulation* sim )
         {
            super_type::set_simulation( sim );
            if( sim && _con )
               _initialise();
         }

         bool
         connected() const
         {
            return _con;
         }

         void
         init_batch( batch<real_type>& bat,
                     query<real_type>& qry ) const
         {
            // Add fields from the query object.
            for( auto const& field : qry.output_fields() )
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

         std::string
         make_box_query_string( box<real_type> const& box,
                                query<real_type>& qry,
                                filter const* filt = 0 ) const
         {
	    using boost::io::group;
	    using std::setprecision;

            boost::format fmt(
	       "SELECT %1% FROM -table- "
	       "WHERE %2% = %3% AND "         // snapshot
	       "%4% > %5% AND %4% < %6% AND " // x position
	       "%7% > %8% AND %7% < %9% AND " // y position
	       "%10% > %11% AND %10% < %12%" // z position
	       "%13%" // filter
	       );
            std::unordered_map<std::string,std::string> map;
            make_field_map( map, qry, box );
            fmt % make_output_field_query_string( qry, map );
            fmt % _field_map.at( "snapnum" ) % box.snapshot();
            fmt % map.at( "posx" ) % group( setprecision( 12 ), box.min()[0] ) % group( setprecision( 12 ), box.max()[0] );
            fmt % map.at( "posy" ) % group( setprecision( 12 ), box.min()[1] ) % group( setprecision( 12 ), box.max()[1] );
            fmt % map.at( "posz" ) % group( setprecision( 12 ), box.min()[2] ) % group( setprecision( 12 ), box.max()[2] );
            std::string filt_str = make_filter_query_string( filt );
            if( !filt_str.empty() )
               filt_str = " AND " + filt_str; 
            fmt % filt_str;
            return fmt.str();
         }

         std::string
         make_tile_query_string( const tile<real_type>& tile,
                                 tao::query<real_type>& query,
                                 filter const* filt = 0 ) const
         {
	    using boost::io::group;
	    using std::setprecision;

            tao::lightcone const& lc = *tile.lightcone();
            real_type eff_ra_min = lc.min_ra() + lc.viewing_angle();
            // if( eff_ra_min > M_PI )
            //    eff_ra_min = M_PI - eff_ra_min;
            real_type eff_ra_max = lc.max_ra() + lc.viewing_angle();
            // if( eff_ra_max > M_PI )
            //    eff_ra_max = M_PI - eff_ra_max;
            // if( eff_ra_max < eff_ra_min )
            // {
            //    std::swap( eff_ra_min, eff_ra_max );
            // }

            if( !lc.single_snapshot() )
            {
               boost::format fmt(
                  "SELECT %1% FROM -table- "
                  "INNER JOIN redshift_ranges ON (-table-.%2% = redshift_ranges.snapshot) "
                  "WHERE "
                  "(POW(%3%,2) + POW(%4%,2) + POW(%5%,2)) >= redshift_ranges.min AND "
                  "(POW(%3%,2) + POW(%4%,2) + POW(%5%,2)) < redshift_ranges.max AND "
                  "((ATAN2(%4%,%3%) >= 0 AND ATAN2(%4%,%3%) >= %6%) OR (ATAN2(%4%,%3%) < 0 AND (2*PI() + ATAN2(%4%,%3%)) >= %6%)) AND "
                  "((ATAN2(%4%,%3%) >= 0 AND ATAN2(%4%,%3%) <  %7%) OR (ATAN2(%4%,%3%) < 0 AND (2*PI() + ATAN2(%4%,%3%)) <  %7%)) AND "
                  "(0.5*PI() - ACOS(%5%/(SQRT(POW(%3%,2) + POW(%4%,2) + POW(%5%,2))))) >= %8% AND "
                  "(0.5*PI() - ACOS(%5%/(SQRT(POW(%3%,2) + POW(%4%,2) + POW(%5%,2))))) < %9% AND "
                  "(POW(%3%,2) + POW(%4%,2) + POW(%5%,2)) >= %10% AND "
                  "(POW(%3%,2) + POW(%4%,2) + POW(%5%,2)) < %11%"
                  "%12%" // filter
                  );
               std::unordered_map<std::string,std::string> map;
               make_field_map( map, query, tile );
               map["redshift"] = "redshift_ranges.redshift";
               fmt % make_output_field_query_string( query, map );
               fmt % _field_map.at( "snapnum" );
               fmt % map.at( "posx" ) % map.at( "posy" ) % map.at( "posz" );
               fmt % group( setprecision( 12 ), eff_ra_min ) % group( setprecision( 12 ), eff_ra_max );
               fmt % group( setprecision( 12 ), lc.min_dec() ) % group( setprecision( 12 ), lc.max_dec() );
               fmt % group( setprecision( 12 ), pow( lc.min_dist(), 2 ) ) % group( setprecision( 12 ), pow( lc.max_dist(), 2 ) );
               std::string filt_str = make_filter_query_string( filt );
               if( !filt_str.empty() )
                  filt_str = " AND " + filt_str; 
               fmt % filt_str;
               return fmt.str();
            }
            else
            {
               boost::format fmt(
                  "SELECT %1% FROM -table- "
                  "WHERE "
                  "-table-.%2% = %3% AND "
                  "((ATAN2(%5%,%4%) >= 0 AND ATAN2(%5%,%4%) >= %7%) OR (ATAN2(%5%,%4%) < 0 AND (2*PI() + ATAN2(%5%,%4%)) >= %7%)) AND "
                  "((ATAN2(%5%,%4%) >= 0 AND ATAN2(%5%,%4%) <  %8%) OR (ATAN2(%5%,%4%) < 0 AND (2*PI() + ATAN2(%5%,%4%)) <  %8%)) AND "
                  "(0.5*PI() - ACOS(%6%/(SQRT(POW(%4%,2) + POW(%5%,2) + POW(%6%,2))))) >= %9% AND "
                  "(0.5*PI() - ACOS(%6%/(SQRT(POW(%4%,2) + POW(%5%,2) + POW(%6%,2))))) < %10% AND "
                  "(POW(%4%,2) + POW(%5%,2) + POW(%6%,2)) >= %11% AND "
                  "(POW(%4%,2) + POW(%5%,2) + POW(%6%,2)) < %12%"
                  "%13%" // filter
                  );
               std::unordered_map<std::string,std::string> map;
               make_field_map( map, query, tile );
               // map["redshift"] = "redshift_ranges.redshift";
               fmt % make_output_field_query_string( query, map );
               fmt % _field_map.at( "snapnum" ) % lc.snapshot();
               fmt % map.at( "posx" ) % map.at( "posy" ) % map.at( "posz" );
               fmt % group( setprecision( 12 ), eff_ra_min ) % group( setprecision( 12 ), eff_ra_max );
               fmt % group( setprecision( 12 ), lc.min_dec() ) % group( setprecision( 12 ), lc.max_dec() );
               fmt % group( setprecision( 12 ), pow( lc.min_dist(), 2 ) ) % group( setprecision( 12 ), pow( lc.max_dist(), 2 ) );
               std::string filt_str = make_filter_query_string( filt );
               if( !filt_str.empty() )
                  filt_str = " AND " + filt_str; 
               fmt % filt_str;
               return fmt.str();
            }
         }

         std::string
         make_drop_snap_rng_query_string() const
         {
            return "DROP TABLE IF EXISTS redshift_ranges";
         }

         std::list<std::string>
         make_snap_rng_query_string( const tao::simulation& sim ) const
         {
	    using boost::io::group;
	    using std::setprecision;

            ASSERT( sim.num_snapshots() >= 2, "Must be at least two snapshots." );

            // Store in a list each command.
            std::list<std::string> queries;

            // Create a temporary table to hold values.
            queries.emplace_back( "CREATE TEMPORARY TABLE IF NOT EXISTS redshift_ranges "
                                  "(snapshot INTEGER, redshift DOUBLE PRECISION, min DOUBLE PRECISION, max DOUBLE PRECISION);" );

            // Insert all ranges.
            for( unsigned ii = 0; ii < sim.num_snapshots() - 1; ++ii )
            {
               boost::format fmt( "\nINSERT INTO redshift_ranges VALUES(%1%, %2%, %3%, %4%);" );
               real_type max = hpc::num::redshift_to_comoving_distance( sim.redshift( ii ), 1000, sim.hubble(), sim.omega_l(), sim.omega_m() )*sim.h();
               real_type min = hpc::num::redshift_to_comoving_distance( sim.redshift( ii + 1 ), 1000, sim.hubble(), sim.omega_l(), sim.omega_m() )*sim.h();
               LOGDLN( "Inserting range for snapshot ", ii + 1, ": [", min*min, ", ", max*max, ")" );
               fmt % (ii + 1) % group( setprecision( 12 ), sim.redshift( ii + 1 ) ) % group( setprecision( 12 ), (min*min) ) % group( setprecision( 12 ), (max*max) );
               queries.emplace_back( fmt.str() );
            }

            return queries;
         }

         std::string
         make_output_field_query_string( tao::query<real_type>& query,
                                         const std::unordered_map<std::string,std::string>& map ) const
         {
            std::string qs;
            for( std::string of : query.output_fields() )
            {
               // // Skip anything which is thought to be calculated later.
               // if( query.calc_fields().find( of ) == query.calc_fields().end() )
               // {

               if( !qs.empty() )
                  qs += ", ";
	       try
	       {
		  qs += map.at( of ) + " AS " + of;
	       }
	       catch( ... )
	       {
		  EXCEPT( 0, "Database does not contain a field named: ", of );
	       }

               // }
            }
            return qs;
         }

         std::string
         make_box_size_query_string() const
         {
            return "SELECT metavalue FROM metadata WHERE metakey='boxsize'";
         }

         std::string
         make_filter_query_string( filter const* filt ) const
         {
	    using boost::io::group;
	    using std::setprecision;

            std::string qry;
            if( filt &&
                !filt->field_name().empty() &&
                _field_map.find( filt->field_name() ) != _field_map.end() && // must have this field in DB
                (filt->minimum<real_type>() || filt->maximum<real_type>()) )
            {
               std::string fn = _field_map.at( filt->field_name() );
               if( filt->minimum<real_type>() )
		 qry += boost::str( boost::format( "%1% >= %2%" ) % fn % group( setprecision( 12 ), *filt->minimum<real_type>() ) );
               if( filt->maximum<real_type>() )
               {
                  if( filt->minimum<real_type>() )
                     qry += " AND ";
                  qry += boost::str( boost::format( "%1% < %2%" ) % fn % group( setprecision( 12 ), *filt->maximum<real_type>() ) );
               }
            }
            return qry;
         }

         void
         make_field_map( std::unordered_map<std::string,std::string>& map,
                         tao::query<real_type>& query,
                         boost::optional<const tao::box<real_type>&> box = boost::optional<const tao::box<real_type>&>() ) const
         {
	    using boost::io::group;
	    using std::setprecision;

            map.clear();
            for( std::string of : query.output_fields() )
            {
               // Only proceed if the field exists on the database.
               if( _field_map.find( of ) != _field_map.end() )
               {
                  // Positions need to be handled specially to take care of translation.
                  if( box && (of == "posx" || of == "posy" || of == "posz" ||
			      of == "pos_x" || of == "pos_y" || of == "pos_z") )
                  {
                     std::string mapped[3] = { "posx", "posy", "posz" };
                     real_type box_size = (*box).simulation()->box_size();
                     std::string repl = "(CASE WHEN %1% + %2% < %3% THEN %1% + %2% ELSE %1% + %2% - %3% END + %4% - %5%)";
                     std::string field;
                     if( of == "posx" )
                     {
                        if( (*box).random() )
                        {
                           field = boost::str( boost::format( repl ) %
					       _field_map.at( mapped[(*box).rotation()[0]] ) %
					       group( setprecision( 12 ), (*box).translation()[(*box).rotation()[0]] ) %
                                               group( setprecision( 12 ), box_size ) % group( setprecision( 12 ), (*box).min()[0] ) %
                                               group( setprecision( 12 ), (*box).origin()[0] ) );
                        }
                        else
                        {
			   field = boost::str( boost::format( "(%1% + %2% - %3%)" ) %
                                               _field_map.at( of ) %
                                               group( setprecision( 12 ), (*box).min()[0] ) %
                                               group( setprecision( 12 ), (*box).origin()[0] ) );
                        }
                     }
                     else if( of == "posy" )
                     {
                        if( (*box).random() )
                        {
                           field = boost::str( boost::format( repl ) %
					       _field_map.at( mapped[(*box).rotation()[1]] ) %
					       group( setprecision( 12 ), (*box).translation()[(*box).rotation()[1]] ) %
                                               group( setprecision( 12 ), box_size ) % group( setprecision( 12 ), (*box).min()[1] ) %
                                               group( setprecision( 12 ), (*box).origin()[1] ) );
                        }
                        else
                        {
			   field = boost::str( boost::format( "(%1% + %2% - %3%)" ) %
                                               _field_map.at( of ) %
                                               group( setprecision( 12 ), (*box).min()[1] ) %
                                               group( setprecision( 12 ), (*box).origin()[1] ) );
                        }
                     }
                     else
                     {
                        if( (*box).random() )
                        {
                           field = boost::str( boost::format( repl ) %
                                               _field_map.at( mapped[(*box).rotation()[2]] ) %
                                               group( setprecision( 12 ), (*box).translation()[(*box).rotation()[2]] ) %
                                               group( setprecision( 12 ), box_size ) % group( setprecision( 12 ), (*box).min()[2] ) %
                                               group( setprecision( 12 ), (*box).origin()[2] ) );
                        }
                        else
                        {
                           field = boost::str( boost::format( "(%1% + %2% - %3%)" ) %
                                               _field_map.at( of ) %
                                               group( setprecision( 12 ), (*box).min()[2] ) %
                                               group( setprecision( 12 ), (*box).origin()[2] ) );
                        }
                     }

                     // Add to map.
                     map[of] = field;
                  }
                  else
                  {
                     std::string field;

                     // Velocity.
                     if( box && (of == "velx" || of == "vely" || of == "velz") )
                     {
                        std::string mapped[3] = { "velx", "vely", "velz" };
                        if( of == "velx" )
                           field = mapped[(*box).rotation()[0]];
                        else if( of == "vely" )
                           field = mapped[(*box).rotation()[1]];
                        else
                           field = mapped[(*box).rotation()[2]];
                     }

                     // Spin.
                     else if( box && (of == "spinx" || of == "spiny" || of == "spinz") )
                     {
                        std::string mapped[3] = { "spinx", "spiny", "spinz" };
                        if( of == "spinx" )
                           field = mapped[(*box).rotation()[0]];
                        else if( of == "spiny" )
                           field = mapped[(*box).rotation()[1]];
                        else
                           field = mapped[(*box).rotation()[2]];
                     }

                     // Anything else.
                     else
                        field = of;

                     // Add to the map.
                     map[of] = _field_map.at( field );
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

	 typename batch<real_type>::field_value_type
	 field_type( std::string const& name )
	 {
	    return _field_types.at( name );
	 }

      protected:

         virtual
         void
         _initialise() = 0;

      protected:

         std::unordered_map<std::string,std::string> _field_map;
         std::map<std::string,typename batch<real_type>::field_value_type> _field_types;
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
                    real_type maxz,
                    unsigned long long size )
            : _name( name ),
              _size( size )
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

         const std::array<real_type,3>&
         min() const
         {
            return _min;
         }

         const std::array<real_type,3>&
         max() const
         {
            return _max;
         }

         unsigned long long
         size() const
         {
            return _size;
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
            // strm << "rdb_table(" << obj._name << ", " << obj._min << ", " << obj._max << ")";
            strm << obj._name;
            return strm;
         }

      protected:

         std::string _name;
         std::array<real_type,3> _min, _max;
         unsigned long long _size;
      };

   }
}

#endif