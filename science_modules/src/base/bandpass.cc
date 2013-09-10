#include <libhpc/numerics/integrate.hh>
#include <libhpc/logging/logging.hh>
#include "bandpass.hh"
#include "sed.hh"

namespace tao {
   using namespace hpc;
   namespace fs = boost::filesystem;

   bandpass::bandpass()
      : _sum( 0 )
   {
   }

   bandpass::bandpass( const fs::path& filename )
   {
      load( filename );
   }

   void
   bandpass::load( const fs::path& filename )
   {
      load_bandpass( filename, _trans );
      _sum = tao::integrate( _trans );
   }

   real_type
   bandpass::integral() const
   {
      return _sum;
   }

   const numerics::spline<real_type>&
   bandpass::transmission() const
   {
      return _trans;
   }

}
