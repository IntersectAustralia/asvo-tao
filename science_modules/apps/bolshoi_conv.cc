#include <cstdlib>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>

using namespace hpc;

///
/// The Bolshoi halo data structure.
///
struct bolshoi_halo_type
{
   double              scale; // Scale factor of halo.
   unsigned long long  id; // ID of halo (unique across entire simulation).
   double              desc_scale; // Scale of descendant halo, if applicable.
   unsigned long long  desc_id; // ID of descendant halo, if applicable.
   unsigned            num_prog; // Number of progenitors.
   unsigned long long  pid; // Host halo ID.
   unsigned long long  upid; // Most massive host halo ID (only different from pid in
                             // cases of sub-subs or sub-sub-subs etc.
   unsigned long long  desc_pid; // pid of descendant halo, if applicable.
   bool                phantom; // Nonzero for halos interpolated across timesteps.
   double              sam_mvir; // Halo mass, smoothed across accretion history; always greater
                                 // than sum of halo masses of contributing progenitors (Msun/h).
                                 // Only for use with select semi-analytic models.
   double              mvir; // Halo mass (Msun/h).
   double              rvir; // Halo radius (kpc/h comoving).
   double              rs; // Scale radius (kpc/h comoving).
   double              vrms; // Velocity dispersion (km/s physical).
   bool                mmp; // Whether the halo is the most massive progenitor or not.
   double              scale_of_last_mm; // Scale factor of the last major merger (mass ratio > 0.3).
   double              vmax; // Maximum circular velocity (km/s physical).
   double              x, y, z; // Halo position (Mpc/h comoving).
   double              vx, vy, vz; // Halo velocity (km/s physical).
   double              jx, jy, jz; // Halo angular momenta ((Msub/h)*(Mpc/h)*km/s physical).
   double              spin; // Halo spin parameter.
   unsigned            breadth_first_id; // Breadth-first ordering of halos within a tree.
   unsigned            depth_first_id; // Depth-first ordering of halos withing a tree.
   unsigned long long  tree_root_id; // ID of the halo at the last timestep in the tree.
   unsigned long long  orig_halo_id; // Original halo ID from the halo finder.
   unsigned            snap_num; // Snapshot number from which halo originated.
   unsigned            next_coprog_depthfirst_id; // Depth-first ID of next coprogenitor.
   unsigned            last_coprog_depthfirst_id; // Depth-first ID of last progenitor.
   double              rs_klypin; // Scale radius determined using Vmax and Mvir (see Rockstar paper).
   double              mvir_all; // Mass enclosed within the specified overdensity, including unbound
                                 // particles (Msun/h).
   double              m200b_m2500c[4]; // Mass enclosed within specified overdensities (Msun/h).
   double              x_offs; // Offset of density peak from average particle position (kpc/h comoving).
   double              v_offs; // Offset of density peak from average particle velocity (km/s physical).
   double              spin_bullock; // Bullock spin parameter (J/(sqrt(2)*GMVR)).
   double              b_to_a, c_to_a; // Ration of second and third largest shape ellipsoid axes (B and C)
                                       // to largest shape ellipsoid axis (A) (dimensionless).
   double              ax, ay, az; // Largest shape ellipsoid axis (kpc/h comoving).
};

///
/// The ? halo finder structure.
///
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

///
/// Read past any comments.
///
void
skip_comments( std::ifstream& file )
{
   if( file.peek() == '#' )
      file.ignore( std::numeric_limits<std::streamsize>::max(), '\n' );
   ASSERT( file );
}

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );

   ASSERT( argc > 1 );
   LOG_CONSOLE();

   // Keep processing files from 0 onwards until we cannot open a file.
   unsigned file_idxs[3] = {0, 0, 0};
   while( 1 )
   {
      // Define our file now, before the loop.
      std::ifstream src_file;

      // Try and open the file with current indices.
      for( unsigned ii = 3; ii > 1; --ii )
      {
         // Try to open the file.
         string filename = boost::str( boost::format( "tree_%1%_%2%_%3%.dat" ) % file_idxs[0] % file_idxs[1] % file_idxs[2] );
         LOGILN( "Trying to open file \"", filename, "\"" );
         src_file.open( filename, std::ios::in );

         // If it succeeded, process it.
         if( src_file )
         {
            LOGILN( "Success." );
            break;
         }

         // Advance the indices.
         file_idxs[ii - 1] = 0;
         ++file_idxs[ii - 2];
      }
      if( !src_file )
      {
         LOGILN( "Finished, terminating loop." );
         break;
      }

      // Read the number of trees in this file.
      skip_comments( src_file );
      unsigned num_trees;
      src_file >> num_trees;
      ASSERT( src_file );
      LOGILN( "File has ", num_trees, " trees." );

      // Loop over the number of trees in order to process each of them.
      for( unsigned ii = 0; ii < num_trees; ++ii )
      {
         // Read each field in turn.
         bolshoi_halo_type bh;
         src_file >> bh.scale >> bh.id >> bh.desc_scale >> bh.desc_id >> bh.num_prog >> bh.pid
                  >> bh.upid >> bh.desc_pid >> bh.phantom >> bh.sam_mvir >> bh.mvir
                  >> bh.rvir >> bh.rs >> bh.vrms >> bh.mmp >> bh.scale_of_last_mm >> bh.vmax
                  >> bh.x >> bh.y >> bh.z >> bh.vx >> bh.vy >> bh.vz >> bh.jx >> bh.jy
                  >> bh.jz >> bh.spin >> bh.breadth_first_id >> bh.depth_first_id
                  >> bh.tree_root_id >> bh.orig_halo_id >> bh.snap_num
                  >> bh.next_coprog_depthfirst_id >> bh.last_coprog_depthfirst_id
                  >> bh.rs_klypin >> bh.mvir_all >> bh.m200b_2500c >> bh.x_offs
                  >> bh.v_offs >> bh.spin_bullock >> bh.b_to_a >> bh.c_to_a
                  >> bh.ax >> bh.ay >> bh.az;
         ASSERT( src_file );

         // I'm not entirely sure I'm reading all the fields. Skip anything remaining on this line.
         src_file.ignore( 1024, '\n' );
      }
   }

   mpi::finalise();
   return EXIT_SUCCESS;
}
