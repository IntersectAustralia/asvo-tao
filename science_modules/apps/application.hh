#ifndef tao_apps_application_hh
#define tao_apps_application_hh

#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>

namespace tao {
   using namespace hpc;

   ///
   ///
   ///
   class application
   {
   public:

      application();

      application( int argc,
                   char* argv[] );

      void
      arguments( int argc,
                 char* argv[] );

      void
      run();

   protected:

      ///
      /// Load modules.
      ///
      void
      _load_modules();

      ///
      /// Connect parents.
      ///
      void
      _connect_parents();

      ///
      /// Insert common options.
      ///
      void
      _setup_common_options( options::dictionary& dict );

      ///
      /// Read the XML file into a dictionary.
      ///
      void
      _read_xml( options::dictionary& dict ) const;

      ///
      /// Prepare log file.
      ///
      void
      _setup_log( const string& filename );

      ///
      /// Execute the application.
      ///
      void
      _execute();

   protected:

      string _xml_file;
      string _dbcfg_file;
   };
}

#endif
