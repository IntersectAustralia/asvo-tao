#include "globals.hh"

namespace tao {

   unix::time_type tao_start_time;

   double
   runtime()
   {
      return unix::seconds( unix::timer() - tao::tao_start_time );
   }



}
