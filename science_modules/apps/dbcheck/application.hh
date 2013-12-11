#ifndef tao_dbcheck_application_hh
#define tao_dbcheck_application_hh

#include <string>
#include <libhpc/mpi/application.hh>

namespace tao {
   namespace dbcheck {

      class application
	 : public hpc::mpi::application
      {
      public:

	 application( int argc,
		      char* argv[] );

	 void
	 operator()();

      protected:

         std::string _sage_fn;
      };

   }
}

#endif
