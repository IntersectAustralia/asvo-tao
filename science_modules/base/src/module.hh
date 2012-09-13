#ifndef tao_base_module_hh
#define tao_base_module_hh

#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include "galaxy.hh"
#include "flat.hh"

namespace tao {

   class module {
   public:

      module();

   protected:

      void
      _db_connect( soci::session& sql,
                   const hpc::string& type,
                   const hpc::string& name );

      void
      _db_disconnect();

   protected:

      bool _connected;
      soci::session _sql;
      hpc::string _dbtype, _dbname, _dbhost, _dbuser, _dbpass;
   };
}

#endif
