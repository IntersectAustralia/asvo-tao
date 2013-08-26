#ifndef tao_base_filter_hh
#define tao_base_filter_hh

#include "types.hh"
#include "batch.hh"

namespace tao {
   using namespace hpc;

   class filter
   {
   public:

      filter();

      template< class T >
      bool
      operator()( const T& val )
      {
         if( _min && boost::any_cast<T>( *_min ) > val )
            return false;
         if( _max && boost::any_cast<T>( *_max ) < val )
            return false;
         return true;
      }

      void
      bind( const tao::batch<real_type>& batch );

      void
      set_field_name( const string& name )
      {
         _field_name = name;
      }

      template< class T >
      void
      set_minimum( const T& val )
      {
         _min = val;
      }

      template< class T >
      void
      set_maximum( const T& val )
      {
         _max = val;
      }

   protected:

      string _field_name;
      batch<real_type>::field_value_type _field_type;
      optional<boost::any> _min;
      optional<boost::any> _max;
      string _min_str;
      string _max_str;
   };

}

#endif
