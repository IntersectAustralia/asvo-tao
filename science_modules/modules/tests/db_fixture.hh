#include "tao/base/globals.hh"
#include "tao/modules/lightcone.hh"
#include "tao/modules/sed.hh"

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
      ssp_filename = tmpnam( NULL );

      // Open it using SOCI, create tables.
      {
         // Open our sqlite connection.
         soci::session sql( soci::sqlite3, db_filename );

	 // Add a snapshot to redshift table.
         sql << "CREATE TABLE snap_redshift (snapnum INTEGER, redshift DOUBLE PRECISION)";

	 // Add a metadata table and insert a value.
         sql << "CREATE TABLE metadata (metakey CHARACTER VARYING, metavalue CHARACTER VARYING)";
	 sql << "INSERT INTO metadata VALUES('boxsize', '500')";

         // Add snapshot tables.
	 for( unsigned ii = 0; ii < 4; ++ii )
	 {
	    sql << "CREATE TABLE tree_" + to_string( ii + 1 ) +
               " (posx DOUBLE PRECISION, posy DOUBLE PRECISION, posz DOUBLE PRECISION, "
	       "globalindex BIGINT, snapnum INTEGER, localgalaxyid INTEGER, globaltreeid BIGINT, "
	       "descendant INTEGER, metalscoldgas DOUBLE PRECISION, metalsbulgemass DOUBLE PRECISION, "
	       "sfr DOUBLE PRECISION, sfrbulge DOUBLE PRECISION)";
	 }
      }

      // Write a sample SSP file, assuming num_times=4, num_spectra=2, num_metals=7.
      std::ofstream file( ssp_filename, std::ios::out );
      file << "4\n";
      file << "0.0 0.03 0.05 0.5\n";
      unsigned val = 0;
      for( unsigned ii = 0; ii < 4; ++ii )
      {
         for( unsigned jj = 0; jj < 2; ++jj )
         {
            for( unsigned kk = 0; kk < 7; ++kk )
               file << to_string( val++ ) << " ";
            file << "\n";
         }
      }

      // Create the XML file by calling the lightcone options setup and filling in the
      // details, then dumping to file.
      lightcone lc;
      sed sed;

      dict["settings:database:type"] = "sqlite";
      dict["database"] = db_filename;
      dict["workflow:light-cone:H0"] = "0.73"; // Need this because I'm an idiot.
      dict["workflow:light-cone:geometry"] = "cone";
      dict["workflow:light-cone:redshift-min"] = "0";
      dict["workflow:sed:single-stellar-population-model"] = ssp_filename;
      dict["workflow:sed:num-spectra"] = "2";
      dict["workflow:sed:num-metals"] = "7";
      xml_filename = tmpnam( NULL );
      xml.write( xml_filename, dict );

      return true;
   }

   bool tearDownWorld()
   {
      remove( db_filename.c_str() );
      remove( xml_filename.c_str() );
      remove( ssp_filename.c_str() );
      dict.clear();
      return true;
   }

   options::dictionary dict;
   options::xml xml;
   std::string db_filename, xml_filename, ssp_filename;
};

static db_setup_fixture db_setup;
