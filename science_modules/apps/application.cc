#include <pugixml.hpp>
#include "application.hh"
#include "tao/base/base.hh"
#include "tao/modules/modules.hh"


using namespace hpc;
using namespace pugi;

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

      // Preprocess the incoming XML file.
      //_preprocess_xml();

      // Load all the modules first up.
      _load_modules();
      _connect_parents();

      // Read the options dictionary.
      options::xml_dict xml;
      _read_xml( xml );







      // Prepare the logging.
      string subjobindex=xml.get<string>( "subjobindex" );
      LOGDLN("LOG DIRECTORY:"+xml.get<string>( "logdir" ) );
      LOGDLN("SubJobIndex:"+xml.get<string>( "SubJobIndex" ) );

      _setup_log( xml.get<string>( "logdir" ) + "tao.log."+ subjobindex);



      // Initialise all the modules.
      for( auto module : tao::factory )
         module->initialise( xml, string( "workflow:" ) + module->name() );

      // Mark the beginning of the run.
      LOGILN( runtime(), ",start" );

      // Run.
      _execute();

      // Finalise all the modules.
      for( auto module : tao::factory )
         module->finalise();

      // Mark the conclusion of the run.
      LOGILN( runtime(), ",end,successful" );

      // Dump timing information to the end of the info file.
      LOGILN( "Module metrics:", setindent( 2 ) );
      for( auto module : tao::factory )
         module->log_metrics();

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

      // Open the primary XML file using pugixml.
      xml_document doc;
      INSIST( doc.load_file( string( _xml_file).c_str() ), == true );

      // Iterate over the module nodes.
      xpath_node_set nodes = doc.select_nodes( "/tao/workflow/*[@module]" );
      for( const xpath_node* it = nodes.begin(); it != nodes.end(); ++it )
      {
         xml_node cur = it->node();
         string type = cur.attribute( "module" ).value();
         string name = cur.name();
         tao::factory.create_module( type, name );
      }

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
      options::xml_dict xml;
      _read_xml( xml);

      // Connect 'em all up!
      for( auto module : tao::factory )
      {
         list<hpc::string> parents = xml.get_list<hpc::string>( string( "workflow:" ) + module->name() + string( ":parents" ) );
         for( auto& name : parents )
            module->add_parent( *tao::factory[name] );
      }

      LOG_EXIT();
   }




   ///
   /// Read the XML file into a dictionary.
   ///
   void
   application::_read_xml( options::xml_dict& xml ) const
   {
      xml.read( _xml_file, "/tao/*" );
      xml.read( _dbcfg_file );
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
