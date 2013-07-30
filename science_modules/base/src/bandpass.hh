#ifndef tao_base_bandpass_hh
#define tao_base_bandpass_hh

#include <libhpc/containers/string.hh>
#include <libhpc/numerics/spline.hh>
#include "types.hh"

namespace tao {
   using namespace hpc;

   class sed;

   void
   load_bandpass( const string& filename );

   class bandpass
   {
   public:

      bandpass();

      bandpass( const string& filename );

      void
      load( const string& filename );

      real_type
      integral() const;

      real_type
      integrate( const sed& op ) const;

      real_type
      integrate( const numerics::spline<real_type>& op ) const;

      const numerics::spline<real_type>&
      transmission() const;

   public:

      numerics::spline<real_type> _trans;
      real_type _sum;
   };

}

#endif
