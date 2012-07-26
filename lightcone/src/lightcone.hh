#ifndef tao_lightcone_lightcone_hh
#define tao_lightcone_lightcone_hh

#include <libhpc/containers/vector.hh>
#include <libhpc/hpcmpi/mpi.hh>

namespace tao {

   ///
   /// Lightcone science module.
   ///
   class lightcone
   {
   public:

      typedef double real_type;

      lightcone();

      ~lightcone();

      ///
      /// Run the module.
      ///
      void
      run();

   protected:

   protected:
   };
}

#endif
