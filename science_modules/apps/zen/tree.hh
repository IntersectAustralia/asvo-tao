#ifndef tao_zen_tree_hh
#define tao_zen_tree_hh

#include <GL/gl.h>
#include "algorithms.hh"

namespace tao {

   unsigned
   calc_max_snapshot( const tao::sfh<real_type>& sfh,
                      unsigned gal_id,
                      unsigned max_snap = std::numeric_limits<unsigned>::max() );

   void
   draw_snapshot_range( const array<real_type,2>& snap_rng );

   void
   draw_sfh_tree( const tao::sfh<real_type>& sfh,
                  unsigned gal_id );

   void
   render_sfh_tree();

}

#endif