#include <libhpc/unit_test/main.hh>
#include <tao/base/lightcone_tile_iterator.hh>
#include <tao/base/globals.hh>

using tao::real_type;
using tao::lightcone_tile_iterator;

TEST_CASE( "/tao/base/lightcone_tile_iterator/constructor/default" )
{
   lightcone_tile_iterator lti;
   TEST( lti.lightcone() == (void*)0 );
   TEST( lti.done() == true );
   TEST( lti.index() == std::numeric_limits<unsigned>::max() );
   TEST( lti.remaining_tiles().empty() == true );
   TEST( lti.done_tiles().empty() == true );
}

TEST_CASE( "/tao/base/lightcone_tile_iterator/constructor/lightcone" )
{
   tao::lightcone lc( &tao::mini_millennium );
   lightcone_tile_iterator lti( lc );
   TEST( lti.lightcone() == &lc );
   TEST( lti.done() == false );
   TEST( lti.index() == 0 );
   TEST( lti.remaining_tiles().empty() == false );
   TEST( lti.done_tiles().size() == 1 );
   auto tile = *lti;
   TEST( tile.lightcone() == &lc );
   DELTA( tile.min()[0], 0.0, 1e-8 );
   DELTA( tile.min()[1], 0.0, 1e-8 );
   DELTA( tile.min()[2], 0.0, 1e-8 );
}

TEST_CASE( "/tao/base/lightcone_tile_iterator/increment/sphere" )
{
   tao::lightcone lc( &tao::mini_millennium );
   lc.set_geometry( 0.0, 360.0, -90.0, 90.0, 1.0 );
   lightcone_tile_iterator lti( lc );
   real_type bs = lc.simulation()->box_size();
   real_type values[] = { 0.0, 0.0, 0.0,
			  -bs, 0.0, 0.0,
			   bs, 0.0, 0.0,
			  0.0, -bs, 0.0,
			  0.0,  bs, 0.0,
			  0.0, 0.0, -bs,
			  0.0, 0.0,  bs,
			  -2.0*bs, 0.0, 0.0,
			  -bs, -bs, 0.0,
			  -bs,  bs, 0.0,
			  -bs, 0.0, -bs,
			  -bs, 0.0,  bs };
   for( unsigned ii = 0; ii < 12; ++ii, ++lti )
   {
      auto tile = *lti;
      DELTA( tile.min()[0], values[3*ii + 0], 1e-8 );
      DELTA( tile.min()[1], values[3*ii + 1], 1e-8 );
      DELTA( tile.min()[2], values[3*ii + 2], 1e-8 );
   }
}

TEST_CASE( "/tao/base/lightcone_tile_iterator/increment/pencil" )
{
   tao::lightcone lc( &tao::mini_millennium );
   lc.set_geometry( 0.0, 1.0, 0.0, 1.0, 0.1 );
   lightcone_tile_iterator lti( lc );
   real_type bs = lc.simulation()->box_size();
   for( unsigned ii = 0; !lti.done(); ++ii, ++lti )
   {
      auto tile = *lti;
      DELTA( tile.min()[0], ii*bs, 1e-8 );
      DELTA( tile.min()[1], 0.0, 1e-8 );
      DELTA( tile.min()[2], 0.0, 1e-8 );
   }
}

TEST_CASE( "/tao/base/lightcone_tile_iterator/increment/initial_point" )
{
   tao::lightcone lc( &tao::mini_millennium );
   lc.set_geometry( 0.0, 1.0, 0.0, 1.0, 0.2, 0.1 );
   lightcone_tile_iterator lti( lc );
   real_type bs = lc.simulation()->box_size();
   for( unsigned ii = 0; !lti.done(); ++ii, ++lti )
   {
      auto tile = *lti;
      DELTA( tile.min()[0], ii*bs + 250.0, 1e-8 );
      DELTA( tile.min()[1], 0.0, 1e-8 );
      DELTA( tile.min()[2], 0.0, 1e-8 );
   }
}
