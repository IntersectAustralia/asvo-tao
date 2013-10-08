#include <libhpc/mpi/unit_test_main.hh>
#include "tao/modules/sqldirect.hh"

using namespace hpc;
using namespace hpc::test;
using namespace tao;

typedef modules::sqldirect<backends::soci<real_type>> sqldirect_type;

test_case<> ANON(
   "/modules/sqldirect/default_constructor",
   "",
   []()
   {
      sqldirect_type lc;
      // TEST( lc.num_boxes() == 0 );
      // TEST( lc.output_fields().empty() == true );
   }
   );
