#include <libhpc/debug/unit_test_main.hh>
#include "tao/base/utils.hh"

using namespace hpc;
using namespace hpc::test;
using namespace tao;

test_case<> ANON(
   "/base/utils/redshift_to_age",
   "Test redshift to age calculation. Ned's cosmological calculator "
   "from online suggests with constants of H0=73, OmegaM=0.25 and "
   "OmegaV=0.75 we should get an age for redshift 3 of 2.211 Gyr.",
   []()
   {
     double age = redshift_to_age<double>( 3.0, 73.0, 0.25, 0.75 );
      DELTA( age, 2.211, 1e-3 );
   }
   );
