#include <libhpc/unit_test/main.hh>
#include "tao/base/simulation.hh"

TEST_CASE( "/tao/base/simulation/constructor/default" )
{
   tao::simulation sim;
   TEST( sim.box_size() == 0.0 );
   TEST( sim.hubble() == 0.0 );
   TEST( sim.h() == 0.0 );
   TEST( sim.omega_m() == 0.0 );
   TEST( sim.omega_l() == 0.0 );
   TEST( sim.omega_r() == 0.0 );
   TEST( sim.omega_k() == 0.0 );
   TEST( sim.redshifts().empty() == true );
}

TEST_CASE( "/tao/base/simulation/constructor/vector" )
{
   std::vector<tao::real_type> snap_zs( 2 );
   snap_zs[0] = 1; snap_zs[1] = 0;
   tao::simulation sim( 10, 75, 0.25, 0.70, snap_zs );
   TEST( sim.box_size() == 10.0 );
   TEST( sim.hubble() == 75.0 );
   TEST( sim.h() == 0.75 );
   TEST( sim.omega_m() == 0.25 );
   TEST( sim.omega_l() == 0.70 );
   TEST( sim.omega_r() == 4.165e-5/(0.75*0.75) );
   TEST( sim.omega_k() == (1.0 - 0.25 - 0.70 - 4.165e-5/(0.75*0.75)) );
   TEST( sim.redshifts().size() == 2 );
   TEST( sim.redshifts()[0] == 1.0 );
   TEST( sim.redshifts()[1] == 0.0 );
}

TEST_CASE( "/tao/base/simulation/constructor/expansions" )
{
   tao::simulation sim( 10, 75, 0.25, 0.70, 2, 0, 1 );
   TEST( sim.box_size() == 10.0 );
   TEST( sim.hubble() == 75.0 );
   TEST( sim.h() == 0.75 );
   TEST( sim.omega_m() == 0.25 );
   TEST( sim.omega_l() == 0.70 );
   TEST( sim.omega_r() == 4.165e-5/(0.75*0.75) );
   TEST( sim.omega_k() == (1.0 - 0.25 - 0.70 - 4.165e-5/(0.75*0.75)) );
   TEST( sim.redshifts().size() == 2 );
   TEST( sim.redshifts()[0] == 127.0 );
   DELTA( sim.redshifts()[1], 79.99, 1e-2 );
}

TEST_CASE( "/tao/base/simulation/set_box_size" )
{
   tao::simulation sim;
   sim.set_box_size( 10.0 );
   TEST( sim.box_size() == 10.0 );
}
