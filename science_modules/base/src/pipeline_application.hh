#ifndef base_pipeline_application_hh
#define base_pipeline_application_hh

#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include "globals.hh"

namespace tao {
   using namespace hpc;

   ///
   ///
   ///
   template< class Pipeline >
   class pipeline_application
   {
   public:

      typedef Pipeline pipeline_type;

   public:

      pipeline_application()
      {
	 tao_start_time = unix::timer();
      }

      pipeline_application( int argc,
                   char* argv[] )
      {
	 tao_start_time = unix::timer();
         arguments( argc, argv );
      }

      void
      arguments( int argc,
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
      run()
      {
         options::dictionary dict;
         //_setup_common_options( dict );
         //_pl.setup_options( dict );
         dict.compile();
         _read_xml( dict );
         _setup_log( dict.get<string>( "logdir" ) + "/tao.log" );
         //_pl.initialise( dict );

	 // Mark the beginning of the run.
	 LOGILN( runtime(), ",start" );

	 // Run.
         _pl.run();

	 // Mark the conclusion of the run.
	 LOGILN( runtime(), ",end,successful" );

	 // Dump timings.
	 _pl.log_timings();
      }

   protected:

      ///
      /// Insert common options.
      ///
      void
      _setup_common_options( options::dictionary& dict )
      {
	 //setup_common_options( dict );
      }

      ///
      /// Read the XML file into a dictionary.
      ///
      void
      _read_xml( options::dictionary& dict ) const
      {
         options::xml xml;
         xml.read( _xml_file, dict, "/tao/*" );
         xml.read( _dbcfg_file, dict );
      }

      ///
      /// Prepare log file.
      ///
      void
      _setup_log( const string& filename )
      {
	 LOG_ENTER();

	 if( mpi::comm::world.rank() == 0 )
	 {
	    LOGDLN( "Setting logging file to: ", filename );
	    LOG_PUSH( new logging::file( filename, logging::info ) );
	 }

	 LOG_EXIT();
      }

   protected:

      pipeline_type _pl;
      string _xml_file;
      string _dbcfg_file;
   };
}

#endif
