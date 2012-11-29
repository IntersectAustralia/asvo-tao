#include <cstdlib>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>

using namespace hpc;

struct halo_type
{
   // merger tree pointers 
   int descendant;
   int first_progenitor;
   int next_progenitor;
   int first_fof;
   int next_fof;

   // properties of halo 
   int num_particles;
   float M_Mean200, Mvir, M_TopHat;  // Mean 200 values (Mvir=M_Crit200)
   float x, y, z;
   float vx, vy, vz;
   float vel_disp;
   float vmax;
   float sx, sy, sz;
   long long most_bound_id;

   // original position in subfind output 
   int snap_num;
   int file_nr;
   int SubhaloIndex;
   float SubHalfMass;
};

std::ostream&
operator<<( std::ostream& strm,
            const halo_type& obj )
{
   strm << "descendant: " << obj.descendant << "\n";
   strm << "first progenitor: " << obj.first_progenitor << "\n";
   strm << "next progenitor: " << obj.next_progenitor << "\n";
   strm << "first in fof group: " << obj.first_fof << "\n";
   strm << "next in fof group: " << obj.next_fof << "\n";
   return strm;
}

int
main( int argc,
      char* argv[] )
{
   LOG_CONSOLE();

   // Need a global range.
   long long global_upp = -1;

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
      ASSERT( !file.fail() );
      LOGDLN( num_trees, " in file." );

      // Iterate over trees.
      vector<halo_type> halos;
      for( unsigned ii = 0; ii < num_trees; ++ii )
      {
         LOGDLN( "Reading tree ", ii, ".", setindent( 2 ) );
         halos.resize( num_tree_halos[ii] );
         file.read( (char*)halos.data(), halos.size()*sizeof(halo_type) );
         ASSERT( !file.fail() );

         // Iterate over each galaxy, checking some values.
         for( unsigned jj = 0; jj < halos.size(); ++jj )
         {
            // All descendants, progenitors and FoFs must be local to the tree.
	    // They can also be -1, indicating no descendant.
            ASSERT( halos[jj].descendant >= -1 && halos[jj].descendant < (int)halos.size(),
                    "Descendant index outside viable range." );
	    ASSERT( halos[jj].first_progenitor >= -1 && halos[jj].first_progenitor < (int)halos.size(),
		    "First progenitor outside viable range." );
	    ASSERT( halos[jj].next_progenitor >= -1 && halos[jj].next_progenitor < (int)halos.size(),
		    "Next progenitor outside viable range." );
	    ASSERT( halos[jj].first_fof >= -1 && halos[jj].first_fof < (int)halos.size(),
		    "First fof outside viable range." );
	    ASSERT( halos[jj].next_fof >= -1 && halos[jj].next_fof < (int)halos.size(),
		    "Next fof outside viable range." );

	    // Hierarchy must match.
	    int halo = halos[jj].first_progenitor;
	    while( halo != -1 )
	    {
	       ASSERT( halos[halo].descendant == jj );
	       halo = halos[halo].next_progenitor;
	    }

	    // FoFs must match.
	    halo = halos[jj].first_fof;
	    int first_fof = halo;
	    bool found = false;
	    while( halo != -1 )
	    {
	       // Each halo in this group must have the same first FoF.
	       ASSERT( halos[halo].first_fof == first_fof );

	       // Current halo must turn up only once.
	       if( halo == jj )
	       {
		  ASSERT( !found );
		  found = true;
	       }

	       halo = halos[halo].next_fof;
	    }
         }

         LOGD( setindent( -2 ) );
      }

      // Advance the file index.
      ++file_idx;
   }

   return EXIT_SUCCESS;
}
