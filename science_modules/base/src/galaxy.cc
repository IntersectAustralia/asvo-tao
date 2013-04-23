#include <stdlib.h>
#include "galaxy.hh"

using namespace hpc;

namespace tao {

   galaxy::galaxy()
      : _table( NULL )
   {
   }

   galaxy::galaxy( const string& table )
      : _table( &table )
   {
   }

   void
   galaxy::clear()
   {
      _batch_size = 0;
      _fields.clear();
   }

   void
   galaxy::set_table( const string& table )
   {
      _table = &table;
   }

   void
   galaxy::set_batch_size( unsigned size )
   {
      _batch_size = size;
   }

   // void
   // galaxy::update( const soci::row& row,
   //                 const string& table )
   // {

   // }

   // void
   // galaxy::update( const galaxy& gal )
   // {
   //    _table = gal._table;
   //    _z = _row->get<real_type>( "redshift" );
   //    _fields.clear();
   // }

   // void
   // galaxy::set_redshift( real_type redshift )
   // {
   //    _z = redshift;
   //    set_field<double>( "redshift", _z );
   // }

   const string&
   galaxy::table() const
   {
      ASSERT( _table );
      return *_table;
   }

   unsigned
   galaxy::batch_size() const
   {
      return _batch_size;
   }

   // const vector<long long>&
   // galaxy::ids() const
   // {
   //    ASSERT( _row );
   //    return _row->get<long long>( "globalindex" );
   // }

   // int
   // galaxy::local_id() const
   // {
   //    ASSERT( _row );
   //    return _row->get<int>( "localgalaxyid" );
   // }

   // long long
   // galaxy::tree_id() const
   // {
   //    ASSERT( _row );
   //    return _row->get<long long>( "globaltreeid" );
   // }

//    const vector<galaxy::real_type>&
//    galaxy::x() const
//    {
//       // This is ridiculous, but it seems sqlite represents
//       // modified aliases, (0 + posx + 0) AS pos_x, as strings.
//       // "Surely not!?" you say, but indeed it is so. This
//       // means sqlite databases won't have the correct rotated/
//       // translated values used as pos_x, pos_y, pos_z.
// #ifndef NDEBUG
//       if( _row->get_properties( "pos_x" ).get_data_type() == soci::dt_string )
// 	 return atof( _row->get<std::string>( "pos_x" ).c_str() );
//       else
// 	 return _row->get<real_type>( "pos_x" );
// #else
//       return _row->get<real_type>( "pos_x" );
// #endif
//    }

//    galaxy::real_type
//    galaxy::y() const
//    {
//       ASSERT( _row );

//       // This is ridiculous, but it seems sqlite represents
//       // modified aliases, (0 + posx + 0) AS pos_x, as strings.
//       // "Surely not!?" you say, but indeed it is so. This
//       // means sqlite databases won't have the correct rotated/
//       // translated values used as pos_x, pos_y, pos_z.
// #ifndef NDEBUG
//       if( _row->get_properties( "pos_y" ).get_data_type() == soci::dt_string )
// 	 return atof( _row->get<std::string>( "pos_y" ).c_str() );
//       else
// 	 return _row->get<real_type>( "pos_y" );
// #else
//       return _row->get<real_type>( "pos_y" );
// #endif
//    }

//    galaxy::real_type
//    galaxy::z() const
//    {
//       ASSERT( _row );

//       // This is ridiculous, but it seems sqlite represents
//       // modified aliases, (0 + posx + 0) AS pos_x, as strings.
//       // "Surely not!?" you say, but indeed it is so. This
//       // means sqlite databases won't have the correct rotated/
//       // translated values used as pos_x, pos_y, pos_z.
// #ifndef NDEBUG
//       if( _row->get_properties( "pos_z" ).get_data_type() == soci::dt_string )
// 	 return atof( _row->get<std::string>( "pos_z" ).c_str() );
//       else
// 	 return _row->get<real_type>( "pos_z" );
// #else
//       return _row->get<real_type>( "pos_z" );
// #endif
//    }

//    galaxy::real_type
//    galaxy::redshift() const
//    {
//       return _z;
//    }

//    galaxy::real_type
//    galaxy::disk_metallicity() const
//    {
//       ASSERT( _row );
//       return _row->get<real_type>( "disk_metal" );
//    }

//    galaxy::real_type
//    galaxy::bulge_metallicity() const
//    {
//       ASSERT( _row );
//       return _row->get<real_type>( "bulge_metal" );
//    }

   galaxy::field_type
   galaxy::field( const string& name ) const
   {
      auto it = _fields.find( name );
      ASSERT( it != _fields.end() );
      return it->second;
   }

   std::ostream&
   operator<<( std::ostream& strm,
               const galaxy& obj )
   {
      return strm;
   }
}
