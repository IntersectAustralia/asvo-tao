#include <libhpc/libhpc.hh>
#include <tao/tao.hh>
#include "application.hh"

using namespace hpc;

namespace tao {
   namespace ssp_restrict {

      application::application( int argc,
				char* argv[] )
      {
	 EXCEPT( argc >= 2, "Insufficient arguments." );
	 _inp_dir = std::string( argv[1] );
	 _out_dir = std::string( argv[2] );
	 for( unsigned ii = 3; ii < argc; ++ii )
	    _ssps.emplace_back( argv[ii] );

	 // Setup logging.
	 LOG_CONSOLE();
	 // LOG_PUSH( new logging::stdout( logging::debug ) );
      }

      void
      application::operator()()
      {
	 LOGILN( "Source directory: ", _inp_dir );
	 LOGILN( "Destination directory: ", _out_dir );
	 LOGILN( "SSPs: ", _ssps );

	 // Process each SSP.
	 for( auto const& ssp_name : _ssps )
	 {
	    LOGBLOCKI( "Processing: ", ssp_name );

	    // Load the SSP.
	    tao::stellar_population ssp;
	    ssp.load(
	       _inp_dir/"ages.dat",
	       _inp_dir/"wavelengths.dat",
	       _inp_dir/"metallicities.dat",
	       _inp_dir/ssp_name
	       );

	    // Restrict.
	    ssp.restrict();

	    // Dump.
	    ssp.save(
	       _out_dir/"ages.dat",
	       _out_dir/"wavelengths.dat",
	       _out_dir/"metallicities.dat",
	       _out_dir/ssp_name
	       );
	 }
      }

   }
}
