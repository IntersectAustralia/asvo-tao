#ifndef tao_base_stellar_population_hh
#define tao_base_stellar_population_hh

#include <vector>
#include <libhpc/system/filesystem.hh>
#include "age_line.hh"
#include "types.hh"

namespace tao {

   ///
   ///
   ///
   class stellar_population
   {
   public:

      stellar_population();

      void
      set_num_metals( unsigned num_metals );

      template< class Seq >
      void
      set_wavelengths( Seq&& waves )
      {
         hpc::assign( _waves, std::forward<Seq>( waves ) );
      }

      template< class Seq >
      void
      set_spectra( Seq&& spectra )
      {
         hpc::assign( _spec, std::forward<Seq>( spectra ) );
      }

      void
      set_recycle_fraction( real_type rec_frac );

      void
      load( hpc::fs::path const& ages_filename,
            hpc::fs::path const& waves_filename,
            hpc::fs::path const& metals_filename,
            hpc::fs::path const& ssp_filename );

      void
      save( hpc::fs::path const& ages_filename,
	    hpc::fs::path const& waves_filename,
	    hpc::fs::path const& metals_filename,
	    hpc::fs::path const& ssp_filename );

      void
      restrict();

      unsigned
      num_metal_bins() const;

      unsigned
      age_masses_size() const;

      real_type
      at( unsigned age_idx,
          unsigned spec_idx,
          unsigned metal_idx ) const;

      std::vector<real_type> const&
      wavelengths() const;

      age_line<real_type> const&
      bin_ages() const;

      template< class MassIterator,
                class OutputIterator >
      void
      sum( MassIterator masses_start,
           const OutputIterator& sed_start ) const
      {
         sum_thibault( masses_start, sed_start );
      }

      template< class MassIterator,
                class OutputIterator >
      void
      sum_thibault( MassIterator masses_start,
                    const OutputIterator& sed_start ) const
      {
         // Erase sed values first.
         {
            OutputIterator sed_it = sed_start;
            for( unsigned ii = 0; ii < _waves.size(); ++ii, ++sed_it )
               *sed_it = 0;
         }

         // Now sum spectra.
         for( unsigned ii = 0; ii < _age_bins.size(); ++ii )
         {
            // Calculate the base index for the ssp table. This skips forwards blocks
            // of age information.
            size_t base = ii*_waves.size()*(_metal_bins.size() + 1);

            // Sum each spectra into the sed bin. We still have wavelengths and
            // metallicities to sum.
            for( unsigned jj = 0; jj <= _metal_bins.size(); ++jj ) // <= because bins are duals
            {
               // Cache the mass.
               real_type mass = *masses_start++;
               ASSERT( mass == mass, "Found NaN for mass during stellar population summation." );

               // Update with the recycling fraction.
               mass *= _com_rec_frac;

               // New SSP offset based on metallicity.
               unsigned met_base = base + jj;

               // Update spectra.
               OutputIterator sed_it = sed_start;
               for( unsigned kk = 0; kk < _waves.size(); ++kk, ++sed_it )
               {
                  *sed_it += _spec[met_base + kk*(_metal_bins.size() + 1)]*mass;
                  ASSERT( *sed_it == *sed_it, "Produced NaN during stellar population summation." );
               }
            }
         }
      }

      template< class MassIterator,
                class MetalIterator,
                class OutputIterator >
      void
      sum_chiara( MassIterator masses_start,
                  MetalIterator metals_start,
                  const OutputIterator& sed_start ) const
      {
         // Erase sed values first.
         {
            OutputIterator sed_it = sed_start;
            for( unsigned ii = 0; ii < _waves.size(); ++ii, ++sed_it )
               *sed_it = 0;
         }

         // Now sum spectra.
         for( unsigned ii = 0; ii < _age_bins.size(); ++ii )
         {
            // Cache mass.
            real_type mass = *masses_start;
            ASSERT( mass == mass, "Found NaN for mass during stellar population summation." );

	    // Update with recycle fraction compliment.
	    mass *= _com_rec_frac;

            // Interpolate the metallicity to an index.
            unsigned metal_idx = find_metal_bin( *metals_start );

            // Calculate the base index for the ssp table.
            size_t base = ii*_waves.size()*(_metal_bins.size() + 1) + metal_idx;

            // Sum each spectra into the sed bin.
            OutputIterator sed_it = sed_start;
            for( unsigned jj = 0; jj < _waves.size(); ++jj )
            {
               // The star formation histories read from the file are in
               // solar masses/1e10. The values in SSP are luminosity densities
               // in erg/s/angstrom, and they're really big.
               *sed_it += _spec[base + jj*(_metal_bins.size() + 1)]*mass;
               ASSERT( *sed_it == *sed_it, "Produced NaN during stellar population summation." );
               ++sed_it;
            }

            ++masses_start;
            ++metals_start;
         }
      }

      unsigned
      find_metal_bin( real_type metal ) const;

   protected:

      void
      _load_metals( hpc::fs::path const& filename );

      void
      _load_ages( hpc::fs::path const& filename );

      void
      _load_waves( hpc::fs::path const& filename );

      void
      _load_ssp( hpc::fs::path const& filename );

      void
      _save_metals( hpc::fs::path const& filename );

      void
      _save_ages( hpc::fs::path const& filename );

      void
      _save_waves( hpc::fs::path const& filename );

      void
      _save_ssp( hpc::fs::path const& filename );

   protected:

      std::vector<real_type> _waves;
      std::vector<real_type> _spec;
      std::vector<real_type> _metal_bins;
      age_line<real_type> _age_bins;
      real_type _com_rec_frac;
   };

}

#endif
