#include <string>
#include <libhpc/unit_test/main.hh>
#include "tao/base/batch.hh"
#include "tao/base/types.hh"

using tao::real_type;
using tao::batch;

TEST_CASE( "/base/batch/set_fields" )
{
   batch<real_type> bat;
   bat.set_size( 1 );

   auto an_int = bat.set_scalar<int>( "an_int" );
   an_int[0] = 4;

   auto a_double = bat.set_scalar<double>( "a_double" );
   a_double[0] = 4.0;

   auto a_string = bat.set_scalar<std::string>( "a_string" );
   a_string[0] = "hello";

   auto& a_matrix = bat.set_vector<int>( "a_matrix", 1 );
   a_matrix( 0, 0 ) = 10;

   TEST( bat.scalar<int>( "an_int" )[0] == 4 );
   TEST( bat.scalar<double>( "a_double" )[0] == 4.0 );
   TEST( bat.scalar<std::string>( "a_string" )[0] == "hello" );
   TEST( bat.vector<int>( "a_matrix" )( 0, 0 ) == 10 );
}
