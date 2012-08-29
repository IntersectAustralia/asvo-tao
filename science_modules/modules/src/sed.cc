#include "sed.hh"

using namespace hpc;

namespace tao {

   ///
   /// Run the module.
   ///
   void
   sed::run()
   {
      LOG_ENTER();

      // TODO: Get access to all required datasets.

      _disk_sfh.reallocate( _num_times );
      _disk_metals.reallocate( _num_times );
      _bulge_sfh.reallocate( _num_times );
      _bulge_metals.reallocate( _num_times );

      for( mpi::lindex ii = 0; ii < _num_galaxies; ++ii )
      {
         _process_galaxy();
      }

      LOG_EXIT();
   }

   void
   sed::_process_galaxy()
   {
      LOG_ENTER();

      for( mpi::lindex ii = 0; ii < _num_times; ++ii )
      {
         _process_time( ii );
      }

      LOG_EXIT();
   }

   void
   sed::_process_time( mpi::lindex time_idx )
   {
      LOG_ENTER();

      // _sum_spectra( time_idx, _disk_metals[time_idx], _disk_sfh[time_idx], _disk_spectra );
      // _sum_spectra( time_idx, _bulge_metals[time_idx], _bulge_sfh[time_idx], _bulge_spectra );

      LOG_EXIT();
   }

   void
   sed::_sum_spectra( mpi::lindex time_idx,
                      real_type metal,
                      real_type sfh,
                      vector<real_type>::view galaxy_spectra )
   {
      LOG_ENTER();

      // Interpolate the metallicity to an index.
      unsigned metal_idx = _interp_metal( metal );

      // // Index the single stellar population spectra table.
      // vector<real_type>::view ssp_spectra = _spectra_lookup( time_idx, metal_idx );

      // for( unsigned ii = 0; ii < _num_spectra; ++ii )
      // {
      //    // TODO: Why using 1e10?
      //    // TODO: Explain the sfh (star formation history) part.
      //    galaxy_spectra[ii] += (ssp_spectra[ii]/1e10)*sfh;
      // }

      LOG_EXIT();
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
