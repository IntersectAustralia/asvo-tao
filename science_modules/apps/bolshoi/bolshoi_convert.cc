#include <cstdlib>
#include <iostream>
#include <omp.h>
#include <boost/lexical_cast.hpp>
#include <boost/iostreams/filtering_stream.hpp>
#include <boost/iostreams/filter/gzip.hpp>
#include <libhpc/libhpc.hh>
#include "exporter.hh"

using namespace hpc;

///
/// Tunable parameters.
///
const unsigned num_threads = 1;
const unsigned num_halos_per_file = 50000;
const float   update_every = 10.0;
const unsigned global_file_offset = 0;

///
/// Constants.
///
const float particle_mass = 1.35e8;
const float newton_gravitation = 6.67428e-11;
const float solar_mass = 1.98892e30;
const float m_per_kpc = 3.08568025e19;

///
/// OpenMP shared variables.
///
unsigned file_offsets[num_threads];

///
/// The Bolshoi halo data structure.
///
struct bolshoi_halo_type
{
   // float     scale; // Scale factor of halo.
   long long  id; // ID of halo (unique across entire simulation).
   // float     desc_scale; // Scale of descendant halo, if applicable.
   long long  desc_id; // ID of descendant halo, if applicable.
   unsigned   num_prog; // Number of progenitors.
   long long  pid; // Host halo ID.
   // long long  upid; // Most massive host halo ID (only different from pid in
   //                  // cases of sub-subs or sub-sub-subs etc.
   // long long  desc_pid; // pid of descendant halo, if applicable.
   // int        phantom; // Nonzero for halos interpolated across timesteps.
   // float     sam_mvir; // Halo mass, smoothed across accretion history; always greater
   //                      // than sum of halo masses of contributing progenitors (Msun/h).
   //                      // Only for use with select semi-analytic models.
   float     mvir; // Halo mass (Msun/h).
   float     rvir; // Halo radius (kpc/h comoving).
   // float     rs; // Scale radius (kpc/h comoving).
   float     vrms; // Velocity dispersion (km/s physical).
   // int        mmp; // Whether the halo is the most massive progenitor or not.
   // float     scale_of_last_mm; // Scale factor of the last major merger (mass ratio > 0.3).
   float     vmax; // Maximum circular velocity (km/s physical).
   float     x, y, z; // Halo position (Mpc/h comoving).
   float     vx, vy, vz; // Halo velocity (km/s physical).
   float     jx, jy, jz; // Halo angular momenta ((Msub/h)*(Mpc/h)*km/s physical).
   float     spin; // Halo spin parameter.
   // unsigned   breadth_first_id; // Breadth-first ordering of halos within a tree.
   // unsigned   depth_first_id; // Depth-first ordering of halos withing a tree.
   // long long  tree_root_id; // ID of the halo at the last timestep in the tree.
   // long long  orig_halo_id; // Original halo ID from the halo finder.
   unsigned   snap_num; // Snapshot number from which halo originated.
   // unsigned   next_coprog_depthfirst_id; // Depth-first ID of next coprogenitor.
   // unsigned   last_coprog_depthfirst_id; // Depth-first ID of last progenitor.
   // float     rs_klypin; // Scale radius determined using Vmax and Mvir (see Rockstar paper).
   // float     mvir_all; // Mass enclosed within the specified overdensity, including unbound
   //                      // particles (Msun/h).
   // float     m200b_m2500c[4]; // Mass enclosed within specified overdensities (Msun/h).
   // float     x_offs; // Offset of density peak from average particle position (kpc/h comoving).
   // float     v_offs; // Offset of density peak from average particle velocity (km/s physical).
   // float     spin_bullock; // Bullock spin parameter (J/(sqrt(2)*GMVR)).
   // float     b_to_a, c_to_a; // Ration of second and third largest shape ellipsoid axes (B and C)
   //                            // to largest shape ellipsoid axis (A) (dimensionless).
   // float     ax, ay, az; // Largest shape ellipsoid axis (kpc/h comoving).
};

///
/// The SAGE compatible halo finder structure.
///
struct sage_halo_type
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

struct mass_compare_type
{
   mass_compare_type( const vector<bolshoi_halo_type>& forest )
      : forest( forest )
   {
   }

   bool
   operator()( unsigned op_a,
	       unsigned op_b )
   {
      return forest[op_a].mvir > forest[op_b].mvir;
   }

   const vector<bolshoi_halo_type>& forest;
};

