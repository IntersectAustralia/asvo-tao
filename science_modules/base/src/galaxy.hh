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

      galaxy( const soci::row& row,
	      const string& table );

      galaxy();

      void
      update( const soci::row& row,
              const string& table );

      void
      update( const galaxy& gal );

      void
      set_redshift( real_type redshift );

      const soci::row&
      row() const;

      const string&
      table() const;

      long long
      id() const;

      int
      local_id() const;

      long long
      tree_id() const;

      real_type
      x() const;

      real_type
      y() const;

      real_type
      z() const;

      real_type
      redshift() const;

      real_type
      disk_metallicity() const;

      real_type
      bulge_metallicity() const;

      template< class T >
      void
      set_field( const string& name,
                 T value )
      {
         field_type& field = _fields[name];
         field.first = value;
         field.second = (field_value_type)boost::mpl::at<type_map,T>::type::value;
      }

      template< class T >
      T
      value( const string& name ) const
      {
         return boost::any_cast<T>( field( name ).first );
      }

      field_type
      field( const string& name ) const;

      friend std::ostream&
      operator<<( std::ostream& strm,
                  const galaxy& obj );

   public:

      const soci::row* _row;
      const string* _table;
      real_type _z;
      std::unordered_map<string,field_type> _fields;
   };
}

#endif
