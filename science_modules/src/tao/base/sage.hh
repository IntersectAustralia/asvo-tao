#ifndef tao_base_sage_hh
#define tao_base_sage_hh

#include <ostream>
#include <libhpc/libhpc.hh>

namespace tao {
   using namespace hpc;

   namespace sage {

      struct galaxy
      {
	 int       type;
	 long long galaxy_index;
	 int       halo_index;
	 int       fof_index;
	 int       tree_index;

	 // LUKE: See struct GALAXY.
	 long long global_index;
	 int       descendant;
	 long long global_descendant;

	 int   snap;
	 int   central_gal;
	 float central_mvir;

	 // properties of subhalo at the last time this galaxy was a central galaaxy 
	 float x, y, z;
	 float vx, vy, vz;
	 float sx, sy, sz;
	 int   len;
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
	 float black_hole_mass;
	 float ics;

	 // metals
	 float metals_cold_gas;
	 float metals_stellar_mass;
	 float metals_bulge_mass;
	 float metals_hot_gas;
	 float metals_ejected_mass;
	 float metals_ics;

	 // misc 
	 float sfr;
	 float sfr_bulge;
	 float sfr_ics;
	 float disk_scale_radius;
	 float cooling;
	 float heating;
      };

      void
      make_hdf5_types( h5::datatype& mem_type,
		       h5::datatype& file_type );

      std::ostream&
      operator<<( std::ostream& strm,
		  const galaxy& gal );
   }
}

#endif
