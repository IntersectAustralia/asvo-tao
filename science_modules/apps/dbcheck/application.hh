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

         std::string _host;
         uint16_t _port;
         std::string _dbname;
         std::string _user;
         std::string _passwd;

         std::string _sage_fn;
      };

   }
}

#endif
