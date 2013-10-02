#ifndef tao_rebin_application_hh
#define tao_rebin_application_hh

namespace tao {
   namespace rebin {

      class application
      {
	 public:

	    application( int argc,
			 char* argv[] );

	 protected:

	    long long _gid;
      };

   }
}

#endif
