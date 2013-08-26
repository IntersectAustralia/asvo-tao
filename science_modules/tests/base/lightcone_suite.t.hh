#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/base/lightcone.hh"

using namespace hpc;
using namespace tao;

///
///
///
class lightcone_suite : public CxxTest::TestSuite
{
public:

   void test_default_constructor()
   {
      lightcone lc;
      TS_ASSERT( lc._sim == NULL );
      TS_ASSERT_EQUALS( lc._ra[0], 0 );
      TS_ASSERT_EQUALS( lc._ra[1], 10 );
      TS_ASSERT_EQUALS( lc._dec[0], 0 );
      TS_ASSERT_EQUALS( lc._dec[1], 10 );
      TS_ASSERT_EQUALS( lc._z[0], 0 );
      TS_ASSERT_EQUALS( lc._z[1], 0.06 );
      TS_ASSERT( _dist_bins.empty() );
      TS_ASSERT( _snap_bins.empty() );
   }

   void test_simulation_constructor()
   {
      lightcone lc( &mini_millennium );
      TS_ASSERT( lc._sim == &mini_millennium );
      TS_ASSERT_EQUALS( lc._ra[0], 0 );
      TS_ASSERT_EQUALS( lc._ra[1], 10 );
      TS_ASSERT_EQUALS( lc._dec[0], 0 );
      TS_ASSERT_EQUALS( lc._dec[1], 10 );
      TS_ASSERT_EQUALS( lc._z[0], 0 );
      TS_ASSERT_EQUALS( lc._z[1], 0.06 );
      TS_ASSERT( !_dist_bins.empty() );
      TS_ASSERT( !_snap_bins.empty() );
   }

   void test_distance_to_redshift()
   {
      lightcone lc( &mini_millennium );
      
   }
};
