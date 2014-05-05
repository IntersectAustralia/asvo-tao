#include <libhpc/unit_test/main.hh>
#include "tao/base/utils.hh"

TEST_CASE( "/tao/base/utils/redshift_to_age" )
{
   // Test redshift to age calculation. Ned's cosmological calculator
   // from online suggests with constants of H0=73, OmegaM=0.25 and
   // OmegaV=0.75 we should get an age for redshift 3 of 2.211 Gyr.
   double age = tao::redshift_to_age<double>( 3.0, 73.0, 0.25, 0.75 );
   DELTA( age, 2.211, 1e-3 );
}
