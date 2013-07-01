#include <cstdlib>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>
#include <tao/base/subfind.hh>

double box_size = 250.0;
unsigned num_snapshots = 181;

using namespace hpc;
using namespace tao;

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );
   LOG_CONSOLE();

   // See if we were given a starting file/chunk.
   unsigned file_idx = 0;
   if( argc >= 2 )
   {
      file_idx = atoi( argv[1] );
   }

   // Keep processing files from 0 onwards until we cannot open a file.
   while( 1 )
   {
      // Try and open the file with current index.
      string filename = boost::str( boost::format( "trees_180.%1%" ) % file_idx );
      LOGILN( "Trying to open file \"", filename, "\"" );
      std::ifstream file( filename, std::ios::in | std::ios::binary );
      if( !file )
      {
	 LOGILN( "Failed, terminating loop." );
	 break;
      }
      LOGILN( "Success." );

      // Read counts.
      unsigned num_trees, net_halos;
      file.read( (char*)&num_trees, sizeof(num_trees) );
      file.read( (char*)&net_halos, sizeof(net_halos) );
      vector<int> num_tree_halos( num_trees );
      file.read( (char*)num_tree_halos.data(), sizeof(int)*num_trees );
      ASSERT( file );
      LOGDLN( num_trees, " in file." );

      // Check number of trees and net halos.
      ASSERT( num_trees, "Invalid number of trees for file." );
      ASSERT( net_halos, "Invalid net halos for file." );

      // Iterate over trees.
      vector<subfind::halo> halos;
      for( unsigned ii = 0; ii < num_trees; ++ii )
      {
         LOGDLN( "Reading tree ", ii, " with ", num_tree_halos[ii], " halos.", setindent( 2 ) );
         halos.resize( num_tree_halos[ii] );
         file.read( (char*)halos.data(), halos.size()*sizeof(subfind::halo) );
         ASSERT( file );

	 // Check number of halos in this tree.
	 ASSERT( num_tree_halos[ii], "Invalid number of halos in tree." );

         // Iterate over each galaxy.
         for( unsigned jj = 0; jj < halos.size(); ++jj )
         {
            // All descendants must be local to the tree. They can also
            // be -1, indicating no descendant.
            ASSERT( halos[jj].descendant < (int)halos.size(),
                    "Descendant index outside viable range." );

	    // Descendants cannot point to themselves.
	    ASSERT( halos[jj].descendant != jj );

            // All snapshot numbers must be < specified value.
            ASSERT( halos[jj].snap_num < num_snapshots,
                    "Bad snapshot number." );

	    // Check positions.
	    ASSERT( halos[jj].x >= 0.0 && halos[jj].x <= box_size,
		    "Bad position value." );
	    ASSERT( halos[jj].y >= 0.0 && halos[jj].y <= box_size,
		    "Bad position value." );
	    ASSERT( halos[jj].z >= 0.0 && halos[jj].z <= box_size,
		    "Bad position value." );
         }

         LOGD( setindent( -2 ) );
      }

      // Advance the file index.
      ++file_idx;
   }

   return EXIT_SUCCESS;
}
