#ifndef tao_base_module_hh
#define tao_base_module_hh

#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include "galaxy.hh"

namespace tao {
   using namespace hpc;

   class module
   {
   public:

      typedef double real_type;

   public:

      module();

      double
      time() const;

   protected:

      void
      _read_db_options( const options::dictionary& dict );

      void
      _db_connect();

      void
      _db_disconnect();

      bool
      _db_cycle();

   protected:

      bool _connected;
      soci::session _sql;
      unsigned _num_restart_its;
      unsigned _cur_restart_it;
      string _dbtype, _dbname, _dbhost, _dbport, _dbuser, _dbpass;
      string _tree_pre;

      profile::timer _timer;
   };
}

#endif
