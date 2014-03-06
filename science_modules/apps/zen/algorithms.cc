#include "algorithms.hh"

namespace tao {
   namespace algorithms {

      unsigned
      tree_height( const tao::sfh<real_type>& sfh,
                   unsigned gal_id,
                   unsigned height,
                   unsigned cur_height )
      {
         ++cur_height;
         if( cur_height > height )
            height = cur_height;
         auto rng = sfh.parents( gal_id );
         while( rng.first != rng.second )
            height = tree_height( sfh, gal_id, height, cur_height );
         return height;
      }

      void
      _tree_heights_recurse( const tao::sfh<real_type>& sfh,
                             unsigned gal_id,
                             vector<unsigned>::view heights )
      {
         heights[gal_id] = 1;
         auto rng = sfh.parents( gal_id );
         while( rng.first != rng.second )
         {
            _tree_heights_recurse( sfh, rng.first->second, heights );
            heights[gal_id] += heights[rng.first->second];
            ++rng.first;
         }
      }

      void
      tree_heights( const tao::sfh<real_type>& sfh,
                    unsigned gal_id,
                    vector<unsigned>::view heights )
      {
         std::fill( heights.begin(), heights.end(), 0 );
         _tree_heights_recurse( sfh, gal_id, heights );
      }

      unsigned
      _tree_widths_recurse( const tao::sfh<real_type>& sfh,
                            unsigned gal_id,
                            vector<unsigned>::view widths )
      {
         // LOGBLOCKD( "Recursing onto: ", gal_id );
         unsigned my_width = 0;
         auto rng = sfh.parents( gal_id );
         while( rng.first != rng.second )
         {
            my_width += _tree_widths_recurse( sfh, rng.first->second, widths );
            ++rng.first;
         }
         if( my_width == 0 )
            my_width = 1;
         widths[gal_id] = my_width;
         return my_width;
      }

      void
      tree_widths( const tao::sfh<real_type>& sfh,
                   unsigned gal_id,
                   vector<unsigned>::view widths )
      {
         // LOGBLOCKD( "Building tree widths for galaxy with local galaxy ID: ", gal_id );
         std::fill( widths.begin(), widths.end(), 0 );
         _tree_widths_recurse( sfh, gal_id, widths );
      }

   }
}
