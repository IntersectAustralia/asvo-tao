#ifndef tao_base_rdb_backend_hh
#define tao_base_rdb_backend_hh

namespace tao {
   namespace backends {

      template< class T >
      class rdb_backend
      {
      public:

         typedef T real_type;

      public:

         string
         make_box_query_string( const box<real_type>& box ) const
         {
            boost::format fmt( "SELECT %1% FROM -table- "
                               "WHERE %2% = %3% AND "         // snapshot
                               "%4% > %5% AND %4% < %6% AND " // x position
                               "%7% > %8% AND %7% < %9% AND " // y position
                               "%10% > %11% AND %10% < %12%" ); // z position
            fmt % make_output_field_query_string();
            fmt % _field_map["snapshot"] % box.snapshot();
            fmt % _field_map["pos_x"] % box.min_pos()[0] % box.max_pos()[0];
            fmt % _field_map["pos_y"] % box.min_pos()[1] % box.max_pos()[1];
            fmt % _field_map["pos_z"] % box.min_pos()[2] % box.max_pos()[2];
            return fmt.str();
         }

         string
         make_output_field_query_string() const
         {
            string query;
            for( const auto& of : _out_fields )
            {
               ASSERT( _field_map.find( of ) != _field_map.end(),
                       "Failed to find output field name in mapping." );
               if( !query.empty() )
                  query += " ";
               query += of + " AS " + _field_map[of];
            }
            return query;
         }

      protected:

         std::unordered_map<string,string> _field_map;
         set<string> _out_fields;
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

      protected:

         void
         increment()
         {
            _be.fetch( _src, _gal );
         }

         bool
         equal( const galaxy_iterator& op ) const
         {
            return ;
         }

         reference_type
         dereference() const
         {
            return _gal;
         }

      protected:

         soci::session _sql;
         galaxy<real_type> _gal;
      };

}
   }

#endif
