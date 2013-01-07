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
      return _row.get<real_type>( "posx" ) + _box[0];
   }

   galaxy::real_type
   galaxy::y() const
   {
      return _row.get<real_type>( "posy" ) + _box[1];
   }

   galaxy::real_type
   galaxy::z() const
   {
      return _row.get<real_type>( "posz" ) + _box[2];
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
