#ifndef tao_base_bandpass_hh
#define tao_base_bandpass_hh

#include <libhpc/system/filesystem.hh>
#include <libhpc/numerics/spline.hh>
#include "integration.hh"
#include "types.hh"

namespace tao {

   template< class > class sed;

   template< class Spline >
   void
   load_bandpass( hpc::fs::path const& filename,
                  Spline& trans )
   {
      LOGBLOCKI( "Loading bandpass filter at: ", filename );

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
         EXCEPT( pnts[ii] >= 0.0, "Found an invalid wavelength in bandpass filter: ", filename );
         EXCEPT( vals[ii] >= 0.0, "Found an invalid transmission in bandpass filter: ", filename );
      }

      // Convert the spectrum to a spline.
      trans.set_knot_points( pnts );
      trans.set_knot_values( vals );
      trans.update();
   }

   class bandpass
   {
   public:

      bandpass();

      bandpass( const hpc::fs::path& filename );

      void
      load( const hpc::fs::path& filename );

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

      const hpc::num::spline<real_type>&
      transmission() const;

   public:

      hpc::num::spline<real_type> _trans;
      real_type _sum;
   };

}

#endif