// std::ostream&
// operator<<( std::ostream& strm,
//             const bolshoi_halo_type& obj )
// {
//    strm << "{scale: " << obj.scale;
//    strm << ", id: " << obj.id;
//    strm << ", desc_scale: " << obj.desc_scale;
//    strm << ", desc_id: " << obj.desc_id;
//    strm << ", num_prog: " << obj.num_prog;
//    strm << ", pid: " << obj.pid;
//    strm << ", upid: " << obj.upid;
//    strm << ", desc_pid: " << obj.desc_pid;
//    strm << ", phantom: " << obj.phantom;
//    strm << ", sam_mvir: " << obj.sam_mvir;
//    strm << ", mvir: " << obj.mvir;
//    strm << ", rs: " << obj.rs;
//    strm << ", vrms: " << obj.vrms;
//    strm << ", mmp: " << obj.mmp;
//    strm << ", scale_of_last_mm: " << obj.scale_of_last_mm;
//    strm << ", vmax: " << obj.vmax;
//    strm << ", x: " << obj.x;
//    strm << ", y: " << obj.y;
//    strm << ", z: " << obj.z;
//    strm << ", vx: " << obj.vx;
//    strm << ", vy: " << obj.vy;
//    strm << ", vz: " << obj.vz;
//    strm << ", jx: " << obj.jx;
//    strm << ", jy: " << obj.jy;
//    strm << ", jz: " << obj.jz;
//    strm << ", spin: " << obj.spin;
//    // unsigned            breadth_first_id; // Breadth-first ordering of halos within a tree.
//    // unsigned            depth_first_id; // Depth-first ordering of halos withing a tree.
//    // long long  tree_root_id; // ID of the halo at the last timestep in the tree.
//    // long long  orig_halo_id; // Original halo ID from the halo finder.
//    strm << ", snap_num: " << obj.snap_num << "}";
//    // unsigned            next_coprog_depthfirst_id; // Depth-first ID of next coprogenitor.
//    // unsigned            last_coprog_depthfirst_id; // Depth-first ID of last progenitor.
//    // float              rs_klypin; // Scale radius determined using Vmax and Mvir (see Rockstar paper).
//    // float              mvir_all; // Mass enclosed within the specified overdensity, including unbound
//    //                               // particles (Msun/h).
// }

bool
id_map_has( const vector<std::pair<long long,unsigned>>& id_map,
	    long long id )
{
   return std::binary_search( id_map.begin(), id_map.end(), id, hpc::less_first<std::pair<long long,unsigned>>() );
}

unsigned
id_map_get( const vector<std::pair<long long,unsigned>>& id_map,
	    long long id )
{
   auto it = std::lower_bound( id_map.begin(), id_map.end(), id, hpc::less_first<std::pair<long long,unsigned>>() );
   ASSERT( it != id_map.end() );
   return it->second;
}

void
convert_ids( vector<bolshoi_halo_type>& forest,
	     const vector<std::pair<long long,unsigned>>& id_map )
	     // const map<long long,unsigned>& id_map )
{
   for( auto& halo : forest )
   {
      halo.id = id_map_get( id_map, halo.id );
      if( halo.pid != -1 )
	 halo.pid = id_map_get( id_map, halo.pid );
      if( halo.upid != -1 )
	 halo.upid = id_map_get( id_map, halo.upid );
      if( halo.desc_id != -1 )
	 halo.desc_id = id_map_get( id_map, halo.desc_id );
      if( halo.desc_pid != -1 )
	 halo.desc_pid = id_map_get( id_map, halo.desc_pid );
   }
}

long long
top_pid( const vector<bolshoi_halo_type>& forest,
	 long long pid )
{
   long long tmp = pid;
   while( tmp != -1 )
   {
      pid = tmp;
      tmp = forest[pid].pid;
   }
   return pid;
}

