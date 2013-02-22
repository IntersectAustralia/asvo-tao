#ifndef tao_base_globals_hh
#define tao_base_globals_hh

#include <libhpc/libhpc.hh>

namespace tao {
   using namespace hpc;

   extern unix::time_type tao_start_time;

   double
   runtime();

   ///
   ///
   ///
   void
   setup_common_options( options::dictionary& dict );

}

#endif
