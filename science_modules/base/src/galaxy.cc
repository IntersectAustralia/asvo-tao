#include "galaxy.hh"

using namespace hpc;

namespace tao {

   galaxy::galaxy( const soci::row& row,
                   const array<real_type,3>& box )
      : _row( row ),
        _box( box )
   {
   }

   int
   galaxy::id() const
   {
      return _row.get<int>( "id" );
   }

   galaxy::real_type
   galaxy::x() const
   {
      return _row.get<real_type>( "Pos1" ) + _box[0];
   }

   galaxy::real_type
   galaxy::y() const
   {
      return _row.get<real_type>( "Pos2" ) + _box[1];
   }

   galaxy::real_type
   galaxy::z() const
   {
      return _row.get<real_type>( "Pos3" ) + _box[2];
   }
}
