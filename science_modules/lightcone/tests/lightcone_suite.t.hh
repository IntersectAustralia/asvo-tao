#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include <libhpc/logging/logging.hh>
#include "tao/lightcone/lightcone.hh"

using namespace hpc;
using namespace tao;

#include "mpi_fixture.hh"

///
/// Database preparation fixture.
///
class db_setup_fixture : public CxxTest::GlobalFixture
{
public:

   bool setUp()
   {
      return true;
   }

   bool tearDown()
   {
      return true;
   }

   bool setUpWorld()
   {
      // Create the database file.
      filename = tmpnam( NULL );
      {
         std::ofstream file( filename, std::fstream::out | std::fstream::app );
      }

      // Open it using SOCI, create a table.
      try
      {
         soci::session sql( soci::sqlite3, filename );
         sql << "create table halo (pos_x double precision, pos_y double precision, pos_z double precision, redshift)";
         sql << "insert into halo values (1.0, 1.0, 1.0, 0.01)";
      }
      catch( const std::exception& ex )
      {
         std::cout << "\n" << ex.what() << "\n";
         exit( 1 );
      }

      return true;
   }

   bool tearDownWorld()
   {
      remove( filename.c_str() );
      return true;
   }

   std::string filename;
};

static db_setup_fixture db_setup;

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
      LOG_PUSH( new logging::file( "log" ) );

// #ifndef NDEBUG
//       lightcone lc;
//       lc._snaps.resize( 2 );
//       lc._snaps[0] = 1.0;
//       lc._snaps[1] = 2.0;
//       lc._sqlite_filename = tmpnam( NULL );
//       lc.initialise();
//       lc.run();
//       remove( lc._sqlite_filename.c_str() );
// #endif

      LOG_POP();
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
      std::string query;
      lc._build_query( 0, 1, 0.0, 0.0, 0.0, query );
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
   }

   void tearDown()
   {
   }

private:

   int num_ranks, my_rank;
};
