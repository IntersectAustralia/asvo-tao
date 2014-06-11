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
      // Prepare the event handler.
      hpc::mpi::async async;
      async.add_event_handler( &_chkr );
      async.add_event_handler( &_idxr );

      // Launch the event handler.
      if( !async.run() )
      {
         // Run a worker.
         worker();
      }
   }

   void
   worker()
   {
      // Use the filename as the finished flag.
      std::string sage_fn;

      do
      {
         // Get the next chunk to work on.
         std::array<size_t,2> chunk;
         _comm->send( 0, 0, _chkr.tag() );
         _comm->recv( sage_fn, 0, _chkr.tag() );
         _comm->recv( chunk, 0, _chkr.tag() );

         // Process this chunk.
         process( sage_fn, chunk );
      }
      while( !sage_fn.empty() );

      // Flag the event handler we're finished.
      _comm->send( 0, 0, 0 );
   }

   void
   process( std::string const& sage_fn,
            std::array<size_t,2> const& chunk )
   {
      
   }

protected:

   file_chunker _chkr;
   hpc::mpi::indexer _idxr;
   hpc::fs::path _sage;
   hpc::fs::path _out;
   bool _verb;
};

#define HPC_APP_CLASS application
#include <libhpc/mpi/main.hh>
