#include <libhpc/unit_test/main.hh>
#include "tao/modules/sqldirect.hh"

typedef tao::modules::sqldirect<tao::backends::soci<tao::real_type>> sqldirect_type;

TEST_CASE( "/tao/modules/sqldirect/default_constructor" )
{
   sqldirect_type sd;
   // TEST( lc.num_boxes() == 0 );
   // TEST( lc.output_fields().empty() == true );
}
