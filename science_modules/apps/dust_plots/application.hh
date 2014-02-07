#ifndef tao_dust_plots_application_hh
#define tao_dust_plots_application_hh

#include <libhpc/main/application.hh>

class application
   : public hpc::application
{
public:

   application( int argc,
                char* argv[] );

   void
   operator()();
};

#endif