void
bolshoi_to_sage( const vector<bolshoi_halo_type>& forest,
		 const csr<unsigned>& progens,
		 const map<long long,unsigned>& fof_group_map,
		 const csr<unsigned>& fof_groups,
		 vector<sage_halo_type>& sage_tree )
{
   LOGDLN( "Converting structures.", setindent( 2 ) );

   // Copy basic info.
   LOGD( "Copying basic information... " );
   for( unsigned ii = 0; ii < forest.size(); ++ii )
   {
      const bolshoi_halo_type& bh = forest[ii];
      sage_halo_type& sh = sage_tree[ii];

      sh.descendant              = bh.desc_id;
      sh.first_progenitor        = -1;
      sh.next_progenitor         = -1;
      sh.first_halo_in_fof_group = -1;
      sh.next_halo_in_fof_group  = -1;
      sh.Len                     = bh.mvir/particle_mass;
      sh.M_Mean200               = 0.0;
      sh.Mvir                    = bh.mvir/1e10;
      sh.M_TopHat                = 0.0;
      sh.Pos[0]                  = bh.x;
      sh.Pos[1]                  = bh.y;
      sh.Pos[2]                  = bh.z;
      sh.Vel[0]                  = bh.vx;
      sh.Vel[1]                  = bh.vy;
      sh.Vel[2]                  = bh.vz;
      sh.VelDisp                 = bh.vrms;
      sh.Vmax                    = bh.vmax;

      // Spin needs some processing.
      float vvir = 1e-3*sqrt( newton_gravitation*bh.mvir*solar_mass/(bh.rvir*m_per_kpc) );
      float spin_amp = bh.spin/sqrt( bh.jx*bh.jx + bh.jy*bh.jy + bh.jz*bh.jz );
      sh.Spin[0]                 = bh.jx*spin_amp*sqrt( 2.0 )*bh.rvir*vvir;
      sh.Spin[1]                 = bh.jy*spin_amp*sqrt( 2.0 )*bh.rvir*vvir;
      sh.Spin[2]                 = bh.jz*spin_amp*sqrt( 2.0 )*bh.rvir*vvir;

      sh.MostBoundID             = 0;
      sh.SnapNum                 = bh.snap_num;
      sh.FileNr                  = 0;
      sh.SubhaloIndex            = 0;
      sh.SubHalfMass             = 0.0;
   }
   LOGDLN( "done." );

   // Process progenitor information.
   LOGD( "Processing progenitor information... " );
   for( unsigned ii = 0; ii < progens.num_rows(); ++ii )
   {
      const auto& row = progens[ii];
      if( row.size() )
      {
	 ASSERT( sage_tree[ii].first_progenitor == -1 );
	 sage_tree[ii].first_progenitor = row[0];
	 for( unsigned jj = 1; jj < row.size(); ++jj )
	 {
	    ASSERT( sage_tree[row[jj - 1]].next_progenitor == -1 );
	    sage_tree[row[jj - 1]].next_progenitor = row[jj];
	 }
      }
   }
   LOGDLN( "done." );

   // Process FOF group information.
   LOGD( "Processing FOF group information... " );
   for( const auto& fof_pair : fof_group_map )
   {
      long long upid = fof_pair.first;
      unsigned ii = fof_pair.second;
      const auto& row = fof_groups[ii];

      // First halo in FOF group should be the most massive, i.e. the
      // first halo in any group should point to itself.
      ASSERT( forest[row[0]].id == upid &&
	      (forest[row[0]].upid == -1 || forest[row[0]].upid == forest[row[0]].id ) );

      for( unsigned jj = 0; jj < row.size(); ++jj )
      {
	 ASSERT( sage_tree[row[jj]].first_halo_in_fof_group == -1 );
	 sage_tree[row[jj]].first_halo_in_fof_group = upid;
      }
      for( unsigned jj = 1; jj < row.size(); ++jj )
      {
	 ASSERT( sage_tree[row[jj - 1]].next_halo_in_fof_group == -1 );
	 sage_tree[row[jj - 1]].next_halo_in_fof_group = row[jj];
      }
   }
   LOGDLN( "done." );

#ifndef NDEBUG
   LOGDLN( "Checking sanity of conversion.", setindent( 2 ) );

   // Trees must be the same size.
   ASSERT( sage_tree.size() == forest.size() );

   // Check progenitors against dscendents.
   LOGDLN( "Checking progenitors.", setindent( 2 ) );
   for( unsigned ii = 0; ii < sage_tree.size(); ++ii )
   {
      int prog = sage_tree[ii].first_progenitor;
      unsigned num_prog = 0;
      while( prog != -1 )
      {
	 LOGDLN( "Progenitor with local ID ", prog, setindent( 2 ) );

	 int desc = sage_tree[prog].descendant;

	 // Must be self-consistent.
	 ASSERT( desc == ii );
	 LOGDLN( "Is self-consistent." );

	 // Must match Bolshoi.
	 ASSERT( forest[prog].desc_id != -1 );
	 ASSERT( forest[prog].desc_id == desc );
	 LOGDLN( "Matches Bolshoi." );

	 // Advance.
	 prog = sage_tree[prog].next_progenitor;
	 ++num_prog;

	 LOGD( setindent( -2 ) );
      }

      // Counts must match.
      ASSERT( num_prog == forest[ii].num_prog );
   }
   LOGDLN( "Done.", setindent( -2 ) );

   // Check FOF groups.
   LOGDLN( "Checking FOF groups.", setindent( 2 ) );
   for( unsigned ii = 0; ii < sage_tree.size(); ++ii )
   {
      int fof = sage_tree[ii].first_halo_in_fof_group;
      LOGDLN( "FOF with local halo ID ", fof );

      // In SAGE every halo belongs to a FOF group.
      ASSERT( fof >= 0 );

      // Single FOF groups will have -1 in upid or upid == id.
      bool single = (sage_tree[fof].next_halo_in_fof_group == -1);
      if( single )
      {
	 LOGDLN( "Single FOF group." );
      	 ASSERT( forest[ii].upid == -1 || forest[ii].upid == forest[ii].id );
      }

      // Otherwise upid must match fof or ID must match fof.
      else
      {
	 LOGDLN( "Multi FOF group." );
	 if( forest[ii].upid != -1 )
	    ASSERT( forest[ii].upid == fof );
	 else
	    ASSERT( forest[ii].id == fof );
      }
   }
   LOGDLN( "Done.", setindent( -2 ) );

   LOGDLN( "Done.", setindent( -2 ) );
#endif

   LOGDLN( "Done.", setindent( -2 ) );
}

