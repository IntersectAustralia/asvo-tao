#include <libhpc/unit_test/main_mpi.hh>
#include "tao/modules/lightcone.hh"
#include "../fixtures/xml_fixture.hh"

typedef tao::modules::lightcone<tao::backends::soci<tao::real_type>> lightcone_type;

TEST_CASE( "/tao/modules/lightcone/default_constructor" )
{
   // lightcone_type lc;
   // TEST( lc.num_boxes() == 0 );
   // TEST( lc.output_fields().empty() == true );
}

TEST_CASE( "/tao/modules/lightcone/initialise_lightcone" )
{
   // options::xml_dict dict = xml.make_lightcone_dict();
   // lightcone_type lc( "light-cone", dict.get_node( "/tao/workflow/light-cone" ).node() );
   // lc.set_backend( &xml.db.be );
   // lc.initialise( dict );
   // TEST( lc.geometry() == lightcone_type::CONE );
   // TEST( lc.tile_repetition_random() == false );
   // TEST( lc.random_seed() == 0.0 );
   // TEST( lc.base_lightcone().min_redshift() == 0.0 );
   // TEST( lc.base_lightcone().max_redshift() == 0.06 );
   // TEST( lc.base_lightcone().min_ra() == 0.0 );
   // TEST( lc.base_lightcone().max_ra() == to_radians( 10.0 ) );
   // TEST( lc.base_lightcone().min_dec() == 0.0 );
   // TEST( lc.base_lightcone().max_dec() == to_radians( 10.0 ) );
}

TEST_CASE( "/tao/modules/lightcone/initialise_box" )
{
   // options::xml_dict dict = xml.make_box_dict();
   // lightcone_type lc( "light-cone", dict.get_node( "/tao/workflow/light-cone" ).node() );
   // lc.set_backend( &xml.db.be );
   // lc.initialise( dict );
   // TEST( lc.geometry() == lightcone_type::BOX );
   // TEST( lc.random_seed() == 0 );
   // TEST( lc.box_size() == 10.0 );
   // TEST( lc.box_redshift() == 0.0 );
}

TEST_CASE( "/tao/modules/lightcone/iterate_cone" )
{
   // options::xml_dict dict = xml.make_lightcone_dict( "unique", 0, 0.0, 0.001, 0.0, 89.0, 0.0, 89.0 );
   //  lightcone_type lc( "light-cone", dict.get_node( "/tao/workflow/light-cone" ).node() );
   //  lc.set_backend( &xml.db.be );
   //  lc.initialise( dict );

   //  int ii = 1;
   //  while( !lc.complete() )
   //  {
   //     lc.process( ii );

   //     if( ii == 1 )
   //        TEST( lc.batch().size() == 1 );
   //     else
   //        TEST( lc.batch().size() == 0 );

   //     ++ii;
   //  }

   //  TEST( ii != 0, "Must have at least tried some tiles." );
}
