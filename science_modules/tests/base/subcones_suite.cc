#include <libhpc/debug/unit_test_main.hh>
#include <libhpc/system/stream_output.hh>
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
	 lc.set_max_redshift( 0.03 );
	 double theta = *tao::calc_subcone_angle( lc );
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
