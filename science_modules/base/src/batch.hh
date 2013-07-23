#ifndef tao_base_batch_hh
#define tao_base_batch_hh

#include <unordered_map>
#include <boost/any.hpp>
#include <boost/mpl/map.hpp>
#include <boost/mpl/int.hpp>
#include <boost/mpl/assert.hpp>
#include <boost/mpl/at.hpp>
#include <libhpc/libhpc.hh>

namespace tao {
   using namespace hpc;

   template< class T >
   class batch
   {
   public:

      enum field_value_type
      {
         STRING,
         DOUBLE,
         INTEGER,
         UNSIGNED_LONG,
         LONG_LONG,
         UNSIGNED_LONG_LONG
      };

      enum field_rank_type
      {
         ATTRIBUTE,
         SCALAR,
         VECTOR
      };

      typedef T real_type;
      typedef std::tuple<boost::any,field_rank_type,field_value_type> field_type;

      typedef boost::mpl::map<mpl::pair<string,             mpl::int_<STRING>>,
                              mpl::pair<double,             mpl::int_<DOUBLE>>,
                              mpl::pair<int,                mpl::int_<INTEGER>>,
                              mpl::pair<unsigned long,      mpl::int_<UNSIGNED_LONG> >,
                              mpl::pair<long long,          mpl::int_<LONG_LONG> >,
                              mpl::pair<unsigned long long, mpl::int_<UNSIGNED_LONG_LONG>>> type_map;

   public:

      batch()
         : _max_size( 1000 ),
           _size( 0 )
      {
      }

      batch( const batch& src )
         : _max_size( src._max_size ),
           _size( src._size )
      {
         for( const auto& item : src._fields )
         {
            const auto& name = item.first;
            const auto& src_field = item.second;
            auto& field = _fields[name];
            std::get<1>( field ) = std::get<1>( src_field );
            std::get<2>( field ) = std::get<2>( src_field );
            const auto& val = std::get<0>( src_field );
            if( std::get<1>( field ) == ATTRIBUTE )
            {
               switch( std::get<2>( field ) )
               {
                  case STRING:
                     std::get<0>( field ) = boost::any_cast<string>( val );
                     break;
                  case DOUBLE:
                     std::get<0>( field ) = boost::any_cast<double>( val );
                     break;
                  case INTEGER:
                     std::get<0>( field ) = boost::any_cast<int>( val );
                     break;
                  case UNSIGNED_LONG:
                     std::get<0>( field ) = boost::any_cast<unsigned long>( val );
                     break;
                  case LONG_LONG:
                     std::get<0>( field ) = boost::any_cast<long long>( val );
                     break;
                  case UNSIGNED_LONG_LONG:
                     std::get<0>( field ) = boost::any_cast<unsigned long long>( val );
                     break;
               };
            }
            else if( std::get<1>( field ) == SCALAR )
            {
               switch( std::get<2>( field ) )
               {
                  case STRING:
                     std::get<0>( field ) = new hpc::vector<string>( *boost::any_cast<hpc::vector<string>*>( val ) );
                     break;
                  case DOUBLE:
                     std::get<0>( field ) = new hpc::vector<double>( *boost::any_cast<hpc::vector<double>*>( val ) );
                     break;
                  case INTEGER:
                     std::get<0>( field ) = new hpc::vector<int>( *boost::any_cast<hpc::vector<int>*>( val ) );
                     break;
                  case UNSIGNED_LONG:
                     std::get<0>( field ) = new hpc::vector<unsigned long>( *boost::any_cast<hpc::vector<unsigned long>*>( val ) );
                     break;
                  case LONG_LONG:
                     std::get<0>( field ) = new hpc::vector<long long>( *boost::any_cast<hpc::vector<long long>*>( val ) );
                     break;
                  case UNSIGNED_LONG_LONG:
                     std::get<0>( field ) = new hpc::vector<unsigned long long>( *boost::any_cast<hpc::vector<unsigned long long>*>( val ) );
                     break;
               };
            }
            else
            {
               switch( std::get<2>( field ) )
               {
                  case STRING:
                     std::get<0>( field ) = new fibre<string>( *boost::any_cast<fibre<string>*>( val ) );
                     break;
                  case DOUBLE:
                     std::get<0>( field ) = new fibre<double>( *boost::any_cast<fibre<double>*>( val ) );
                     break;
                  case INTEGER:
                     std::get<0>( field ) = new fibre<int>( *boost::any_cast<fibre<int>*>( val ) );
                     break;
                  case UNSIGNED_LONG:
                     std::get<0>( field ) = new fibre<unsigned long>( *boost::any_cast<fibre<unsigned long>*>( val ) );
                     break;
                  case LONG_LONG:
                     std::get<0>( field ) = new fibre<long long>( *boost::any_cast<fibre<long long>*>( val ) );
                     break;
                  case UNSIGNED_LONG_LONG:
                     std::get<0>( field ) = new fibre<unsigned long long>( *boost::any_cast<fibre<unsigned long long>*>( val ) );
                     break;
               };
            }
         }
      }

