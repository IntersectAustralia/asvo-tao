#ifndef tao_base_rdb_backend_hh
#define tao_base_rdb_backend_hh

#include <unordered_map>
#include <libhpc/containers/set.hh>
#include <libhpc/containers/string.hh>
#include "query.hh"

namespace tao {
   namespace backends {

      template< class T >
      class rdb_table;

      template< class T >
      class rdb
      {
      public:

         typedef T real_type;
         typedef rdb_table<real_type> table;

      public:

         // string
         // make_box_query_string( const box<real_type>& box ) const
         // {
         //    boost::format fmt( "SELECT %1% FROM -table- "
         //                       "WHERE %2% = %3% AND "         // snapshot
         //                       "%4% > %5% AND %4% < %6% AND " // x position
         //                       "%7% > %8% AND %7% < %9% AND " // y position
         //                       "%10% > %11% AND %10% < %12%" ); // z position
         //    fmt % make_output_field_query_string();
         //    fmt % _field_map["snapshot"] % box.snapshot();
         //    fmt % _field_map["pos_x"] % box.min_pos()[0] % box.max_pos()[0];
         //    fmt % _field_map["pos_y"] % box.min_pos()[1] % box.max_pos()[1];
         //    fmt % _field_map["pos_z"] % box.min_pos()[2] % box.max_pos()[2];
         //    return fmt.str();
         // }

         string
         make_tile_query_string( const tile<real_type>& tile,
                                 tao::query<real_type>& query )
         {
            boost::format fmt(
               "SELECT %1% FROM -table- "
               "INNER JOIN redshift_ranges ON (-table-.%2% = redshift_ranges.snapshot) "
               "(POW(-pos1-,2) + POW(-pos2-,2) + POW(-pos3-,2)) >= redshift_ranges.min AND "
               "(POW(-pos1-,2) + POW(-pos2-,2) + POW(-pos3-,2)) < redshift_ranges.max AND "
               "-pos1-/(SQRT(POW(-pos1-,2) + POW(-pos2-,2))) >= %3% AND "
               "-pos1-/(SQRT(POW(-pos1-,2) + POW(-pos2-,2))) < %4% AND "
               "SQRT(POW(-pos1-,2) + POW(-pos2-,2))/(SQRT(POW(-pos1-,2) + POW(-pos2-,2) + POW(-pos3-,2))) > %5% AND "
               "SQRT(POW(-pos1-,2) + POW(-pos2-,2))/(SQRT(POW(-pos1-,2) + POW(-pos2-,2) + POW(-pos3-,2))) < %6%"
               "%11%" // filter
               );
            if( tile.random() )
               fmt % make_output_field_query_string( query, tile );
            else
               fmt % make_output_field_query_string( query );
            fmt % _field_map.at( "snapshot" );
            fmt % tile.lightcone().max_ra() % tile.lightcone().min_ra();
            fmt % tile.lightcone().max_dec() % tile.lightcone().min_dec();
            fmt % ""; // TODO
            std::cout << fmt.str() << "\n";
            return fmt.str();
         }

         string
         make_snap_rng_query_string( const simulation<real_type>& sim ) const
         {
            ASSERT( sim.num_snapshots() >= 2, "Must be at least two snapshots." );

            // Create a temporary table to hold values.
            string query = "CREATE TEMPORARY TABLE redshift_ranges "
               "(snapshot INTEGER, redshift DOUBLE PRECISION, min DOUBLE PRECISION, max DOUBLE PRECISION);";

            // Insert all ranges.
            for( unsigned ii = 0; ii < sim.num_snapshots() - 1; ++ii )
            {
               boost::format fmt( "\nINSERT INTO redshift_ranges VALUES(%1%, %2%, %3%, %4%);" );
               real_type max = numerics::redshift_to_comoving_distance( sim.redshift( ii ), 1000, sim.hubble(), sim.omega_l(), sim.omega_m() );
               real_type min = numerics::redshift_to_comoving_distance( sim.redshift( ii + 1 ), 1000, sim.hubble(), sim.omega_l(), sim.omega_m() );
               fmt % (ii + 1) % sim.redshift( ii + 1 ) % (min*min) % (max*max);
               query += fmt.str();
            }

            return query;
         }

         string
         make_output_field_query_string( tao::query<real_type>& query,
                                         optional<const tile<real_type>&> tile = optional<const tile<real_type>&>() ) const
         {
            string qs;
            for( string of : query.output_fields() )
            {
               ASSERT( _field_map.find( of ) != _field_map.end(),
                       "Failed to find output field name in mapping." );
               if( !qs.empty() )
                  qs += " ";

               // Positions need to be handled specially to take care of translation.
               if( tile && (of == "pos_x" || of == "pos_y" || of == "pos_z") )
               {
                  string mapped[3] = { "pos_x", "pos_y", "pos_z" };
                  real_type box_size = tile.lightcone().simulation().box_size();
                  string repl = "CASE WHEN %1% + %2% < %3% THEN %1% + %2% ELSE %1% + %2% - %3% END + %4%";
                  string field;
                  if( of == "pos_x" )
                  {
                     of = mapped[(*tile).rotation()[0]];
                     field = boost::str( boost::format( repl ) % _field_map.at( of ) % (*tile).translation()[0] %
                                         box_size % (*tile).min()[0] );
                  }
                  else if( of == "pos_y" )
                  {
                     of = mapped[(*tile).rotation()[1]];
                     field = boost::str( boost::format( repl ) % _field_map.at( of ) % (*tile).translation()[1] %
                                         box_size % (*tile).min()[1] );
                  }
                  else
                  {
                     of = mapped[(*tile).rotation()[2]];
                     field = boost::str( boost::format( repl ) % _field_map.at( of ) % (*tile).translation()[2] %
                                         box_size % (*tile).min()[2] );
                  }

                  // Add to query.
                  qs += field + " AS " + of;
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

                  // Add to the query.
                  qs += _field_map.at( of ) + " AS " + of;
               }
            }
            return qs;
         }

      protected:

         std::unordered_map<string,string> _field_map;
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

      protected:

         std::string _name;
         array<real_type,3> _min, _max;
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

      //    galaxy_iterator()
      //    {
      //    }

      // protected:

      //    void
      //    increment()
      //    {
      //       _be.fetch( _src, _gal );
      //    }

      //    bool
      //    equal( const galaxy_iterator& op ) const
      //    {
      //       return ;
      //    }

      //    reference_type
      //    dereference() const
      //    {
      //       return _gal;
      //    }

      // protected:

      //    soci::session _sql;
      //    galaxy<real_type> _gal;
      // };

   }
}

#endif
