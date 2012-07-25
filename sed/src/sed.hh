#ifndef tao_sed_sed_hh
#define tao_sed_sed_hh

#include <libhpc/containers/vector.hh>
#include <libhpc/hpcmpi/mpi.hh>

namespace tao {

   ///
   /// SED science module.
   ///
   /// The SED module is responsible for calculating the
   /// energy spectra of each galaxy.
   ///
   class sed
   {
   public:

      typedef double real_type;

      sed();

      ~sed();

      ///
      /// Run the module.
      ///
      void
      run();

   protected:

      void
      _process_galaxy();

      void
      _process_time( hpc::mpi::lindex time_idx );

      void
      _sum_spectra( hpc::mpi::lindex time_idx,
                    real_type metal,
                    real_type sfh,
                    hpc::vector<real_type>::view galaxy_spectra );

      unsigned
      _interp_metal( real_type metal );

   protected:

      hpc::mpi::lindex _num_galaxies;
      hpc::mpi::lindex _num_times;
      hpc::vector<real_type> _disk_sfh, _disk_metals;
      hpc::vector<real_type> _bulge_sfh, _bulge_metals;
   };
}

#endif
