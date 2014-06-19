#include <libhpc/unit_test/main_mpi.hh>
#include "tao/modules/lightcone.hh"
#include "../fixtures/xml_fixture.hh"

typedef tao::modules::lightcone<tao::backends::soci<tao::real_type>> lightcone_type;

SUITE_FIXTURE( xml_fixture ) xml;

TEST_CASE( "/tao/modules/lightcone/constructor/default" )
{
   lightcone_type lc;
   TEST( lc.backend() == (void*)0 );
}

TEST_CASE( "/tao/modules/lightcone/initialise/simulation" )
{
   lightcone_type lc;
   lc.set_backend( &xml->db.be );
   lc.initialise( xml->make_lightcone_dict() );
   TEST( lc.simulation() != (void*)0 );
}
