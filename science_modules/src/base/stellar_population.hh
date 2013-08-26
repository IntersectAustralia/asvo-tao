#ifndef tao_base_stellar_population_hh
#define tao_base_stellar_population_hh

#include "timed.hh"
#include "age_line.hh"
#include "types.hh"

// Forward declaration of test suites to allow direct access.
class stellar_population_suite;

namespace tao {
   using namespace hpc;

   ///
   ///
   ///
   class stellar_population
      : public timed
   {
      friend class ::stellar_population_suite;

   public:

      stellar_population();

      void
      set_num_metals( unsigned num_metals );

      void
      set_wavelengths( vector<real_type>& waves );

      void
      set_spectra( vector<real_type>& spectra );

      void
      load( const string& wave_filename,
            const string& ssp_filename );

      real_type
      at( unsigned age_idx,
          unsigned spec_idx,
          unsigned metal_idx ) const;

      const vector<real_type>::view
      wavelengths() const;

      const age_line<real_type>&
      bin_ages() const;

      template< class MassIterator,
                class MetalIterator,
                class OutputIterator >
      void
      sum( MassIterator masses_start,
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

            // Interpolate the metallicity to an index.
            unsigned metal_idx = _interp_metal( *metals_start );

            // Calculate the base index for the ssp table.
            size_t base = ii*_waves.size()*_num_metals + metal_idx;

            // Sum each spectra into the sed bin.
            OutputIterator sed_it = sed_start;
            for( unsigned ii = 0; ii < _waves.size(); ++ii )
            {
               // The star formation histories read from the file are in
               // solar masses/1e10. The values in SSP are luminosity densities
               // in erg/s/angstrom, and they're really big. Scale them down
               // by 1e10 to make it more manageable.
               *sed_it += _spec[base + ii*_num_metals]*mass;
               ++sed_it;
            }

            ++masses_start;
            ++metals_start;
         }
      }
           

   protected:

      unsigned
      _interp_metal( real_type metal ) const;

      void
      _load_waves( const string& filename );

      void
      _load_ssp( const string& filename );

   protected:

      unsigned _num_metals;
      vector<real_type> _waves;
      vector<real_type> _spec;
      age_line<real_type> _age_bins;
   };

}

#endif
