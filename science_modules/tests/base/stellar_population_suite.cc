#include <boost/range/algorithm_ext/iota.hpp>
#include <libhpc/unit_test/main.hh>
#include <libhpc/system/tmpfile.hh>
#include "tao/base/stellar_population.hh"

SUITE_PREFIX( "/tao/base/stellar_population/" );

hpc::tmpfile
write_ages_file()
{
   hpc::tmpfile tf;
   std::ofstream of( tf.filename().native() );
   std::vector<tao::real_type> ages( 3 );
   boost::iota( ages, 0.0 );
   of << ages.size() << "\n";
   for( tao::real_type x : ages )
      of << x << "\n";
   return tf;
}

hpc::tmpfile
write_waves_file()
{
   hpc::tmpfile tf;
   std::ofstream of( tf.filename().native() );
   std::vector<tao::real_type> waves( 3 );
   boost::iota( waves, 10.0 );
   for( tao::real_type x : waves )
      of << x << "\n";
   return tf;
}

hpc::tmpfile
write_metals_file( bool dual = false )
{
   hpc::tmpfile tf;
   std::ofstream of( tf.filename().native() );
   std::vector<tao::real_type> mets( 3 );
   boost::iota( mets, 1.0 );
   if( dual )
   {
      std::vector<tao::real_type> dual( 2 );
      hpc::algorithm::dual( mets.begin(), mets.end(), dual.begin() );
      hpc::assign( mets, dual );
      of << "dual\n";
   }
   of << mets.size() << "\n";
   for( tao::real_type x : mets )
      of << x << "\n";
   return tf;
}

hpc::tmpfile
write_ssp_file()
{
   hpc::tmpfile tf;
   std::ofstream of( tf.filename().native() );
   for( unsigned agei = 0; agei < 3; ++agei )
   {
      for( unsigned wavei = 0; wavei < 3; ++wavei )
      {
         for( unsigned meti = 0; meti < 3; ++meti )
         {
            of << (agei*100 + wavei*10 + meti);
            if( meti == 2 )
               of << "\n";
            else
               of << " ";
         }
      }
   }
   return tf;
}

TEST_CASE( "set_metallicities" )
{
   std::vector<tao::real_type> mets( 3 );
   boost::iota( mets, 1.0 );
   tao::stellar_population ssp;
   ssp.set_metallicities( mets );
   TEST( ssp.metal_bins().size() == 2 );
   TEST( ssp.metal_bins()[0] == 1.5 );
   TEST( ssp.metal_bins()[1] == 2.5 );
}

TEST_CASE( "set_metallicities/one_value" )
{
   std::vector<tao::real_type> mets( 1 );
   boost::iota( mets, 1.0 );
   tao::stellar_population ssp;
   ssp.set_metallicities( mets );
   TEST( ssp.metal_bins().size() == 0 );
}

TEST_CASE( "set_metallicities/empty" )
{
   std::vector<tao::real_type> mets;
   tao::stellar_population ssp;
   ssp.set_metallicities( mets );
   TEST( ssp.metal_bins().size() == 0 );
}

TEST_CASE( "n_metal_bins" )
{
   std::vector<tao::real_type> mets( 3 );
   boost::iota( mets, 1.0 );
   tao::stellar_population ssp;
   ssp.set_metallicities( mets );
   TEST( ssp.n_metal_bins() == 3 );
}

TEST_CASE( "load_metals" )
{
   hpc::tmpfile tf = write_metals_file();
   tao::stellar_population ssp;
   ssp._load_metals( tf.filename() );
   TEST( ssp.n_metal_bins() == 3 );
   TEST( ssp.metal_bins()[0] == 1.5 );
   TEST( ssp.metal_bins()[1] == 2.5 );
}

TEST_CASE( "load_metals/dual" )
{
   hpc::tmpfile tf = write_metals_file( true );
   tao::stellar_population ssp;
   ssp._load_metals( tf.filename() );
   TEST( ssp.n_metal_bins() == 3 );
   TEST( ssp.metal_bins()[0] == 1.5 );
   TEST( ssp.metal_bins()[1] == 2.5 );
}

TEST_CASE( "find_metal_bin" )
{
   std::vector<tao::real_type> mets( 3 );
   boost::iota( mets, 1.0 );
   tao::stellar_population ssp;
   ssp.set_metallicities( mets );
   TEST( ssp.find_metal_bin( -0.1 ) == 0 );
   TEST( ssp.find_metal_bin( 0.1 ) == 0 );
   TEST( ssp.find_metal_bin( 1.499 ) == 0 );
   TEST( ssp.find_metal_bin( 1.501 ) == 1 );
   TEST( ssp.find_metal_bin( 2.499 ) == 1 );
   TEST( ssp.find_metal_bin( 2.501 ) == 2 );
   TEST( ssp.find_metal_bin( 3.0 ) == 2 );
}

TEST_CASE( "sum_thibault/erases_values" )
{
   hpc::tmpfile ages_tf = write_ages_file();
   hpc::tmpfile waves_tf = write_waves_file();
   hpc::tmpfile met_tf = write_metals_file();
   hpc::tmpfile ssp_tf = write_ssp_file();
   tao::stellar_population ssp;
   ssp.load( ages_tf.filename(), waves_tf.filename(), met_tf.filename(),
             ssp_tf.filename() );
   std::vector<tao::real_type> age_masses( ssp.age_masses_size() );
   std::vector<tao::real_type> spectra( ssp.wavelengths().size() );
   std::fill( age_masses.begin(), age_masses.end(), 0.0 );
   std::fill( spectra.begin(), spectra.end(), 1.0 );
   ssp.sum( age_masses.begin(), spectra.begin() );
   for( auto x : spectra )
      TEST( x == 0.0 );
}

TEST_CASE( "sum_thibault" )
{
   hpc::tmpfile ages_tf = write_ages_file();
   hpc::tmpfile waves_tf = write_waves_file();
   hpc::tmpfile met_tf = write_metals_file();
   hpc::tmpfile ssp_tf = write_ssp_file();
   tao::stellar_population ssp;
   ssp.load( ages_tf.filename(), waves_tf.filename(), met_tf.filename(),
             ssp_tf.filename() );
   std::vector<tao::real_type> age_masses( ssp.age_masses_size() );
   std::vector<tao::real_type> spectra( ssp.wavelengths().size() );
   boost::iota( age_masses, 1.0 );
   std::fill( spectra.begin(), spectra.end(), 1.0 );
   ssp.sum( age_masses.begin(), spectra.begin() );
   TEST( spectra[0] == 6351 );
   TEST( spectra[1] == 6801 );
   TEST( spectra[2] == 7251 );
}
