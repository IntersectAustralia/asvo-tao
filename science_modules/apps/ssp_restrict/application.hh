#ifndef tao_ssp_restrict_application_hh
#define tao_ssp_restrict_application_hh

#include <boost/filesystem.hpp>

namespace tao {
   namespace ssp_restrict {
      namespace fs = boost::filesystem;

      class application
      {
      public:

	 application( int argc,
		      char* argv[] );

	 void
	 operator()();

      protected:

	 fs::path _inp_dir;
	 fs::path _out_dir;
	 std::list<fs::path> _ssps;
      };

   }
}

#endif
