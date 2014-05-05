#ifndef tao_apps_application_hh
#define tao_apps_application_hh

#include <libhpc/libhpc.hh>
#include <libhpc/mpi/application.hh>
#include <tao/base/base.hh>

//#define PREPROCESSING
namespace tao {
   using namespace hpc;

   ///
   ///
   ///
   class application
      : public mpi::application
   {
   public:

      application( int argc,
                   char* argv[] );

      void
      arguments( int argc,
                 char* argv[] );

      void
      operator()();

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
      _read_xml( xml_dict& xml ) const;

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
      pugi::xml_document _doc;
      factory<backends::multidb<real_type>> _fact;
   };
}

#endif
