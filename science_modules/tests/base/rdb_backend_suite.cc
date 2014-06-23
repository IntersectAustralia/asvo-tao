#include <libhpc/unit_test/main.hh>
#include "tao/base/rdb_backend.hh"
#include "tao/base/globals.hh"

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

TEST_CASE( "/tao/base/rdb_backend/constructor/default" )
{
   dummy be;
   TEST( be.connected() == false );
   TEST( be.init_called == false );
}

TEST_CASE( "/tao/base/rdb_backend/constructor/simulation" )
{
   tao::simulation sim;
   dummy be( &sim );
   TEST( be.simulation() == &sim );
   TEST( be.init_called == false );
}

TEST_CASE( "/tao/base/rdb_backend/set_simulation" )
{
   tao::simulation sim;
   dummy be;
   be.set_simulation( &sim );
   TEST( be.simulation() == &sim );
   TEST( be.init_called == false );
}

TEST_CASE( "/tao/base/rdb_backend/init_batch" )
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

TEST_CASE( "/tao/base/rdb_backend/make_box_query_string" )
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
   be.add_field( "sfrdisk" );
   be.add_field( "sfrbulge" );
   be.add_field( "sfrdiskz" );
   be.add_field( "sfrbulgez" );
   be.add_field( "snapnum" );
   be.add_field( "diskscaleradius" );
   tao::box<tao::real_type> box( &tao::mini_millennium );
   box.set_size( 10.0 );
   box.set_snapshot( 3 );

   // Standard.
   auto res = be.make_box_query_string( box, qry );
   TEST( res == "SELECT diskscaleradius AS diskscaleradius, globalindex AS globalindex, globaltreeid AS globaltreeid, localgalaxyid AS localgalaxyid, (posx + 0 - 0) AS posx, (posy + 0 - 0) AS posy, (posz + 0 - 0) AS posz, sfrbulge AS sfrbulge, sfrbulgez AS sfrbulgez, sfrdisk AS sfrdisk, sfrdiskz AS sfrdiskz, snapnum AS snapnum, velx AS velx, vely AS vely, velz AS velz FROM -table- WHERE snapnum = 3 AND (posx + 0 - 0) > 0 AND (posx + 0 - 0) < 10 AND (posy + 0 - 0) > 0 AND (posy + 0 - 0) < 10 AND (posz + 0 - 0) > 0 AND (posz + 0 - 0) < 10" );

   // Filter.

   // Origin.
   box.set_origin( std::array<tao::real_type,3>{ { 1.0, 2.0, 3.0 } } );
   res = be.make_box_query_string( box, qry );
   TEST( res == "SELECT diskscaleradius AS diskscaleradius, globalindex AS globalindex, globaltreeid AS globaltreeid, localgalaxyid AS localgalaxyid, (posx + 0 - 1) AS posx, (posy + 0 - 2) AS posy, (posz + 0 - 3) AS posz, sfrbulge AS sfrbulge, sfrbulgez AS sfrbulgez, sfrdisk AS sfrdisk, sfrdiskz AS sfrdiskz, snapnum AS snapnum, velx AS velx, vely AS vely, velz AS velz FROM -table- WHERE snapnum = 3 AND (posx + 0 - 1) > 0 AND (posx + 0 - 1) < 10 AND (posy + 0 - 2) > 0 AND (posy + 0 - 2) < 10 AND (posz + 0 - 3) > 0 AND (posz + 0 - 3) < 10" );

   // Random.
}

TEST_CASE( "/tao/base/rdb_backend/make_tile_query_string" )
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
   be.add_field( "sfrdisk" );
   be.add_field( "sfrbulge" );
   be.add_field( "sfrdiskz" );
   be.add_field( "sfrbulgez" );
   be.add_field( "snapnum" );
   be.add_field( "coldgas" );
   be.add_field( "metalscoldgas" );
   be.add_field( "diskscaleradius" );
   tao::lightcone lc( &tao::mini_millennium );

   // Standard.

   // Filter.

   // Origin.
   lc.set_origin( std::array<tao::real_type,3>{ { 1.0, 2.0, 3.0 } } );
   tao::tile<tao::real_type> tile( &lc );
   auto res = be.make_tile_query_string( tile, qry );
   // TEST( res == "SELECT diskscaleradius AS diskscaleradius, globalindex AS globalindex, globaltreeid AS globaltreeid, localgalaxyid AS localgalaxyid, (posx + 0 - 1) AS posx, (posy + 0 - 2) AS posy, (posz + 0 - 3) AS posz, sfrbulge AS sfrbulge, sfrbulgez AS sfrbulgez, sfrdisk AS sfrdisk, sfrdiskz AS sfrdiskz, snapnum AS snapnum, velx AS velx, vely AS vely, velz AS velz FROM -table- INNER JOIN redshift_ranges ON (-table-.snapnum = redshift_ranges.snapshot) WHERE (POW((posx + 0 - 1),2) + POW((posy + 0 - 2),2) + POW((posz + 0 - 3),2)) >= redshift_ranges.min AND (POW((posx + 0 - 1),2) + POW((posy + 0 - 2),2) + POW((posz + 0 - 3),2)) < redshift_ranges.max AND ATAN2((posy + 0 - 2),(posx + 0 - 1)) >= 0 AND ATAN2((posy + 0 - 2),(posx + 0 - 1)) < 0.174532925199 AND (0.5*PI() - ACOS((posz + 0 - 3)/(SQRT(POW((posx + 0 - 1),2) + POW((posy + 0 - 2),2) + POW((posz + 0 - 3),2))))) >= 0 AND (0.5*PI() - ACOS((posz + 0 - 3)/(SQRT(POW((posx + 0 - 1),2) + POW((posy + 0 - 2),2) + POW((posz + 0 - 3),2))))) < 0.174532925199 AND (POW((posx + 0 - 1),2) + POW((posy + 0 - 2),2) + POW((posz + 0 - 3),2)) >= 0 AND (POW((posx + 0 - 1),2) + POW((posy + 0 - 2),2) + POW((posz + 0 - 3),2)) < 31598.4212922" );

   // Random.
}

