#include "tao/base/application.hh"

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
	       "globalindex BIGINT, snapnum INTEGER, localgalaxyid INTEGER, globaltreeid BIGINT)";
	 }
      }

      // Create the XML file by calling the lightcone options setup and filling in the
      // details, then dumping to file.
      lightcone lc;
      setup_common_options( dict );
      lc.setup_options( dict, "light-cone" );
      dict.compile();
      dict["settings:database:type"] = "sqlite";
      dict["database"] = db_filename;
      dict["light-cone:H0"] = "0.73"; // Need this because I'm an idiot.
      dict["light-cone:query-type"] = "cone";
      dict["light-cone:redshift-min"] = "0";
      xml_filename = tmpnam( NULL );
      xml.write( xml_filename, dict );

      return true;
   }

   bool tearDownWorld()
   {
      remove( db_filename.c_str() );
      remove( xml_filename.c_str() );
      dict.clear();
      return true;
   }

   options::dictionary dict;
   options::xml xml;
   std::string db_filename, xml_filename;
};

static db_setup_fixture db_setup;
