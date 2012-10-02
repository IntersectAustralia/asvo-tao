#include <cstdlib>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>

using namespace hpc;

struct galaxy_type
{
  int   Type;
  long long   GalaxyIndex;
  int   HaloIndex;
  int   FOFHaloIndex;
  int   TreeIndex;

  // LUKE: See struct GALAXY.
  int   descendant;
  
  int   SnapNum;
  int   CentralGal;
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

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );

   ASSERT( argc > 1 );
   LOG_CONSOLE();

   // Open the file.
   string filename = string( argv[1] );
   std::ifstream file( filename, std::ios::in | std::ios::binary );

   // Read counts.
   int num_trees, net_halos;
   file.read( (char*)&num_trees, sizeof(num_trees) );
   file.read( (char*)&net_halos, sizeof(num_trees) );
   vector<int> num_tree_halos( num_trees );
   file.read( (char*)num_tree_halos.data(), sizeof(int)*num_trees );

   // Read first tree.
   vector<galaxy_type> halos( num_tree_halos[0] );
   file.read( (char*)halos.data(), num_tree_halos[0]*sizeof(galaxy_type) );

   // Write out some details.
   std::cout << "Number of trees: " << num_trees << "\n";
   std::cout << "Net halos: " << net_halos << "\n";
   std::cout << "Number of halos per tree: " << num_tree_halos[0] << "\n";



   unsigned num_prim = 0;
   for( unsigned ii = 0; ii < num_tree_halos[0]; ++ii )
   {
      if( halos[ii].Type == 0 )
         ++num_prim;
   }
   std::cout << num_prim << "\n";

   // {
   //    int cur = 0;
   //    while( cur != -1 )
   //    {
   //       std::cout << cur << ", " << halos[cur].Type << "\n";
   //       cur = halos[cur].next_halo_in_fof_group;
   //    }
   // }

   // {
   //    int cur = 1;
   //    set<int> fofs;
   //    while( cur != -1 )
   //    {
   //       fofs.insert( cur );
   //       std::cout << halos[cur].next_halo_in_fof_group << ", " << halos[cur].SubhaloIndex << ", " << halos[cur].Mvir << "\n";
   //       cur = halos[cur].next_halo_in_fof_group;
   //    }
   //    // std::cout << fofs << "\n";
   // }
   // {
   //    int cur = 1;
   //    set<int> fofs;
   //    while( cur != -1 )
   //    {
   //       fofs.insert( cur );
   //       std::cout << halos[cur].next_halo_in_fof_group << ", " << halos[cur].descendant << "\n";
   //       cur = halos[cur].next_halo_in_fof_group;
   //    }
   //    // std::cout << fofs << "\n";
   // }

   mpi::finalise();
   return EXIT_SUCCESS;
}