      void
      clear()
      {
         _size = 0;
         for( auto& field : _fields )
         {
            switch( std::get<1>( field ) )
            {
               case SCALAR:
                  _del_scalar( std::get<0>( field ), std::get<2>( field ) );
                  break;
               case VECTOR:
                  _del_vector( std::get<0>( field ), std::get<2>( field ) );
                  break;
            };
         }
         _fields.clear();
      }

      void
      set_max_size( unsigned size )
      {
         _max_size = size;
      }

      void
      set_size( unsigned size )
      {
         _size = size;
      }

      void
      update_size()
      {
         bool done = false;
         for( const auto& item : _fields )
         {
            const auto& field = item.second;
            const auto& val = std::get<0>( field );
            if( std::get<1>( field ) == ATTRIBUTE )
               continue;
            switch( std::get<2>( field ) )
            {
               case STRING:
                  if( std::get<1>( field ) == SCALAR )
                     _size = boost::any_cast<hpc::vector<string>*>( val )->size();
                  else
                     _size = boost::any_cast<fibre<string>*>( val )->size();
                  done = true;
                  break;
               case DOUBLE:
                  if( std::get<1>( field ) == SCALAR )
                     _size = boost::any_cast<hpc::vector<double>*>( val )->size();
                  else
                     _size = boost::any_cast<fibre<double>*>( val )->size();
                  done = true;
                  break;
               case INTEGER:
                  if( std::get<1>( field ) == SCALAR )
                     _size = boost::any_cast<hpc::vector<int>*>( val )->size();
                  else
                     _size = boost::any_cast<fibre<int>*>( val )->size();
                  done = true;
                  break;
               case UNSIGNED_LONG:
                  if( std::get<1>( field ) == SCALAR )
                     _size = boost::any_cast<hpc::vector<unsigned long>*>( val )->size();
                  else
                     _size = boost::any_cast<fibre<unsigned long>*>( val )->size();
                  done = true;
                  break;
               case LONG_LONG:
                  if( std::get<1>( field ) == SCALAR )
                     _size = boost::any_cast<hpc::vector<long long>*>( val )->size();
                  else
                     _size = boost::any_cast<fibre<long long>*>( val )->size();
                  done = true;
                  break;
               case UNSIGNED_LONG_LONG:
                  if( std::get<1>( field ) == SCALAR )
                     _size = boost::any_cast<hpc::vector<unsigned long long>*>( val )->size();
                  else
                     _size = boost::any_cast<fibre<unsigned long long>*>( val )->size();
                  done = true;
                  break;
            };

            // Only need one.
            if( done )
               break;
         }

         // If we couldn't find anything, set batch size to 0.
         if( !done )
            _size = 0;
      }

      unsigned
      size() const
      {
         return _size;
      }

      unsigned
      max_size() const
      {
         return _max_size;
      }

      template< class U >
      void
      set_attribute( const string& name,
                     const U& value )
      {
         field_type& field = _fields[name];
         std::get<0>( field ) = value;
         std::get<1>( field ) = ATTRIBUTE;
         std::get<2>( field ) = (field_value_type)boost::mpl::at<type_map,U>::type::value;
      }

      template< class U >
      void
      set_scalar( const string& name )
      {
         ASSERT( _max_size, "Cannot set fields on batches with zero maximum size." );
         field_type& field = _fields[name];
         boost::any& val = std::get<0>( field );
         if( val.empty() )
         {
            val = new hpc::vector<U>( _max_size );
            std::get<1>( field ) = (field_rank_type)SCALAR;
            std::get<2>( field ) = (field_value_type)boost::mpl::at<type_map,U>::type::value;
         }
      }

