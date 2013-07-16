#ifndef tao_base_rdb_backend_hh
#define tao_base_rdb_backend_hh

#include <unordered_map>
#include <libhpc/containers/set.hh>
#include <libhpc/containers/string.hh>

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

         // string
         // make_output_field_query_string() const
         // {
         //    string query;
         //    for( const auto& of : _out_fields )
         //    {
         //       ASSERT( _field_map.find( of ) != _field_map.end(),
         //               "Failed to find output field name in mapping." );
         //       if( !query.empty() )
         //          query += " ";
         //       query += of + " AS " + _field_map[of];
         //    }
         //    return query;
         // }

      protected:

         std::unordered_map<string,string> _field_map;
         set<string> _out_fields;
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
