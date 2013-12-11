#ifndef tao_base_filter_hh
#define tao_base_filter_hh

#include <libhpc/containers/vector.hh>
#include <libhpc/containers/view.hh>
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

      template< class T >
      bool
      operator()( const T& val ) const
      {
         if( _min && boost::any_cast<T>( *_min ) > val )
            return false;
         if( _max && boost::any_cast<T>( *_max ) < val )
            return false;
         return true;
      }

      // void
      // bind( const tao::batch<real_type>& batch );

      void
      set_field_name( const string& name );

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

      const string&
      field_name() const;

      template< class T >
      optional<const T&>
      minimum() const
      {
         if( _min )
            return optional<const T&>( boost::any_cast<const T&>( *_min ) );
         else
            return none;
      }

      template< class T >
      optional<const T&>
      maximum() const
      {
         if( _max )
            return optional<const T&>( boost::any_cast<const T&>( *_max ) );
         else
            return none;
      }

      iterator
      begin( const tao::batch<real_type>& bat ) const;

      iterator
      end( const tao::batch<real_type>& bat ) const;

   protected:

      string _field_name;
      // batch<real_type>::field_value_type _field_type;
      optional<boost::any> _min;
      optional<boost::any> _max;
      // string _min_str;
      // string _max_str;
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
      vector<real_type>::view _vals;
      unsigned _idx;
   };

}

#endif
