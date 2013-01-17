#ifndef base_application_hh
#define base_application_hh

#include <cstdlib>
#include <iostream>
#include <libhpc/debug/debug.hh>
#include <libhpc/options/options.hh>

namespace tao {

   ///
   ///
   ///
   void
   setup_common_options( hpc::options::dictionary& dict );

   ///
   ///
   ///
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
         if( argc != 3 || !argv[1] || !argv[2] )
         {
            std::cout << "Insufficient arguments.\n";
            std::cout << "Please supply a path to an input XML and a database\n";
            std::cout << "configuration XML.\n";
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
         _dbcfg_file = argv[2];
      }

      void
      run()
      {
         hpc::options::dictionary dict;
         _setup_common_options( dict );
         _pl.setup_options( dict );
         dict.compile();
         _read_xml( dict );
         _pl.initialise( dict );
         _pl.run();
      }

   protected:

      ///
      /// Insert common options.
      ///
      void
      _setup_common_options( hpc::options::dictionary& dict )
      {
	 setup_common_options( dict );
      }

      ///
      /// Read the XML file into a dictionary.
      ///
      void
      _read_xml( hpc::options::dictionary& dict ) const
      {
         hpc::options::xml xml;
         xml.read( _xml_file, dict, "/tao/workflow/*" );
         xml.read( _dbcfg_file, dict, "/settings/*" );
      }

   protected:

      pipeline_type _pl;
      hpc::string _xml_file;
      hpc::string _dbcfg_file;
   };
}

#endif
