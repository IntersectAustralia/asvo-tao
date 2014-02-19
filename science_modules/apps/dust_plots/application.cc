#include <libhpc/libhpc.hh>
#include <tao/tao.hh>
#include "application.hh"

application::application( int argc,
                          char* argv[] )
   : hpc::application( argc, argv )
{
}

void
application::operator()()
{
   // Pick a simulation.
   tao::simulation* sim = &tao::mini_millennium;

   // Connect the backend.
   tao::backends::multidb<tao::real_type> be;
   {
#include "credentials.hh"
      hpc::vector<tao::backends::multidb<tao::real_type>::server_type> servers( 2 );
      servers[0].dbname = "millennium_mini_balanced_v3";
      servers[0].user = username;
      servers[0].passwd = password;
      servers[0].host = hpc::string( "tao01.hpc.swin.edu.au" );
      servers[0].port = 3306;
      servers[1].dbname = "millennium_mini_balanced_v3";
      servers[1].user = username;
      servers[1].passwd = password;
      servers[1].host = hpc::string( "tao02.hpc.swin.edu.au" );
      servers[1].port = 3306;
      be.connect( servers.begin(), servers.end() );
      be.set_simulation( sim );
   }

   // Load the stellar population model.
   tao::stellar_population ssp;
   ssp.load( "data/stellar_populations/m05/ages.dat",
             "data/stellar_populations/m05/wavelengths.dat",
             "data/stellar_populations/m05/metallicities.dat",
             "data/stellar_populations/m05/ssp.ssz" );

   // Stuff for histogram.
   tao::real_type width = 1.0;
   unsigned nbins = 100;
   tao::real_type bin_width = width/(tao::real_type)nbins;
   std::vector<unsigned> histo( nbins );
   unsigned lambda_1500 = 0;
   while( ssp.wavelengths()[lambda_1500] < 1500.0 )
      ++lambda_1500;

   for( unsigned jj = 0; jj < 1000; ++jj )
   {
      // Pick a table and entry at random.
      hpc::string tbl = "tree_" + hpc::to_string( hpc::generate_uniform<int>( 1, 50 ) );
      unsigned ngals;
      be.session( tbl ) << "SELECT COUNT(*) FROM " + tbl + " WHERE sfr > 1",
         soci::into( ngals );
      unsigned obj_idx = hpc::generate_uniform<unsigned>( 0, ngals - 1 );

      // Query.
      unsigned num_objs = 1;
      std::vector<long long> tree_ids( num_objs ), gids( num_objs );
      std::vector<int> snapshot( num_objs );
      std::vector<tao::real_type> disk_radius( num_objs ), cold_gas_mass( num_objs ),
         cold_gas_metal( num_objs ), stellar_mass( num_objs );
      be.session( tbl ) << "SELECT globaltreeid, globalindex, diskscaleradius, coldgas, metalscoldgas, "
         "stellarmass, snapnum FROM " + tbl + " WHERE sfr > 1 OFFSET :o",
         soci::into( tree_ids ), soci::into( gids ),
         soci::into( disk_radius ), soci::into( cold_gas_mass ), soci::into( cold_gas_metal ),
         soci::into( stellar_mass ), soci::into( snapshot ),
         soci::use( obj_idx );

      // Process each galaxy.
      for( unsigned ii = 0; ii < gids.size(); ++ii )
      {
         // Load the SFH.
         tao::sfh<tao::real_type> sfh;
         tao::age_line<tao::real_type> snap_ages( be.session(), *sim );
         sfh.set_snapshot_ages( &snap_ages );
         sfh.set_bin_ages( &ssp.bin_ages() );
         sfh.load_tree_data( be.session( tbl ), tbl, tree_ids[ii], gids[ii] );

         // Rebin.
         hpc::vector<tao::real_type> age_masses( ssp.bin_ages().size() );
         hpc::vector<tao::real_type> age_bulge_masses( ssp.bin_ages().size() );
         hpc::vector<tao::real_type> age_metals( ssp.bin_ages().size() );
         std::fill( age_masses.begin(), age_masses.end(), 0 );
         std::fill( age_bulge_masses.begin(), age_bulge_masses.end(), 0 );
         std::fill( age_metals.begin(), age_metals.end(), 0 );
         sfh.rebin<tao::real_type>( age_masses, age_bulge_masses, age_metals );

         // Sum.
         hpc::vector<tao::real_type> total_spectra( ssp.wavelengths().size() );
         hpc::vector<tao::real_type> bulge_spectra( ssp.wavelengths().size() );
         ssp.sum( age_masses.begin(), age_metals.begin(), total_spectra.begin() );
         ssp.sum( age_bulge_masses.begin(), age_metals.begin(), bulge_spectra.begin() );

         // Calculate transmission for the slab dust model.
         std::vector<tao::real_type> waves( ssp.wavelengths().begin(), ssp.wavelengths().end() );
         tao::dust::slab slab( "data/dust/nebform.dat", waves );
         hpc::vector<tao::real_type> fesc( ssp.wavelengths().size() );
         slab.calc_transmission(
            sim->h(),
            sim->redshifts()[snapshot[ii]],
            cold_gas_mass[ii],
            cold_gas_metal[ii],
            disk_radius[ii],
            fesc.begin(),
            fesc.end()
            );

         // // Print scatter plot data.
         // std::cout << stellar_mass[ii] << ", " << fesc[lambda_1500] << "\n";

         // Rebin histogram.
         unsigned idx = fesc[lambda_1500]/bin_width;
         if( idx == histo.size() )
            --idx;
         ++histo[idx];
      }
   }

   // Print histogram data.
   for( auto v : histo )
      std::cout << v << "\n";
}
