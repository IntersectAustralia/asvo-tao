#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>
#include <tao/tao.hh>
#include "application.hh"

using namespace hpc;

namespace tao {
   namespace rebin {

      application::application( int argc,
				char* argv[] )
	 : hpc::application( argc, argv )
      {
	 EXCEPT( argc >= 4, "Insufficient arguments." );
	 try
	 {
	    _tbl = boost::lexical_cast<std::string>( argv[1] );
	    _tree = boost::lexical_cast<long long>( argv[2] );
	    _lid = boost::lexical_cast<int>( argv[3] );
	 }
	 catch( ... )
	 {
	    EXCEPT( 0, "Invalid arguments." );
	 }

	 // Setup logging.
	 LOG_PUSH( new logging::stdout( logging::debug ) );
      }

      void
      application::operator()()
      {
	 // Pick a simulation.
	 tao::simulation* sim = &mini_millennium;

	 // Connect the backend.
	 backends::multidb<real_type> be;
	 {
#include "credentials.hh"
	    vector<backends::multidb<real_type>::server_type> servers( 2 );
	    servers[0].dbname = "millennium_mini_hdf5_test";
	    servers[0].user = username;
	    servers[0].passwd = password;
	    servers[0].host = string( "tao01.hpc.swin.edu.au" );
	    servers[0].port = 3306;
	    servers[1].dbname = "millennium_mini_hdf5_test";
	    servers[1].user = username;
	    servers[1].passwd = password;
	    servers[1].host = string( "tao02.hpc.swin.edu.au" );
	    servers[1].port = 3306;
	    be.connect( servers.begin(), servers.end() );
	    be.set_simulation( sim );
	 }

	 // Load the stellar population model.
	 tao::stellar_population ssp;
	 ssp.load( "data/stellar_populations/m05/ages.dat",
		   "data/stellar_populations/m05/wavelengths.dat",
		   "data/stellar_populations/m05/metallicities.dat",
		   "data/stellar_populations/m05/ssp.ssz" );

	 // Load the SFH.
	 tao::sfh<tao::real_type> sfh;
	 tao::age_line<real_type> snap_ages( be.session(), *sim );
	 sfh.set_snapshot_ages( &snap_ages );
	 sfh.set_bin_ages( &ssp.bin_ages() );
	 sfh.load_tree_data( be.session( _tbl ), _tbl, _tree, _lid );

	 // Rebin.
	 vector<real_type> age_masses( ssp.bin_ages().size() );
	 vector<real_type> age_bulge_masses( ssp.bin_ages().size() );
	 vector<real_type> age_metals( ssp.bin_ages().size() );
	 std::fill( age_masses.begin(), age_masses.end(), 0 );
	 std::fill( age_bulge_masses.begin(), age_bulge_masses.end(), 0 );
	 std::fill( age_metals.begin(), age_metals.end(), 0 );
	 sfh.rebin<real_type>( age_masses, age_bulge_masses, age_metals );

         // Dump output to file.
	 std::cout << "MASSES: " << age_masses << "\n";
	 std::cout << "METALS: " << age_metals << "\n";
      }

   }
}
