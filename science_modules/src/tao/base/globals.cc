#include "globals.hh"
#include "types.hh"

namespace tao {

   hpc::timer timer( true );

   hpc::timer::time_type
   runtime()
   {
      return timer.total();
   }

   ///
   /// Simulations.
   ///

   simulation millennium(
      500,
      73, 0.25, 0.75,
      64,
      0.0078125,
      0.012346,
      0.019608,
      0.032258,
      0.047811,
      0.051965,
      0.056419,
      0.061188,
      0.066287,
      0.071732,
      0.077540,
      0.083725,
      0.090306,
      0.097296,
      0.104713,
      0.112572,
      0.120887,
      0.129675,
      0.138950,
      0.148724,
      0.159012,
      0.169824,
      0.181174,
      0.193070,
      0.205521,
      0.218536,
      0.232121,
      0.246280,
      0.261016,
      0.276330,
      0.292223,
      0.308691,
      0.325730,
      0.343332,
      0.361489,
      0.380189,
      0.399419,
      0.419161,
      0.439397,
      0.460105,
      0.481261,
      0.502839,
      0.524807,
      0.547136,
      0.569789,
      0.592730,
      0.615919,
      0.639314,
      0.662870,
      0.686541,
      0.710278,
      0.734031,
      0.757746,
      0.781371,
      0.804849,
      0.828124,
      0.851138,
      0.873833,
      0.896151,
      0.918031,
      0.939414,
      0.960243,
      0.980457,
      1.000000
      );

   simulation mini_millennium(
      62.5,
      73, 0.25, 0.75,
      64,
      0.0078125,
      0.012346,
      0.019608,
      0.032258,
      0.047811,
      0.051965,
      0.056419,
      0.061188,
      0.066287,
      0.071732,
      0.077540,
      0.083725,
      0.090306,
      0.097296,
      0.104713,
      0.112572,
      0.120887,
      0.129675,
      0.138950,
      0.148724,
      0.159012,
      0.169824,
      0.181174,
      0.193070,
      0.205521,
      0.218536,
      0.232121,
      0.246280,
      0.261016,
      0.276330,
      0.292223,
      0.308691,
      0.325730,
      0.343332,
      0.361489,
      0.380189,
      0.399419,
      0.419161,
      0.439397,
      0.460105,
      0.481261,
      0.502839,
      0.524807,
      0.547136,
      0.569789,
      0.592730,
      0.615919,
      0.639314,
      0.662870,
      0.686541,
      0.710278,
      0.734031,
      0.757746,
      0.781371,
      0.804849,
      0.828124,
      0.851138,
      0.873833,
      0.896151,
      0.918031,
      0.939414,
      0.960243,
      0.980457,
      1.000000
      );

}
