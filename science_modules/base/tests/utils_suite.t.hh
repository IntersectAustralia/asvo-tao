#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/base/utils.hh"
#include "mpi_fixture.hh"

using namespace tao;
using namespace hpc;

///
/// Utilities test suite.
///
class utils_suite : public CxxTest::TestSuite
{
public:

   ///
   /// Test redshift to age calculation. Ned's cosmological calculator
   /// from online suggests with constants of H0=73, OmegaM=0.25 and
   /// OmegaV=0.75 we should get an age for redshift 3 of 2.211 Gyr.
   ///
   void test_redshift_to_age()
   {
      double age = redshift_to_age<double>( 3.0 );
      TS_ASSERT_DELTA( age, 2.211, 1e-3 )
   }
};
