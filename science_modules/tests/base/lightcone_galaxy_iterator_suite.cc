#include <libhpc/unit_test/main_mpi.hh>
#include "tao/base/soci_backend.hh"
#include "../fixtures/db_fixture.hh"

using tao::real_type;
using tao::lightcone_galaxy_iterator;

typedef lightcone_galaxy_iterator<tao::backends::soci<real_type>> iterator_type;

TEST_CASE( "/base/lightcone_galaxy_iterator/begin_constructor" )
{
   // // Create first iterator.
   // query<real_type> qry;
   // iterator_type src( db.lc, db.be, qry );
}
