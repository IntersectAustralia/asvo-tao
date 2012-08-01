#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
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
   void test_run()
   {
      lightcone lc;
      lc._snaps.resize( 2 );
      lc._snaps[0] = 1.0;
      lc._snaps[1] = 2.0;
      lc._setup_query_template();
      std::string query = lc._build_query( 0, 1, 0.0, 0.0, 0.0 );
   }

   ///
   ///
   ///
   void test_build_query()
   {
      lightcone lc;
      lc._snaps.resize( 2 );
      lc._snaps[0] = 1.0;
      lc._snaps[1] = 2.0;
      lc._setup_query_template();
      std::string query = lc._build_query( 0, 1, 0.0, 0.0, 0.0 );
   }

   ///
   ///
   ///
   void test_random_rotation_and_shifting()
   {
      lightcone lc;
      vector<std::string> ops;
      lc._random_rotation_and_shifting( ops );
   }

   void setUp()
   {
      CLEAR_STACK_TRACE();

      this->num_ranks = mpi::comm::world.size();
      this->my_rank = mpi::comm::world.rank();

      // Create the database file.
      filename = tmpnam( NULL );
      {
         std::ofstream file( filename, std::fstream::out | std::fstream::app );
      }

      // Open it using SOCI.
      soci::session sql( soci::sqlite3, filename );
      sql << ;
   }

   void tearDown()
   {
      remove( filename.c_str() );
   }

private:

   std::string filename;
   int num_ranks, my_rank;
};
