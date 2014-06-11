#ifndef sage_hh
#define sage_hh

namespace sage {

   struct galaxy
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

}

#endif
