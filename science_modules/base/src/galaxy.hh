#ifndef tao_base_galaxy_hh
#define tao_base_galaxy_hh

#include <unordered_map>
#include <boost/any.hpp>
#include <boost/mpl/map.hpp>
#include <boost/mpl/int.hpp>
#include <boost/mpl/assert.hpp>
#include <boost/mpl/at.hpp>
#include <soci/soci.h>
#include <libhpc/libhpc.hh>

namespace tao {
   using namespace hpc;

   class galaxy
   {
   public:

      enum field_value_type
      {
         STRING = soci::dt_string,
         DOUBLE = soci::dt_double,
         INTEGER = soci::dt_integer,
         UNSIGNED_LONG = soci::dt_unsigned_long,
         LONG_LONG = soci::dt_long_long,
         UNSIGNED_LONG_LONG = soci::dt_unsigned_long_long
      };

      typedef double real_type;
      typedef std::pair<boost::any,field_value_type> field_type;

      typedef boost::mpl::map<mpl::pair<string, mpl::int_<STRING>>,
                              mpl::pair<double, mpl::int_<DOUBLE>>,
                              mpl::pair<int, mpl::int_<INTEGER>>,
                              mpl::pair<unsigned long, mpl::int_<UNSIGNED_LONG> >,
                              mpl::pair<long long, mpl::int_<LONG_LONG> >,
                              mpl::pair<unsigned long long, mpl::int_<UNSIGNED_LONG_LONG>>> type_map;

   public:

      galaxy();

      galaxy( const string& table );

      // void
      // update( const soci::row& row,
      //         const string& table );

      // void
      // update( const galaxy& gal );

      // void
      // set_redshifts( vector<real_type>& redshift );

      // const soci::row&
      // row() const;

      void
      clear();

      void
      set_table( const string& table );

      const string&
      table() const;

      void
      set_batch_size( unsigned size );

      // const vector<long long>&
      // ids() const;

      // const vector<int>&
      // local_ids() const;

      // const vector<long long>&
      // tree_ids() const;

      // const vector<real_type>&
      // x() const;

      // const vector<real_type>&
      // y() const;

      // const vector<real_type>&
      // z() const;

      // const vector<real_type>&
      // redshifts() const;

      unsigned
      batch_size() const;

      template< class T >
      void
      set_field( const string& name,
                 typename vector<T>::view value )
      {
         ASSERT( value.size() == _batch_size );
         field_type& field = _fields[name];
         field.first = value;
         field.second = (field_value_type)boost::mpl::at<type_map,T>::type::value;
      }

      template< class T >
      void
      set_vector_field( const string& name,
                        fibre<T>& value )
      {
         ASSERT( value.size() == _batch_size );
         field_type& field = _fields[name];
         field.first = &value;
         field.second = (field_value_type)boost::mpl::at<type_map,T>::type::value;
      }

      template< class T >
      typename vector<T>::view
      values( const string& name ) const
      {
         return boost::any_cast<typename vector<T>::view>( field( name ).first );
      }

      template< class T >
      fibre<T>&
      vector_values( const string& name ) const
      {
         return *boost::any_cast<fibre<T>*>( field( name ).first );
      }

      field_type
      field( const string& name ) const;

      friend std::ostream&
      operator<<( std::ostream& strm,
                  const galaxy& obj );

   public:

      const string* _table;
      unsigned _batch_size;
      std::unordered_map<string,field_type> _fields;
   };
}

#endif
