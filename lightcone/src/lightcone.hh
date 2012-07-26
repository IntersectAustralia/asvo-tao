#ifndef tao_lightcone_lightcone_hh
#define tao_lightcone_lightcone_hh

#include <string>
#include <libhpc/containers/vector.hh>
#include <libhpc/hpcmpi/mpi.hh>

namespace tao {

   ///
   /// Lightcone science module.
   ///
   class lightcone
   {
   public:

      typedef double real_type;

      lightcone();

      ~lightcone();

      ///
      /// Run the module.
      ///
      void
      run();

   protected:

      void
      _build_pixels( hpc::mpi::lindex cur_snap_idx,
                     optional<hpc::mpi::lindex> next_snap_idx,
                     real_type offs_x,
                     real_type offs_y,
                     real_type offs_z );

      void
      _build_query( hpc::mpi::lindex cur_snap_idx,
                    optional<hpc::mpi::lindex> next_snap_idx,
                    real_type offs_x,
                    real_type offs_y,
                    real_type offs_z );

      void
      _random_rotation_and_shifting( hpc::vector<std::string>& ops );

      real_type
      _redshift_to_distance( real_type redshift );

      void
      _setup_params();

   protected:

      std::string _type;
      real_type _box_side;
      hpc::vector<real_type> _snaps;
      hpc::vector<hpc::mpi::lindex> _snap_idxs;
      real_type _z_max;
      real_type _ra_min, _ra_max;
      real_type _dec_min, _dec_max;
      bool _unique;
      real_type _unique_offs_x, _unique_offs_y, _unique_offs_z;
   };
}

#endif
