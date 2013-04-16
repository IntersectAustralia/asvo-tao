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

   void setup_common_options( options::dictionary& dict )
   {
	 // Create "dbcfg" dictionary.
	 dict.add_option( new options::string( "type", "postgresql" ), "settings:database" );
	 dict.add_option( new options::string( "host" ), "settings:database" );
	 dict.add_option( new options::string( "port" ), "settings:database" );
	 dict.add_option( new options::string( "user" ), "settings:database" );
	 dict.add_option( new options::string( "password" ), "settings:database" );
	 dict.add_option( new options::string( "treetableprefix", "tree_" ), "settings:database" );
	 dict.add_option( new options::string( "acceleration", "none" ), "settings:database" );

	 // Add database name.
	 dict.add_option( new options::string( "database" ) );

	 // Output options and subjobindex
	 dict.add_option( new options::string( "outputdir", "." ) );
	 dict.add_option( new options::string( "logdir", "." ) );
	 dict.add_option( new options::string( "subjobindex" ) );

	 // Record filter.
	 dict.add_option( new options::string( "filter-type", "" ), "workflow:record-filter" );
	 dict.add_option( new options::string( "filter-min", "" ), "workflow:record-filter" );
	 dict.add_option( new options::string( "filter-max", "" ), "workflow:record-filter" );
   }

  void lightconesetup_options( options::dictionary& dict,optional<const string&> prefix )
  {
	 dict.add_option( new options::string( "geometry", "light-cone" ), prefix );
	 dict.add_option( new options::string( "box-repetition", "unique" ), prefix );
	 dict.add_option( new options::real( "redshift-max" ), prefix );
	 dict.add_option( new options::real( "redshift-min" ), prefix );
	 dict.add_option( new options::real( "redshift" ), prefix );
	 dict.add_option( new options::real( "query-box-size" ), prefix );
	 dict.add_option( new options::real( "ra-min", 0.0 ), prefix );
	 dict.add_option( new options::real( "ra-max", 90.0 ), prefix );
	 dict.add_option( new options::real( "dec-min", 0.0 ), prefix );
	 dict.add_option( new options::real( "dec-max", 90.0 ), prefix );
	 dict.add_option( new options::real( "h0", 73.0 ), prefix );
	 dict.add_option( new options::list<options::string>( "output-fields" ), prefix );
	 dict.add_option( new options::integer( "rng-seed" ), prefix );
	 dict.add_option( new options::string( "decomposition-method", "tables" ), prefix );

	 // Setup table names.
	 dict.add_option( new options::string( "snapshot-redshift-table", "snap_redshift" ), prefix );

	 // Setup the field mappings we might need to use.
	 dict.add_option( new options::string( "pos_x", "posx" ), prefix );
	 dict.add_option( new options::string( "pos_y", "posy" ), prefix );
	 dict.add_option( new options::string( "pos_z", "posz" ), prefix );
	 dict.add_option( new options::string( "global_id", "globalindex" ), prefix );
	 dict.add_option( new options::string( "local_id", "localgalaxyid" ), prefix );
	 dict.add_option( new options::string( "tree_id", "globaltreeid" ), prefix );
	 dict.add_option( new options::string( "snapshot", "snapnum" ), prefix );
  }
  void sedsetup_options( options::dictionary& dict, optional<const string&> prefix )
  {
	 dict.add_option( new options::string( "single-stellar-population-model" ), prefix );
	 dict.add_option( new options::integer( "num-spectra", 1221 ), prefix );
	 dict.add_option( new options::integer( "num-metals", 7 ), prefix );
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
      setup_common_options(dict);
      lightconesetup_options(dict,string( "workflow:light-cone" ) );
      sedsetup_options(dict,string( "workflow:sed" ) );
      dict.compile();

      dict["settings:database:type"] = "sqlite";
      dict["database"] = db_filename;
      dict["workflow:light-cone:H0"] = "0.73"; // Need this because I'm an idiot.
      dict["workflow:light-cone:geometry"] = "cone";
      dict["workflow:light-cone:redshift-min"] = "0";
      dict["workflow:sed:single-stellar-population-model"] = ssp_filename;
      dict["workflow:sed:num-spectra"] = "2";
      dict["workflow:sed:num-metals"] = "7";
      dict["workflow:light-cone:output-fields"]="pos_x";
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