      void
      set_scalar( const string& name,
                  field_value_type type )
      {
         ASSERT( _max_size, "Cannot set fields on batches with zero maximum size." );
         field_type& field = _fields[name];
         boost::any& val = std::get<0>( field );
         if( val.empty() )
         {
            switch( type )
            {
               case STRING:
                  val = new hpc::vector<std::string>( _max_size );
                  break;
               case DOUBLE:
                  val = new hpc::vector<double>( _max_size );
                  break;
               case INTEGER:
                  val = new hpc::vector<int>( _max_size );
                  break;
               case UNSIGNED_LONG:
                  val = new hpc::vector<unsigned long>( _max_size );
                  break;
               case LONG_LONG:
                  val = new hpc::vector<long long>( _max_size );
                  break;
               case UNSIGNED_LONG_LONG:
                  val = new hpc::vector<unsigned long long>( _max_size );
                  break;
            }
            std::get<1>( field ) = (field_rank_type)SCALAR;
            std::get<2>( field ) = type;
         }
      }

      template< class U >
      fibre<U>&
      set_vector( const string& name )
      {
         ASSERT( _max_size, "Cannot set fields on batches with zero maximum size." );
         field_type& field = _fields[name];
         boost::any& val = std::get<0>( field );
         if( val.empty() )
         {
            val = new hpc::vector<U>( _max_size );
            std::get<1>( field ) = (field_rank_type)VECTOR;
            std::get<2>( field ) = (field_value_type)boost::mpl::at<type_map,U>::type::value;
         }
         return *boost::any_cast<fibre<U>*>( val );
      }

      template< class U >
      const U&
      attribute( const string& name )
      {
         return boost::any_cast<U&>( std::get<0>( field( name ) ) );
      }

      template< class U >
      typename hpc::vector<U>::view
      scalar( const string& name )
      {
         return *boost::any_cast<hpc::vector<U>*>( std::get<0>( field( name ) ) );
      }

      template< class U >
      const typename hpc::vector<U>::view
      scalar( const string& name ) const
      {
         return *boost::any_cast<hpc::vector<U>*>( std::get<0>( field( name ) ) );
      }

      template< class U >
      const fibre<U>&
      vector( const string& name ) const
      {
         return *boost::any_cast<fibre<U>*>( std::get<0>( field( name ) ) );
      }

      field_type&
      field( const string& name )
      {
         auto it = _fields.find( name );
         ASSERT( it != _fields.end(), "No field by that name on batch object." );
         return it->second;
      }

      const field_type&
      field( const string& name ) const
      {
         auto it = _fields.find( name );
         ASSERT( it != _fields.end() );
         return it->second;
      }

      friend std::ostream&
      operator<<( std::ostream& strm,
                  const batch& obj )
      {
         return strm;
      }

   protected:

      void
      _del_scalar( boost::any& val,
                   field_value_type type )
      {
         switch( type )
         {
            case STRING:
               delete boost::any_cast<hpc::vector<string>*>( val );
               break;
            case DOUBLE:
               delete boost::any_cast<hpc::vector<double>*>( val );
               break;
            case INTEGER:
               delete boost::any_cast<hpc::vector<int>*>( val );
               break;
            case UNSIGNED_LONG:
               delete boost::any_cast<hpc::vector<unsigned long>*>( val );
               break;
            case LONG_LONG:
               delete boost::any_cast<hpc::vector<long long>*>( val );
               break;
            case UNSIGNED_LONG_LONG:
               delete boost::any_cast<hpc::vector<unsigned long long>*>( val );
               break;
         };
      }

      void
      _del_vector( boost::any& val,
                   field_value_type type )
      {
         switch( type )
         {
            case STRING:
               delete boost::any_cast<fibre<string>*>( val );
               break;
            case DOUBLE:
               delete boost::any_cast<fibre<double>*>( val );
               break;
            case INTEGER:
               delete boost::any_cast<fibre<int>*>( val );
               break;
            case UNSIGNED_LONG:
               delete boost::any_cast<fibre<unsigned long>*>( val );
               break;
            case LONG_LONG:
               delete boost::any_cast<fibre<long long>*>( val );
               break;
            case UNSIGNED_LONG_LONG:
               delete boost::any_cast<fibre<unsigned long long>*>( val );
               break;
         };
      }

   protected:

      unsigned _max_size, _size;
      std::unordered_map<string,field_type> _fields;
   };

}

#endif
