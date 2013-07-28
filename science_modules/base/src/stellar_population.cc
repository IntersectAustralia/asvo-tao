#include <boost/algorithm/string/trim.hpp>
#include "stellar_population.hh"

namespace tao {
   using namespace hpc;

   stellar_population::stellar_population()
      : _num_metals( 7 )
   {
   }

   void
   stellar_population::set_num_metals( unsigned num_metals )
   {
      _num_metals = num_metals;
   }

   void
   stellar_population::set_wavelengths( vector<real_type>& waves )
   {
      _waves.deallocate();
      _waves.swap( waves );
   }

   void
   stellar_population::set_spectra( vector<real_type>& spectra )
   {
      _spec.deallocate();
      _spec.swap( spectra );
   }

   void
   stellar_population::load( const string& wave_filename,
                             const string& ssp_filename )
   {
      _load_waves( wave_filename );
      _load_ssp( ssp_filename );
   }

   real_type
   stellar_population::at( unsigned age_idx,
                           unsigned spec_idx,
                           unsigned metal_idx ) const
   {
      ASSERT( age_idx < _age_bins.size(), "Invalid age index." );
      ASSERT( spec_idx < _waves.size(), "Invalid wavelength index." );
      ASSERT( metal_idx < _num_metals, "Invalid metallicity index." );
      return _spec[age_idx*_waves.size()*_num_metals + spec_idx*_num_metals + metal_idx];
   }

   const vector<real_type>::view
   stellar_population::wavelengths() const
   {
      return _waves;
   }

   const age_line<real_type>&
   stellar_population::bin_ages() const
   {
      return _age_bins;
   }

   unsigned
   stellar_population::_interp_metal( real_type metal ) const
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

   void
   stellar_population::_load_waves( const string& filename )
   {
      LOGILN( "Loading wavelengths from: ", filename, setindent( 2 ) );

      // Open the file.
      std::ifstream file( filename );
      ASSERT( file.is_open(), "Couldn't find wavelengths file." );

      // Need to get number of lines in file first.
      unsigned num_waves = 0;
      {
         string line;
         while( !file.eof() )
         {
            std::getline( file, line );
            if( boost::trim_copy( line ).length() )
               ++num_waves;
         }
      }
      LOGILN( "Number of wavelengths: ", num_waves );

      // Allocate. Note that the ordering goes time,spectra,metals.
      _waves.reallocate( num_waves );

      // Read in the file in one big go.
      file.clear();
      file.seekg( 0 );
      for( unsigned ii = 0; ii < _waves.size(); ++ii )
         file >> _waves[ii];

      LOGILN( "Done.", setindent( -2 ) );
   }

   void
   stellar_population::_load_ssp( const string& filename )
   {
      LOGILN( "Loading stellar population from: ", filename, setindent( 2 ) );

      // The SSP file contains the age grid information first.
      std::ifstream file( filename );
      unsigned num_ages;
      file >> num_ages;
      ASSERT( file.good(), "Error reading SSP file." );
      LOGILN( "Number of ages: ", num_ages );

      // Read the bin ages.
      {
         vector<real_type> bin_ages( num_ages );
         for( unsigned ii = 0; ii < num_ages; ++ii )
         {
            file >> bin_ages[ii];
            ASSERT( file.good(), "Error reading SSP file." );
         }

#ifndef NDEBUG
         // Must be ordered.
         for( unsigned ii = 1; ii < bin_ages.size(); ++ii )
            ASSERT( bin_ages[ii] >= bin_ages[ii - 1], "Bin ages must be descending ordered." );
#endif

         // Setup the bin ages.
         _age_bins.set_ages( bin_ages );
      }

      // Allocate. Note that the ordering goes time,spectra,metals.
      _spec.reallocate( _age_bins.size()*_waves.size()*_num_metals );
      LOGILN( "Number of spectra entries: ", _spec.size() );

      // Read in the file in one big go.
      for( unsigned ii = 0; ii < _spec.size(); ++ii )
      {
         // These values are luminosity densities, in erg/s/angstrom.
         file >> _spec[ii];
         ASSERT( file.good(), "Error reading SSP file." );
      }

      LOGILN( "Done.", setindent( -2 ) );
   }

}
