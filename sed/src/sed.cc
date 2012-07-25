#include <libhpc/containers/vector.hh>
#include "sed.hh"

using hpc::vector;

namespace tao {

   ///
   /// Run the module.
   ///
   void
   sed::run()
   {
      MPI_LOG_ENTER();

      // TODO: Get access to all required datasets.

      mpi::lindex num_galaxies;

      for( mpi::lindex ii = 0; ii < num_galaxies; ++ii )
      {
         _process_galaxy();
      }

      MPI_LOG_EXIT();
   }

   void
   sed::_process_galaxy()
   {
      MPI_LOG_ENTER();

      vector<real_type> disk_sfh( num_times ), disk_metals( num_times );
      vector<real_type> bulge_sfh( num_times ), bulge_metals( num_times );

      for( mpi::lindex ii = 0; ii < num_times; ++ii )
      {
         _process_time();
      }

      MPI_LOG_EXIT();
   }

   void
   sed::_process_time()
   {
      MPI_LOG_ENTER();

      _sum_spectra( time_idx, disk_metals[time_idx], disk_sfh[time_idx], disk_spectra );
      _sum_spectra( time_idx, bulge_metals[time_idx], bulge_sfh[time_idx], bulge_spectra );

      MPI_LOG_EXIT();
   }

   void
   sed::_sum_spectra( mpi::lindex time_idx,
                      real_type metal,
                      real_type sfh,
                      vector<real_type>::view galaxy_spectra )
   {
      MPI_LOG_ENTER();

      // Interpolate the metallicity to an index.
      unsigned metal_idx = _interp_metal( metal );

      // Index the single stellar population spectra table.
      vector<real_type>::view ssp_spectra = _spectra_lookup( time_idx, metal_idx );

      for( unsigned ii = 0; ii < _num_spectra; ++ii )
      {
         // TODO: Why using 1e10?
         // TODO: Explain the sfh (star formation history) part.
         galaxy_spectra[ii] += (ssp_spectra[ii]/1e10)*sfh;
      }

      MPI_LOG_EXIT();
   }

   unsigned
   sed::_interp_metal( real_type metal )
   {
      if( metal <= 0.0005 )
         return 0;
      else if( metal <= 0.0025 )
         return 1;
      else if( metal <= 0.007 )
         return 2;
      else if( metal <= 0.015 )
         return 3;
      else if( metal <= 0.03 )
         return 4;
      else if( metal <= 0.055 )
         return 5;
      else
         return 6;
   }
}
