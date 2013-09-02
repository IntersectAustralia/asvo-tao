#include <libhpc/mpi/unit_test_main.hh>
#include "tao/modules/lightcone.hh"
#include "../fixtures/xml_fixture.hh"

using namespace hpc;
using namespace hpc::test;
using namespace tao;

typedef modules::lightcone<backends::soci<real_type>> lightcone_type;

test_case<> ANON(
   "/modules/lightcone/default_constructor",
   "",
   []()
   {
      lightcone_type lc;
      // TEST( lc.num_boxes() == 0 );
      // TEST( lc.output_fields().empty() == true );
   }
   );

test_case<xml_fixture> ANON(
   "/modules/lightcone/initialise_lightcone",
   "",
   []( xml_fixture& xml )
   {
      options::xml_dict dict = xml.make_lightcone_dict();
      lightcone_type lc( "light-cone", dict.get_node( "/tao/workflow/light-cone" ).node() );
      lc.initialise( dict, &xml.db.be );
      TEST( lc.geometry() == lightcone_type::CONE );
      TEST( lc.tile_repetition_random() == false );
      TEST( lc.random_seed() == 0.0 );
      TEST( lc.base_lightcone().min_redshift() == 0.0 );
      TEST( lc.base_lightcone().max_redshift() == 0.06 );
      TEST( lc.base_lightcone().min_ra() == 0.0 );
      TEST( lc.base_lightcone().max_ra() == to_radians( 10.0 ) );
      TEST( lc.base_lightcone().min_dec() == 0.0 );
      TEST( lc.base_lightcone().max_dec() == to_radians( 10.0 ) );
   }
   );

test_case<xml_fixture> ANON(
   "/modules/lightcone/initialise_box",
   "",
   []( xml_fixture& xml )
   {
      options::xml_dict dict = xml.make_box_dict();
      lightcone_type lc( "light-cone", dict.get_node( "/tao/workflow/light-cone" ).node() );
      lc.initialise( dict, &xml.db.be );
      TEST( lc.geometry() == lightcone_type::BOX );
      TEST( lc.random_seed() == 0 );
      TEST( lc.box_size() == 10.0 );
      TEST( lc.box_redshift() == 0.0 );
   }
   );

test_case<xml_fixture> ANON(
   "/modules/lightcone/iterate_cone",
   "",
   []( xml_fixture& xml )
   {
     options::xml_dict dict = xml.make_lightcone_dict( "unique", 0, 0.0, 0.001, 0.0, 89.0, 0.0, 89.0 );
      lightcone_type lc( "light-cone", dict.get_node( "/tao/workflow/light-cone" ).node() );
      lc.initialise( dict, &xml.db.be );

      int ii = 1;
      while( !lc.complete() )
      {
         lc.process( ii );

         if( ii == 1 )
            TEST( lc.batch().size() == 1 );
         else
            TEST( lc.batch().size() == 0 );

         ++ii;
      }

      TEST( ii != 0, "Must have at least tried some tiles." );
   }
   );
