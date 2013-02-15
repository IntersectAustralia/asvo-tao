#include <cstdlib>
#include <iostream>
#include <libhpc/libhpc.hh>
#include "tao/base/sage.hh"

using namespace hpc;
using namespace tao;

bool
iter_files( std::ifstream& file,
	    unsigned& file_idx,
	    unsigned& chunk_idx )
{
   // Try and open the file with current index.
   string filename = boost::str( boost::format( "model_%1%_%2%" ) % file_idx % chunk_idx );
   LOGILN( "Trying to open file \"", filename, "\"" );
   file.close();
   file.open( filename, std::ios::in | std::ios::binary );
   if( !file )
   {
      // Try with advanced file index and reset chunk index.
      if( ++file_idx < 512 )
      {
	 chunk_idx = 0;
	 filename = boost::str( boost::format( "model_%1%_%2%" ) % file_idx % chunk_idx );
	 LOGILN( "Trying to open file \"", filename, "\"" );
	 file.open( filename, std::ios::in | std::ios::binary );
      }
      if( !file )
      {
	 LOGILN( "Failed, terminating loop." );
	 return false;
      }
   }
   LOGILN( "Success." );
   return true;
}

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );

   LOG_CONSOLE();

   // Create the HDF5 data types.
   h5::datatype mem_type, file_type;
   sage::make_hdf5_types( mem_type, file_type );

   // Calculate the net trees and galaxies.
   long long net_trees = 0, net_gals = 0;
   {
      unsigned file_idx = 0, chunk_idx = 0;
      std::ifstream file;
      while( iter_files( file, file_idx, chunk_idx ) )
      {
	 // Read counts.
	 int num_trees, num_gals;
	 file.read( (char*)&num_trees, sizeof(num_trees) );
	 file.read( (char*)&num_gals, sizeof(num_gals) );

	 // Accumulate.
	 net_trees += num_trees;
	 net_gals += num_gals;

	 // Advance.
	 ++chunk_idx;
      }
   }
   LOGILN( "Have ", net_trees, " trees." );
   LOGILN( "Have ", net_gals, " galaxies." );

   // Create a property list to split the galaxies dataset
   // across multiple files.
   h5::property_list props( H5P_DATASET_CREATE );
   {
      long long remain = net_gals*file_type.size();
      char name[15];
      unsigned file_idx = 0;
      while( remain )
      {
	 sprintf( name, "galaxies.%04d", file_idx++ );
	 long long size = std::min<long long>( remain, (long long)1 << 31 );
	 props.set_external( name, size );
	 remain -= size;

	 // Must create the files, HDF5 won't do it!
	 std::ofstream tmp( name );
      }
      LOGILN( "Splitting across ", file_idx, " files." );
   }

   // Create the HDF5 file and a couple of groups.
   h5::file output( "output.h5", H5F_ACC_TRUNC );
   h5::dataspace tree_mem_space, tree_file_space;
   tree_mem_space.create( 1 );
   tree_file_space.create( net_trees );
   h5::dataset tree_displ_dset( output, "tree_displs", h5::datatype::std_i64be, tree_file_space );
   h5::dataset tree_count_dset( output, "tree_counts", h5::datatype::std_i64be, tree_file_space );
   h5::dataspace gal_file_space;
   gal_file_space.create( net_gals );
   h5::dataset gal_dset( output, "galaxies", file_type, gal_file_space, none, false, props );

   // Keep processing files from 0 onwards until we cannot open a file.
   {
      long long displ = 0, cur_tree = 0;
      unsigned file_idx = 0, chunk_idx = 0;
      std::ifstream file;
      while( iter_files( file, file_idx, chunk_idx ) )
      {
	 // Read counts.
	 int num_trees, num_gals;
	 file.read( (char*)&num_trees, sizeof(num_trees) );
	 file.read( (char*)&num_gals, sizeof(num_gals) );
	 vector<int> num_tree_gals( num_trees );
	 file.read( (char*)num_tree_gals.data(), sizeof(int)*num_trees );
	 ASSERT( file );
	 LOGDLN( num_trees, " in file." );

	 // Iterate over trees.
	 vector<sage::galaxy> gals;
	 for( unsigned ii = 0; ii < num_trees; ++ii )
	 {
	    // Load the current tree.
	    LOGDLN( "Reading tree ", ii, ".", setindent( 2 ) );
	    gals.resize( num_tree_gals[ii] );
	    file.read( (char*)gals.data(), gals.size()*sizeof(sage::galaxy) );
	    ASSERT( file );

	    // Write out to HDF5.
	    tree_file_space.select_one( cur_tree++ );
	    tree_count_dset.write( &num_tree_gals[ii], h5::datatype::native_int, tree_mem_space, tree_file_space );
	    tree_displ_dset.write( &displ, h5::datatype::native_llong, tree_mem_space, tree_file_space );
	    if( gals.size() )
	    {
	       h5::dataspace gal_mem_space;
	       gal_mem_space.create( gals.size() );
	       ASSERT( displ + gals.size() <= net_gals );
	       gal_file_space.select_range( displ, displ + gals.size() );
	       gal_dset.write( gals.data(), mem_type, gal_mem_space, gal_file_space );
	    }

	    // Accumulate.
	    displ += num_tree_gals[ii];

	    LOGD( setindent( -2 ) );
	 }

	 // Advance the file chunk index.
	 ++chunk_idx;
      }
   }

   mpi::finalise();
   return EXIT_SUCCESS;
}