void
build_progenitors( const vector<bolshoi_halo_type>& forest,
		   csr<unsigned>& progens )
{
   LOG_ENTER();
   LOGDLN( "Building progenitors.", setindent( 2 ) );

   progens.clear();

   // First construct the counts and setup the arrays.
   progens.num_rows( forest.size() );
   {
      auto cnts = progens.counts();
      unsigned ii = 0;
      for( const auto& bh : forest )
	 cnts[ii++] = bh.num_prog;
      progens.setup_array( true );
   }

   // Fill each array.
   vector<unsigned> cnts( forest.size() );
   std::fill( cnts.begin(), cnts.end(), 0 );
   for( const auto& bh : forest )
   {
      if( bh.desc_id != -1 )
      {
	 unsigned id = bh.desc_id;
	 progens( id, cnts[id]++ ) = bh.id;
      }
   }

   // Order the progenitors for each halo with most massive first.
   mass_compare_type cmp( forest );
   for( unsigned ii = 0; ii < progens.num_rows(); ++ii )
   {
      auto row = progens[ii];
      std::sort( row.begin(), row.end(), cmp );
   }

#ifndef NDEBUG
   // Check each set of progenitors.
   LOGDLN( "Checking consistency.", setindent( 2 ) );
   for( unsigned ii = 0; ii < progens.num_rows(); ++ii )
   {
      auto row = progens[ii];
      LOGD( "Halo ", ii, " with ", row.size(), " progenitors... " );

      // No duplicates.
      set<unsigned> dup;
      dup.insert( row.begin(), row.end() );
      ASSERT( dup.size() == row.size() );

      // Descendants must match.
      for( auto prog : row )
	 ASSERT( forest[prog].desc_id == ii );

      // Must be in most massive order.
      for( unsigned jj = 1; jj < row.size(); ++jj )
	 ASSERT( forest[row[jj]].mvir <= forest[row[jj - 1]].mvir );

      LOGDLN( "okay." );
   }
   LOGDLN( "Done.", setindent( -2 ) );
#endif

   LOGDLN( "Done.", setindent( -2 ) );
   LOG_EXIT();
}

