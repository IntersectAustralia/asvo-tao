#include <libhpc/libhpc.hh>
#include "application.hh"

namespace tao {
   namespace rebin {

      application::application( int argc,
				char* argv[] )
      {
	 EXCEPT( argc >= 2, "Insufficient arguments. Must supply a galaxy global index." );
	 try
	 {
	    _gid = boost::lexical_cast<long long>( argv[1] );
	 }
	 catch( ... )
	 {
	    EXCEPT( 0, "Invalid galaxy global index." );
	 }
      }

      void
      application::operator()()
      {
	 // Pick a simulation.
	 tao::simulation<tao::real_type>* sim = &mini_millennium;

	 // Connect the backend.
#include "credentials.hh"
	 vector<backends::multidb<real_type>::server_type> servers( 2 );
	 servers[0].dbname = "millennium_mini_hdf5_dist";
	 servers[0].user = username;
	 servers[0].passwd = password;
	 servers[0].host = string( "tao01.hpc.swin.edu.au" );
	 servers[0].port = 3306;
	 servers[1].dbname = "millennium_mini_hdf5_dist";
	 servers[1].user = username;
	 servers[1].passwd = password;
	 servers[1].host = string( "tao02.hpc.swin.edu.au" );
	 servers[1].port = 3306;
	 be.connect( servers.begin(), servers.end() );
	 be.set_simulation( sim );

	 // Must first find the table and tree first.
	 string table;
	 long long tree;
	 for( auto it = be.table_begin(); it != be.table_end(); ++it )
	 {
	    int size = 0;
	    be.session( it->name() ) << "SELECT COUNT(globaltreeid) FROM " + it->name() + " WHERE globalindex = :gid",
	       soci::into( size ), soci::use( *val );
	    if( size )
	    {
	       be.session( it->name() ) << "SELECT globaltreeid, localgalaxyid FROM " + it->name() + " WHERE globalindex = :gid",
		  soci::into( tree ), soci::into( cur_gal_id ), soci::use( *val );
	       table = it->name();
	       break;
	    }
	 }

	 // Load the stellar population model.
	 tao::stellar_population ssp;
	 ssp.load( "ages.dat", "wavelengths.dat", "metallicities.dat", "ssp.dat" );

	 // Load the SFH.
	 tao::sfh<tao::real_type> sfh;
	 sfh.load_tree_data( be.session( table ), table, tree );

	 // Rebin.
	 std::fill( age_masses.begin(), age_masses.end(), 0 );
	 std::fill( age_bulge_masses.begin(), age_bulge_masses.end(), 0 );
	 std::fill( age_metals.begin(), age_metals.end(), 0 );
	 sfh.rebin<real_type>( be.session( table ), gal_id, age_masses, age_bulge_masses, age_metals );

         // Dump output.
         std::cout << "MASSES: " << age_masses << "\n";
         std::cout << "METALS: " << age_metals << "\n";
      }

   }
}
