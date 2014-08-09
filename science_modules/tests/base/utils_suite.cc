#include <libhpc/unit_test/main.hh>
#include "tao/base/globals.hh"
#include "tao/base/lightcone.hh"
#include "tao/base/utils.hh"

SUITE_PREFIX( "/tao/base/utils/" );

TEST_CASE( "redshift_to_age" )
{
   // Test redshift to age calculation. Ned's cosmological calculator
   // from online suggests with constants of H0=73, OmegaM=0.25 and
   // OmegaV=0.75 we should get an age for redshift 3 of 2.211 Gyr.
   double age = tao::redshift_to_age<double>( 3.0, 73.0, 0.25, 0.75 );
   DELTA( age, 2.211, 1e-3 );
}

TEST_CASE( "observed_redshift/zero_z" )
{
   hpc::varray<tao::real_type,3> pos{ 0.0, 0.0, 0.0 }, vel{ 0.0, 0.0, 0.0 };
   TEST( tao::observed_redshift( 0.0, pos, vel, 75.0 ) == 0.0 );
}

TEST_CASE( "observed_redshift/zero_velocity" )
{
   hpc::varray<tao::real_type,3> pos{ 1.0, 1.0, 1.0 }, vel{ 0.0, 0.0, 0.0 };
   tao::lightcone lc( &tao::mini_millennium );
   lc.set_geometry( 0.0, 10.0, 0.0, 10.0, 10.0, 0.0 );
   tao::real_type z = lc.distance_to_redshift( pos.magnitude() );
   DELTA( tao::observed_redshift( z, pos, vel, lc.simulation()->hubble() ), z, 1e-8 );
}

TEST_CASE( "observed_redshift/low_redshift" )
{
   hpc::varray<tao::real_type,3> pos{ 1.0, 1.0, 1.0 }, vel{ 1.0, 1.0, 1.0 };
   tao::lightcone lc( &tao::mini_millennium );
   lc.set_geometry( 0.0, 10.0, 0.0, 10.0, 10.0, 0.0 );
   tao::real_type z = lc.distance_to_redshift( pos.magnitude() );
   tao::real_type res = 3.0*(1.0 + z)/(sqrt( 3.0 )*hpc::constant::c_km_s) + z;
   DELTA( tao::observed_redshift( z, pos, vel, lc.simulation()->hubble() ), res, 1e-8 );
}

TEST_CASE( "observed_redshift/high_redshift" )
{
   hpc::varray<tao::real_type,3> pos{ 5200.0, 5200.0, 5200.0 }, vel{ 1.0, 1.0, 1.0 };
   tao::lightcone lc( &tao::mini_millennium );
   lc.set_geometry( 0.0, 10.0, 0.0, 10.0, 60.0, 0.0 );
   tao::real_type z = lc.distance_to_redshift( pos.magnitude() );
   tao::real_type res = 3.0*(1.0 + z)/(sqrt( 81120000.0 )*hpc::constant::c_km_s) + z;
   DELTA( tao::observed_redshift( z, pos, vel, lc.simulation()->hubble() ), res, 1e-3 );
}

TEST_CASE( "approx_observed_redshift/zero_z" )
{
   hpc::varray<tao::real_type,3> pos{ 0.0, 0.0, 0.0 }, vel{ 0.0, 0.0, 0.0 };
   tao::lightcone lc( &tao::mini_millennium );
   lc.set_geometry( 0.0, 10.0, 0.0, 10.0, 10.0, 0.0 );
   TEST( tao::approx_observed_redshift( lc, pos, vel ) == 0.0 );
}

TEST_CASE( "approx_observed_redshift/zero_velocity" )
{
   hpc::varray<tao::real_type,3> pos{ 1.0, 1.0, 1.0 }, vel{ 0.0, 0.0, 0.0 };
   tao::lightcone lc( &tao::mini_millennium );
   lc.set_geometry( 0.0, 10.0, 0.0, 10.0, 10.0, 0.0 );
   tao::real_type z = lc.distance_to_redshift( pos.magnitude() );
   DELTA( tao::approx_observed_redshift( lc, pos, vel ), z, 1e-8 );
}

TEST_CASE( "approx_observed_redshift/low_redshift" )
{
   hpc::varray<tao::real_type,3> pos{ 1.0, 1.0, 1.0 }, vel{ 1.0, 1.0, 1.0 };
   tao::lightcone lc( &tao::mini_millennium );
   lc.set_geometry( 0.0, 10.0, 0.0, 10.0, 10.0, 0.0 );
   tao::real_type z = lc.distance_to_redshift( pos.magnitude() );
   tao::real_type res = lc.distance_to_redshift( sqrt( 3.0 ) + (3.0/sqrt( 3.0 ))/lc.simulation()->hubble() );
   TEST( tao::approx_observed_redshift( lc, pos, vel ) == res );
}

TEST_CASE( "approx_observed_redshift/high_redshift" )
{
   hpc::varray<tao::real_type,3> pos{ 5200.0, 5200.0, 5200.0 }, vel{ 1.0, 1.0, 1.0 };
   tao::lightcone lc( &tao::mini_millennium );
   lc.set_geometry( 0.0, 10.0, 0.0, 10.0, 60.0, 0.0 );
   tao::real_type z = lc.distance_to_redshift( pos.magnitude() );
   tao::real_type res = lc.distance_to_redshift( sqrt( 81120000.0 ) + (15600.0/sqrt( 81120000.0 ))/lc.simulation()->hubble() );
   TEST( tao::approx_observed_redshift( lc, pos, vel ) == res );
}
