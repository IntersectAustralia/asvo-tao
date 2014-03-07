#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>
#include <tao/tao.hh>
#include "application.hh"

application::application( int argc,
			  char* argv[] )
  : hpc::mpi::application( argc, argv )
{
   // // Setup logging.
   // LOG_PUSH( new hpc::logging::stdout( hpc::logging::info ) );

   // Setup some options.
   options().add_options()
      ( "load-sfh,s", hpc::po::value<fs::path>( &_sfh_path ), "Path of star formation history." );

   // Parse options.
   parse_options( argc, argv );
}

void
application::operator()()
{
   typedef hpc::view<std::vector<tao::real_type>>::type view_type;
   typedef hpc::numerics::spline<tao::real_type,view_type,view_type> spline_type;

   // Pick a simulation.
   tao::simulation* sim = &tao::millennium;

   // Connect the backend.
   tao::backends::multidb<tao::real_type> be;
   {
#include "credentials.hh"
      hpc::vector<tao::backends::multidb<tao::real_type>::server_type> servers( 3 );
      servers[0].dbname = "millennium_full_3servers_v2";
      servers[0].user = username;
      servers[0].passwd = password;
      servers[0].host = hpc::string( "tao01.hpc.swin.edu.au" );
      servers[0].port = 3306;
      servers[1].dbname = "millennium_full_3servers_v2";
      servers[1].user = username;
      servers[1].passwd = password;
      servers[1].host = hpc::string( "tao02.hpc.swin.edu.au" );
      servers[1].port = 3306;
      servers[2].dbname = "millennium_full_3servers_v2";
      servers[2].user = username;
      servers[2].passwd = password;
      servers[2].host = hpc::string( "tao03.hpc.swin.edu.au" );
      servers[2].port = 3306;
      be.connect( servers.begin(), servers.end() );
      be.set_simulation( sim );
   }

   // Load the stellar population model.
   tao::stellar_population ssp;
   ssp.load( "data/stellar_populations/m05/ages.dat",
	     "data/stellar_populations/m05/wavelengths.dat",
	     "data/stellar_populations/m05/metallicities.dat",
	     "data/stellar_populations/m05/ssp.ssz" );

   // Load the bandpass filter.
   tao::bandpass bpf( "data/bandpass_filters/k.dat" );

   // Load snapshot age line.
   tao::age_line<tao::real_type> snap_ages( be.session(), *sim );

   // Check if we should be loading a star formation history.
   if( _sfh_path.empty() )
   {
      // Track results and global indices.
      std::vector<long long> gids;
      gids.reserve( 40000 );
      std::vector<tao::real_type> results;
      results.reserve( 40000 );

      // Do a silly iteration over all the galaxies.
      tao::box<tao::real_type> box( sim );
      box.set_snapshot( 63 );
      tao::query<tao::real_type> qry;
      qry.add_output_field( "stellarmass" );
      for( auto gal_it = be.galaxy_begin( qry, box ); gal_it != be.galaxy_end( qry, box ); ++gal_it )
      {
	 tao::batch<tao::real_type> bat = *gal_it;
	 auto const snaps = bat.scalar<int>( "snapnum" );
	 auto const& tbl = bat.attribute<hpc::string>( "table" );
	 auto const tree_gids = bat.scalar<long long>( "globaltreeid" );
	 auto gal_gids = bat.scalar<long long>( "globalindex" );
	 auto stellar_mass = bat.scalar<tao::real_type>( "stellarmass" );

	 for( unsigned ii = 0; ii < bat.size(); ++ii )
	 {
	    // Only use galaxies at redshift 0.
	    if( snaps[ii] != 63 )
	       continue;

	    // Load the SFH.
	    tao::sfh<tao::real_type> sfh;
	    sfh.set_snapshot_ages( &snap_ages );
	    sfh.set_bin_ages( &ssp.bin_ages() );
	    sfh.load_tree_data( be.session( tbl ), tbl, tree_gids[ii], gal_gids[ii] );

	    // Rebin.
	    hpc::vector<tao::real_type> age_masses( ssp.age_masses_size() );
	    hpc::vector<tao::real_type> age_bulge_masses( ssp.age_masses_size() );
	    // hpc::vector<tao::real_type> age_masses( ssp.bin_ages().size() );
	    // hpc::vector<tao::real_type> age_bulge_masses( ssp.bin_ages().size() );
	    // hpc::vector<tao::real_type> age_metals( ssp.bin_ages().size() );
	    std::fill( age_masses.begin(), age_masses.end(), 0 );
	    std::fill( age_bulge_masses.begin(), age_bulge_masses.end(), 0 );
	    // std::fill( age_metals.begin(), age_metals.end(), 0 );
	    // sfh.rebin_chiara<tao::real_type>( age_masses, age_bulge_masses, age_metals );
	    sfh.rebin<tao::real_type>( age_masses, age_bulge_masses, ssp );

	    // std::cout << sfh.size() << "\n";
	    tao::real_type my_mass = std::accumulate( age_masses.begin(), age_masses.end(), 0.0 ); //*0.43;
	    // tao::real_type sage_mass = stellar_mass[ii]*1e10;
	    // if( sage_mass > 0.0 )
	    //    std::cout << my_mass << ", " << sage_mass << ", " << (my_mass - sage_mass)/sage_mass << "\n";

	    // if( gal_gids[ii] == 554394 )
	    // {
	    //    for( unsigned jj = 0; jj < ssp.bin_ages().size(); ++jj )
	    //    {
	    //    	  std::cout << jj << "  :  ";
	    //    	  for( unsigned kk = 0; kk < ssp.num_metal_bins(); ++kk )
	    //    	     std::cout << age_masses[jj*ssp.num_metal_bins() + kk] << "  ";
	    //    	  std::cout << "\n";
	    //    }
	    //    std::cout << sfh.snapshots() << "\n";
	    //    std::cout << sfh.sfrs() << "\n";
	    //    std::cout << sfh.masses() << "\n";
	    //    std::cout << sfh.ages() << "\n";
	    //    exit( 0 );
	    // }

	    // Sum from SSP.
	    hpc::vector<tao::real_type> total_spectra( ssp.wavelengths().size() );
	    // ssp.sum_chiara( age_masses.begin(), age_metals.begin(), total_spectra.begin() );
	    ssp.sum( age_masses.begin(), total_spectra.begin() );

	    // Compute magnitudes.
	    auto waves = ssp.wavelengths();
	    tao::sed<spline_type> sed(
	       (const hpc::view<std::vector<tao::real_type>>::type&)waves,
	       (const hpc::vector_view<std::vector<tao::real_type>>&)total_spectra
	       );
	    auto abs_mag = tao::absolute_magnitude( sed, bpf );

	    // std::cout << abs_mag << "\n";
	    // gids.push_back( gal_gids[ii] );
	    // results.push_back( abs_mag );
	 }
      }

      // // Order based on global indices.
      // std::sort(
      // 	 hpc::make_sort_permute_iter( gids.begin(), results.begin() ),
      // 	 hpc::make_sort_permute_iter( gids.end(), results.end() ),
      // 	 hpc::sort_permute_iter_compare<std::vector<long long>::iterator,std::vector<tao::real_type>::iterator>()
      // 	 );

      // // Dump results.
      // for( unsigned ii = 0; ii < results.size(); ++ii )
      // 	 std::cout << gids[ii] << "   " << results[ii] << "\n";
   }
   else
   {
      // Load the SFH.
      tao::sfh<tao::real_type> sfh( &snap_ages, &ssp.bin_ages(), _sfh_path );

      // Rebin.
      hpc::vector<tao::real_type> age_masses( ssp.age_masses_size() );
      hpc::vector<tao::real_type> age_bulge_masses( ssp.age_masses_size() );
      // hpc::vector<tao::real_type> age_masses( ssp.bin_ages().size() );
      // hpc::vector<tao::real_type> age_bulge_masses( ssp.bin_ages().size() );
      // hpc::vector<tao::real_type> age_metals( ssp.bin_ages().size() );
      std::fill( age_masses.begin(), age_masses.end(), 0 );
      std::fill( age_bulge_masses.begin(), age_bulge_masses.end(), 0 );
      // std::fill( age_metals.begin(), age_metals.end(), 0 );
      // sfh.rebin_chiara<tao::real_type>( age_masses, age_bulge_masses, age_metals );
      sfh.rebin<tao::real_type>( age_masses, age_bulge_masses, ssp );

      std::cout << std::accumulate( age_masses.begin(), age_masses.end(), 0.0 ) << "\n";
      for( unsigned ii = 0; ii < ssp.bin_ages().size(); ++ii )
      {
      	 std::cout << ii << "  :  ";
      	 for( unsigned jj = 0; jj < ssp.num_metal_bins(); ++jj )
      	    std::cout << age_masses[ii*ssp.num_metal_bins() + jj] << " ";
      	 std::cout << "\n";
      }

      // Sum from SSP.
      hpc::vector<tao::real_type> total_spectra( ssp.wavelengths().size() );
      // ssp.sum_chiara( age_masses.begin(), age_metals.begin(), total_spectra.begin() );
      ssp.sum( age_masses.begin(), total_spectra.begin() );

      // Compute magnitudes.
      auto waves = ssp.wavelengths();
      tao::sed<spline_type> sed(
      	 (const hpc::view<std::vector<tao::real_type>>::type&)waves,
      	 (const hpc::vector_view<std::vector<tao::real_type>>&)total_spectra
      	 );
      auto abs_mag = tao::absolute_magnitude( sed, bpf );

      std::cout << abs_mag << "\n";
   }
}
