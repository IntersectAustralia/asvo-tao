#include "filter.hh"

namespace tao {
   using namespace hpc;

   filter::filter()
      // : _field_type( batch<real_type>::FIELD_VALUE_TERMINAL )
   {
   }

   // void
   // filter::bind( const tao::batch<real_type>& batch )
   // {
   //    _field_type = std::get<2>( batch.field( _field_name ) );
   //    switch( _field_type )
   //    {
   //       case tao::batch<real_type>::DOUBLE:
   //          _min = boost::lexical_cast<double>( _min_str );
   //          _max = boost::lexical_cast<double>( _max_str );
   //          break;

   //       default:
   //          ASSERT( "Unknown filter type." );
   //    }
   // }

   void
   filter::set_field_name( const string& name )
   {
      _field_name = name;

      // Check if the field name has been set to none.
      string tmp = _field_name;
      to_lower( tmp );
      if( tmp == "none" )
         _field_name.clear();
   }

   filter::iterator
   filter::begin( const tao::batch<real_type>& bat ) const
   {
      return iterator( this, &bat, false );
   }

   filter::iterator
   filter::end( const tao::batch<real_type>& bat ) const
   {
      return iterator( this, &bat, true );
   }

   const string&
   filter::field_name() const
   {
      return _field_name;
   }

   filter_iterator::filter_iterator()
      : _filt( 0 ),
        _bat( 0 ),
        _idx( 0 )
   {
   }

   filter_iterator::filter_iterator( const filter* filt,
                                     const batch<real_type>* bat,
                                     bool done )
      : _filt( filt ),
        _bat( bat ),
        _idx( 0 )
   {
      if( !done )
      {
         if( !filt->field_name().empty() )
         {
            _vals = bat->scalar<real_type>( filt->field_name() );
            _settle();
         }
      }
      else
         _idx = bat->size();
   }

   void
   filter_iterator::increment()
   {
      ++_idx;
      if( !_filt->field_name().empty() )
         _settle();
   }

   bool
   filter_iterator::equal( const filter_iterator& op ) const
   {
      return _idx == op._idx;
   }

   unsigned
   filter_iterator::dereference() const
   {
      return _idx;
   }

   void
   filter_iterator::_settle()
   {
      while( _idx < _vals.size() && !(*_filt)( _vals[_idx] ) )
         ++_idx;
   }

}
