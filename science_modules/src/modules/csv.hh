#ifndef tao_modules_csv_hh
#define tao_modules_csv_hh

#include <fstream>
#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/batch.hh"
#include "tao/base/types.hh"

namespace tao {
   namespace modules {
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

         virtual
         void
         log_metrics();

      protected:

         void
         _write_field( const tao::batch<real_type>& bat,
                       unsigned idx,
                       const string& field );

      protected:

         std::ofstream _file;
         string _fn;
         list<string> _fields;
         unsigned long long _records;
      };

   }
}

#endif
