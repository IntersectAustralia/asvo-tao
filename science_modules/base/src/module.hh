#ifndef tao_base_module_hh
#define tao_base_module_hh

#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include "galaxy.hh"

namespace tao {

   class module {
   public:

   protected:

      void
      _db_connect( soci::session& sql,
                   const hpc::string& type,
                   const hpc::string& name );
   };
}

#endif
