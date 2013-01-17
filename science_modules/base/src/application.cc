#include "application.hh"

using namespace hpc;

namespace tao {

   void
   setup_common_options( options::dictionary& dict )
   {
      dict.add_option( new options::string( "type", "postgresql" ), "database" );
      dict.add_option( new options::string( "name" ), "database" );
      dict.add_option( new options::string( "host" ), "database" );
      dict.add_option( new options::string( "port" ), "database" );
      dict.add_option( new options::string( "user" ), "database" );
      dict.add_option( new options::string( "password" ), "database" );
      dict.add_option( new options::string( "treetableprefix", "tree_" ), "database" );
   }
}
