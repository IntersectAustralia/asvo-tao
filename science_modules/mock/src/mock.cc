#include "filter.hh"

namespace tao {

   ///
   /// Run the module.
   ///
   void
   filter::run()
   {
      MPI_LOG_ENTER();

      // TODO: Read filters.

      for( mpi::lindex ii = 0; ii < num_filters; ++ii )
         _process_filter();

      MPI_LOG_EXIT();
   }

   void
   filter::_process_filter()
   {
      
   }
}
