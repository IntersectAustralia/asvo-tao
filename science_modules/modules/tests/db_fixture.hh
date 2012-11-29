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

	 // Add a summary table and insert a value.
         sql << "CREATE TABLE summary (domain_size DOUBLE PRECISION)";
	 sql << "INSERT INTO summary VALUES(1000)";

         // Add snapshot tables.
         sql << "CREATE TABLE tree_1 (posx DOUBLE PRECISION, posy DOUBLE PRECISION, posz DOUBLE PRECISION, "
	   "globalindex INTEGER, snapnum INTEGER)";
         sql << "CREATE TABLE tree_2 (posx DOUBLE PRECISION, posy DOUBLE PRECISION, posz DOUBLE PRECISION, "
	   "globalindex INTEGER, snapnum INTEGER)";
         sql << "CREATE TABLE tree_3 (posx DOUBLE PRECISION, posy DOUBLE PRECISION, posz DOUBLE PRECISION, "
	   "globalindex INTEGER, snapnum INTEGER)";
         sql << "CREATE TABLE tree_4 (posx DOUBLE PRECISION, posy DOUBLE PRECISION, posz DOUBLE PRECISION, "
	   "globalindex INTEGER, snapnum INTEGER)";
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
