#ifndef tao_base_bandpass_hh
#define tao_base_bandpass_hh

#include <boost/filesystem.hpp>
#include <libhpc/containers/string.hh>
#include <libhpc/numerics/spline.hh>
#include "integration.hh"
#include "types.hh"

namespace tao {
   using namespace hpc;
   namespace fs = boost::filesystem;

   template< class > class sed;

   template< class Spline >
   void
   load_bandpass( const fs::path& filename,
                  Spline& trans )
   {
      LOGILN( "Loading bandpass filter at: ", filename, setindent( 2 ) );

      // Open the file and validate.
      std::ifstream file( filename.c_str(), std::ios::in );
      EXCEPT( (bool)file, "Couldn't find bandpass filter: ", filename );

      // First entry is number of spectral bands.
      unsigned num_spectra;
      file >> num_spectra;

      // Allocate.
      typename Spline::knot_points_type pnts( num_spectra );
      typename Spline::knot_values_type vals( num_spectra );

      // Read in all the values.
      for( unsigned ii = 0; ii < num_spectra; ++ii )
      {
         file >> pnts[ii];
         file >> vals[ii];
      }

      // Convert the spectrum to a spline.
      trans.set_knot_points( pnts );
      trans.set_knot_values( vals );
      trans.update();

      LOGILN( "Done.", setindent( -2 ) );
   }

   class bandpass
   {
   public:

      bandpass();

      bandpass( const fs::path& filename );

      void
      load( const fs::path& filename );

      real_type
      integral() const;

      template< class Spline >
      real_type
      integrate( const sed<Spline>& op ) const
      {
         return this->integrate( op.spectrum() );
      }

      template< class Spline >
      real_type
      integrate( const Spline& op ) const
      {
         return tao::integrate( op, _trans );
      }

      const numerics::spline<real_type>&
      transmission() const;

   public:

      numerics::spline<real_type> _trans;
      real_type _sum;
   };

}

#endif
