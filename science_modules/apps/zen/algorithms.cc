#include "algorithms.hh"

namespace tao {
   namespace algorithms {

      unsigned
      tree_height( tao::sfh const& sfh,
                   unsigned gal_id,
                   unsigned height,
                   unsigned cur_height )
      {
         ++cur_height;
         if( cur_height > height )
            height = cur_height;
         auto pars = sfh.parents( gal_id );
         for( size_t ii = 0; ii < pars.size(); ++ii )
            height = tree_height( sfh, gal_id, height, cur_height );
         return height;
      }

      void
      _tree_heights_recurse( tao::sfh const& sfh,
                             unsigned gal_id,
                             hpc::view<std::vector<unsigned>> heights )
      {
         heights[gal_id] = 1;
         auto pars = sfh.parents( gal_id );
         for( size_t ii = 0; ii < pars.size(); ++ii )
         {
            _tree_heights_recurse( sfh, pars[ii], heights );
            heights[gal_id] += heights[pars[ii]];
         }
      }

      void
      tree_heights( const tao::sfh& sfh,
                    unsigned gal_id,
                    hpc::view<std::vector<unsigned>> heights )
      {
         std::fill( heights.begin(), heights.end(), 0 );
         _tree_heights_recurse( sfh, gal_id, heights );
      }

      unsigned
      _tree_widths_recurse( const tao::sfh& sfh,
                            unsigned gal_id,
                            hpc::view<std::vector<unsigned>> widths )
      {
         // LOGBLOCKD( "Recursing onto: ", gal_id );
         unsigned my_width = 0;
         auto pars = sfh.parents( gal_id );
         for( size_t ii = 0; ii < pars.size(); ++ii )
            my_width += _tree_widths_recurse( sfh, pars[ii], widths );
         if( my_width == 0 )
            my_width = 1;
         widths[gal_id] = my_width;
         return my_width;
      }

      void
      tree_widths( const tao::sfh& sfh,
                   unsigned gal_id,
                   hpc::view<std::vector<unsigned>> widths )
      {
         // LOGBLOCKD( "Building tree widths for galaxy with local galaxy ID: ", gal_id );
         std::fill( widths.begin(), widths.end(), 0 );
         _tree_widths_recurse( sfh, gal_id, widths );
      }

   }
}
