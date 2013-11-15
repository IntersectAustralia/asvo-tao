#ifndef tao_analytic_application_hh
#define tao_analytic_application_hh

#include <libhpc/mpi/application.hh>

namespace tao {
   namespace analytic {

      class application
	 : public hpc::mpi::application
      {
      public:

	 application( int argc,
		      char* argv[] );

	 void
	 operator()();
      };

   }
}

#endif
