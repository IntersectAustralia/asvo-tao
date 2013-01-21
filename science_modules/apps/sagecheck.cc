#include <cstdlib>
#include <iostream>
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>

using namespace hpc;

struct galaxy_type
{
   int   type;
   long long   GalaxyIndex;
   int   HaloIndex;
   int   fof_idx;
   int   tree_idx;

#ifndef NLUKE
   // LUKE: See struct GALAXY.
   long long  global_index;
   int        descendant;
   long long  global_descendant;
#endif
  
   int   snap;
   int   central_gal;
   float CentralMvir;

   // properties of subhalo at the last time this galaxy was a central galaaxy 
   float Pos[3];
   float Vel[3];
   float Spin[3];
   int   Len;   
   float Mvir;
   float Rvir;
   float Vvir;
   float Vmax;
   float VelDisp;

   // baryonic reservoirs 
   float ColdGas;
   float StellarMass;
   float BulgeMass;
   float HotGas;
   float EjectedMass;
   float BlackHoleMass;
   float ICS;

   // metals
   float MetalsColdGas;
   float MetalsStellarMass;
   float MetalsBulgeMass;
   float MetalsHotGas;
   float MetalsEjectedMass;
   float MetalsICS;

   // misc 
   float Sfr;
   float SfrBulge;
   float SfrICS;
   float DiskScaleRadius;
   float Cooling;
   float Heating;
};

std::ostream&
operator<<( std::ostream& strm,
            const galaxy_type& obj )
{
   // strm << "descendant: " << obj.descendant << "\n";
   // strm << "first progenitor: " << obj.first_progenitor << "\n";
   // strm << "first in fof group: " << obj.first_halo_in_fof_group << "\n";
   // strm << "next in fof group: " << obj.next_halo_in_fof_group << "\n";
}

#ifndef NLUKE

void
walk_tree( int idx,
           int tree_idx,
           vector<galaxy_type>& halos,
           multimap<int,int>& parents )
{
   // Mark each galaxy with a tree index. If this galaxy already has
   // a tree index then we have a problem. This tests for the
   // independance of each tree.
   ASSERT( halos[idx].tree_idx == -1,
           "Overlapping trees." );
   halos[idx].tree_idx = tree_idx;

   // Process each parent.
   auto rng = parents.equal_range( idx );
   while( rng.first != rng.second )
   {
      walk_tree( (*rng.first).second, tree_idx, halos, parents );
      ++rng.first;
   }
}

#endif

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );

   // ASSERT( argc > 1 );
   // LOG_CONSOLE();
   LOG_PUSH( new logging::stdout() );

#ifndef NLUKE
   // Need a global range.
   long long global_upp = -1;
#endif

   // Keep processing files from 0 onwards until we cannot open a file.
   unsigned file_idx = 0, chunk_idx = 0;
   while( 1 )
   {
      // Try and open the file with current chunk index.
      string filename = boost::str( boost::format( "model_%1%_%2%" ) % file_idx % chunk_idx );
      LOGILN( "Trying to open file \"", filename, "\"" );
      std::ifstream file( filename, std::ios::in | std::ios::binary );
      if( !file )
      {
         // Try with advanced file index and reset chunk index.
         ++file_idx;
         chunk_idx = 0;
         filename = boost::str( boost::format( "model_%1%_%2%" ) % file_idx % chunk_idx );
         LOGILN( "Trying to open file \"", filename, "\"" );
         file.open( filename, std::ios::in | std::ios::binary );
         if( !file )
         {
            LOGILN( "Failed, terminating loop." );
            break;
         }
      }
      LOGILN( "Success." );

      // Read counts.
      int num_trees, net_halos;
      file.read( (char*)&num_trees, sizeof(num_trees) );
      file.read( (char*)&net_halos, sizeof(num_trees) );
      vector<int> num_tree_halos( num_trees );
      file.read( (char*)num_tree_halos.data(), sizeof(int)*num_trees );
      ASSERT( !file.fail() );
      LOGDLN( num_trees, " in file." );

      // Iterate over trees.
      vector<galaxy_type> halos;
      for( unsigned ii = 0; ii < num_trees; ++ii )
      {
         LOGDLN( "Reading tree ", ii, ".", setindent( 2 ) );
         halos.resize( num_tree_halos[ii] );
         file.read( (char*)halos.data(), halos.size()*sizeof(galaxy_type) );
         ASSERT( !file.fail() );

         // Need to represent the parents of each galaxy, and also
         // the bases of each tree. We also need to store the FOF
         // groups to check galaxy types.
         multimap<int,int> parents;
         list<int> bases;
         multimap<int,int> fof_groups;
         map<long long,int> global_to_local;

         // Iterate over each galaxy, checking some values.
         for( unsigned jj = 0; jj < halos.size(); ++jj )
         {
            // All descendants must be local to the tree. They can also
            // be -1, indicating no descendant.
            ASSERT( halos[jj].descendant < (int)halos.size(),
                    "Descendant index outside viable range." );

	    // Descendants cannot point to themselves.
	    ASSERT( halos[jj].descendant != jj );

            // All types must be 0, 1 or 2.
            ASSERT( halos[jj].type >= 0 && halos[jj].type <= 2,
                    "Bad galaxy type." );

            // All snapshot numbers must be <= 63.
            ASSERT( halos[jj].snap <= 63,
                    "Bad snapshot number." );

            // Add parent information.
            if( halos[jj].descendant != -1 )
               parents.insert( halos[jj].descendant, jj );
            else
               bases.push_back( jj );

            // Clear the tree index to a dummy value.
            halos[jj].tree_idx = -1;

            // Insert the FOF group details.
            fof_groups.insert( halos[jj].fof_idx, jj );

            // Insert global to local mapping and range.
            ASSERT( !global_to_local.has( halos[jj].global_index ) );
            global_to_local.insert( halos[jj].global_index, jj );
	    ASSERT( halos[jj].global_index > global_upp );
	    global_upp = halos[jj].global_index;
         }

         // Starting from the bases, walk up the tree to compute some
         // values and checks.
         int tree_idx = 0;
         for( auto idx : bases )
         {
            LOGDLN( "Walking tree with base at ", idx, "." );
            walk_tree( idx, tree_idx, halos, parents );
            ++tree_idx;
         }

         // Need another loop over halos to check things.
         for( unsigned jj = 0; jj < halos.size(); ++jj )
         {
            // Check global descandant.
            if( halos[jj].descendant != -1 )
               ASSERT( global_to_local.get( halos[jj].global_descendant ) == halos[jj].descendant );
            else
               ASSERT( halos[jj].global_descendant == -1 );

            // Check FOF groups.
            bool have_primary = false;
            auto rng = fof_groups.equal_range( jj );
            while( rng.first != rng.second )
            {
               unsigned idx = (*rng.first).second;
               if( halos[idx].type == 0 )
               {
                  ASSERT( !have_primary, "Multiple primary galaxies in FOF group." );
                  have_primary = true;
               }
               ++rng.first;
            }
         }

         LOGD( setindent( -2 ) );
      }

      // Advance the chunk.
      ++chunk_idx;
   }

   mpi::finalise();
   return EXIT_SUCCESS;
}
