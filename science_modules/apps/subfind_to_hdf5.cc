#include <cstdlib>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>

using namespace hpc;

int
main( int argc,
      char* argv[] )
{
   LOG_CONSOLE();

   // Create the HDF5 data types.
   h5::datatype mem_type, file_type;
   subfind::make_hdf5_types( mem_type, file_type );

   // Keep processing files from 0 onwards until we cannot open a file.
   unsigned file_idx = 0;
   while( 1 )
   {
      // Try and open the file with current index.
      string filename = boost::str( boost::format( "bolshoi_subfind.%1%" ) % file_idx );
      LOGILN( "Trying to open file \"", filename, "\"" );
      std::ifstream file( filename, std::ios::in | std::ios::binary );
      if( !file )
      {
	 LOGILN( "Failed, terminating loop." );
	 break;
      }
      LOGILN( "Success." );

      // Read counts.
      int num_trees, net_halos;
      file.read( (char*)&num_trees, sizeof(num_trees) );
      file.read( (char*)&net_halos, sizeof(net_halos) );
      vector<int> num_tree_halos( num_trees );
      file.read( (char*)num_tree_halos.data(), sizeof(int)*num_trees );
      ASSERT( file );
      LOGDLN( num_trees, " in file." );

      // Iterate over trees.
      vector<subfind::halo> halos;
      for( unsigned ii = 0; ii < num_trees; ++ii )
      {
         LOGDLN( "Reading tree ", ii, ".", setindent( 2 ) );
         halos.resize( num_tree_halos[ii] );
         file.read( (char*)halos.data(), halos.size()*sizeof(halo_type) );
         ASSERT( file );

         // Iterate over each galaxy.
         for( unsigned jj = 0; jj < halos.size(); ++jj )
         {
         }

         LOGD( setindent( -2 ) );
      }

      // Advance the file index.
      ++file_idx;
   }

   return EXIT_SUCCESS;
}