TEST_CASE( "/tao/base/rdb_backend/make_tile_query_string/ra_dec" )
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
   be.add_field( "sfrdisk" );
   be.add_field( "sfrbulge" );
   be.add_field( "sfrdiskz" );
   be.add_field( "sfrbulgez" );
   be.add_field( "snapnum" );
   be.add_field( "coldgas" );
   be.add_field( "metalscoldgas" );
   be.add_field( "diskscaleradius" );
   tao::lightcone lc( &tao::mini_millennium );

   // Minimums 0, maximums within 90.
   lc.set_geometry( 0.0, 45.0, 0.0, 45.0, 1.0 );
   {
      tao::tile<tao::real_type> tile( &lc );
      auto res = be.make_tile_query_string( tile, qry );
      // TODO
/*
  TEST( res == "SELECT diskscaleradius AS diskscaleradius, globalindex AS globalindex, globaltreeid AS globaltreeid, localgalaxyid AS localgalaxyid, (posx + 0 - 0) AS posx, (posy + 0 - 0) AS posy, (posz + 0 - 0) AS posz, sfrbulge AS sfrbulge, sfrbulgez AS sfrbulgez, sfrdisk AS sfrdisk, sfrdiskz AS sfrdiskz, snapnum AS snapnum, velx AS velx, vely AS vely, velz AS velz FROM -table- INNER JOIN redshift_ranges ON (-table-.snapnum = redshift_ranges.snapshot) WHERE (POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2)) >= redshift_ranges.min AND (POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2)) < redshift_ranges.max AND "

  //       // Greater than RAmin.
  //       "ATAN2((posy + 0 - 0),(posx + 0 - 0)) >= 0 AND "

  //       // Less than RAmax.
  //       "ATAN2((posy + 0 - 0),(posx + 0 - 0)) < 0.785398163397 AND "

  //       // Greater than DECmin.
  //       "(0.5*PI() - ACOS((posz + 0 - 0)/(SQRT(POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2))))) >= 0 AND "

  //       // Less than DECmax.
  //       "(0.5*PI() - ACOS((posz + 0 - 0)/(SQRT(POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2))))) < 0.785398163397 AND "

  //       "(POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2)) >= 0 AND (POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2)) < 5688333.71237" );
  }

  // Minimums and maximums within 90.
  lc.set_geometry( 10.0, 45.0, 15.0, 50.0, 1.0 );
  {
  tao::tile<tao::real_type> tile( &lc );
  auto res = be.make_tile_query_string( tile, qry );
  // TEST( res == "SELECT diskscaleradius AS diskscaleradius, globalindex AS globalindex, globaltreeid AS globaltreeid, localgalaxyid AS localgalaxyid, (posx + 0 - 0) AS posx, (posy + 0 - 0) AS posy, (posz + 0 - 0) AS posz, sfrbulge AS sfrbulge, sfrbulgez AS sfrbulgez, sfrdisk AS sfrdisk, sfrdiskz AS sfrdiskz, snapnum AS snapnum, velx AS velx, vely AS vely, velz AS velz FROM -table- INNER JOIN redshift_ranges ON (-table-.snapnum = redshift_ranges.snapshot) WHERE (POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2)) >= redshift_ranges.min AND (POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2)) < redshift_ranges.max AND "

  //       // Greater than RAmin.
  //       "ATAN2((posy + 0 - 0),(posx + 0 - 0)) >= 0.174532925199 AND "

  //       // Less than RAmax.
  //       "ATAN2((posy + 0 - 0),(posx + 0 - 0)) < 0.785398163397 AND "

  //       // Greater than DECmin.
  //       "(0.5*PI() - ACOS((posz + 0 - 0)/(SQRT(POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2))))) >= 0.261799387799 AND "

  //       // Less than DECmax.
  //       "(0.5*PI() - ACOS((posz + 0 - 0)/(SQRT(POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2))))) < 0.872664625997 AND "

  //       "(POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2)) >= 0 AND (POW((posx + 0 - 0),2) + POW((posy + 0 - 0),2) + POW((posz + 0 - 0),2)) < 5688333.71237" );
  }
*/
   }
}
