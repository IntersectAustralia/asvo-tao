#include <libhpc/libhpc.hh>
#include <tao/tao.hh>
#include "application.hh"

namespace tao {
   namespace analytic {

      application::application( int argc,
				char* argv[] )
	 : hpc::mpi::application( argc, argv )
      {
	 // LOG_PUSH( new hpc::logging::stdout( hpc::logging::debug ) );
      }

      void
      application::operator()()
      {
	 // Pick a simulation for cosmological constants.
	 tao::simulation<tao::real_type>* sim = &mini_millennium;

	 // Load the stellar population model.
	 tao::stellar_population ssp;
	 ssp.load( "ssp_ages.dat",
		   "ssp_wavelengths.dat",
		   "ssp_metallicities.dat",
		   "ssp.dat" );

	 // Load snapshot ages.
	 tao::age_line<real_type> snap_ages( "snapshots.dat" );

	 // Load the SFH from file.
	 tao::sfh<tao::real_type> sfh(
	    &snap_ages, &ssp.bin_ages(),
	    "merger_tree.dat"
	    );

	 // Rebin.
	 vector<real_type> age_masses( ssp.bin_ages().size() );
	 vector<real_type> age_bulge_masses( ssp.bin_ages().size() );
	 vector<real_type> age_metals( ssp.bin_ages().size() );
	 sfh.rebin<real_type>( age_masses, age_bulge_masses, age_metals );
	 // std::cout << "Rebinned masses: " << age_masses << "\n";
	 // std::cout << "Rebinned metals: " << age_metals << "\n";

	 // Sum stellar population into SED. I first create an efficient SED object,
	 // that being one that uses a view to access abscissa and a normal vector
	 // to store the spectrum.
	 typedef hpc::vector<real_type>::view view_type;
	 typedef hpc::numerics::spline<real_type,view_type> spline_type;
	 tao::sed<spline_type> sed;
	 {
	    std::vector<real_type> spectra( ssp.wavelengths().size() );
	    ssp.sum( age_masses.begin(), age_metals.begin(), spectra.begin() );
	    // std::cout << "Summed spectra: " << spectra << "\n";
	    sed.spectrum().set_knot_points( ssp.wavelengths() );
	    sed.spectrum().set_knot_values( spectra );
	    sed.spectrum().update();
	 }

	 // Load the bandpass filter.
	 tao::bandpass bpf( "bandpass.dat" );

	 // Calculate the magnitude.
	 std::cout << std::setprecision( 12 ) << "denominator = " << bpf.integral() << "\n";
	 std::cout << std::setprecision( 12 ) << "enumerator = " << sed.integrate( bpf ) << "\n";
	 real_type mag = tao::apparent_magnitude( sed, bpf, 0 );

	 // Dump result.
	 std::cout << std::setprecision( 12 ) << "magnitude = " << mag << "\n";
      }

   }
}
