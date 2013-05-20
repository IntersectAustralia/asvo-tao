#include "globals.hh"

namespace tao {

   posix::time_type tao_start_time;

   double
   runtime()
   {
      return posix::seconds( posix::timer() - tao::tao_start_time );
   }



}
