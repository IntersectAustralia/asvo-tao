#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>
#include <tao/tao.hh>
#include "application.hh"

using namespace hpc;

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

	 // // Setup logging.
	 // LOG_PUSH( new logging::stdout( logging::debug ) );
      }

      void
      application::operator()()
      {
	 // Pick a simulation.
	 tao::simulation<tao::real_type>* sim = &mini_millennium;

	 // Connect the backend.
	 backends::multidb<real_type> be;
	 {
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
	 }

	 // Must first find the table and tree.
	 string table;
	 long long tree;
	 unsigned gal_id;
	 for( auto it = be.table_begin(); it != be.table_end(); ++it )
	 {
	    LOGD( "Trying table ", it->name(), ": " );
	    int size = 0;
	    be.session( it->name() ) << "SELECT COUNT(globaltreeid) FROM " + it->name() + " WHERE globalindex = :gid",
	       soci::into( size ), soci::use( _gid );
	    if( size )
	    {
	       LOGDLN( "yes!" );
	       be.session( it->name() ) << "SELECT globaltreeid, localgalaxyid FROM " + it->name() + " WHERE globalindex = :gid",
		  soci::into( tree ), soci::into( gal_id ), soci::use( _gid );
	       table = it->name();
	       break;
	    }
#ifndef NLOGDEBUG
	    else
	       LOGDLN( "nope." );
#endif
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
	 sfh.load_tree_data( be.session( table ), table, tree );

	 // Rebin.
	 vector<real_type> age_masses( ssp.bin_ages().size() );
	 vector<real_type> age_bulge_masses( ssp.bin_ages().size() );
	 vector<real_type> age_metals( ssp.bin_ages().size() );
	 std::fill( age_masses.begin(), age_masses.end(), 0 );
	 std::fill( age_bulge_masses.begin(), age_bulge_masses.end(), 0 );
	 std::fill( age_metals.begin(), age_metals.end(), 0 );
	 sfh.rebin<real_type>( be.session( table ), gal_id, age_masses, age_bulge_masses, age_metals );

         // Dump output to file.
         std::ofstream outf( boost::lexical_cast<std::string>( _gid ) + ".dat" );
         outf << "MASSES: " << age_masses << "\n";
         outf << "METALS: " << age_metals << "\n";
      }

   }
}
