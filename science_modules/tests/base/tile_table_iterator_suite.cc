#include <libhpc/debug/unit_test_main.hh>
#include "tao/base/tile_table_iterator.hh"
#include "tao/base/soci_backend.hh"
#include "../fixtures/db_fixture.hh"

using namespace hpc;
using namespace hpc::test;
using namespace tao;

typedef backends::tile_table_iterator<backends::soci<real_type>> iterator_type;

test_case<db_fixture> ANON(
   "/base/tile_table_iterator/copy_constructor",
   "",
   []( db_fixture& db )
   {
      // Create first iterator.
      iterator_type src( db.tile, db.be );

      // Copy first iterator.
      iterator_type cpy( src );

      TEST( cpy.backend() == &db.be );
      TEST( cpy.backend() == src.backend() );
      TEST( cpy.tile() == &db.tile );
      TEST( cpy.tile() == src.tile() );

      TEST( cpy.polyhedra().size() == src.polyhedra().size() );
      for( unsigned ii = 0; ii < cpy.polyhedra().size(); ++ii )
         TEST( cpy.polyhedra()[ii] == src.polyhedra()[ii] );

      TEST( cpy.planes().size() == src.planes().size() );
      {
         auto cpy_it = cpy.planes().begin();
         auto src_it = src.planes().begin();
         TEST( *cpy_it == *src_it );
         ++cpy_it;
         ++src_it;
      }

      TEST( cpy.walls().size() == src.walls().size() );
      for( unsigned ii = 0; ii < cpy.walls().size(); ++ii )
         TEST( cpy.walls()[ii] == src.walls()[ii] );

      TEST( cpy.tables().size() == src.tables().size() );
      for( unsigned ii = 0; ii < cpy.tables().size(); ++ii )
         TEST( cpy.tables()[ii] == src.tables()[ii] );

      TEST( (cpy.table_iter() - cpy.tables().begin()) == (src.table_iter() - src.tables().begin()) );
   }
   );
