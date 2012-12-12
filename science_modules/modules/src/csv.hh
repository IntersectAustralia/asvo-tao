#ifndef tao_modules_csv_hh
#define tao_modules_csv_hh

#include <fstream>
#include <libhpc/libhpc.hh>
#include "tao/base/galaxy.hh"

namespace tao {
   using namespace hpc;

   class csv
   {
   public:

      csv( const string& filename="tao.output" );

      void
      process_galaxy( const tao::galaxy& galaxy,
		      double app_mag=0.0 );

   protected:

      std::ofstream _file;
   };
}

#endif
