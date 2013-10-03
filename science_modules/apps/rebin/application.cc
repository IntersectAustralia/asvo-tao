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
      }

   }
}
