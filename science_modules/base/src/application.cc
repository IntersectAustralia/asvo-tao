#include "application.hh"

using namespace hpc;

namespace tao {

   unix::time_type tao_start_time;

   double
   runtime()
   {
      return unix::seconds( unix::timer() - tao::tao_start_time );
   }

   void
   setup_common_options( options::dictionary& dict )
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

      // Output options.
      dict.add_option( new options::string( "outputdir", "." ) );
      dict.add_option( new options::string( "logdir", "." ) );

      // Record filter.
      dict.add_option( new options::string( "filter-type", "" ), "workflow:record-filter" );
      dict.add_option( new options::string( "filter-min", "" ), "workflow:record-filter" );
      dict.add_option( new options::string( "filter-max", "" ), "workflow:record-filter" );
   }
}
