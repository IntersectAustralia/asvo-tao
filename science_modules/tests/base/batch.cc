#include <libhpc/debug/unit_test_main.hh>
#include "tao/base/batch.hh"
#include "tao/base/types.hh"

using namespace hpc;
using namespace hpc::test;
using namespace tao;

test_case<> ANON(
   "/base/batch/set_fields",
   "",
   []()
   {
      batch<real_type> bat;
      bat.set_size( 1 );

      auto an_int = bat.set_scalar<int>( "an_int" );
      an_int[0] = 4;

      auto a_double = bat.set_scalar<double>( "a_double" );
      a_double[0] = 4.0;

      auto a_string = bat.set_scalar<string>( "a_string" );
      a_string[0] = "hello";

      auto& a_fibre = bat.set_vector<int>( "a_fibre", 1 );
      a_fibre( 0, 0 ) = 10;

      TEST( bat.scalar<int>( "an_int" )[0] == 4 );
      TEST( bat.scalar<double>( "a_double" )[0] == 4.0 );
      TEST( bat.scalar<string>( "a_string" )[0] == "hello" );
      TEST( bat.vector<int>( "a_fibre" )( 0, 0 ) == 10 );
   }
   );
