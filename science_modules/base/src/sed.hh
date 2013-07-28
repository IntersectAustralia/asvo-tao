#ifndef tao_base_sed_hh
#define tao_base_sed_hh

#include <libhpc/containers/string.hh>
#include <libhpc/numerics/spline.hh>
#include "types.hh"

namespace tao {

   class bandpass;

   void
   load_sed( const string& filename );

   class sed
   {
   public:

      sed();

      sed( const vector<real_type>::view waves );

      sed( const string& filename );

      void
      load( const string& filename );

      real_type
      integrate( const bandpass& op ) const;

      real_type
      integrate( const numerics::spline<real_type>& op ) const;

      numerics::spline<real_type>&
      spectrum();

      const numerics::spline<real_type>&
      spectrum() const;

   public:

      numerics::spline<real_type> _spec;
   };

}

#endif
