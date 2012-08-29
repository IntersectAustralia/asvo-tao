#include <libhpc/libhpc.hh>
#include "filter.hh"

using namespace hpc;

namespace tao {

   ///
   /// Run the module.
   ///
   void
   filter::run()
   {
      LOG_ENTER();

      // TODO: Read filters.

      mpi::lindex num_filters = 0;
      for( mpi::lindex ii = 0; ii < num_filters; ++ii )
         _process_filter();

      LOG_EXIT();
   }

   void
   filter::_process_filter()
   {
      
   }
}
