#ifndef hdf5_types_hh
#define hdf5_types_hh

#include <libhpc/libhpc.hh>
#include "sage.hh"

namespace sage {

   void
   make_hdf5_types( hpc::h5::datatype& mem_type,
		    hpc::h5::datatype& file_type );

}

#endif
