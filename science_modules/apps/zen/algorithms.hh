#ifndef tao_zen_algorithms_hh
#define tao_zen_algorithms_hh

#include <tao/base/sfh.hh>
#include <tao/base/types.hh>

namespace tao {
   namespace algorithms {

      unsigned
      tree_height( const tao::sfh<real_type>& sfh,
                   unsigned gal_id,
                   unsigned height = 0,
                   unsigned cur_height = 0 );

      void
      tree_heights( const tao::sfh<real_type>& sfh,
                    unsigned gal_id,
                    vector<unsigned>::view heights );

      void
      tree_widths( const tao::sfh<real_type>& sfh,
                   unsigned gal_id,
                   vector<unsigned>::view widths );

   }
}

#endif
