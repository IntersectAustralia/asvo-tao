#include "application.hh"

using namespace hpc;

namespace tao {

   void
   setup_common_options( options::dictionary& dict )
   {
      dict.add_option( new options::string( "database-type", "postgresql" ) );
      dict.add_option( new options::string( "database-name", "millennium_full_mpi" ) );
      dict.add_option( new options::string( "database-host", "tao02.hpc.swin.edu.au" ) );
      dict.add_option( new options::string( "database-port", "3306" ) );
      dict.add_option( new options::string( "database-user", string() ) );
      dict.add_option( new options::string( "database-pass", string() ) );
   }
}
