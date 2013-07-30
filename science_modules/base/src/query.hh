#ifndef tao_base_query_hh
#define tao_base_query_hh

#include "filter.hh"

namespace tao {

   template< class T >
   class query
   {
   public:

      typedef T real_type;

   public:

      void
      clear()
      {
         _of_set.clear();
         _out_fields.clear();
      }

      void
      add_base_output_fields()
      {
         add_output_field( "pos_x" );
         add_output_field( "pos_y" );
         add_output_field( "pos_z" );
         add_output_field( "snapshot" );
         add_output_field( "global_tree_id" );
         add_output_field( "local_galaxy_id" );
         add_output_field( "redshift" );
      }

      void
      add_output_field( const string& field )
      {
         string low = field;
         to_lower( low );
         _out_fields.clear();
         _of_set.insert( low );
      }

      const vector<string>::view
      output_fields()
      {
         if( _out_fields.empty() )
         {
            _out_fields.resize( _of_set.size() );
            std::copy( _of_set.begin(), _of_set.end(), _out_fields.begin() );
         }
         return _out_fields;
      }

      void
      add_calc_field( const string& field )
      {
         _calc_fields.insert( field );
      }

      const set<string>&
      calc_fields() const
      {
         return _calc_fields;
      }

      void
      set_filter( const tao::filter& filt )
      {
         _filt = filt;
      }

      const tao::filter&
      filter() const
      {
         return _filt;
      }

   protected:

      set<string> _of_set;
      vector<string> _out_fields;
      set<string> _calc_fields;
      tao::filter _filt;
   };

}

#endif
