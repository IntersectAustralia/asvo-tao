#ifndef tao_analytic_application_hh
#define tao_analytic_application_hh

#include <libhpc/mpi/application.hh>
#include <libhpc/libhpc.hh>
#include <tao/tao.hh>

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

      protected:

	 real_type _box;
	 real_type _ra, _dec;
	 real_type _z;
	 unsigned _idx;
      };

   }
}

#endif
