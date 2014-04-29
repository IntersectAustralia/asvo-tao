#ifndef tao_base_filter_hh
#define tao_base_filter_hh

#include <string>
#include <boost/optional.hpp>
#include "types.hh"
#include "batch.hh"

namespace tao {
   using namespace hpc;

   class filter_iterator;

   class filter
   {
   public:

      typedef filter_iterator iterator;

   public:

      filter();

      bool
      operator()( batch<real_type> const& bat,
		  unsigned idx ) const
      {
	 switch( _type )
	 {
	    case batch<real_type>::DOUBLE:
	    {
	       double val = bat.scalar<double>( _field_name )[idx];
	       if( _min && boost::any_cast<double>( *_min ) > val )
		  return false;
	       if( _max && boost::any_cast<double>( *_max ) < val )
		  return false;
	    }
	    break;

	    case batch<real_type>::INTEGER:
	    {
	       int val = bat.scalar<int>( _field_name )[idx];
	       if( _min && boost::any_cast<int>( *_min ) > val )
		  return false;
	       if( _max && boost::any_cast<int>( *_max ) < val )
		  return false;
	    }
	    break;

	    case batch<real_type>::UNSIGNED_LONG:
	    {
	       unsigned long val = bat.scalar<unsigned long>( _field_name )[idx];
	       if( _min && boost::any_cast<unsigned long>( *_min ) > val )
		  return false;
	       if( _max && boost::any_cast<unsigned long>( *_max ) < val )
		  return false;
	    }
	    break;

	    case batch<real_type>::LONG_LONG:
	    {
	       long long val = bat.scalar<long long>( _field_name )[idx];
	       if( _min && boost::any_cast<long long>( *_min ) > val )
		  return false;
	       if( _max && boost::any_cast<long long>( *_max ) < val )
		  return false;
	    }
	    break;

	    case batch<real_type>::UNSIGNED_LONG_LONG:
	    {
	       unsigned long long val = bat.scalar<unsigned long long>( _field_name )[idx];
	       if( _min && boost::any_cast<unsigned long long>( *_min ) > val )
		  return false;
	       if( _max && boost::any_cast<unsigned long long>( *_max ) < val )
		  return false;
	    }
	    break;
	 }
         return true;
      }

      void
      set_field( const std::string& name,
		 const std::string& min,
		 const std::string& max );

      void
      set_type( batch<real_type>::field_value_type type );

      template< class T >
      void
      set_minimum( const T& val )
      {
	 switch( _type )
	 {
	    case batch<real_type>::DOUBLE:
	       _min = (double)val;
	       break;

	    case batch<real_type>::INTEGER:
	       _min = (int)val;
	       break;

	    case batch<real_type>::UNSIGNED_LONG:
	       _min = (unsigned long)val;
	       break;

	    case batch<real_type>::LONG_LONG:
	       _min = (long long)val;
	       break;

	    case batch<real_type>::UNSIGNED_LONG_LONG:
	       _min = (unsigned long long)val;
	       break;
	 }
      }

      template< class T >
      void
      set_maximum( const T& val )
      {
	 switch( _type )
	 {
	    case batch<real_type>::DOUBLE:
	       _max = (double)val;
	       break;

	    case batch<real_type>::INTEGER:
	       _max = (int)val;
	       break;

	    case batch<real_type>::UNSIGNED_LONG:
	       _max = (unsigned long)val;
	       break;

	    case batch<real_type>::LONG_LONG:
	       _max = (long long)val;
	       break;

	    case batch<real_type>::UNSIGNED_LONG_LONG:
	       _max = (unsigned long long)val;
	       break;
	 }
      }

      const std::string&
      field_name() const;

      template< class T >
      boost::optional<T>
      minimum() const
      {
         if( _min )
	 {
	    T val;
	    switch( _type )
	    {
	       case batch<real_type>::DOUBLE:
		  val = boost::any_cast<double>( *_min );
		  break;

	       case batch<real_type>::INTEGER:
		  val = boost::any_cast<int>( *_min );
		  break;

	       case batch<real_type>::UNSIGNED_LONG:
		  val = boost::any_cast<unsigned long>( *_min );
		  break;

	       case batch<real_type>::LONG_LONG:
		  val = boost::any_cast<long long>( *_min );
		  break;

	       case batch<real_type>::UNSIGNED_LONG_LONG:
		  val = boost::any_cast<unsigned long long>( *_min );
		  break;
	    }
	    return boost::optional<T>( val );
	 }
         else
	    return boost::none;
      }

      template< class T >
      boost::optional<T>
      maximum() const
      {
         if( _max )
	 {
	    T val;
	    switch( _type )
	    {
	       case batch<real_type>::DOUBLE:
		  val = boost::any_cast<double>( *_max );
		  break;

	       case batch<real_type>::INTEGER:
		  val = boost::any_cast<int>( *_max );
		  break;

	       case batch<real_type>::UNSIGNED_LONG:
		  val = boost::any_cast<unsigned long>( *_max );
		  break;

	       case batch<real_type>::LONG_LONG:
		  val = boost::any_cast<long long>( *_max );
		  break;

	       case batch<real_type>::UNSIGNED_LONG_LONG:
		  val = boost::any_cast<unsigned long long>( *_max );
		  break;
	    }
	    return boost::optional<T>( val );
	 }
         else
            return boost::none;
      }

      iterator
      begin( const tao::batch<real_type>& bat ) const;

      iterator
      end( const tao::batch<real_type>& bat ) const;

   protected:

      std::string _field_name;
      std::string _min_str;
      std::string _max_str;
      boost::optional<boost::any> _min;
      boost::optional<boost::any> _max;
      batch<real_type>::field_value_type _type;
   };

   
   class filter_iterator
      : public boost::iterator_facade< filter_iterator,
                                       unsigned,
                                       std::forward_iterator_tag,
                                       unsigned >
   {
      friend class boost::iterator_core_access;

   public:

      filter_iterator();

      filter_iterator( const filter* filt,
                       const batch<real_type>* bat,
                       bool done );

   protected:

      void
      increment();

      bool
      equal( const filter_iterator& op ) const;

      unsigned
      dereference() const;

      void
      _settle();

   protected:

      const tao::filter* _filt;
      const tao::batch<real_type>* _bat;
      unsigned _idx;
   };

}

#endif
