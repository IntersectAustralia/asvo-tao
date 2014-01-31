#include <math.h>
#include <libhpc/algorithm/ridders.hh>
#include "subcones.hh"

namespace tao {

   boost::optional<double>
   calc_subcone_angle( tao::lightcone const& lc )
   {
      EXCEPT( lc.min_ra() == 0.0, "Subcones must have mininum RA of 0." );
      EXCEPT( lc.min_dec() == 0.0, "Subcones must have mininum DEC of 0." );

      tao::simulation const* sim = lc.simulation();
      double b = sim->box_size();
      double ra = lc.max_ra() - lc.min_ra();
      double d = lc.max_dist();

      // If the cone fits in one box then return zero.
      if( d <= b )
	 return 0.0;

      // Use Ridder's method to find the optimal angle for
      // unique cones.
      return hpc::algorithm::ridders(
      	 [ra, d, b]( double x )
	 {
	    double phi = ra + x;
	    double y = b - d*(cos( x ) - sin( x )/tan( phi ));
	    return y;
      	 },
	 0.5*M_PI,
	 0.0
      	 );
   }

   unsigned
   calc_max_subcones( tao::lightcone const& lc )
   {
      auto theta = calc_subcone_angle( lc );
      if( !theta )
	 return 0;
      double b = lc.simulation()->box_size();
      double d = lc.max_dist();
      double phi = *theta + lc.max_ra();
      double h = d*sin( phi );
      double h_dec = d*sin( lc.max_dec() );
      return (unsigned)(floor( b/h )*floor( b/h_dec ));
   }

}