void
build_fof_groups( const vector<bolshoi_halo_type>& forest,
		  map<long long,unsigned>& fof_group_map,
		  csr<unsigned>& fof_groups )
{
   LOG_ENTER();
   LOGDLN( "Building FOF groups.", setindent( 2 ) );

   fof_group_map.clear();
   fof_groups.clear();

   // I need a mapping from the UPID identifying the most massive
   // halo in a FOF group (the parent halo) to the local FOF group
   // index.
   for( const auto& halo : forest )
   {
      long long upid = (halo.upid != -1) ? halo.upid : halo.id;
      auto it = fof_group_map.insert( upid );
      if( it.second )
	 it.first->second = fof_group_map.size() - 1;
   }
   LOGDLN( "Found ", fof_group_map.size(), " FOF groups." );

   // First construct the counts and setup the arrays.
   fof_groups.num_rows( fof_group_map.size() );
   {
      auto cnts = fof_groups.counts();
      std::fill( cnts.begin(), cnts.end(), 0 );
      for( const auto& bh : forest )
      {
	 long long upid = (bh.upid != -1) ? bh.upid : bh.id;
	 unsigned id = fof_group_map.get( upid );
	 cnts[id]++;
      }
      LOGDLN( "FOF group counts: ", cnts );
      fof_groups.setup_array( true );
   }

   // Fill each array.
   vector<unsigned> cnts( fof_group_map.size() );
   std::fill( cnts.begin(), cnts.end(), 0 );
   for( const auto& bh : forest )
   {
      long long upid = (bh.upid != -1) ? bh.upid : bh.id;
      unsigned id = fof_group_map.get( upid );
      fof_groups( id, cnts[id]++ ) = bh.id;
   }

   // Order the FOF groups for each halo with most massive first.
   mass_compare_type cmp( forest );
   for( unsigned ii = 0; ii < fof_groups.num_rows(); ++ii )
   {
      auto row = fof_groups[ii];
      std::sort( row.begin(), row.end(), cmp );
   }

   // There are cases where the most massive FOF is not
   // the host halo. We need to find these cases and swap
   // them.
   for( auto fof_pair : fof_group_map )
   {
      unsigned fof_id = fof_pair.first;
      unsigned ii = fof_pair.second;
      auto row = fof_groups[ii];

      if( forest[row[0]].id != fof_id )
      {
	 unsigned jj = 1;
	 for( ; jj < row.size(); ++jj )
	 {
	    if( forest[row[jj]].id == fof_id )
	       break;
	 }
	 ASSERT( jj < row.size() );
	 LOGDLN( "Swapping misplaced host halo FOF index." );
	 std::swap( row[0], row[jj] );
      }
   }

#ifndef NDEBUG
   // Check each set of FOF halos.
   LOGDLN( "Checking consistency.", setindent( 2 ) );
   for( auto fof_pair : fof_group_map )
   {
      unsigned fof_id = fof_pair.first;
      unsigned ii = fof_pair.second;
      auto row = fof_groups[ii];
      LOGDLN( "FOF group ", ii, " with ", row.size(), " halos.", setindent( 2 ) );
      LOGDLN( "upid: ", fof_id );
      LOGD( "FOF IDs: [", forest[row[0]].id );
      for( unsigned jj = 1; jj < row.size(); ++jj )
	 LOGD( ", ", forest[row[jj]].id );
      LOGDLN( "]" );
      LOGD( "FOF masses: [", forest[row[0]].mvir );
      for( unsigned jj = 1; jj < row.size(); ++jj )
	 LOGD( ", ", forest[row[jj]].mvir );
      LOGDLN( "]" );

      // No duplicates.
      set<unsigned> dup;
      dup.insert( row.begin(), row.end() );
      ASSERT( dup.size() == row.size() );

      // FOF entries must match up.
      for( auto halo : row )
      {
	 if( forest[halo].upid != -1 )
	    ASSERT( forest[halo].upid == fof_id );
	 else
	    ASSERT( forest[halo].id == fof_id );
      }

      // // Must be in most massive order. Unfortunately this won't be
      // // true now that I'm reordering to fix Bolshoi problems.
      // for( unsigned jj = 1; jj < row.size(); ++jj )
      // 	 ASSERT( forest[row[jj]].mvir <= forest[row[jj - 1]].mvir );

      // The first halo in the FOF group must have the same ID as
      // the FOF group has been given.
      ASSERT( forest[row[0]].id == fof_id );

      LOGDLN( "Done.", setindent( -2 ) );
   }
   LOGDLN( "Done.", setindent( -2 ) );
#endif

   LOGDLN( "Done.", setindent( -2 ) );
   LOG_EXIT();
}

///
/// Finish processing a single Bolshoi forest.
///
void
process_forest( vector<bolshoi_halo_type>& forest,
		vector<std::pair<long long,unsigned>>& id_map,
		// map<long long,unsigned>& id_map,
		exporter& exp )
{
   LOGILN( "Post processing forest.", setindent( 2 ) );

   // First need to prepare the ID map.
   std::sort( id_map.begin(), id_map.end(), hpc::less_first<std::pair<long long,unsigned>>() );

#ifndef NDEBUG
   // Check that the ID map and the tree are consistent.
   for( auto ids : id_map )
      ASSERT( ids.first == forest[ids.second].id );

   for( const auto& halo : forest )
   {
      // Check that each referenced ID is in this forest.
      ASSERT( id_map_has( id_map, halo.id ) );
      if( halo.desc_id != -1 )
	 ASSERT( id_map_has( id_map, halo.desc_id ) );
      if( halo.pid != -1 )
	 ASSERT( id_map_has( id_map, halo.pid ) );
      if( halo.upid != -1 )
	 ASSERT( id_map_has( id_map, halo.upid ) );
      if( halo.desc_pid != -1 )
	 ASSERT( id_map_has( id_map, halo.desc_pid ) );

      // Check that the x,y,z position is in range.
      ASSERT( halo.x >= 0.0 && halo.x <= 250.0 );
      ASSERT( halo.y >= 0.0 && halo.y <= 250.0 );
      ASSERT( halo.z >= 0.0 && halo.z <= 250.0 );
   }

   // Walk each halo's host halo chain and make sure all masses are larger
   // the further up the chain we go. Also check that host and subhalos
   // exist in the same snapshot.
   for( const auto& halo : forest )
   {
      long long pid = halo.pid;
      float mass = halo.mvir;
      unsigned snap_num = halo.snap_num;
      while( pid != -1 )
      {
   	 unsigned id = id_map_get( id_map, pid );

// 	 // Need to confirm that each host halo has greater mass than
// 	 // all subhalos, as these subhalos are included in the mass
// 	 // of parent halos.
//    	 // ASSERT( forest[id].mvir >= mass );
// 	 if( forest[id].mvir < mass )
// 	 {
// 	    LOGDLN( "Found a host halo with lower mass than subhalo." );
// #pragma omp critical
// 	    {
// 	       std::ofstream bmf( "bad_mass.dat", std::ios::out | std::ios::app );
// 	       ASSERT( bmf );
// 	       bmf << pid << "  " << forest[id].mvir << "  " << halo.id << "  " << mass << "\n";
// 	    }
// 	 }

	 // Snapshot numbers must match parents.
	 ASSERT( forest[id].snap_num == snap_num );

	 // Move to parent.
   	 pid = forest[id].pid;
      }
   }
#endif

   // First, convert all the IDs so we can free the ID map, which can be huge.
   convert_ids( forest, id_map );
   id_map.deallocate();

   // Convert all the UPID values to their actual top most containing halo.
   // I need to do this because it seems UPID does not actually point to
   // this, and I need it to.
   for( auto& halo : forest )
      halo.upid = top_pid( forest, halo.pid );

   // Build the progenitors.
   csr<unsigned> progens;
   build_progenitors( forest, progens );

   // Build the FOF groups.
   map<long long,unsigned> fof_group_map;
   csr<unsigned> fof_groups;
   build_fof_groups( forest, fof_group_map, fof_groups );

   // Convert to sage format.
   vector<sage_halo_type> sage_tree( forest.size() );
   bolshoi_to_sage( forest, progens, fof_group_map, fof_groups, sage_tree );

   // Save current sage tree.
   exp.export_forest( sage_tree );

   LOGILN( "Done.", setindent( -2 ) );
}

