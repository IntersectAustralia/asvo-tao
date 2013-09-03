#include <libhpc/system/exe.hh>
#include "utils.hh"

namespace tao {
   using namespace hpc;

   boost::filesystem::path
   data_prefix()
   {
      return nix::executable_path().parent_path().parent_path()/"data";
   }

}
