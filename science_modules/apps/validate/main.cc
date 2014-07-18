#include <string>
#include <vector>
#include <libhpc/system/filesystem.hh>
#include <libhpc/mpi/application.hh>
#include <tao/tao.hh>

class application
   : public hpc::mpi::application
{
public:

   application( int argc,
                char* argv[] )
      : hpc::mpi::application( argc, argv )
   {
      // Setup some options.
      options().add_options()
         ( "mode,m", hpc::po::value<std::string>( &_mode )->default_value( "mass" ), "operation mode [mass]" )
         ( "sim,s", hpc::po::value<std::string>( &_sim )->default_value( "minimill" ), "simulation [minimill,mill]" )
         ( "snap,n", hpc::po::value<int>( &_snap )->default_value( 63 ), "snapshot" )
         ( "verbose,v", hpc::po::value<bool>( &_verb )->default_value( false ), "verbosity" );

      // Parse options.
      parse_options( argc, argv );

      // Check options.
      EXCEPT( _mode == "mass" || _mode == "ages" || _mode == "count", "Invalid mode." );
      EXCEPT( _sim == "minimill" || _sim == "mill" || _sim == "bolshoi", "Invalid simulation." );

      // Setup logging.
      if( _verb )
         LOG_PUSH( new hpc::log::stdout( hpc::log::info ) );
   }

   void
   operator()()
   {
      if( _mode == "mass" )
         _mass();
      else if( _mode == "count" )
         _count();
      else if( _mode == "ages" )
	 _ages();
   }

protected:

   void
   _mass()
   {
      typedef hpc::view<std::vector<tao::real_type>> view_type;
      typedef hpc::num::spline<tao::real_type,view_type,view_type> spline_type;

      tao::backends::multidb<tao::real_type> be;
      tao::simulation const* sim;
      _connect( be, sim );

      // Load the stellar population model.
      tao::stellar_population ssp;
      ssp.load( "data/stellar_populations/m05/ages.dat",
                "data/stellar_populations/m05/wavelengths.dat",
                "data/stellar_populations/m05/metallicities.dat",
                "data/stellar_populations/m05/ssp.ssz" );

      // Prepare staf formation history.
      tao::age_line<tao::real_type> snap_ages( be.session(), *sim );
      tao::sfh sfh;
      sfh.set_snapshot_ages( &snap_ages );

      // Do a silly iteration over all the galaxies.
      tao::box<tao::real_type> box( sim );
      box.set_snapshot( _snap );
      tao::query<tao::real_type> qry;
      qry.add_output_field( "stellarmass" );
      for( auto gal_it = be.galaxy_begin( qry, box ); gal_it != be.galaxy_end( qry, box ); ++gal_it )
      {
         tao::batch<tao::real_type> bat = *gal_it;
         auto const  snaps        = bat.scalar<int>( "snapnum" );
         auto const& tbl          = bat.attribute<std::string>( "table" );
         auto const  tree_gids    = bat.scalar<long long>( "globaltreeid" );
         auto        gal_gids     = bat.scalar<long long>( "globalindex" );
         auto        stellar_mass = bat.scalar<tao::real_type>( "stellarmass" );

         for( unsigned ii = 0; ii < bat.size(); ++ii )
         {
            // Load the SFH.
            sfh.load_tree_data( be.session( tbl ), tbl, tree_gids[ii], gal_gids[ii] );

            // Rebin.
            std::vector<tao::real_type> disk_masses( ssp.age_masses_size() );
            std::vector<tao::real_type> bulge_masses( ssp.age_masses_size() );
#ifndef NDEBUG
            tao::rebin_stats_type stats = sfh.rebin<decltype(disk_masses)>( disk_masses, bulge_masses, ssp );
#else
            sfh.rebin<decltype(disk_masses)>( disk_masses, bulge_masses, ssp );
#endif

            // Combine.
            std::vector<tao::real_type> total_masses( disk_masses.size() );
            std::transform( disk_masses.begin(), disk_masses.end(), bulge_masses.begin(), 
                            total_masses.begin(), std::plus<tao::real_type>() );

            // Display mass comparisons.
            tao::real_type my_mass  = std::accumulate( total_masses.begin(), total_masses.end(), 0.0 )*(1.0 - 0.43);
            tao::real_type mod_mass = stellar_mass[ii]*1e10;
            tao::real_type error = (mod_mass > 0.0) ? (my_mass - mod_mass)/mod_mass : 0.0;
            if( mod_mass > 0.0 )
            {
               std::cout << my_mass << ", " << mod_mass << ", " << (my_mass - mod_mass)/mod_mass;
#ifndef NDEBUG
               std::cout << ", " << stats.n_gals << ", " << stats.n_mergers << ", ";
               std::cout << stats.n_major << ", " << stats.n_minor << ", " << stats.n_disrupt;
#endif
               std::cout << "\n";
            }
         }
      }
   }

   void
   _count()
   {
      typedef hpc::view<std::vector<tao::real_type>> view_type;
      typedef hpc::num::spline<tao::real_type,view_type,view_type> spline_type;

      tao::backends::multidb<tao::real_type> be;
      tao::simulation const* sim;
      _connect( be, sim );

      // Keep count.
      unsigned long long cnt = 0;

      // Find all galaxies at redshift.
      tao::box<tao::real_type> box( sim );
      box.set_snapshot( _snap );
      tao::query<tao::real_type> qry;
      qry.add_output_field( "stellarmass" );
      for( auto gal_it = be.galaxy_begin( qry, box ); gal_it != be.galaxy_end( qry, box ); ++gal_it )
      {
         tao::batch<tao::real_type> bat = *gal_it;
	 auto const masses = bat.scalar<tao::real_type>( "stellarmass" );

	 // Check masses.
         for( unsigned ii = 0; ii < bat.size(); ++ii )
            ++cnt;
      }

      // Print results.
      std::cout << "Number of galaxies found: " << cnt << "\n";
   }

   void
   _ages()
   {
      tao::backends::multidb<tao::real_type> be;
      tao::simulation const* sim;
      _connect( be, sim );

      for( unsigned ii = 0; ii < sim->redshifts().size(); ++ii )
      {
	 tao::real_type z = sim->redshifts()[ii];
	 tao::real_type age = tao::redshift_to_age<tao::real_type>( z );
	 printf( "Age[%02d]\t (z=%e)\t = %e", ii, z, age );
	 if( ii > 0 )
	 {
	    tao::real_type zp = sim->redshifts()[ii - 1];
	    tao::real_type agep = tao::redshift_to_age<tao::real_type>( zp );
	    printf( "\t %e", fabs( age - agep ) );
	 }
	 printf( "\n" );
      }
   }

   void
   _connect( tao::backends::multidb<tao::real_type>& be,
	     tao::simulation const*& sim )
   {
      // Pick a simulation.
      std::string db_name;
      if( _sim == "bolshoi" )
         db_name = "bolshoi_full_3servers_v4";
      else if( _sim == "mill" )
         db_name = "millennium_full_3servers_v4";
      else
         db_name = "millennium_mini_3servers_v2";

      // Connect the backend.
#include "credentials.hh"
      std::vector<tao::backends::multidb<tao::real_type>::server_type> servers( 3 );
      servers[0].dbname = db_name;
      servers[0].user = username;
      servers[0].passwd = password;
      servers[0].host = std::string( "tao01.hpc.swin.edu.au" );
      servers[0].port = 3306;
      servers[1].dbname = db_name;
      servers[1].user = username;
      servers[1].passwd = password;
      servers[1].host = std::string( "tao02.hpc.swin.edu.au" );
      servers[1].port = 3306;
      servers[2].dbname = db_name;
      servers[2].user = username;
      servers[2].passwd = password;
      servers[2].host = std::string( "tao03.hpc.swin.edu.au" );
      servers[2].port = 3306;
      be.connect( servers.begin(), servers.end() );
      sim = be.load_simulation();
   }

protected:

   std::string _mode;
   std::string _sim;
   int _snap;
   bool _verb;
};

#define HPC_APP_CLASS application
#include <libhpc/mpi/main.hh>
