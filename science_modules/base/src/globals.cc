#include "globals.hh"
#include "types.hh"

namespace tao {

   posix::time_type tao_start_time;

   double
   runtime()
   {
      return posix::seconds( posix::timer() - tao::tao_start_time );
   }

   // Simulations.
   simulation<real_type> millennium( 500, 73, 0.25, 0.75 );
   simulation<real_type> mini_millennium( 62.5, 73, 0.25, 0.75 );

}
