#include <boost/algorithm/string/trim.hpp>
#include <libhpc/logging/logging.hh>
#include "sed.hh"
#include "integration.hh"
#include "bandpass.hh"

namespace tao {
   using namespace hpc;

   void
   load_sed( const string& filename,
             numerics::spline<real_type>& spec )
   {
      LOGILN( "Loading SED at: ", filename, setindent( 2 ) );

      std::ifstream file( filename, std::ios::in );
      ASSERT( file );

      // The Vega file is a spectrum. First column is wavelength and
      // second column is luminosity density.
      unsigned num_waves = 0;
      while( !file.eof() )
      {
         string line;
         std::getline( file, line );
         if( boost::trim_copy( line ).length() )
            ++num_waves;
      }

      // Allocate.
      fibre<real_type> knots( 2, num_waves );

      // Reset the file position and go again.
      file.clear();
      file.seekg( 0, std::ios_base::beg );
      for( unsigned ii = 0; ii < num_waves; ++ii )
      {
         file >> knots(ii,0); // angstroms
         file >> knots(ii,1); // 2e17*erg/s/angstrom

         // I first need to multiply by 2e-17 to get to erg/s/angstrom.
         knots(ii,1) *= 2e-17;
      }

      // Convert the spectrum to a spline and convolve with each
      // filter.
      spec.set_knots( knots );

      LOGILN( "Done.", setindent( -2 ) );
   }

   sed::sed()
   {
   }

   sed::sed( const vector<real_type>::view waves )
   {
      _spec.set_size( waves.size() );
      std::copy( waves.begin(), waves.end(), _spec.abscissa_begin() );
      std::fill( _spec.values_begin(), _spec.values_end(), 0 );
   }

   sed::sed( const string& filename )
   {
      load( filename );
   }

   void
   sed::load( const string& filename )
   {
      load_sed( filename, _spec );
   }

   real_type
   sed::integrate( const bandpass& op ) const
   {
      return this->integrate( op.transmission() );
   }

   real_type
   sed::integrate( const numerics::spline<real_type>& op ) const
   {
      return integ::integrate( _spec, op );
   }

   numerics::spline<real_type>&
   sed::spectrum()
   {
      return _spec;
   }

   const numerics::spline<real_type>&
   sed::spectrum() const
   {
      return _spec;
   }

}
