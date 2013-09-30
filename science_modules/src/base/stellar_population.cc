#include <boost/algorithm/string/trim.hpp>
#include <libhpc/algorithm/bin.hh>
#include <libhpc/algorithm/dual.hh>
#include "stellar_population.hh"

namespace tao {
   namespace fs = boost::filesystem;
   using namespace hpc;

   stellar_population::stellar_population()
   {
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
   stellar_population::load( const fs::path& ages_filename,
                             const fs::path& waves_filename,
                             const fs::path& metals_filename,
                             const fs::path& ssp_filename )
   {
      _load_ages( ages_filename );
      _load_waves( waves_filename );
      _load_metals( metals_filename );
      _load_ssp( ssp_filename );
   }

   real_type
   stellar_population::at( unsigned age_idx,
                           unsigned spec_idx,
                           unsigned metal_idx ) const
   {
      ASSERT( age_idx < _age_bins.size(), "Invalid age index." );
      ASSERT( spec_idx < _waves.size(), "Invalid wavelength index." );
      ASSERT( metal_idx <= _metal_bins.size(), "Invalid metallicity index." );
      return _spec[age_idx*_waves.size()*(_metal_bins.size() + 1) + spec_idx*(_metal_bins.size() + 1) + metal_idx];
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
      return algorithm::bin( _metal_bins.begin(), _metal_bins.end(), metal );
   }

   void
   stellar_population::_load_metals( const fs::path& filename )
   {
      LOGILN( "Loading metallicities from: ", filename, setindent( 2 ) );

      std::ifstream file( filename.c_str() );
      EXCEPT( file.is_open(), "Couldn't find metallicities file: ", filename );

      // The first line can be the word "dual", indicating
      // the dual has already been taken.
      string dual;
      file >> dual;
      ASSERT( file, "Error reading metallicity file." );

      unsigned num_metals;
      if( dual == "dual" )
	 file >> num_metals;
      else
	 num_metals = boost::lexical_cast<unsigned>( dual );
      ASSERT( file, "Error reading metallicity file." );
      if( num_metals )
      {
         vector<real_type> metals( num_metals );
         for( unsigned ii = 0; ii < num_metals; ++ii )
            file >> metals[ii];
         ASSERT( file, "Error reading metallicity file." );
	 ASSERT( std::is_sorted( metals.begin(), metals.end() ),
		 "Metallicities must be in ascending order." );

	 // Store the duals if not already in that format.
	 if( dual == "dual" )
	 {
	    _metal_bins.resize( num_metals );
	    std::copy( metals.begin(), metals.end(), _metal_bins.begin() );
	 }
	 else
	 {
	    _metal_bins.resize( num_metals - 1 );
	    algorithm::dual( metals.begin(), metals.end(), _metal_bins.begin() );
	 }
      }

      LOGILN( "Done.", setindent( -2 ) );
   }

   void
   stellar_population::_load_waves( const fs::path& filename )
   {
      LOGILN( "Loading wavelengths from: ", filename, setindent( 2 ) );

      // Open the file.
      std::ifstream file( filename.c_str() );
      EXCEPT( file.is_open(), "Couldn't find wavelengths file: ", filename );

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
   stellar_population::_load_ages( const fs::path& filename )
   {
      LOGILN( "Loading ages from: ", filename, setindent( 2 ) );

      // Open the file.
      std::ifstream file( filename.c_str() );
      EXCEPT( file.is_open(), "Couldn't find ages file: ", filename );

      // Read the number of ages.
      unsigned num_ages;
      file >> num_ages;
      EXCEPT( file.good(), "Error reading ages file." );
      LOGILN( "Number of ages: ", num_ages );

      // Read the ages.
      vector<real_type> bin_ages( num_ages );
      for( unsigned ii = 0; ii < num_ages; ++ii )
         file >> bin_ages[ii];
      EXCEPT( file.good(), "Error reading ages file." );

#ifndef NDEBUG
      // Must be ordered.
      for( unsigned ii = 1; ii < bin_ages.size(); ++ii )
         ASSERT( bin_ages[ii] >= bin_ages[ii - 1], "Bin ages must be descending ordered." );
#endif

      // Setup the bin ages.
      _age_bins.set_ages( bin_ages );

      LOGILN( "Done.", setindent( -2 ) );
   }

   void
   stellar_population::_load_ssp( const fs::path& filename )
   {
      LOGILN( "Loading stellar population from: ", filename, setindent( 2 ) );

      std::ifstream file( filename.c_str() );
      EXCEPT( file.is_open(), "Couldn't find SSP file: ", filename );

      // Allocate. Note that the ordering goes time,spectra,metals.
      _spec.reallocate( _age_bins.size()*_waves.size()*(_metal_bins.size() + 1) );
      LOGILN( "Number of spectra entries: ", _spec.size() );

      // Read in the file in one big go.
      for( unsigned ii = 0; ii < _spec.size(); ++ii )
      {
         // These values are luminosity densities, in erg/s/angstrom.
         file >> _spec[ii];
      }
      EXCEPT( file.good(), "Error reading SSP file." );

      LOGILN( "Done.", setindent( -2 ) );
   }

}
