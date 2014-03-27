#include <libhpc/mpi/unit_test_main.hh>
#include "tao/base/soci_backend.hh"
#include "../fixtures/db_fixture.hh"

using namespace hpc;
using namespace hpc::test;
using namespace tao;

typedef lightcone_galaxy_iterator<backends::soci<real_type>> iterator_type;

test_case<db_fixture> ANON(
   "/base/lightcone_galaxy_iterator/begin_constructor",
   "Test the begin constructor works. There can be issues with "
   "the copying of batch objects; this is important.",
   []( db_fixture& db )
   {
      // // Create first iterator.
      // query<real_type> qry;
      // iterator_type src( db.lc, db.be, qry );
   }
   );
