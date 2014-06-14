#ifndef sage_hh
#define sage_hh

struct OUTPUT_GALAXY
{
  int   Type;
  long long   GalaxyIndex;
  int   HaloIndex;
  int   FOFHaloIndex;
  int   TreeIndex;
  
  int   SnapNum;
  float dt;
  int   CentralGal;
  float CentralMvir;

  int   mergeType;  //0=none; 1=minor merger; 2=major merger; 3=disk instability; 4=disrupt to ICS
  int   mergeIntoID;
  int   mergeIntoSnapNum;

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

  // to calculate magnitudes
  float SfrDisk;
  float SfrBulge;
  float SfrDiskZ;
  float SfrBulgeZ;
  
  // misc 
  float DiskScaleRadius;
  float Cooling;
  float Heating;
  float LastMajorMerger;
  float OutflowRate;

  //infall properties
  float infallMvir;
  float infallVvir;
  float infallVmax;
};

namespace sage {

   struct galaxy
   {
      int       type;
      long long galaxy_idx;
      int       halo_idx;
      int       fof_halo_idx;
      int       tree_idx;

      // LUKE: See struct GALAXY.
      long long global_index;
      int       descendant;
      long long global_descendant;

      int       snapshot;
      float     dt;
      int       central_gal;
      float     central_mvir;

      int       merge_type;     //0=none; 1=minor merger; 2=major merger; 3=disk instability; 4=disrupt to ICS
      int       merge_into_id;
      int       merge_into_snapshot;

      // properties of subhalo at the last time this galaxy was a central galaaxy 
      float pos[3];
      float vel[3];
      float spin[3];
      int   num_particles;
      float mvir;
      float rvir;
      float vvir;
      float vmax;
      float vel_disp;

      // baryonic reservoirs 
      float cold_gas;
      float stellar_mass;
      float bulge_mass;
      float hot_gas;
      float ejected_mass;
      float blackhole_mass;
      float ics;

      // metals
      float metals_cold_gas;
      float metals_stellar_mass;
      float metals_bulge_mass;
      float metals_hot_gas;
      float metals_ejected_mass;
      float metals_ics;

      // to calculate magnitudes
      float sfr_disk;
      float sfr_bulge;
      float sfr_disk_z;
      float sfr_bulge_z;

      // misc
      float disk_scale_radius;
      float cooling;
      float heating;
      float last_major_merger;
      float outflow_rate;

      float infall_mvir;
      float infall_vvir;
      float infall_vmax;
   };

}

#endif
