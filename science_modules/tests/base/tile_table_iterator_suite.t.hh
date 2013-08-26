#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/base/tile_table_iterator.hh"
#include "tao/base/lightcone.hh"
#include "tao/base/soci_backend.hh"
#include "tao/base/globals.hh"
#include "tao/base/types.hh"
#include "mpi_fixture.hh"
#include "db_fixture.hh"

using namespace hpc;
using namespace tao;

///
///
///
class tile_table_iterator_suite : public CxxTest::TestSuite
{
public:

   ///
   /// Test copy constructor.
   ///
   void test_copy_constructor()
   {
      backends::soci<real_type> be;
      be.connect( "millennium_mini_1", "taoadmin", "taoadmin" );
      be.set_simulation( &mini_millennium );
      lightcone<real_type> lc( &mini_millennium );
      tao::tile<real_type> tile( &lc );
      iterator_type src( tile, be );

      // Copy first iterator.
      iterator_type cpy( src );

      TS_ASSERT_EQUALS( cpy._be, &be );
      TS_ASSERT_EQUALS( cpy._be, src._be );
      TS_ASSERT_EQUALS( cpy._tile, &tile );
      TS_ASSERT_EQUALS( cpy._tile, src._tile );

      TS_ASSERT_EQUALS( cpy._ph.size(), src._ph.size() );
      for( unsigned ii = 0; ii < cpy._ph.size(); ++ii )
      {
         TS_ASSERT( cpy._ph[ii] == src._ph[ii] );
      }

      TS_ASSERT_EQUALS( cpy._planes.size(), src._planes.size() );
      {
         auto cpy_it = cpy._planes.begin();
         auto src_it = src._planes.begin();
         TS_ASSERT( *cpy_it == *src_it );
         ++cpy_it;
         ++src_it;
      }

      TS_ASSERT_EQUALS( cpy._walls.size(), src._walls.size() );
      for( unsigned ii = 0; ii < cpy._walls.size(); ++ii )
      {
         TS_ASSERT( cpy._walls[ii] == src._walls[ii] );
      }

      TS_ASSERT_EQUALS( cpy._tables.size(), src._tables.size() );
      for( unsigned ii = 0; ii < cpy._tables.size(); ++ii )
      {
         TS_ASSERT( cpy._tables[ii] == src._tables[ii] );
      }

      TS_ASSERT_EQUALS( (cpy._it - cpy._tables.begin()), (src._it - src._tables.begin()) );
   }

   // TODO: Change this to a more appropriate backend.
   typedef backends::tile_table_iterator<backends::soci<real_type>> iterator_type;
};
