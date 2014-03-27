#ifndef tao_base_subcones_hh
#define tao_base_subcones_hh

#include <array>
#include <boost/optional.hpp>
#include "types.hh"
#include "lightcone.hh"

namespace tao {

   boost::optional<double>
   calc_subcone_angle( tao::lightcone const& lc );

   unsigned
   calc_max_subcones( tao::lightcone const& lc );

   template< class T >
   std::array<T,3>
   calc_subcone_origin( tao::lightcone const& lc,
			unsigned sub_idx )
   {
      // Cache certain values.
      double theta = *calc_subcone_angle( lc );
      double b = lc.simulation()->box_size();
      double d0 = lc.min_dist();
      double d1 = lc.max_dist();
      double phi = theta + lc.max_ra();

      // Calculate the cone RA height and declination height.
      double h = d1*sin( phi ) - d0*sin( theta );
      double h_dec = d1*sin( lc.max_dec() );

      // How many will fit in the domain?
      unsigned ny = floor( b/h );
      unsigned nz = floor( b/h_dec );

      // Calc origin of sub_idx.
      return std::array<T,3>{ -d0*cos( phi ), (sub_idx%ny)*h - d0*sin( theta ), (sub_idx/ny)*h_dec };
   }

}

#endif
