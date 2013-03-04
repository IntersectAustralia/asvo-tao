#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include "tao/base/sage.hh"

using namespace hpc;
using namespace tao;

int
application()
{
   // Create the HDF5 data types.
   h5::datatype mem_type, file_type;
   sage::make_hdf5_types( mem_type, file_type );

   // Open the HDF5 main file.
   h5::file file( "output.h5", H5F_ACC_RDWR, mpi::comm::world );

   // Parallel load the counts and displacements.
   vector<long long> tree_counts, tree_displs;
   file.reada( "tree_counts", tree_counts, mpi::comm::world );
   file.reada( "tree_displs", tree_displs, mpi::comm::world );
   size_t num_global_trees = mpi::comm::world.all_reduce( tree_counts.size() );
   size_t tree_offs = mpi::comm::world.scan( tree_counts.size(), MPI_SUM, true );
   LOGILN( "Number of local trees: ", tree_counts.size() );

   // Get hold of the galaxy dataset and space.
   h5::dataset gals_dset( file, "galaxies" );
   h5::dataspace file_space( gals_dset );

   // Create the tree dataset.
   h5::property_list props( H5P_DATASET_CREATE );
   {
      size_t remain = num_global_trees*6*4;
      char name[20];
      unsigned file_idx = 0;
      while( remain )
      {
	 sprintf( name, "tree_info.%04d", file_idx++ );
	 size_t size = std::min<size_t>( remain, (size_t)1 << 31 );
	 props.set_external( name, size );
	 remain -= size;

	 // Must create the files, HDF5 won't do it!
	 std::ofstream tmp( name );
      }
   }
   h5::dataspace bnd_mem_space, bnd_file_space;
   bnd_mem_space.create( 3 );
   bnd_file_space.create( 6*num_global_trees );
   h5::dataset tree_bnd_dset( file, "tree_bounds", h5::datatype::ieee_f32be, bnd_file_space, none, false, props );

   // Use persistant storage to avoid a lot of allocations.
   vector<sage::galaxy> gals;

   // Process each tree, one at a time.
   for( long long ii = 0; ii < tree_counts.size(); ++ii )
   {
      // Load the tree data.
      h5::dataspace mem_space;
      mem_space.create( tree_counts[ii] );
      file_space.select_range( tree_displs[ii], tree_displs[ii] + tree_counts[ii] );
      gals.resize( tree_counts[ii] );
      gals_dset.read( gals.data(), mem_type, mem_space, file_space );

      // Calculate the bounding box.
      array<float,3> min(
	 std::numeric_limits<float>::max(),
	 std::numeric_limits<float>::max(),
	 std::numeric_limits<float>::max()
	 );
      array<float,3> max(
	 std::numeric_limits<float>::min(),
	 std::numeric_limits<float>::min(),
	 std::numeric_limits<float>::min()
	 );
      for( unsigned jj = 0; jj < gals.size(); ++jj )
      {
	 min[0] = std::min( min[0], gals[jj].x );
	 min[1] = std::min( min[1], gals[jj].y );
	 min[2] = std::min( min[2], gals[jj].z );
	 max[0] = std::max( max[0], gals[jj].x );
	 max[1] = std::max( max[1], gals[jj].y );
	 max[2] = std::max( max[2], gals[jj].z );
      }

      // Write the bounding box out.
      bnd_file_space.select_range( 6*(tree_offs + ii), 6*(tree_offs + ii) + 3 );
      tree_bnd_dset.write( min.data(), h5::datatype::native_float, bnd_mem_space, bnd_file_space );
      bnd_file_space.select_range( 6*(tree_offs + ii) + 3, 6*(tree_offs + ii) + 6 );
      tree_bnd_dset.write( max.data(), h5::datatype::native_float, bnd_mem_space, bnd_file_space );
   }

   return EXIT_SUCCESS;
}

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );
   LOG_CONSOLE();
   int ec = application();
   mpi::finalise();
   return ec;
}
