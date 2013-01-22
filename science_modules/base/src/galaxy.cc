#include <stdlib.h>
#include "galaxy.hh"

using namespace hpc;

namespace tao {

   galaxy::galaxy( const soci::row& row,
                   const array<real_type,3>& box,
		   const string& table )
      : _row( row ),
        _box( box ),
	_table( table )
   {
   }

   const soci::row&
   galaxy::row() const
   {
      return _row;
   }

   const string&
   galaxy::table() const
   {
      return _table;
   }

   long long
   galaxy::id() const
   {
      return _row.get<long long>( "globalindex" );
   }

   int
   galaxy::local_id() const
   {
      return _row.get<int>( "localgalaxyid" );
   }

   long long
   galaxy::tree_id() const
   {
      return _row.get<long long>( "globaltreeid" );
   }

   galaxy::real_type
   galaxy::x() const
   {
      // This is ridiculous, but it seems sqlite represents
      // modified aliases, (0 + posx + 0) AS pos_x, as strings.
      // "Surely not!?" you say, but indeed it is so. This
      // means sqlite databases won't have the correct rotated/
      // translated values used as pos_x, pos_y, pos_z.
#ifndef NDEBUG
      if( _row.get_properties( "pos_x" ).get_data_type() == soci::dt_string )
	 return atof( _row.get<std::string>( "pos_x" ).c_str() );
      else
	 return _row.get<real_type>( "pos_x" );
#else
      return _row.get<real_type>( "pos_x" );
#endif
   }

   galaxy::real_type
   galaxy::y() const
   {
      // This is ridiculous, but it seems sqlite represents
      // modified aliases, (0 + posx + 0) AS pos_x, as strings.
      // "Surely not!?" you say, but indeed it is so. This
      // means sqlite databases won't have the correct rotated/
      // translated values used as pos_x, pos_y, pos_z.
#ifndef NDEBUG
      if( _row.get_properties( "pos_y" ).get_data_type() == soci::dt_string )
	 return atof( _row.get<std::string>( "pos_y" ).c_str() );
      else
	 return _row.get<real_type>( "pos_y" );
#else
      return _row.get<real_type>( "pos_y" );
#endif
   }

   galaxy::real_type
   galaxy::z() const
   {
      // This is ridiculous, but it seems sqlite represents
      // modified aliases, (0 + posx + 0) AS pos_x, as strings.
      // "Surely not!?" you say, but indeed it is so. This
      // means sqlite databases won't have the correct rotated/
      // translated values used as pos_x, pos_y, pos_z.
#ifndef NDEBUG
      if( _row.get_properties( "pos_z" ).get_data_type() == soci::dt_string )
	 return atof( _row.get<std::string>( "pos_z" ).c_str() );
      else
	 return _row.get<real_type>( "pos_z" );
#else
      return _row.get<real_type>( "pos_z" );
#endif
   }

   galaxy::real_type
   galaxy::redshift() const
   {
      return _row.get<real_type>( "redshift" );
   }

   galaxy::real_type
   galaxy::disk_metallicity() const
   {
      return _row.get<real_type>( "disk_metal" );
   }

   galaxy::real_type
   galaxy::bulge_metallicity() const
   {
      return _row.get<real_type>( "bulge_metal" );
   }

   unsigned
   galaxy::flat_file() const
   {
      return _row.get<int>( "flat_file" );
   }

   unsigned
   galaxy::flat_offset() const
   {
      return _row.get<int>( "flat_offset" );
   }

   unsigned
   galaxy::flat_length() const
   {
      return _row.get<int>( "flat_length" );
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
