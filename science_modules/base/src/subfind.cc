#include "subfind.hh"

namespace tao {
   namespace subfind {

      void
      make_hdf5_types( h5::datatype& mem_type,
		       h5::datatype& file_type )
      {
	 // Create memory type.
	 mem_type.compound( sizeof(halo) );
	 mem_type.insert( h5::datatype::native_int, "descendant", HOFFSET( halo, descendant ) );
	 mem_type.insert( h5::datatype::native_int, "first progenitor", HOFFSET( halo, first_progenitor ) );
	 mem_type.insert( h5::datatype::native_int, "next progenitor", HOFFSET( halo, next_progenitor ) );
	 mem_type.insert( h5::datatype::native_int, "first friend-of-friend", HOFFSET( halo, first_fof ) );
	 mem_type.insert( h5::datatype::native_int, "next friend-of-friend", HOFFSET( halo, next_fof ) );
	 mem_type.insert( h5::datatype::native_int, "number of particles", HOFFSET( halo, num_particles ) );
	 mem_type.insert( h5::datatype::native_float, "mass, mean 200", HOFFSET( halo, m_mean200 ) );
	 mem_type.insert( h5::datatype::native_float, "virial mass", HOFFSET( halo, mvir ) );
	 mem_type.insert( h5::datatype::native_float, "mass, top hat", HOFFSET( halo, m_top_hat ) );
	 mem_type.insert( h5::datatype::native_float, "x position", HOFFSET( halo, x ) );
	 mem_type.insert( h5::datatype::native_float, "y position", HOFFSET( halo, y ) );
	 mem_type.insert( h5::datatype::native_float, "z position", HOFFSET( halo, z ) );
	 mem_type.insert( h5::datatype::native_float, "x velocity", HOFFSET( halo, vx ) );
	 mem_type.insert( h5::datatype::native_float, "y velocity", HOFFSET( halo, vy ) );
	 mem_type.insert( h5::datatype::native_float, "z velocity", HOFFSET( halo, vz ) );
	 mem_type.insert( h5::datatype::native_float, "velocity dispersion (?)", HOFFSET( halo, vel_disp ) );
	 mem_type.insert( h5::datatype::native_float, "maximum velocity", HOFFSET( halo, vmax ) );
	 mem_type.insert( h5::datatype::native_float, "x spin", HOFFSET( halo, sx ) );
	 mem_type.insert( h5::datatype::native_float, "y spin", HOFFSET( halo, sy ) );
	 mem_type.insert( h5::datatype::native_float, "z spin", HOFFSET( halo, sz ) );
	 mem_type.insert( h5::datatype::native_llong, "most bound ID", HOFFSET( halo, most_bound_id ) );
	 mem_type.insert( h5::datatype::native_int, "snapshot", HOFFSET( halo, snap_num ) );
	 mem_type.insert( h5::datatype::native_int, "file number", HOFFSET( halo, file_nr ) );
	 mem_type.insert( h5::datatype::native_int, "subhalo index", HOFFSET( halo, subhalo_index ) );
	 mem_type.insert( h5::datatype::native_int, "subhalo half-mass", HOFFSET( halo, sub_half_mass ) );

	 // Create file type.
	 file_type.compound( 104 );
	 file_type.insert( h5::datatype::std_i32be, "descendant", 0 );
	 file_type.insert( h5::datatype::std_i32be, "first progenitor", 4 );
	 file_type.insert( h5::datatype::std_i32be, "next progenitor", 8 );
	 file_type.insert( h5::datatype::std_i32be, "first friend-of-friend", 12 );
	 file_type.insert( h5::datatype::std_i32be, "next friend-of-friend", 16 );
	 file_type.insert( h5::datatype::std_i32be, "number of particles", 20 );
	 file_type.insert( h5::datatype::ieee_f32be, "mass, mean 200", 24 );
	 file_type.insert( h5::datatype::ieee_f32be, "virial mass", 28 );
	 file_type.insert( h5::datatype::ieee_f32be, "mass, top hat", 32 );
	 file_type.insert( h5::datatype::ieee_f32be, "x position", 36 );
	 file_type.insert( h5::datatype::ieee_f32be, "y position", 40 );
	 file_type.insert( h5::datatype::ieee_f32be, "z position", 44 );
	 file_type.insert( h5::datatype::ieee_f32be, "x velocity", 48 );
	 file_type.insert( h5::datatype::ieee_f32be, "y velocity", 52 );
	 file_type.insert( h5::datatype::ieee_f32be, "z velocity", 56 );
	 file_type.insert( h5::datatype::ieee_f32be, "velocity dispersion (?)", 60 );
	 file_type.insert( h5::datatype::ieee_f32be, "maximum velocity", 64 );
	 file_type.insert( h5::datatype::ieee_f32be, "x spin", 68 );
	 file_type.insert( h5::datatype::ieee_f32be, "y spin", 72 );
	 file_type.insert( h5::datatype::ieee_f32be, "z spin", 76 );
	 file_type.insert( h5::datatype::std_i64be, "most bound ID", 80 );
	 file_type.insert( h5::datatype::std_i32be, "snapshot", 88 );
	 file_type.insert( h5::datatype::std_i32be, "file number", 92 );
	 file_type.insert( h5::datatype::std_i32be, "subhalo index", 96 );
	 file_type.insert( h5::datatype::std_i32be, "subhalo half-mass", 100 );
      }

   }
}
