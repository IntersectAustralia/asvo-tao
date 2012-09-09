#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/modules/lightcone.hh"
#include "tao/modules/sed.hh"
#include "tao/modules/filter.hh"

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
      // Setup filenames.
      db_filename = tmpnam( NULL );
      xml_filename = tmpnam( NULL );
      ssp_filename = tmpnam( NULL );
      waves_filename = tmpnam( NULL );

      // Open the database.
      soci::session sql( soci::sqlite3, db_filename );

      // Write a simple set of galaxies.
      sql << "create table snapshot_000 (Pos1 double precision, Pos2 double precision, Pos3 double precision, id integer, "
         "disk_sfr double precision, bulge_sfr double precision)";
      sql << "create table snapshot_001 (Pos1 double precision, Pos2 double precision, Pos3 double precision, id integer, "
         "disk_sfr double precision, bulge_sfr double precision)";
      sql << "insert into snapshot_000 values (1, 0.001, 0.001, 0, 1, 2)";
      sql << "insert into snapshot_000 values (0.866, 0.5, 0.001, 1, 3, 4)";
      sql << "insert into snapshot_000 values (0.5, 0.866, 0.001, 2, 5, 6)";
      sql << "insert into snapshot_001 values (1, 0.001, 0.001, 0, 1, 2)";
      sql << "insert into snapshot_001 values (0.866, 0.5, 0.001, 1, 3, 4)";
      sql << "insert into snapshot_001 values (0.5, 0.866, 0.001, 2, 5, 6)";

      // Write a sample set of star formation histories/metallicities.
      sql << "create table disk_star_formation (galaxy_id integer, history double precision, "
         "metal double precision, age double precision)";
      sql << "create table bulge_star_formation (galaxy_id integer, history double precision, "
         "metal double precision, age double precision)";
      sql << "insert into disk_star_formation values (0, 1, 0.00, 3)";
      sql << "insert into disk_star_formation values (0, 2, 0.01, 2)";
      sql << "insert into disk_star_formation values (0, 3, 0.02, 1)";
      sql << "insert into disk_star_formation values (1, 4, 0.00, 3)";
      sql << "insert into disk_star_formation values (1, 5, 0.01, 2)";
      sql << "insert into disk_star_formation values (1, 6, 0.02, 1)";
      sql << "insert into disk_star_formation values (2, 7, 0.00, 3)";
      sql << "insert into disk_star_formation values (2, 8, 0.01, 2)";
      sql << "insert into disk_star_formation values (2, 9, 0.02, 1)";
      sql << "insert into bulge_star_formation values (0, 10, 0.00, 3)";
      sql << "insert into bulge_star_formation values (0, 11, 0.01, 2)";
      sql << "insert into bulge_star_formation values (0, 12, 0.02, 1)";
      sql << "insert into bulge_star_formation values (1, 13, 0.00, 3)";
      sql << "insert into bulge_star_formation values (1, 14, 0.01, 2)";
      sql << "insert into bulge_star_formation values (1, 15, 0.02, 1)";
      sql << "insert into bulge_star_formation values (2, 16, 0.00, 3)";
      sql << "insert into bulge_star_formation values (2, 17, 0.01, 2)";
      sql << "insert into bulge_star_formation values (2, 18, 0.02, 1)";

      // Write a sample SSP file, assuming num_times=3, num_spectra=2, num_metals=7.
      {
         std::ofstream file( ssp_filename, std::ios::out );
         unsigned val = 0;
         for( unsigned ii = 0; ii < 3; ++ii )
         {
            for( unsigned jj = 0; jj < 2; ++jj )
            {
               for( unsigned kk = 0; kk < 7; ++kk )
                  file << to_string( val++ ) << " ";
               file << "\n";
            }
         }
      }

      // Write a dummy wavelengths file.
      {
         std::ofstream file( waves_filename, std::ios::out );
         unsigned val = 1;
         for( unsigned ii = 0; ii < 2; ++ii )
            file << to_string( 1000*val++ ) << " ";
         file << "\n";
      }

      // Create an appropriate XML file for both the lightcone and
      // the SED modules.
      lightcone lc;
      tao::sed sed;
      tao::filter filter;
      options::dictionary dict;
      lc.setup_options( dict, "lightcone" );
      sed.setup_options( dict, "sed" );
      filter.setup_options( dict, "filter" );
      dict.compile();

      dict["lightcone-database_type"] = "sqlite";
      dict["lightcone-database_name"] = db_filename;
      dict["lightcone-box_type"] = "cone";
      dict["lightcone-box_side"] = "100";
      dict["lightcone-snapshots"] = "0.01,0";

      dict["sed-database_type"] = "sqlite";
      dict["sed-database_name"] = db_filename;
      dict["sed-ssp_filename"] = ssp_filename;
      dict["sed-num_times"] = "3";
      dict["sed-num_spectra"] = "2";
      dict["sed-num_metals"] = "7";

      dict["filter-filter_filenames"] = "bbv.dat,bub.dat";
      dict["filter-vega_filename"] = "A0V_KUR_BB.SED";

      xml_filename = tmpnam( NULL );
      xml.write( xml_filename, dict );

      return true;
   }

   bool tearDownWorld()
   {
      remove( db_filename.c_str() );
      remove( xml_filename.c_str() );
      remove( ssp_filename.c_str() );
      remove( waves_filename.c_str() );
      return true;
   }

   options::xml xml;
   std::string db_filename, xml_filename, ssp_filename, waves_filename;
};

