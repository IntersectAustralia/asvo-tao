#include "hdf5_types.hh"

using namespace hpc;

namespace sage {

   void
   make_hdf5_types( h5::datatype& mem_type,
		    h5::datatype& file_type )
   {
      h5::derive der( sizeof(galaxy) );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, type ),                h5::datatype::std_i32be,  "type" );
      der.add( h5::datatype::native_llong, HOFFSET( galaxy, galaxy_idx ),          h5::datatype::std_i64be,  "galaxy_index" );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, halo_idx ),            h5::datatype::std_i32be,  "halo_index" );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, fof_halo_idx ),        h5::datatype::std_i32be,  "fof_halo_index" );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, tree_idx ),            h5::datatype::std_i32be,  "tree_index" );
      der.add( h5::datatype::native_llong, HOFFSET( galaxy, global_index ),        h5::datatype::std_i64be,  "global_index" );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, descendant ),          h5::datatype::std_i32be,  "descendant" );
      der.add( h5::datatype::native_llong, HOFFSET( galaxy, global_descendant ),   h5::datatype::std_i64be,  "global_descendant" );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, snapshot ),            h5::datatype::std_i32be,  "snapshot" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, dt ),                  h5::datatype::ieee_f32be, "dt" );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, central_gal ),         h5::datatype::std_i32be,  "central_galaxy_index" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, central_mvir ),        h5::datatype::ieee_f32be, "central_galaxy_mvir" );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, merge_type ),          h5::datatype::std_i32be,  "merge_type" );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, merge_into_id ),       h5::datatype::std_i32be,  "merge_into_id" );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, merge_into_snapshot ), h5::datatype::std_i32be,  "merge_into_snapshot" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, pos[0] ),              h5::datatype::ieee_f32be, "position_x" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, pos[1] ),              h5::datatype::ieee_f32be, "position_y" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, pos[2] ),              h5::datatype::ieee_f32be, "position_z" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, vel[0] ),              h5::datatype::ieee_f32be, "velocity_x" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, vel[1] ),              h5::datatype::ieee_f32be, "velocity_y" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, vel[2] ),              h5::datatype::ieee_f32be, "velocity_z" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, spin[0] ),             h5::datatype::ieee_f32be, "spin_x" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, spin[1] ),             h5::datatype::ieee_f32be, "spin_y" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, spin[2] ),             h5::datatype::ieee_f32be, "spin_z" );
      der.add( h5::datatype::native_int,   HOFFSET( galaxy, num_particles ),       h5::datatype::std_i32be,  "n_darkmatter_particles" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, mvir ),                h5::datatype::ieee_f32be, "virial_mass" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, rvir ),                h5::datatype::ieee_f32be, "virial_radius" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, vvir ),                h5::datatype::ieee_f32be, "virial_velocity" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, vmax ),                h5::datatype::ieee_f32be, "max_velocity" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, vel_disp ),            h5::datatype::ieee_f32be, "velocity_dispersion" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, cold_gas ),            h5::datatype::ieee_f32be, "cold_gas" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, stellar_mass ),        h5::datatype::ieee_f32be, "stellar_mass" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, bulge_mass ),          h5::datatype::ieee_f32be, "bulge_mass" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, hot_gas ),             h5::datatype::ieee_f32be, "hot_gas" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, ejected_mass ),        h5::datatype::ieee_f32be, "ejected_mass" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, blackhole_mass ),      h5::datatype::ieee_f32be, "blackhole_mass" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, ics ),                 h5::datatype::ieee_f32be, "ics" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, metals_cold_gas ),     h5::datatype::ieee_f32be, "metals_cold_gas" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, metals_stellar_mass ), h5::datatype::ieee_f32be, "metals_stellar_mass" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, metals_bulge_mass ),   h5::datatype::ieee_f32be, "metals_bulge_mass" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, metals_hot_gas ),      h5::datatype::ieee_f32be, "metals_hot_gas" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, metals_ejected_mass ), h5::datatype::ieee_f32be, "metals_ejected_mass" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, metals_ics ),          h5::datatype::ieee_f32be, "metals_ics" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, sfr_disk ),            h5::datatype::ieee_f32be, "sfr_disk" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, sfr_bulge ),           h5::datatype::ieee_f32be, "sfr_bulge" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, sfr_disk_z ),          h5::datatype::ieee_f32be, "sfr_disk_z" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, sfr_bulge_z ),         h5::datatype::ieee_f32be, "sfr_bulge_z" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, disk_scale_radius ),   h5::datatype::ieee_f32be, "disk_scale_radius" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, cooling ),             h5::datatype::ieee_f32be, "cooling" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, heating ),             h5::datatype::ieee_f32be, "heating" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, last_major_merger ),   h5::datatype::ieee_f32be, "last_major_merger" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, outflow_rate ),        h5::datatype::ieee_f32be, "outflow_rate" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, infall_mvir ),         h5::datatype::ieee_f32be, "infall_mvir" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, infall_vvir ),         h5::datatype::ieee_f32be, "infall_vvir" );
      der.add( h5::datatype::native_float, HOFFSET( galaxy, infall_vmax ),         h5::datatype::ieee_f32be, "infall_vmax" );
      der.commit( mem_type, file_type );
   }

}