void
load_forests( multimap<long long,long long>& forests,
	      set<long long>& forest_ids )
{
   LOG_ENTER();

   // Open the gzip stream.
   std::ifstream file( "forests.list", std::ios_base::in );

   // There will be at least one commented line at the start.
   skip_comments( file );

   // Then each line will have a tree ID and a forest ID.
   forests.clear();
   while( file.peek() != '\n' && !file.eof() )
   {
      long long tree, forest;
      file >> tree >> forest;
      finish_line( file );
      ASSERT( !file.fail() );
      forests.insert( forest, tree );
      forest_ids.insert( forest );
   }

   // Select which forests to process. Do half at a time.
   unsigned num_forests = 600;
   auto it = forest_ids.begin();
   unsigned ii = 0;
   for( ; ii < num_forests; ++ii )
      ++it;
   for( ; ii < forest_ids.size(); ++ii )
   {
      long long id = *it;
      auto to_go = it++;
      forest_ids.erase( to_go );
      forests.erase( id );
   }

   LOG_EXIT();
}

void
load_locations( map<long long,std::pair<unsigned,size_t>>& locations,
		map<unsigned,string>& file_map )
{
   LOG_ENTER();

   // Clear structures.
   locations.clear();
   file_map.clear();

   // Open the gzip stream.
   std::ifstream file( "locations.dat", std::ios_base::in );

   // There will be at least one commented line at the start.
   skip_comments( file );

   // Then each line will have a tree ID and a forest ID.
   while( file.peek() != '\n' && !file.eof() )
   {
      long long tree, file_id;
      size_t offset;
      string filename;
      file >> tree >> file_id >> offset >> filename;
      finish_line( file );
      ASSERT( !file.fail() );
      locations.insert( tree, std::make_pair( file_id, offset ) );
#ifndef NDEBUG
      if( file_map.has( file_id ) )
	 ASSERT( file_map.get( file_id ) == filename );
#endif
      file_map.insert( file_id, filename );
   }

   LOG_EXIT();
}

void
load_counts( const set<long long>& forest_ids,
	     map<long long,unsigned>& counts )
{
   LOG_ENTER();

   counts.clear();

   // Open the gzip stream.
   std::ifstream file( "counts.dat", std::ios_base::in );

   // Then each line will have a tree ID and a forest ID.
   while( file.peek() != '\n' && !file.eof() )
   {
      long long forest;
      unsigned cnt;
      file >> forest >> cnt;
      finish_line( file );
      ASSERT( !file.fail() );
      if( forest_ids.has( forest ) )
	 counts.insert( forest, cnt );
   }

   LOG_EXIT();
}