static db_setup_fixture db_setup;

///
/// SED class test suite.
///
class filter_suite : public CxxTest::TestSuite
{
public:

   ///
   ///
   ///
   void test_integral()
   {
      tao::lightcone lc;
      tao::sed sed;
      tao::filter filter;
      setup_filter( lc, sed, filter );

      fibre<double> one_knots( 2, 3 ), two_knots( 2, 5 );
      one_knots(0,0) = 0.0; one_knots(0,1) = 0.0;
      one_knots(1,0) = 1.0; one_knots(1,1) = 1.0;
      one_knots(2,0) = 2.0; one_knots(2,1) = 0.0;
      two_knots(0,0) = -1.0; two_knots(0,1) = 2.0;
      two_knots(1,0) = 0.0; two_knots(1,1) = 2.0;
      two_knots(2,0) = 0.9; two_knots(2,1) = 2.0;
      two_knots(3,0) = 1.9; two_knots(3,1) = 2.0;
      two_knots(4,0) = 3.0; two_knots(4,1) = 2.0;
      numerics::spline<double> one, two;
      one.set_knots( one_knots );
      two.set_knots( two_knots );

      TS_ASSERT( num::approx<double>( filter._integrate( one, two ), 2.5, 1e-8 ) );
   }

   ///
   ///
   ///
   // void test_process_vega()
   // {
   //    tao::lightcone lc;
   //    tao::sed sed;
   //    tao::filter filter;
   //    setup_filter( lc, sed, filter );
   // }

   ///
   ///
   ///
   void test_filters()
   {
      tao::lightcone lc;
      tao::sed sed;
      tao::filter filter;
      setup_filter( lc, sed, filter );

      unsigned galaxy = 0;
      for( lc.begin(); !lc.done(); ++lc, ++galaxy )
      {
         sed.process_galaxy( *lc );
         filter.process_galaxy( *lc, sed.total_spectra() );
      }
   }

   void setup_filter( tao::lightcone& lc, tao::sed& sed, tao::filter& filter )
   {
      // Setup the dictionary.
      options::dictionary dict;
      lc.setup_options( dict, "lightcone" );
      sed.setup_options( dict, "sed" );
      filter.setup_options( dict, "filter" );
      dict.compile();
      db_setup.xml.read( db_setup.xml_filename, dict );

      // Initialise modules.
      lc.initialise( dict, "lightcone" );
      sed.initialise( dict, "sed" );
      filter.initialise( dict, "filter" );

      // Switch off random rotation and shifting.
      lc._use_random = false;
   }

   void setUp()
   {
      CLEAR_STACK_TRACE();

      num_ranks = mpi::comm::world.size();
      my_rank = mpi::comm::world.rank();
   }

   void tearDown()
   {
   }

private:

   int num_ranks, my_rank;
};
