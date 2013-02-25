#include <stdlib.h>
#include "galaxy.hh"

using namespace hpc;

namespace tao {

   galaxy::galaxy( const soci::row& row,
		   const string& table )
      : _row( NULL ),
	_table( NULL )
   {
      update( row, table );
   }

   galaxy::galaxy()
      : _row( NULL ),
        _table( NULL )
   {
   }

   void
   galaxy::update( const soci::row& row,
                   const string& table )
   {
      _row = &row;
      _table = &table;
      _z = _row->get<real_type>( "redshift" );
      _fields.clear();
   }

   void
   galaxy::update( const galaxy& gal )
   {
      update( *gal._row, *gal._table );
   }

   void
   galaxy::set_redshift( real_type redshift )
   {
      _z = redshift;
      set_field<double>( "redshift", _z );
   }

   const soci::row&
   galaxy::row() const
   {
      ASSERT( _row );
      return *_row;
   }

   const string&
   galaxy::table() const
   {
      ASSERT( _table );
      return *_table;
   }

   long long
   galaxy::id() const
   {
      ASSERT( _row );
      return _row->get<long long>( "globalindex" );
   }

   int
   galaxy::local_id() const
   {
      ASSERT( _row );
      return _row->get<int>( "localgalaxyid" );
   }

   long long
   galaxy::tree_id() const
   {
      ASSERT( _row );
      return _row->get<long long>( "globaltreeid" );
   }

   galaxy::real_type
   galaxy::x() const
   {
      ASSERT( _row );

      // This is ridiculous, but it seems sqlite represents
      // modified aliases, (0 + posx + 0) AS pos_x, as strings.
      // "Surely not!?" you say, but indeed it is so. This
      // means sqlite databases won't have the correct rotated/
      // translated values used as pos_x, pos_y, pos_z.
#ifndef NDEBUG
      if( _row->get_properties( "pos_x" ).get_data_type() == soci::dt_string )
	 return atof( _row->get<std::string>( "pos_x" ).c_str() );
      else
	 return _row->get<real_type>( "pos_x" );
#else
      return _row->get<real_type>( "pos_x" );
#endif
   }

   galaxy::real_type
   galaxy::y() const
   {
      ASSERT( _row );

      // This is ridiculous, but it seems sqlite represents
      // modified aliases, (0 + posx + 0) AS pos_x, as strings.
      // "Surely not!?" you say, but indeed it is so. This
      // means sqlite databases won't have the correct rotated/
      // translated values used as pos_x, pos_y, pos_z.
#ifndef NDEBUG
      if( _row->get_properties( "pos_y" ).get_data_type() == soci::dt_string )
	 return atof( _row->get<std::string>( "pos_y" ).c_str() );
      else
	 return _row->get<real_type>( "pos_y" );
#else
      return _row->get<real_type>( "pos_y" );
#endif
   }

   galaxy::real_type
   galaxy::z() const
   {
      ASSERT( _row );

      // This is ridiculous, but it seems sqlite represents
      // modified aliases, (0 + posx + 0) AS pos_x, as strings.
      // "Surely not!?" you say, but indeed it is so. This
      // means sqlite databases won't have the correct rotated/
      // translated values used as pos_x, pos_y, pos_z.
#ifndef NDEBUG
      if( _row->get_properties( "pos_z" ).get_data_type() == soci::dt_string )
	 return atof( _row->get<std::string>( "pos_z" ).c_str() );
      else
	 return _row->get<real_type>( "pos_z" );
#else
      return _row->get<real_type>( "pos_z" );
#endif
   }

   galaxy::real_type
   galaxy::redshift() const
   {
      return _z;
   }

   galaxy::real_type
   galaxy::disk_metallicity() const
   {
      ASSERT( _row );
      return _row->get<real_type>( "disk_metal" );
   }

   galaxy::real_type
   galaxy::bulge_metallicity() const
   {
      ASSERT( _row );
      return _row->get<real_type>( "bulge_metal" );
   }

   galaxy::field_type
   galaxy::field( const string& name ) const
   {
      ASSERT( _row );

      auto it = _fields.find( name );

      // If the name is not in the fields, assume it's in
      // the SOCI row.
      if( it == _fields.end() )
      {
         switch( _row->get_properties( name ).get_data_type() )
         {
            case soci::dt_string:
               return field_type( _row->get<std::string>( name ), STRING );

            case soci::dt_double:
               return field_type( _row->get<double>( name ), DOUBLE );

            case soci::dt_integer:
               return field_type( _row->get<int>( name ), INTEGER );

            case soci::dt_unsigned_long_long:
               return field_type( _row->get<unsigned long long>( name ), UNSIGNED_LONG_LONG );

            case soci::dt_long_long:
               return field_type( _row->get<long long>( name ), LONG_LONG );

            default:
               ASSERT( 0 );
         }
      }
      else
         return it->second;
   }

   std::ostream&
   operator<<( std::ostream& strm,
               const galaxy& obj )
   {
      strm << obj.id() << ": ";
      strm << "(" << obj.x() << ", " << obj.y() << ", " << obj.z() << ")";
      return strm;
   }
}
