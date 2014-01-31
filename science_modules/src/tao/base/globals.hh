#ifndef tao_base_globals_hh
#define tao_base_globals_hh

#include <libhpc/libhpc.hh>
#include "simulation.hh"

namespace tao {
   using namespace hpc;

   extern time_type tao_start_time;

   typedef double real_type;

   double
   runtime();

   // Simulations.
   extern simulation millennium;
   extern simulation mini_millennium;

}

#endif