int
main( int argc,
      char* argv[] )
{
   LOG_PUSH( new logging::omp::file( "conv.", 0 ) );

   // Using nohup ruins cout logging. Open a file to log to.
   std::ofstream log_file( "conv.log", std::ios::out );

   // Keep track of how many Halos each thread has seen.
   unsigned long long halos_seen[num_threads];
   unsigned long long forests_seen[num_threads];
   unsigned long long total_halos_seen, total_forests_seen;
   unix::time_type since_update;
   std::fill( halos_seen, halos_seen + num_threads, 0 );
   std::fill( forests_seen, forests_seen + num_threads, 0 );

   log_file << "Loading auxilliary tables... ";
   log_file.flush();

   // Load in tables needed to locate FOF groups.
   multimap<long long,long long> forests;
   set<long long> forest_ids;
   map<long long,std::pair<unsigned,size_t>> locations;
   map<unsigned,string> file_map;
   map<long long,unsigned> counts;
   LOGILN( "Loading forests... ", setindent( 2 ) );
   load_forests( forests, forest_ids );
   LOGILN( "Done.", setindent( -2 ) );
   LOGILN( "Loading locations... ", setindent( 2 ) );
   load_locations( locations, file_map );
   LOGILN( "Done.", setindent( -2 ) );
   LOGILN( "Loading counts... ", setindent( 2 ) );
   load_counts( forest_ids, counts );
   LOGILN( "Done.", setindent( -2 ) );

   log_file << "done.\n";
   log_file << "Processing " << forest_ids.size() << " forests.\n";
   log_file << "Beginning conversion...\n";
   log_file.flush();

   // How many forests are we working with?
   size_t num_forests = forest_ids.size();
   LOGILN( "Have ", num_forests, " forests to process." );

   // Setup the number of threads to use.
   omp_set_num_threads( num_threads );
   LOGILN( "Running with ", num_threads, " threads." );

   // Calculate for each thread the start and finish offsets. I will
   // do this by balancing the number of halos (approximately) each
   // will have to process. First count the total number of halos
   // we have.
   LOGILN( "Distributing.", setindent( 2 ) );
   unsigned long long net_halos = 0;
   for( auto& cnt_pair : counts )
      net_halos += cnt_pair.second;
   unsigned long long halos_per_thread = net_halos/num_threads;
   LOGILN( net_halos, " total halos, giving ~", halos_per_thread, " per thread." );

   // Now add forests to each thead until they reach the balance point.
   vector<set<long long>::const_iterator> start_it( num_threads ), finish_it( num_threads );
   vector<unsigned long long> num_thread_halos( num_threads );
   vector<unsigned> num_thread_forests( num_threads );
   for( unsigned ii = 0; ii < num_threads; ++ii )
   {
      if( ii == 0 )
	 start_it[ii] = forest_ids.begin();
      else
	 start_it[ii] = finish_it[ii - 1];
      finish_it[ii] = start_it[ii];
      ++finish_it[ii];
      num_thread_halos[ii] = counts.get( *start_it[ii] );
      num_thread_forests[ii] = 1;
      while( finish_it[ii] != forest_ids.end() && num_thread_halos[ii] < halos_per_thread )
      {
	 num_thread_halos[ii] += counts.get( *finish_it[ii] );
	 ++num_thread_forests[ii];
	 ++finish_it[ii];
      }
      LOGILN( "Thread ", ii, " has ", num_thread_forests[ii], " forests and ", num_thread_halos[ii], " halos."  );

      log_file << "Thread " << ii << " has " << num_thread_forests[ii] << " forests and " << num_thread_halos[ii] << " halos.\n";
   }

   // Finished distributing.
   LOGILN( "Done.", setindent( -2 ) );

   // Kick off the update timer.
   since_update = unix::timer();

   // Form a team of threads here.
#pragma omp parallel
   {
      int tid = omp_get_thread_num();
      LOGILN( "Thread ", tid, " active." );

      // Create the exporter.
      exporter exp( start_it[tid], finish_it[tid], counts );

      // Loop over our section of the forests.
      unsigned long long forest_idx = 0;
      while( start_it[tid] != finish_it[tid] )
      {
	 auto cur_forest = *start_it[tid]++;
	 LOGILN( "Processing forest ", forest_idx, ".", setindent( 2 ) );

	 // Count how many trees are in this forest.
	 unsigned num_trees = forests.count( cur_forest );
	 LOGILN( "Number of trees in forest: ", num_trees );

	 // Use a mapping to map from global Bolshoi tree IDs to
	 // local tree IDs for SAGE.
	 vector<std::pair<long long,unsigned>> id_map( counts.get( cur_forest ) );
	 long long cur_halo = 0;

	 // Store current forest in a vector of halos.
	 vector<bolshoi_halo_type> bol_forest( counts.get( cur_forest ) );

	 // TODO: Remove.
	 log_file << "Allocated " << bol_forest.size()*sizeof(bolshoi_halo_type) << "\n";
	 log_file.flush();

	 // Select the range of trees we need to process and
	 // iterate over each tree.
	 // NOTE: Looks like 'equal_range' is not thread safe.
	 unsigned tree_idx = 0;
	 auto tree_rng = forests.equal_range( cur_forest );
	 while( tree_rng.first != tree_rng.second )
	 {
	    auto cur_tree = (*tree_rng.first++).second;
	    LOGILN( "Processing tree ", tree_idx, ".", setindent( 2 ) );

	    // Map to the location information.
	    auto loc = locations.get( cur_tree );

	    // Open the file in which the tree lives then scan to
	    // the appropriate offset for the tree.
	    LOGDLN( "Opening file \"", file_map.get( loc.first ), "\"." );
	    std::ifstream src_file( file_map.get( loc.first ), std::ios::in );
	    ASSERT( src_file );
	    LOGDLN( "Seeking to ", loc.second, "." );
	    src_file.seekg( loc.second );
	    ASSERT( src_file );

	    // We aren't given information about how many halos are in
	    // each tree, so we just have to loop until we hit the end
	    // of the file.
	    while( src_file.peek() != '#' && !src_file.eof()  )
	    {
	       LOGDLN( "Processing halo ", cur_halo, ".", setindent( 2 ) );

	       // Put this halo on the back of the current tree.
	       bolshoi_halo_type& bh = bol_forest[cur_halo];

	       // Read each field in turn.
	       src_file >> bh.scale >> bh.id >> bh.desc_scale >> bh.desc_id >> bh.num_prog >> bh.pid
	       		>> bh.upid >> bh.desc_pid >> bh.phantom >> bh.sam_mvir >> bh.mvir
	       		>> bh.rvir >> bh.rs >> bh.vrms >> bh.mmp >> bh.scale_of_last_mm >> bh.vmax
	       		>> bh.x >> bh.y >> bh.z >> bh.vx >> bh.vy >> bh.vz >> bh.jx >> bh.jy
	       		>> bh.jz >> bh.spin >> bh.breadth_first_id >> bh.depth_first_id
	       		>> bh.tree_root_id >> bh.orig_halo_id >> bh.snap_num
	       		>> bh.next_coprog_depthfirst_id >> bh.last_coprog_depthfirst_id
	       		>> bh.rs_klypin >> bh.mvir_all >> bh.m200b_m2500c[0] >> bh.m200b_m2500c[1]
	       		>> bh.m200b_m2500c[2] >> bh.m200b_m2500c[3] >> bh.x_offs
	       		>> bh.v_offs >> bh.spin_bullock >> bh.b_to_a >> bh.c_to_a
	       		>> bh.ax >> bh.ay >> bh.az;
	       finish_line( src_file );
	       ASSERT( !src_file.fail() );
	       LOGDLN( "ID: ", bh.id );
	       LOGDLN( "Position: ", bh.x, ", ", bh.y, ", ", bh.z );
	       LOGDLN( "Mvir: ", bh.mvir );

	       // Insert the ID into the ID map, must be unique!
	       id_map[cur_halo].first = bh.id;
	       id_map[cur_halo].second = cur_halo;

	       // Advance.
	       ++cur_halo;

	       LOGD( setindent( -2 ) );
	    }

	    // Advance tree index.
	    ++tree_idx;

	    LOGILN( "Done.", setindent( -2 ) );
	 }
	 LOGDLN( "Loaded ", bol_forest.size(), " halos." );

	 // Must have filled the entire forest.
	 ASSERT( cur_halo == counts.get( cur_forest ) );

	 // Process the forest.
	 process_forest( bol_forest, id_map, exp );

// 	 // Dump halo count.
// #pragma omp critical
// 	 {
// 	   std::ofstream cnt_file( "counts.dat", std::ios::out | std::ios::app );
// 	   cnt_file << cur_forest << "  " << cur_halo << "\n";
// 	 }

	 // Update the number of halos seen.
	 halos_seen[tid] += cur_halo;
	 ++forests_seen[tid];
	 LOGILN( "Seen ", halos_seen[tid], " halos." );

	 // Check if we need to update the user.
#pragma omp critical
	 if( unix::seconds( unix::timer() - since_update ) > update_every )
	 {
	    // Sum the net results.
	    total_halos_seen = halos_seen[0];
	    total_forests_seen = forests_seen[0];
	    for( unsigned jj = 1; jj < num_threads; ++jj )
	    {
	       total_halos_seen += halos_seen[jj];
	       total_forests_seen += forests_seen[jj];
	    }

	    // Print some info.
	    log_file << "\n";
	    log_file << "Total halos seen:    " << total_halos_seen << "\n";
	    log_file << "Total forests seen:  " << total_forests_seen << "\n";
	    log_file << "Percentage complete: " << 100.0*(float)total_forests_seen/(float)num_forests << "\n";
	    log_file.flush();

	    // Reset the update clock.
	    since_update = unix::timer();
	 }

	 // Advance forest index.
	 ++forest_idx;

	 LOGILN( "Done.", setindent( -2 ) );
      }

#pragma omp critical
      log_file << "\nThread " << OMP_TID << " done.\n";
   }

   log_file << "\nComplete.\n";
   log_file.close();

   return EXIT_SUCCESS;
}
