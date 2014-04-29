#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include "filter.hh"

namespace tao {
   using namespace hpc;

   filter::filter()
   {
   }

   void
   filter::set_field( const std::string& name,
		      const std::string& min,
		      const std::string& max )
   {
      _field_name = name;
      if( boost::algorithm::to_lower_copy( min ) != "none" )
	 _min_str = min;
      else
	 _min_str = "";
      if( boost::algorithm::to_lower_copy( max ) != "none" )
	 _max_str = max;
      else
	 _max_str = "";

      // Check if the field name has been set to none.
      if( boost::algorithm::to_lower_copy( _field_name ) == "none" )
	 _field_name.clear();
   }

   void
   filter::set_type( batch<real_type>::field_value_type type )
   {
      _type = type;
      switch( _type )
      {
	 case batch<real_type>::DOUBLE:
	    if( !_max_str.empty() )
	       set_maximum( boost::lexical_cast<double>( _max_str ) );
	    if( !_min_str.empty() )
	       set_minimum( boost::lexical_cast<double>( _min_str ) );
	    break;

	 case batch<real_type>::INTEGER:
	    if( !_max_str.empty() )
	       set_maximum( boost::lexical_cast<int>( _max_str ) );
	    if( !_min_str.empty() )
	       set_minimum( boost::lexical_cast<int>( _min_str ) );
	    break;

	 case batch<real_type>::UNSIGNED_LONG:
	    if( !_max_str.empty() )
	       set_maximum( boost::lexical_cast<unsigned long>( _max_str ) );
	    if( !_min_str.empty() )
	       set_minimum( boost::lexical_cast<unsigned long>( _min_str ) );
	    break;

	 case batch<real_type>::LONG_LONG:
	    if( !_max_str.empty() )
	       set_maximum( boost::lexical_cast<long long>( _max_str ) );
	    if( !_min_str.empty() )
	       set_minimum( boost::lexical_cast<long long>( _min_str ) );
	    break;

	 case batch<real_type>::UNSIGNED_LONG_LONG:
	    if( !_max_str.empty() )
	       set_maximum( boost::lexical_cast<unsigned long long>( _max_str ) );
	    if( !_min_str.empty() )
	       set_minimum( boost::lexical_cast<unsigned long long>( _min_str ) );
	    break;
      }
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

   const std::string&
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
            // _vals = bat->scalar<real_type>( filt->field_name() );
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
      while( _idx < _bat->size() && !(*_filt)( *_bat, _idx ) )
         ++_idx;
   }

}
