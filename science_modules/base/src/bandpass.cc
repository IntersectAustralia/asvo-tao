#include "bandpass.hh"
#include "integration.hh"

namespace tao {

   void
   load_bandpass( const string& filename,
                  numerics::spline<real_type>& trans )
   {
      LOGILN( "Loading bandpass filter at: ", filename, setindent( 2 ) );

      std::ifstream file( filename, std::ios::in );
      ASSERT( file );

      // First entry is number of spectral bands.
      unsigned num_spectra;
      file >> num_spectra;

      // Read in all the values.
      fibre<real_type> knots( 2, num_spectra );
      for( unsigned ii = 0; ii < num_spectra; ++ii )
      {
         file >> knots(ii,0);
         file >> knots(ii,1);
      }

      // Setup the spline.
      trans.set_knots( knots );

      LOGILN( "Done.", setindent( -2 ) );
   }

   bandpass::bandpass()
      : _sum( 0 )
   {
   }

   bandpass::bandpass( const string& filename )
   {
      load( filename );
   }

   void
   bandpass::load( const string& filename )
   {
      // Load the filter.
      load_bandpass( filename, _trans );

      // Integrate the filter and cache the result.
      _sum = integrate( _trans );
   }

   real_type
   bandpass::integral() const
   {
      return _sum;
   }

   real_type
   bandpass::integrate( const sed& op ) const
   {
      return this->integrate( op.spectrum() );
   }

   real_type
   bandpass::integrate( const numerics::spline<real_type>& op ) const
   {
      return tao::integrate( _trans, op );
   }

   const numerics::splie<real_type>&
   bandpass::transmission() const
   {
      return _trans;
   }

}
