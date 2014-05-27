#include <libhpc/system/filesystem.hh>
#include "utils.hh"

namespace tao {

   hpc::fs::path
   data_prefix()
   {
      return hpc::executable_path().parent_path().parent_path()/"data";
   }

}
