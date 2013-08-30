#include <libhpc/debug/unit_test_main.hh>
#include "tao/base/tile_table_iterator.hh"
#include "tao/base/soci_backend.hh"
#include "db_fixture.hh"

using namespace hpc;
using namespace hpc::test;
using namespace tao;

typedef backends::tile_table_iterator<backends::soci<real_type>> iterator_type;

test_case<db_fixture> ANON(
   "/base/tile_table_iterator/copy_constructor",
   "",
   []( db_fixture& db )
   {
      // backends::soci<real_type> be;
      // be.connect( "millennium_mini_1", "taoadmin", "taoadmin" );
      // be.set_simulation( &mini_millennium );
      // lightcone<real_type> lc( &mini_millennium );
      // tao::tile<real_type> tile( &lc );

      // // Create first iterator.
      // iterator_type src( tile, be );

      // // Copy first iterator.
      // iterator_type cpy( src );

      // TEST( cpy._be == &be );
      // TEST( cpy._be == src._be );
      // TEST( cpy._tile == &tile );
      // TEST( cpy._tile == src._tile );

      // TEST( cpy._ph.size() == src._ph.size() );
      // for( unsigned ii = 0; ii < cpy._ph.size(); ++ii )
      //    TEST( cpy._ph[ii] == src._ph[ii] );

      // TEST( cpy._planes.size() == src._planes.size() );
      // {
      //    auto cpy_it = cpy._planes.begin();
      //    auto src_it = src._planes.begin();
      //    TEST( *cpy_it == *src_it );
      //    ++cpy_it;
      //    ++src_it;
      // }

      // TEST( cpy._walls.size() == src._walls.size() );
      // for( unsigned ii = 0; ii < cpy._walls.size(); ++ii )
      // {
      //    TEST( cpy._walls[ii] == src._walls[ii] );
      // }

      // TEST( cpy._tables.size(), src._tables.size() );
      // for( unsigned ii = 0; ii < cpy._tables.size(); ++ii )
      // {
      //    TEST( cpy._tables[ii] == src._tables[ii] );
      // }

      // TEST( (cpy._it - cpy._tables.begin()) == (src._it - src._tables.begin()) );
   }
   );
