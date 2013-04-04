#ifndef tao_apps_application_hh
#define tao_apps_application_hh

#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include <libhpc/options/xml_dict.hh>

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
	  /// Massage incoming XML.
	  ///
	  void
	  _preprocess_xml();



      ///
      /// Read the XML file into a dictionary.
      ///
      void
      _read_xml( options::xml_dict& xml ) const;

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
      string _currentxml_version;
   };
}

#endif
