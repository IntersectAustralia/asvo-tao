#ifndef tao_base_module_hh
#define tao_base_module_hh

#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include "galaxy.hh"
#include "flat.hh"

namespace tao {
   using namespace hpc;

   class module
   {
   public:

      typedef double real_type;

   public:

      module();

   protected:

      void
      _read_db_options( const options::dictionary& dict );

      void
      _db_connect( soci::session& sql );

      void
      _db_disconnect();

   protected:

      bool _connected;
      soci::session _sql;
      string _dbtype, _dbname, _dbhost, _dbport, _dbuser, _dbpass;
      string _tree_pre;
   };
}

#endif
