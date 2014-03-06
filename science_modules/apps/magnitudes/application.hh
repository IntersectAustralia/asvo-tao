#ifndef tao_magnitudes_application_hh
#define tao_magnitudes_application_hh

#include <string>
#include <boost/filesystem.hpp>
#include <libhpc/mpi/application.hh>

namespace fs = boost::filesystem;

class application
   : public hpc::mpi::application
{
public:

   application( int argc,
		char* argv[] );

   void
   operator()();

protected:

   fs::path _sfh_path;
};

#endif
