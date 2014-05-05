#include <libhpc/unit_test/main.hh>
#include "tao/base/backend.hh"

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

TEST_CASE( "/tao/base/backend/constructor/default" )
{
   dummy be;
   TEST( be.simulation() == (void*)0 );
}

TEST_CASE( "/tao/base/backend/constructor/simulation" )
{
   tao::simulation sim;
   dummy be( &sim );
   TEST( be.simulation() == &sim );
}

TEST_CASE( "/tao/base/backend/set_simulation" )
{
   tao::simulation sim;
   dummy be;
   be.set_simulation( &sim );
   TEST( be.simulation() == &sim );
}
