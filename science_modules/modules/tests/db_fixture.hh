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

         // Add meta table.
         sql << "CREATE TABLE meta (snap_table INTEGER, redshift DOUBLE PRECISION, box_size DOUBLE PRECISION)";

         // Add snapshot tables.
         sql << "CREATE TABLE snapshot_000 (x DOUBLE PRECISION, y DOUBLE PRECISION, z DOUBLE PRECISION, id INTEGER)";
         sql << "CREATE TABLE snapshot_001 (x DOUBLE PRECISION, y DOUBLE PRECISION, z DOUBLE PRECISION, id INTEGER)";
         sql << "CREATE TABLE snapshot_002 (x DOUBLE PRECISION, y DOUBLE PRECISION, z DOUBLE PRECISION, id INTEGER)";
         sql << "CREATE TABLE snapshot_003 (x DOUBLE PRECISION, y DOUBLE PRECISION, z DOUBLE PRECISION, id INTEGER)";
      }

      // Create the XML file by calling the lightcone options setup and filling in the
      // details, then dumping to file.
      lightcone lc;
      lc.setup_options( dict );
      dict.compile();
      dict["database_type"] = "sqlite";
      dict["database_name"] = db_filename;
      dict["box_type"] = "cone";
      dict["z_min"] = "0";
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
