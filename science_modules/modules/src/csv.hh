#ifndef tao_modules_csv_hh
#define tao_modules_csv_hh

#include <fstream>
#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/galaxy.hh"
#include "lightcone.hh"

namespace tao {
   using namespace hpc;

   class csv
      : public module
   {
   public:

      static
      module*
      factory( const string& name,
	       pugi::xml_node base );

   public:

     csv( const string& name = string(),
	  pugi::xml_node base = pugi::xml_node() );

      virtual
      ~csv();

      ///
      ///
      ///
      virtual
      void
      initialise( const options::xml_dict& global_dict );

      ///
      ///
      ///
      virtual
      void
      execute();

      void
      open();

      void
      process_galaxy( const tao::galaxy& galaxy );

      virtual
      void
      log_metrics();

   protected:

      void
      _write_field( const tao::galaxy& galaxy,
                    const string& field,
                    unsigned idx );

   protected:

      std::ofstream _file;
      string _fn;
      list<string> _fields;
      unsigned long long _records;
   };

}

#endif
