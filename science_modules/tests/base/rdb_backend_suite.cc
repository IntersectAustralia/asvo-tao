#include <libhpc/debug/unit_test_main.hh>
#include "tao/base/rdb_backend.hh"
#include "tao/base/globals.hh"

using namespace hpc::test;

namespace {

   class dummy
      : public tao::backends::rdb<tao::real_type>
   {
   public:

      dummy( tao::simulation const* sim = nullptr )
         : tao::backends::rdb<tao::real_type>( sim ),
           init_called( false )
      {
      }

      virtual
      tao::simulation const*
      load_simulation()
      {
         return nullptr;
      }

      virtual
      void
      _initialise()
      {
         init_called = true;
      }

      bool init_called;
   };

   test_case<> ANON(
      "/tao/base/rdb_backend/constructor/default",
      "",
      []()
      {
         dummy be;
         TEST( be.connected() == false );
         TEST( be.init_called == false );
      }
      );

   test_case<> ANON(
      "/tao/base/rdb_backend/constructor/simulation",
      "",
      []()
      {
         tao::simulation sim;
         dummy be( &sim );
         TEST( be.simulation() == &sim );
         TEST( be.init_called == false );
      }
      );

   test_case<> ANON(
      "/tao/base/rdb_backend/set_simulation",
      "",
      []()
      {
         tao::simulation sim;
         dummy be;
         be.set_simulation( &sim );
         TEST( be.simulation() == &sim );
         TEST( be.init_called == false );
      }
      );

   test_case<> ANON(
      "/tao/base/rdb_backend/init_batch",
      "",
      []()
      {
         dummy be;
         tao::batch<tao::real_type> bat;
         tao::query<tao::real_type> qry;
         be.init_batch( bat, qry );
         TEST( bat.has_field( "redshift_cosmological" ) == true );
         TEST( bat.has_field( "redshift_observed" ) == true );
         TEST( bat.has_field( "ra" ) == true );
         TEST( bat.has_field( "dec" ) == true );
         TEST( bat.has_field( "distance" ) == true );
      }
      );

   test_case<> ANON(
      "/tao/base/rdb_backend/make_box_query_string",
      "",
      []()
      {
         dummy be;
         tao::batch<tao::real_type> bat;
         tao::query<tao::real_type> qry;
         be.init_batch( bat, qry );
         be.add_field( "globalindex" );
         be.add_field( "globaltreeid" );
         be.add_field( "localgalaxyid" );
         be.add_field( "posx" );
         be.add_field( "posy" );
         be.add_field( "posz" );
         be.add_field( "velx" );
         be.add_field( "vely" );
         be.add_field( "velz" );
         be.add_field( "sfr" );
         be.add_field( "snapnum" );
         tao::box<tao::real_type> box( &tao::mini_millennium );
         box.set_size( 10.0 );
         box.set_snapshot( 3 );

         // Standard.
         auto res = be.make_box_query_string( box, qry );
         TEST( res == "SELECT globalindex AS globalindex, globaltreeid AS globaltreeid, localgalaxyid AS localgalaxyid, (posx + 0 - 0) AS posx, (posy + 0 - 0) AS posy, (posz + 0 - 0) AS posz, sfr AS sfr, snapnum AS snapnum, velx AS velx, vely AS vely, velz AS velz FROM -table- WHERE snapnum = 3 AND (posx + 0 - 0) > 0 AND (posx + 0 - 0) < 10 AND (posy + 0 - 0) > 0 AND (posy + 0 - 0) < 10 AND (posz + 0 - 0) > 0 AND (posz + 0 - 0) < 10" );

         // Filter.

         // Origin.

         // Random.
      }
      );

}
