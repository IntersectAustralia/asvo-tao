#include <libhpc/debug/unit_test_main.hh>
#include <libhpc/system/stream_output.hh>
#include <libhpc/containers/mymath.hh>
#include "tao/base/subcones.hh"
#include "tao/base/globals.hh"

using namespace hpc::test;

namespace {

   test_case<> ANON(
      "/tao/base/subcones/calc_cone_angle",
      "",
      []()
      {
	 tao::lightcone lc( &tao::mini_millennium );

	 // Single tile.
	 lc.set_max_redshift( 0.01 );
	 lc.set_min_redshift( 0.0 );
	 auto theta = tao::calc_subcone_angle( lc );
	 TEST( (bool)theta == true, "Must be valid." );
	 TEST( *theta == 0.0, "Contained in one tile." );

	 // Two tiles.
	 lc.set_max_redshift( 0.03 );
	 lc.set_min_redshift( 0.0 );
	 theta = tao::calc_subcone_angle( lc );
	 TEST( (bool)theta == true, "Must be valid." );
	 DELTA( *theta, 0.0764749, 1e-5, "Contained in two tiles." );

	 // Minimum in one tile.
	 lc.set_min_redshift( 0.01 );
	 lc.set_max_redshift( 0.03 );
	 theta = tao::calc_subcone_angle( lc );
	 TEST( (bool)theta == true, "Must be valid." );
	 TEST( *theta == 0.0, "Contained in one tile." );

	 // Minimum in two tiles.
	 lc.set_min_redshift( 0.01 );
	 lc.set_max_redshift( 0.04 );
	 theta = tao::calc_subcone_angle( lc );
	 TEST( (bool)theta == true, "Must be valid." );
	 DELTA( *theta, 0.16234, 1e-5, "Contained in two tiles." );

	 // Specific test.
	 lc.set_simulation( &tao::millennium );
	 lc.set_max_redshift( 3.0 );
	 lc.set_min_redshift( 1.0 );
	 lc.set_max_ra( 1.0 );
	 lc.set_max_dec( 1.0 );
	 theta = tao::calc_subcone_angle( lc );
	 TEST( (bool)theta == true, "Must be valid." );
	 DELTA( *theta, 0.146973, 1e-5, "Contained in two tiles." );
      }
      );

   test_case<> ANON(
      "/tao/base/subcones/calc_max_subcones",
      "",
      []()
      {
	 tao::lightcone lc( &tao::millennium );

	 // Minimum z.
	 lc.set_max_ra( 1.0 );
	 lc.set_max_dec( 1.0 );
	 lc.set_max_redshift( 3.0 );
	 lc.set_min_redshift( 1.0 );
	 unsigned nc = calc_max_subcones( lc );
	 TEST( nc == 6 );
      }
      );

   test_case<> ANON(
      "/tao/base/subcones/calc_cone_origin",
      "",
      []()
      {
	 tao::lightcone lc( &tao::mini_millennium );
	 lc.set_max_redshift( 0.03 );
	 // std::cout << "\n";
	 auto ori = tao::calc_subcone_origin<double>( lc, 1 );
	 // std::cout << ori[0] << ", " << ori[1] << ", " << ori[2] << "\n";
      }
      );

}
