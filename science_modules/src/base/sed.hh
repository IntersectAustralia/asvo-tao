#ifndef tao_base_sed_hh
#define tao_base_sed_hh

#include <boost/algorithm/string/trim.hpp>
#include <boost/filesystem.hpp>
#include <libhpc/logging/logging.hh>
#include <libhpc/containers/string.hh>
#include <libhpc/numerics/spline.hh>
#include "integration.hh"
#include "types.hh"

namespace tao {
   using namespace hpc;
   namespace fs = boost::filesystem;

   class bandpass;

   template< class Spline >
   void
   load_sed( const fs::path& filename,
             Spline& spec )
   {
      LOGILN( "Loading SED at: ", filename, setindent( 2 ) );

      // Open the file and check it exists.
      std::ifstream file( filename.c_str() );
      EXCEPT( (bool)file, "Unable to locate SED file: ", filename );

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
      EXCEPT( (bool)file, "Error reading SED file." );
      LOGILN( "Have ", num_waves, " wavelength entries." );

      // Allocate.
      typename Spline::knot_points_type pnts( num_waves );
      typename Spline::knot_values_type vals( num_waves );

      // Reset the file position and go again.
      file.clear();
      file.seekg( 0, std::ios_base::beg );
      for( unsigned ii = 0; ii < num_waves; ++ii )
      {
         file >> pnts[ii]; // angstroms
         file >> vals[ii]; // 2e17*erg/s/angstrom

         // I first need to multiply by 2e-17 to get to erg/s/angstrom.
         vals[ii] *= 2e-17;
      }
      EXCEPT( (bool)file, "Error reading SED file." );

      // Convert the spectrum to a spline.
      spec.set_knot_points( pnts );
      spec.set_knot_values( vals );
      spec.update();

      LOGILN( "Done.", setindent( -2 ) );
   }

   template< class Spline = numerics::spline<real_type> >
   class sed
   {
   public:

      typedef Spline spline_type;

   public:

      sed()
      {
      }

      sed( const typename spline_type::knot_points_type& pnts,
           const typename spline_type::knot_values_type& vals )
      {
         _spec.set_knot_points( pnts );
         _spec.set_knot_values( vals );
         _spec.update();
      }

      sed( const fs::path& filename )
      {
         load( filename );
      }

      void
      load( const fs::path& filename )
      {
         load_sed( filename, _spec );
      }

      real_type
      integrate( const bandpass& op ) const;

      template< class _Spline >
      real_type
      integrate( const _Spline& op ) const
      {
         return tao::integrate( _spec, op );
      }

      spline_type&
      spectrum()
      {
         return _spec;
      }

      const spline_type&
      spectrum() const
      {
         return _spec;
      }

   public:

      spline_type _spec;
   };

}

#include "bandpass.hh"

template< class Spline >
tao::real_type
tao::sed<Spline>::integrate( const tao::bandpass& op ) const
{
   return this->integrate( op.transmission() );
}

#endif
