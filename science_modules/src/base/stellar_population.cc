#include <boost/algorithm/string/trim.hpp>
#include <libhpc/algorithm/bin.hh>
#include <libhpc/algorithm/dual.hh>
#include <libhpc/logging/block.hh>
#include "stellar_population.hh"

namespace tao {
   namespace fs = boost::filesystem;
   using namespace hpc;

   stellar_population::stellar_population()
      : _com_rec_frac( 1.0 )
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
   stellar_population::set_recycle_fraction( real_type rec_frac )
   {
      ASSERT( rec_frac >= 0.0 && rec_frac <= 1.0,
              "Invalid recycle fraction given to SSP summation: ", rec_frac );
      _com_rec_frac = 1.0 - rec_frac;
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

   void
   stellar_population::save( const fs::path& ages_filename,
                             const fs::path& waves_filename,
                             const fs::path& metals_filename,
                             const fs::path& ssp_filename )
   {
      _save_ages( ages_filename );
      _save_waves( waves_filename );
      _save_metals( metals_filename );
      _save_ssp( ssp_filename );
   }

   void
   stellar_population::restrict()
   {
      // Just use new vectors for simplicity.
      vector<real_type> new_waves( _waves.size()/2 );
      vector<real_type> new_ages( _age_bins.size()/2 );
      vector<real_type> new_spec( new_waves.size()*new_ages.size()*(_metal_bins.size() + 1) );

      // Halve things.
      for( unsigned ii = 0; ii < new_waves.size(); ++ii )
      {
	 new_waves[ii] = _waves[2*ii];

	 for( unsigned jj = 0; jj < new_ages.size(); ++jj )
	 {
	    new_ages[jj] = _age_bins[2*jj];

	    for( unsigned kk = 0; kk <= _metal_bins.size(); ++kk )
	    {
	       new_spec[jj*new_waves.size()*(_metal_bins.size() + 1) + ii*(_metal_bins.size() + 1) + kk]
		  = at( 2*jj, 2*ii, kk );
	    }
	 }
      }

      // Swap everything out.
      _waves.swap( new_waves );
      _spec.swap( new_spec );
      _age_bins.set_ages( new_ages );
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

#if 0
      // Read recycling fraction first.
      real_type rec_frac;
      file >> rec_frac;
      EXCEPT( !file.fail(), "Failed while reading recycling fraction." );
      set_recycle_fraction( rec_frac );
      LOGILN( "Set recycling fraction to: ", rec_frac );
#endif

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

   void
   stellar_population::_save_metals( const fs::path& filename )
   {
      LOGBLOCKI( "Saving metallicities to: ", filename );

      std::ofstream file( filename.c_str() );
      EXCEPT( file.is_open(), "Couldn't open metallicities file: ", filename );

      // Store the dual values.
      file << "dual\n";
      file << _metal_bins.size() << "\n";
      for( auto met : _metal_bins )
	 file << met << "\n";

      ASSERT( file, "Failed to write metallicities file: ", filename );
   }

   void
   stellar_population::_save_waves( const fs::path& filename )
   {
      LOGBLOCKI( "Saving wavelengths to: ", filename );

      // Open the file.
      std::ofstream file( filename.c_str() );
      EXCEPT( file.is_open(), "Couldn't open wavelengths file: ", filename );

      // Dump wavelengths.
      for( auto wave : _waves )
	 file << wave << "\n";
   }

   void
   stellar_population::_save_ages( const fs::path& filename )
   {
      LOGBLOCKI( "Saving ages to: ", filename );

      // Open the file.
      std::ofstream file( filename.c_str() );
      EXCEPT( file.is_open(), "Couldn't open ages file: ", filename );

      // Dump the ages.
      file << _age_bins.size() << "\n";
      for( auto age : _age_bins.ages() )
	 file << age << "\n";
   }

   void
   stellar_population::_save_ssp( const fs::path& filename )
   {
      LOGBLOCKI( "Saving stellar population to: ", filename );

      std::ofstream file( filename.c_str() );
      EXCEPT( file.is_open(), "Couldn't open SSP file: ", filename );

#if 0
      // Write recycling fraction first.
      real_type rec_frac = 1.0 - _com_rec_frac;
      file << rec_frac;
      EXCEPT( !file.fail(), "Failed while writing recycling fraction." );
#endif

      // Dump the SSP data in the same kind of format as
      // the originals.
      unsigned pos = 0;
      for( auto val : _spec )
      {
	 file << val;
	 if( ++pos == _metal_bins.size() + 1 )
	 {
	    file << "\n";
	    pos = 0;
	 }
	 else
	    file << " ";
      }
   }

}
