#include <libhpc/debug/unit_test_main.hh>
#include "tao/base/lightcone.hh"
#include "tao/base/globals.hh"

using namespace hpc::test;

namespace {

   test_case<> ANON(
      "/tao/base/lightcone/constructor/default",
      "",
      []()
      {
         tao::lightcone lc;
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
      "/tao/base/lightcone/constructor/simulation",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );
         TEST( lc.simulation() == &tao::mini_millennium );
         TEST( lc.min_ra() == 0.0 );
         TEST( lc.max_ra() == to_radians( 10.0 ) );
         TEST( lc.min_dec() == 0.0 );
         TEST( lc.max_dec() == to_radians( 10.0 ) );
         TEST( lc.min_redshift() == 0.0 );
         TEST( lc.max_redshift() == 0.06 );
         TEST( lc.distance_bins().empty() == false );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_simulation",
      "",
      []()
      {
         tao::lightcone lc;
         TEST( lc.simulation() == (void*)0 );
         lc.set_simulation( &tao::mini_millennium );
         TEST( lc.simulation() == &tao::mini_millennium );
         lc.set_simulation( nullptr );
         TEST( lc.simulation() == (void*)0 );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_geometry",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );

         // Catch errors.
         THROWSANY( lc.set_geometry( -1, 20, 10, 20, 2, 1 ), "RA >= 0" );
         THROWSANY( lc.set_geometry( 10, 91, 10, 20, 2, 1 ), "RA <= 90" );
         THROWSANY( lc.set_geometry( 10, 20, -1, 20, 2, 1 ), "DEC >= 0" );
         THROWSANY( lc.set_geometry( 10, 20, 10, 91, 2, 1 ), "DEC <= 90" );
         THROWSANY( lc.set_geometry( 20, 10, 10, 20, 2, 1 ), "RA_max >= RA_min" );
         THROWSANY( lc.set_geometry( 10, 20, 20, 10, 2, 1 ), "DEC_max >= DEC_min" );
         THROWSANY( lc.set_geometry( 10, 20, 10, 20, 2, -1 ), "Z > 0" );
         THROWSANY( lc.set_geometry( 10, 20, 10, 20, 2, 3 ), "Z_max >= Z_min" );

         // This one works.
         lc.set_geometry( 10, 20, 30, 40, 2, 1 );

         // Values must have been set.
         DELTA( lc.min_ra(), to_radians( 10.0 ), 1e-4 );
         DELTA( lc.max_ra(), to_radians( 20.0 ), 1e-4 );
         DELTA( lc.min_dec(), to_radians( 30.0 ), 1e-4 );
         DELTA( lc.max_dec(), to_radians( 40.0 ), 1e-4 );
         DELTA( lc.min_redshift(), 1.0, 1e-4 );
         DELTA( lc.max_redshift(), 2.0, 1e-4 );

         // Recalculation must have happened.
         TEST( lc.min_dist() > 0.0 );
         TEST( lc.max_dist() > 0.0 );
         TEST( lc.snapshot_bins().size() > 0 );
         TEST( lc.distance_bins().size() > 0 );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_min_ra",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );
         lc.set_max_ra( 40 );
         THROWSANY( lc.set_min_ra( -1 ) );
         THROWSANY( lc.set_min_ra( 91 ) );
         lc.set_min_ra( 20 );
         DELTA( lc.min_ra(), to_radians( 20.0 ), 1e-4 );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_max_ra",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );
         lc.set_max_ra( 40 );
         lc.set_min_ra( 20 );
         THROWSANY( lc.set_max_ra( -1 ) );
         THROWSANY( lc.set_max_ra( 91 ) );
         lc.set_max_ra( 40 );
         DELTA( lc.max_ra(), to_radians( 40.0 ), 1e-4 );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_min_dec",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );
         lc.set_max_dec( 40 );
         THROWSANY( lc.set_min_dec( -1 ) );
         THROWSANY( lc.set_min_dec( 91 ) );
         lc.set_min_dec( 20 );
         DELTA( lc.min_dec(), to_radians( 20.0 ), 1e-4 );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_max_dec",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );
         lc.set_max_dec( 40 );
         lc.set_min_dec( 20 );
         THROWSANY( lc.set_max_dec( -1 ) );
         THROWSANY( lc.set_max_dec( 91 ) );
         lc.set_max_dec( 40 );
         DELTA( lc.max_dec(), to_radians( 40.0 ), 1e-4 );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_min_redshift",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );
         lc.set_max_redshift( 4 );
         THROWSANY( lc.set_min_redshift( -1 ) );
         THROWSANY( lc.set_min_redshift( 5 ) );
         lc.set_min_redshift( 2 );
         DELTA( lc.min_redshift(), 2, 1e-4 );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_max_redshift",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );
         lc.set_max_redshift( 4 );
         lc.set_min_redshift( 2 );
         THROWSANY( lc.set_max_redshift( -1 ) );
         THROWSANY( lc.set_max_redshift( 1 ) );
         lc.set_max_redshift( 3 );
         DELTA( lc.max_redshift(), 3, 1e-4 );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_random",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );
         lc.set_random( true );
         TEST( lc.random() == true );
         lc.set_random( false );
         TEST( lc.random() == false );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_viewing_angle",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );
         lc.set_viewing_angle( 10 );
         DELTA( lc.viewing_angle(), 10.0, 1e-4 );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/set_origin",
      "",
      []()
      {
         tao::lightcone lc( &tao::mini_millennium );
         lc.set_origin( { 1.0, 1.0, 1.0 } );
         DELTA( lc.origin()[0], 1.0, 1e-4 );
         DELTA( lc.origin()[1], 1.0, 1e-4 );
         DELTA( lc.origin()[2], 1.0, 1e-4 );
      }
      );

   test_case<> ANON(
      "/tao/base/lightcone/recalculate",
      "",
      []()
      {
         tao::lightcone lc;

         // No simulation.
         lc.set_geometry( 0, 5, 0, 5, 0.1 );
         TEST( lc.snapshot_bins().size() == 0 );
         TEST( lc.distance_bins().size() == 0 );

         // Normal case.
         tao::real_type h = tao::mini_millennium.h();
         lc.set_simulation( &tao::mini_millennium );
         lc.set_geometry( 0, 5, 0, 5, 2, 1 );
         DELTA( lc.min_dist(), 3267.8*h, 1.0 );
         DELTA( lc.max_dist(), 5198.7*h, 1.0 );
         {
            tao::real_type bin_vals[] = {
               3794.88, 3697.33, 3524.91, 3353.44, 3183.26, 3014.77, 2848.29, 2684.2, 2522.84, 2385.02
            };
            unsigned snap_vals[] = { 33, 34, 35, 36, 37, 38, 39, 40, 41 };
            TEST( lc.distance_bins().size() > 0 );
            for( unsigned ii = 0; ii < lc.distance_bins().size(); ++ii )
               DELTA( lc.distance_bins()[ii], bin_vals[ii], 1e-1 );
            TEST( lc.snapshot_bins().size() > 0 );
            for( unsigned ii = 0; ii < lc.snapshot_bins().size(); ++ii )
               TEST( lc.snapshot_bins()[ii] == snap_vals[ii] );
         }

         // Short lightcone.
         lc.set_geometry( 0, 5, 0, 5, 0.1, 0.0999 );
         DELTA( lc.min_dist(), 402.8*h, 1.0 );
         DELTA( lc.max_dist(), 402.8*h, 1.0 );
         TEST( lc.distance_bins().size() == 2 );
         DELTA( lc.distance_bins()[0], 293.9, 1e-1 );
         DELTA( lc.distance_bins()[1], 293.6, 1e-1 );
         TEST( lc.snapshot_bins().size() == 1 );

         // Beyond simulation limit.
         tao::simulation<tao::real_type> sim( 500.0, 73.0, 0.25, 0.75, 2, 0.9, 1.0 );
         lc.set_simulation( &sim );
         lc.set_geometry( 0, 5, 0, 5, 1.0 );
         DELTA( lc.min_dist(), 0.0, 1.0 );
         DELTA( lc.max_dist(), 3267.8*h, 1.0 );
         TEST( lc.distance_bins().size() == 3 );
         TEST( lc.snapshot_bins().size() == 2 );
      }
      );

}
