#ifndef tao_analytic_application_hh
#define tao_analytic_application_hh

#include <libhpc/main/application.hh>

class application
   : public hpc::main::application
{
public:

   application( int argc,
		char* argv[] );

   void
   operator()();
};

#endif
