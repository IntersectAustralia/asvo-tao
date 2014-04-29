#include <libhpc/numerics/integrate.hh>
#include <libhpc/logging.hh>
#include "bandpass.hh"
#include "sed.hh"

namespace tao {

   bandpass::bandpass()
      : _sum( 0 )
   {
   }

   bandpass::bandpass( const hpc::fs::path& filename )
   {
      load( filename );
   }

   void
   bandpass::load( const hpc::fs::path& filename )
   {
      load_bandpass( filename, _trans );
      _sum = tao::integrate( _trans );
      ASSERT( _sum == _sum, "Produced NaN for integration of bandpass filter: ", filename );
   }

   real_type
   bandpass::integral() const
   {
      return _sum;
   }

  const hpc::num::spline<real_type>&
   bandpass::transmission() const
   {
      return _trans;
   }

}
