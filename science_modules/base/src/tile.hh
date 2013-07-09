#ifndef tao_base_tile_hh
#define tao_base_tile_hh

#include <libhpc/containers/array.hh>

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone;

   template< class T >
   class tile
   {
   public:

      typedef T real_type;

   public:

      tile( lightcone<real_type>& lc,
            const array<real_type,3>& offs )
         : _lc( lc ),
           _offs( offs )
      {
      }

      array<real_type,3>
      min() const
      {
         return _offs;
      }

      array<real_type,3>
      max() const
      {
         real_type bs = _lc.simulation().box_size();
         return array<real_type,3>( _offs[0] + bs, _offs[1] + bs, _offs[2] + bs );
      }

   protected:

      lightcone<real_type>& _lc;
      array<real_type,3> _offs;
   };

}

#endif
