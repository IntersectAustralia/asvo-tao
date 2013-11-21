#include <boost/lexical_cast.hpp>
#include "application.hh"

namespace tao {
   namespace analytic {

      application::application( int argc,
				char* argv[] )
	 : hpc::mpi::application( argc, argv )
      {
	 _box = boost::lexical_cast<real_type>( argv[1] );
	 _ra = boost::lexical_cast<real_type>( argv[2] );
	 _dec = boost::lexical_cast<real_type>( argv[3] );
	 _z = boost::lexical_cast<real_type>( argv[4] );
	 _idx = boost::lexical_cast<unsigned>( argv[5] );
      }

      void
      application::operator()()
      {
	 // Create a simulation.
	 tao::simulation<real_type> sim( _box, 0.73, 0.25, 0.75, 2, 0.1, 0.2 );

	 // Create a lightcone.
	 tao::lightcone<real_type> lc( &sim );
	 lc.set_geometry( 0.0, _ra, 0.0, _dec, _z );
	 std::cout << "Cone distance    = " << lc.max_dist() << "\n";

	 // Calculate origin and things.
	 unsigned max_cones = tao::calc_max_subcones( lc );
	 std::cout << "Maximum subcones = " << max_cones << "\n";
	 if( max_cones )
	 {
	    double theta = *tao::calc_subcone_angle( lc );
	    std::cout << "Angle            = " << to_degrees( theta ) << " degrees\n";
	    std::array<real_type,3> ori = tao::calc_subcone_origin<real_type>( lc, _idx );
	    std::cout << "Origin           = (" << ori[0] << ", " << ori[1] << ", " << ori[2] << ")\n";
	 }
      }

   }
}
