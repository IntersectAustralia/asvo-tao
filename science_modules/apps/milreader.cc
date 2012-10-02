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
   int first_halo_in_fof_group;
   int next_halo_in_fof_group;

   // properties of halo 
   int Len;
   float M_Mean200, Mvir, M_TopHat;  // Mean 200 values (Mvir=M_Crit200)
   float Pos[3];
   float Vel[3];
   float VelDisp;
   float Vmax;
   float Spin[3];
   long long MostBoundID;

   // original position in subfind output 
   int SnapNum;
   int FileNr;
   int SubhaloIndex;
   float SubHalfMass;
};

std::ostream&
operator<<( std::ostream& strm,
            const halo_type& obj )
{
   strm << "descendant: " << obj.descendant << "\n";
   strm << "first progenitor: " << obj.first_progenitor << "\n";
   strm << "first in fof group: " << obj.first_halo_in_fof_group << "\n";
   strm << "next in fof group: " << obj.next_halo_in_fof_group << "\n";
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
   vector<halo_type> halos( num_tree_halos[0] );
   file.read( (char*)halos.data(), num_tree_halos[0]*sizeof(halo_type) );

   // Write out some details.
   std::cout << "Number of trees: " << num_trees << "\n";
   std::cout << "Net halos: " << net_halos << "\n";
   std::cout << "Number of halos per tree: " << num_tree_halos[0] << "\n";


   // {
   //    int cur = 1626;
   //    while( cur != -1 )
   //    {
   //       std::cout << cur << "\n";
   //       cur = halos[cur].first_progenitor;
   //    }
   // }

   // // Hunt down all the primary halos at the last snapshot.
   // unsigned num_prim = 0;
   // for( unsigned ii = 0; ii < num_tree_halos[0]; ++ii )
   // {
   //    if( halos[ii].SnapNum == 63 && halos[ii].first_halo_in_fof_group == ii )
   //    {
   //       std::cout << ii << ", " << halos[ii].first_halo_in_fof_group << "\n";
   //       ++num_prim;
   //    }
   // }
   // std::cout << num_prim << "\n";

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
