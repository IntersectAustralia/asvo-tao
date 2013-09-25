#include <libhpc/debug/unit_test_main.hh>
#include "tao/base/lightcone.hh"
#include "tao/base/globals.hh"

using namespace hpc;
using namespace hpc::test;
using namespace tao;

test_case<> ANON(
   "/base/lightcone/default_constructor",
   "",
   []()
   {
      lightcone<real_type> lc;
      TEST( lc.simulation() == (void*)0 );
      TEST( lc.min_ra() == 0.0 );
      TEST( lc.max_ra() == to_radians( 10.0 ) );
      TEST( lc.min_dec() == 0.0 );
      TEST( lc.max_dec() == to_radians( 10.0 ) );
      TEST( lc.min_redshift() == 0.0 );
      TEST( lc.max_redshift() == 0.06 );
      TEST( lc.distance_bins().empty() == true );
   }
   );

test_case<> ANON(
   "/base/lightcone/simulation_constructor",
   "",
   []()
   {
      lightcone<real_type> lc( &mini_millennium );
      TEST( lc.simulation() == &mini_millennium );
      TEST( lc.min_ra() == 0.0 );
      TEST( lc.max_ra() == to_radians( 10.0 ) );
      TEST( lc.min_dec() == 0.0 );
      TEST( lc.max_dec() == to_radians( 10.0 ) );
      TEST( lc.min_redshift() == 0.0 );
      TEST( lc.max_redshift() == 0.06 );
      TEST( lc.distance_bins().empty() == false );
   }
   );
