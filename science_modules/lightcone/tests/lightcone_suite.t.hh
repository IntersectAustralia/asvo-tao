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
      db_filename = tmpnam( NULL );
      {
         std::ofstream file( db_filename, std::fstream::out | std::fstream::app );
      }

      // Open it using SOCI, create a table.
      try
      {
         // Open our sqlite connection.
         soci::session sql( soci::sqlite3, db_filename );

         // Add tables.
         sql << "create table snapshot_000 (Pos1 double precision, Pos2 double precision, Pos3 double precision)";
         sql << "create table snapshot_001 (Pos1 double precision, Pos2 double precision, Pos3 double precision)";
         sql << "create table snapshot_002 (Pos1 double precision, Pos2 double precision, Pos3 double precision)";
         sql << "create table snapshot_003 (Pos1 double precision, Pos2 double precision, Pos3 double precision)";

         // We'll be using a box side of 100, so place key halos in there for testing.
         sql << "insert into snapshot_000 values (1, 1, 1)";
         sql << "insert into snapshot_001 values (2, 2, 2)";
         sql << "insert into snapshot_002 values (3, 3, 3)";
         sql << "insert into snapshot_003 values (4, 4, 4)";
      }
      catch( const std::exception& ex )
      {
         std::cout << "\n" << ex.what() << "\n";
         exit( 1 );
      }

      // Create the XML file by calling the lightcone options setup and filling in the
      // details, then dumping to file.
      options::dictionary dict;
      lightcone lc;
      lc.setup_options( dict );
      dict.compile();
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_filename;
      dict["box_type"] = "cone";
      dict["box_side"] = "100";
      dict["snapshots"] = "10,5,2,1";
      dict["z_min"] = "1";
      xml_filename = tmpnam( NULL );
      options::xml xml;
      xml.write( xml_filename, dict );

      return true;
   }

   bool tearDownWorld()
   {
      remove( db_filename.c_str() );
      remove( xml_filename.c_str() );
      return true;
   }

   std::string db_filename, xml_filename;
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
      lightcone lc;
      setup_lightcone( lc );
      lc.run();
   }

   // ///
   // ///
   // ///
   // void test_build_query()
   // {
   //    lightcone lc;
   //    lc._snaps.resize( 2 );
   //    lc._snaps[0] = 1.0;
   //    lc._snaps[1] = 2.0;
   //    lc._setup_query_template();
   //    std::string query;
   //    lc._build_query( 0, 1, 0.0, 0.0, 0.0, query );
   // }

   // ///
   // ///
   // ///
   // void test_random_rotation_and_shifting()
   // {
   //    lightcone lc;
   //    vector<std::string> ops;
   //    lc._random_rotation_and_shifting( ops );
   // }

   void setup_lightcone( lightcone& lc )
   {
      options::dictionary dict;
      lc.setup_options( dict );
      dict.compile();
      options::xml xml;
      xml.read( db_setup.xml_filename, dict );
      lc.initialise( dict );
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
