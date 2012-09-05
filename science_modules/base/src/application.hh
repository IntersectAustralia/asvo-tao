#ifndef base_application_hh
#define base_application_hh

#include <cstdlib>
#include <iostream>
#include <libhpc/debug/debug.hh>
#include <libhpc/options/options.hh>

namespace tao {

   template< class Pipeline >
   class application
   {
   public:

      typedef Pipeline pipeline_type;

   public:

      application()
      {
      }

      application( int argc,
                   char* argv[] )
      {
         arguments( argc, argv );
      }

      void
      arguments( int argc,
                 char* argv[] )
      {
         // Check for insufficient arguments.
         if( argc != 2 ||
             !argv[1] )
         {
            std::cout << "Insufficient arguments.\n";
            std::cout << "Please supply a path to an input XML.\n";
            exit( 1 );
         }

         // Check that the file exists.
         std::ifstream file( argv[1] );
         if( !file )
         {
            std::cout << "Could not open XML file.\n";
            exit( 1 );
         }

         // Cache the filename.
         _xml_file = argv[1];
      }

      void
      run()
      {
         hpc::options::dictionary dict;
         _pl.setup_options( dict );
         dict.compile();
         _read_xml( dict );
         _pl.initialise( dict );
         _pl.run();
      }

   protected:

      void
      _read_xml( hpc::options::dictionary& dict ) const
      {
         hpc::options::xml xml;
         xml.read( _xml_file, dict );
      }

   protected:

      pipeline_type _pl;
      hpc::string _xml_file;
   };
}

#endif