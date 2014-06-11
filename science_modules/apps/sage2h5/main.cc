#include <string>
#include <vector>
#include <libhpc/system/filesystem.hh>
#include <libhpc/mpi/application.hh>

class application
   : public hpc::mpi::application
{
public:

   application( int argc,
                char* argv[] )
      : hpc::mpi::application( argc, argv )
   {
      // Setup some options.
      options().add_options()
         ( "sage,s", hpc::po::value<hpc::fs::path>( &_sage ), "SAGE path" )
         ( "output,o", hpc::po::value<hpc::fs::path>( &_out ), "output file" );
         ( "verbose,v", hpc::po::value<bool>( &_verb )->default_value( false ), "verbosity" );
      positional_options().add( "sage", 1 );
      positional_options().add( "output", 1 );

      // Parse options.
      parse_options( argc, argv );

      // Setup logging.
      if( _verb )
         LOG_PUSH( new hpc::log::stdout( hpc::log::info ) );
   }

   void
   operator()()
   {
      hpc::mpi::managed<manager,worker> mgd;
      mgd.run();
   }

protected:

   hpc::fs::path _sage;
   hpc::fs::path _out;
   bool _verb;
};

#define HPC_APP_CLASS application
#include <libhpc/mpi/main.hh>
