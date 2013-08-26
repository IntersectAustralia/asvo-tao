#include "filter.hh"

namespace tao {
   using namespace hpc;

   filter::filter()
      : _field_type( batch<real_type>::FIELD_VALUE_TERMINAL )
   {
   }

   void
   filter::bind( const tao::batch<real_type>& batch )
   {
      _field_type = std::get<2>( batch.field( _field_name ) );
      switch( _field_type )
      {
         case tao::batch<real_type>::DOUBLE:
            _min = boost::lexical_cast<double>( _min_str );
            _max = boost::lexical_cast<double>( _max_str );
            break;

         default:
            ASSERT( "Unknown filter type." );
      }
   }

}
