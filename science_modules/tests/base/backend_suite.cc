#include <libhpc/debug/unit_test_main.hh>
#include "tao/base/backend.hh"

using namespace hpc::test;

namespace {

   class dummy
      : public tao::backend
   {
   public:

      dummy( tao::simulation const* sim = nullptr )
         : tao::backend( sim )
      {
      }

      virtual
      tao::simulation const*
      load_simulation()
      {
         return nullptr;
      }
   };

   test_case<> ANON(
      "/tao/base/backend/constructor/default",
      "",
      []()
      {
         dummy be;
         TEST( be.simulation() == (void*)0 );
      }
      );

   test_case<> ANON(
      "/tao/base/backend/constructor/simulation",
      "",
      []()
      {
         tao::simulation sim;
         dummy be( &sim );
         TEST( be.simulation() == &sim );
      }
      );

   test_case<> ANON(
      "/tao/base/backend/set_simulation",
      "",
      []()
      {
         tao::simulation sim;
         dummy be;
         be.set_simulation( &sim );
         TEST( be.simulation() == &sim );
      }
      );

}
