#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/lightcone/lightcone.hh"

using namespace hpc;
using namespace tao;

#include "mpi_fixture.hh"

///
/// Lightcone class test suite.
///
class lightcone_suite : public CxxTest::TestSuite
{
public:

   ///
   /// Test default constructor.
   ///
   void test_ctor()
   {
      lightcone lc;
   }

   ///
   ///
   ///
   void test_build_query()
   {
   }

   ///
   ///
   ///
   void test_random_rotation_and_shifting()
   {
      lightcone lc;
   }

   void setUp()
   {
      CLEAR_STACK_TRACE();

      this->num_ranks = mpi::comm::world.size();
      this->my_rank = mpi::comm::world.rank();
   }

private:

   int num_ranks, my_rank;
};
