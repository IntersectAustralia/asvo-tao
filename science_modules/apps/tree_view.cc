#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include "tao/base/sage.hh"

using namespace hpc;
using namespace tao;

int
application( int argc,
	     char* argv[] )
{
   // Must have been given a tree number.
   if( argc < 2 )
   {
      std::cout << "Too few arguments.\n";
      return EXIT_FAILURE;
   }
   long tree_id = atol( argv[1] );

   // Create the HDF5 data types.
   h5::datatype mem_type, file_type;
   sage::make_hdf5_types( mem_type, file_type );

   // Open the HDF5 main file.
   h5::file file( "output.h5", H5F_ACC_RDWR, mpi::comm::world );

   // Load the count and displacement.
   long long num_gals = file.read<long long>( "tree_counts", tree_id );
   long long displ = file.read<long long>( "tree_displs", tree_id );

   // Load the galaxies.
   h5::dataset gals_dset( file, "galaxies" );
   h5::dataspace file_space( gals_dset );
   file_space.select_range( displ, displ + num_gals );
   vector<sage::galaxy> gals( num_gals );
   h5::dataspace mem_space;
   mem_space.create( num_gals );
   gals_dset.read( gals.data(), mem_type, mem_space, file_space );

   // Print results.
   for( unsigned ii = 0; ii < gals.size(); ++ii )
      std::cout << gals[ii] << "\n";

   return EXIT_SUCCESS;
}

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );
   LOG_CONSOLE();
   int ec = application( argc, argv );
   mpi::finalise();
   return ec;
}
