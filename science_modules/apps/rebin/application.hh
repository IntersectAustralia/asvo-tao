#ifndef tao_rebin_application_hh
#define tao_rebin_application_hh

#include <string>
#include <libhpc/main/application.hh>

namespace tao {
   namespace rebin {

      class application
	 : public hpc::application
      {
      public:

	 application( int argc,
		      char* argv[] );

	 void
	 operator()();

      protected:

	 std::string _tbl;
	 long long _tree;
	 int _lid;
      };

   }
}

#endif
