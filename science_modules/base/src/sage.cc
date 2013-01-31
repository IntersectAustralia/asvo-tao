#include "sage.hh"

namespace tao {
   using namespace hpc;

   namespace sage {

      void
      make_hdf5_types( h5::datatype& mem_type,
		       h5::datatype& file_type )
      {
	 // Create memory type.
	 mem_type.compound( sizeof(galaxy) );
	 mem_type.insert( h5::datatype::native_int, "type", HOFFSET( galaxy, type ) );
	 mem_type.insert( h5::datatype::native_llong, "galaxy index", HOFFSET( galaxy, galaxy_index ) );
	 mem_type.insert( h5::datatype::native_int, "halo index", HOFFSET( galaxy, halo_index ) );
	 mem_type.insert( h5::datatype::native_int, "friends-of-friends index", HOFFSET( galaxy, fof_index ) );
	 mem_type.insert( h5::datatype::native_int, "tree index", HOFFSET( galaxy, tree_index ) );
	 mem_type.insert( h5::datatype::native_llong, "gobal galaxy index", HOFFSET( galaxy, global_index ) );
	 mem_type.insert( h5::datatype::native_int, "descendant", HOFFSET( galaxy, descendant ) );
	 mem_type.insert( h5::datatype::native_llong, "global descendant", HOFFSET( galaxy, global_descendant ) );
	 mem_type.insert( h5::datatype::native_int, "snapshot", HOFFSET( galaxy, snap ) );
	 mem_type.insert( h5::datatype::native_int, "central galaxy", HOFFSET( galaxy, central_gal ) );
	 mem_type.insert( h5::datatype::native_float, "central galaxy virial mass", HOFFSET( galaxy, central_mvir ) );
	 mem_type.insert( h5::datatype::native_float, "x position", HOFFSET( galaxy, x ) );
	 mem_type.insert( h5::datatype::native_float, "y position", HOFFSET( galaxy, y ) );
	 mem_type.insert( h5::datatype::native_float, "z position", HOFFSET( galaxy, z ) );
	 mem_type.insert( h5::datatype::native_float, "x velocity", HOFFSET( galaxy, vx ) );
	 mem_type.insert( h5::datatype::native_float, "y velocity", HOFFSET( galaxy, vy ) );
	 mem_type.insert( h5::datatype::native_float, "z velocity", HOFFSET( galaxy, vz ) );
	 mem_type.insert( h5::datatype::native_float, "x spin", HOFFSET( galaxy, sx ) );
	 mem_type.insert( h5::datatype::native_float, "y spin", HOFFSET( galaxy, sy ) );
	 mem_type.insert( h5::datatype::native_float, "z spin", HOFFSET( galaxy, sz ) );
	 mem_type.insert( h5::datatype::native_int, "length (?)", HOFFSET( galaxy, len ) );
	 mem_type.insert( h5::datatype::native_float, "virial mass", HOFFSET( galaxy, mvir ) );
	 mem_type.insert( h5::datatype::native_float, "virial radius", HOFFSET( galaxy, rvir ) );
	 mem_type.insert( h5::datatype::native_float, "virial velocity (?)", HOFFSET( galaxy, vvir ) );
	 mem_type.insert( h5::datatype::native_float, "maximum velocity", HOFFSET( galaxy, vmax ) );
	 mem_type.insert( h5::datatype::native_float, "velocity dispersion (?)", HOFFSET( galaxy, vel_disp ) );
	 mem_type.insert( h5::datatype::native_float, "cold gas", HOFFSET( galaxy, cold_gas ) );
	 mem_type.insert( h5::datatype::native_float, "stellar mass", HOFFSET( galaxy, stellar_mass ) );
	 mem_type.insert( h5::datatype::native_float, "bulge mass", HOFFSET( galaxy, bulge_mass ) );
	 mem_type.insert( h5::datatype::native_float, "hot gas", HOFFSET( galaxy, hot_gas ) );
	 mem_type.insert( h5::datatype::native_float, "ejected mass", HOFFSET( galaxy, ejected_mass ) );
	 mem_type.insert( h5::datatype::native_float, "black hole mass", HOFFSET( galaxy, black_hole_mass ) );
	 mem_type.insert( h5::datatype::native_float, "ics", HOFFSET( galaxy, ics ) );
	 mem_type.insert( h5::datatype::native_float, "metals cold gas", HOFFSET( galaxy, metals_cold_gas ) );
	 mem_type.insert( h5::datatype::native_float, "metals stellar mass", HOFFSET( galaxy, metals_stellar_mass ) );
	 mem_type.insert( h5::datatype::native_float, "metals bulge mass", HOFFSET( galaxy, metals_bulge_mass ) );
	 mem_type.insert( h5::datatype::native_float, "metals hot gas", HOFFSET( galaxy, metals_hot_gas ) );
	 mem_type.insert( h5::datatype::native_float, "metals ejected mass", HOFFSET( galaxy, metals_ejected_mass ) );
	 mem_type.insert( h5::datatype::native_float, "metals ics", HOFFSET( galaxy, metals_ics ) );
	 mem_type.insert( h5::datatype::native_float, "star formation rate", HOFFSET( galaxy, sfr ) );
	 mem_type.insert( h5::datatype::native_float, "bulge star formation rate", HOFFSET( galaxy, sfr_bulge ) );
	 mem_type.insert( h5::datatype::native_float, "ics star formation rate", HOFFSET( galaxy, sfr_ics ) );
	 mem_type.insert( h5::datatype::native_float, "disk scale radius", HOFFSET( galaxy, disk_scale_radius ) );
	 mem_type.insert( h5::datatype::native_float, "cooling", HOFFSET( galaxy, cooling ) );
	 mem_type.insert( h5::datatype::native_float, "heating", HOFFSET( galaxy, heating ) );

	 // Create file type.
	 file_type.compound( 192 );
	 file_type.insert( h5::datatype::std_i32be, "type", 0 );
	 file_type.insert( h5::datatype::std_i64be, "galaxy index", 4 );
	 file_type.insert( h5::datatype::std_i32be, "halo index", 12 );
	 file_type.insert( h5::datatype::std_i32be, "friends-of-friends index", 16 );
	 file_type.insert( h5::datatype::std_i32be, "tree index", 20 );
	 file_type.insert( h5::datatype::std_i64be, "gobal galaxy index", 24 );
	 file_type.insert( h5::datatype::std_i32be, "descendant", 32 );
	 file_type.insert( h5::datatype::std_i64be, "global descendant", 36 );
	 file_type.insert( h5::datatype::std_i32be, "snapshot", 44 );
	 file_type.insert( h5::datatype::std_i32be, "central galaxy", 48 );
	 file_type.insert( h5::datatype::ieee_f32be, "central galaxy virial mass", 52 );
	 file_type.insert( h5::datatype::ieee_f32be, "x position", 56 );
	 file_type.insert( h5::datatype::ieee_f32be, "y position", 60 );
	 file_type.insert( h5::datatype::ieee_f32be, "z position", 64 );
	 file_type.insert( h5::datatype::ieee_f32be, "x velocity", 68 );
	 file_type.insert( h5::datatype::ieee_f32be, "y velocity", 72 );
	 file_type.insert( h5::datatype::ieee_f32be, "z velocity", 76 );
	 file_type.insert( h5::datatype::ieee_f32be, "x spin", 80 );
	 file_type.insert( h5::datatype::ieee_f32be, "y spin", 84 );
	 file_type.insert( h5::datatype::ieee_f32be, "z spin", 88 );
	 file_type.insert( h5::datatype::std_i32be, "length (?)", 92 );
	 file_type.insert( h5::datatype::ieee_f32be, "virial mass", 96 );
	 file_type.insert( h5::datatype::ieee_f32be, "virial radius", 100 );
	 file_type.insert( h5::datatype::ieee_f32be, "virial velocity (?)", 104 );
	 file_type.insert( h5::datatype::ieee_f32be, "maximum velocity", 108 );
	 file_type.insert( h5::datatype::ieee_f32be, "velocity dispersion (?)", 112 );
	 file_type.insert( h5::datatype::ieee_f32be, "cold gas", 116 );
	 file_type.insert( h5::datatype::ieee_f32be, "stellar mass", 120 );
	 file_type.insert( h5::datatype::ieee_f32be, "bulge mass", 124 );
	 file_type.insert( h5::datatype::ieee_f32be, "hot gas", 128 );
	 file_type.insert( h5::datatype::ieee_f32be, "ejected mass", 132 );
	 file_type.insert( h5::datatype::ieee_f32be, "black hole mass", 136 );
	 file_type.insert( h5::datatype::ieee_f32be, "ics", 140 );
	 file_type.insert( h5::datatype::ieee_f32be, "metals cold gas", 144 );
	 file_type.insert( h5::datatype::ieee_f32be, "metals stellar mass", 148 );
	 file_type.insert( h5::datatype::ieee_f32be, "metals bulge mass", 152 );
	 file_type.insert( h5::datatype::ieee_f32be, "metals hot gas", 156 );
	 file_type.insert( h5::datatype::ieee_f32be, "metals ejected mass", 160 );
	 file_type.insert( h5::datatype::ieee_f32be, "metals ics", 164 );
	 file_type.insert( h5::datatype::ieee_f32be, "star formation rate", 168 );
	 file_type.insert( h5::datatype::ieee_f32be, "bulge star formation rate", 172 );
	 file_type.insert( h5::datatype::ieee_f32be, "ics star formation rate", 176 );
	 file_type.insert( h5::datatype::ieee_f32be, "disk scale radius", 180 );
	 file_type.insert( h5::datatype::ieee_f32be, "cooling", 184 );
	 file_type.insert( h5::datatype::ieee_f32be, "heating", 188 );
      }

   }
}
