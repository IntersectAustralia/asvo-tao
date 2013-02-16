#include "application.hh"
#include "tao/base/base.hh"
#include "tao/modules/modules.hh"

using namespace hpc;

namespace tao {

   application::application()
   {
      tao_start_time = unix::timer();
   }

   application::application( int argc,
                             char* argv[] )
   {
      tao_start_time = unix::timer();
      arguments( argc, argv );
   }

   void
   application::arguments( int argc,
                           char* argv[] )
   {
      // Check for insufficient arguments.
      if( argc != 3 || !argv[1] || !argv[2] )
      {
         std::cout << "Insufficient arguments.\n";
         std::cout << "Please supply a path to an input XML and a database\n";
         std::cout << "configuration XML.\n";
         exit( 1 );
      }

      // Check that the files exists.
      {
         std::ifstream file( argv[1] );
         if( !file )
         {
            std::cout << "Could not open XML file.\n";
            exit( 1 );
         }
      }
      {
         std::ifstream file( argv[2] );
         if( !file )
         {
            std::cout << "Could not open DB config file.\n";
            exit( 1 );
         }
      }

      // Cache the filename.
      _xml_file = argv[1];
      _dbcfg_file = argv[2];
   }

   void
   application::run()
   {
      LOG_ENTER();

      // Load all the modules first up.
      _load_modules();
      _connect_parents();

      // Read the options dictionary.
      options::dictionary dict;
      _setup_common_options( dict );
      for( auto module : tao::factory )
         module->setup_options( dict, string( "workflow:" ) + module->name() );
      dict.compile();
      _read_xml( dict );

      // Prepare the logging.
      _setup_log( dict.get<string>( "logdir" ) + "/tao.log" );

      // Initialise all the modules.
      for( auto module : tao::factory )
         module->initialise( dict, string( "workflow:" ) + module->name() );

      // Mark the beginning of the run.
      LOGILN( runtime(), ",start" );

      // Run.
      _execute();

      // Mark the conclusion of the run.
      LOGILN( runtime(), ",end,successful" );

      LOG_EXIT();
   }

   ///
   /// Load modules.
   ///
   void
   application::_load_modules()
   {
      LOG_ENTER();

      // Register all the available science modules.
      tao::register_modules();

      // Read the dictionary once to get at the modules.
      options::dictionary dict;
      dict.add_option( new options::list<options::string>( "modules" ) );
      dict.compile();
      _read_xml( dict );

      // Get the list and add them all.
      list<string> modules = dict.get_list<string>( "modules" );
      for( const auto& name : modules )
         tao::factory.create_module( name );

      LOG_EXIT();
   }

   ///
   /// Connect parents.
   ///
   void
   application::_connect_parents()
   {
      LOG_ENTER();

      // Compile a dictionary for parents and read them in.
      options::dictionary dict;
      for( auto module : tao::factory )
         dict.add_option( new options::list<options::string>( "parents" ), string( "workflow:" ) + module->name() );
      dict.compile();
      _read_xml( dict );

      // Connect 'em all up!
      for( auto module : tao::factory )
      {
         list<string> parents = dict.get_list<string>( string( "workflow:" ) + module->name() + string( ":parents" ) );
         for( auto& name : parents )
            module->add_parent( *tao::factory[name] );
      }

      LOG_EXIT();
   }

   ///
   /// Insert common options.
   ///
   void
   application::_setup_common_options( options::dictionary& dict )
   {
      setup_common_options( dict );
   }

   ///
   /// Read the XML file into a dictionary.
   ///
   void
   application::_read_xml( options::dictionary& dict ) const
   {
      options::xml xml;
      xml.read( _xml_file, dict, "/tao/*" );
      xml.read( _dbcfg_file, dict );
   }

   ///
   /// Prepare log file.
   ///
   void
   application::_setup_log( const string& filename )
   {
      LOG_ENTER();

      if( mpi::comm::world.rank() == 0 )
      {
         LOGDLN( "Setting logging file to: ", filename );
         LOG_PUSH( new logging::file( filename, logging::info ) );
      }

      LOG_EXIT();
   }

   ///
   /// Execute the application.
   ///
   void
   application::_execute()
   {
      LOG_ENTER();

      // Keep looping over modules until all report being complete.
      bool complete;
      unsigned long long it = 1;
      do
      {
         LOGDLN( "Beginning iteration: ", it, hpc::setindent( 2 ) );

         // Reset the complete flag.
         complete = true;

         // Loop over the modules.
         for( auto module : tao::factory )
         {
            module->process( it );
            if( !module->complete() )
               complete = false;
         }

         // Advance the counter.
         ++it;

         LOGD( hpc::setindent( -2 ) );
      }
      while( !complete );

      LOG_EXIT();
   }
}
