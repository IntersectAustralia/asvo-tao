#ifndef tao_base_subfind_hh
#define tao_base_subfind_hh

#include <libhpc/h5.hh>

namespace tao {
   namespace subfind {

      struct halo
      {
	 // merger tree pointers 
	 int descendant;
	 int first_progenitor;
	 int next_progenitor;
	 int first_fof;
	 int next_fof;

	 // properties of halo 
	 int num_particles;
	 float m_mean200, mvir, m_top_hat;  // Mean 200 values (Mvir=M_Crit200)
	 float x, y, z;
	 float vx, vy, vz;
	 float vel_disp;
	 float vmax;
	 float sx, sy, sz;
	 long long most_bound_id;

	 // original position in subfind output 
	 int snap_num;
	 int file_nr;
	 int subhalo_index;
	 float sub_half_mass;
      };

      void
      make_hdf5_types( hpc::h5::datatype& mem_type,
		       hpc::h5::datatype& file_type );

   }
}

#endif
