#include <libhpc/unit_test/main.hh>
#include "tao/base/sfh.hh"
#include "../fixtures/db_fixture.hh"

SUITE_PREFIX( "/tao/base/sfh/" );
SUITE_FIXTURE( db_fixture ) db;

TEST_CASE( "constructor/default" )
{
   tao::sfh sfh;
   TEST( sfh.snapshot_ages() == (void*)0 );
   TEST( sfh.closest_snapshot() == std::numeric_limits<int>::max() );
   TEST( sfh.tree_id() == std::numeric_limits<unsigned long long>::max() );
   TEST( sfh.root_galaxy_id() == std::numeric_limits<unsigned long long>::max() );
   TEST( sfh.root_galaxy_index() == std::numeric_limits<unsigned>::max() );
}

TEST_CASE( "clear_tree_data" )
{
   tao::sfh sfh;
   sfh.load_tree_data( db->sql, "tree_1", 1, 101 );
   TEST( sfh.descendants().empty() == false );
   TEST( sfh.snapshots().empty() == false );
   TEST( sfh.local_galaxy_ids().empty() == false );
   TEST( sfh.disk_sfrs().empty() == false );
   TEST( sfh.bulge_sfrs().empty() == false );
   TEST( sfh.masses().empty() == false );
   sfh.clear_tree_data();
   TEST( sfh.descendants().empty() == true );
   TEST( sfh.snapshots().empty() == true );
   TEST( sfh.local_galaxy_ids().empty() == true );
   TEST( sfh.disk_sfrs().empty() == true );
   TEST( sfh.bulge_sfrs().empty() == true );
   TEST( sfh.masses().empty() == true );
}

TEST_CASE( "load_tree_data" )
{
   tao::sfh sfh;
   sfh.load_tree_data( db->sql, "tree_1", 1, 100 );

   // Check descendants.
   TEST( sfh.descendants().size() == 7 );
   TEST( sfh.descendants()[0] == -1 );
   TEST( sfh.descendants()[1] == 0 );
   TEST( sfh.descendants()[2] == 1 );
   TEST( sfh.descendants()[3] == 1 );
   TEST( sfh.descendants()[4] == 2 );
   TEST( sfh.descendants()[5] == 3 );
   TEST( sfh.descendants()[6] == 3 );

   // Check snapshots.
   TEST( sfh.snapshots().size() == 7 );
   TEST( sfh.snapshots()[0] == 4 );
   TEST( sfh.snapshots()[1] == 3 );
   TEST( sfh.snapshots()[2] == 2 );
   TEST( sfh.snapshots()[3] == 2 );
   TEST( sfh.snapshots()[4] == 1 );
   TEST( sfh.snapshots()[5] == 1 );
   TEST( sfh.snapshots()[6] == 1 );

   // Check disk SFRs.
   TEST( sfh.disk_sfrs().size() == 7 );
   TEST( sfh.disk_sfrs()[0] == 0.1 );
   TEST( sfh.disk_sfrs()[1] == 0.2 );
   TEST( sfh.disk_sfrs()[2] == 0.3 );
   TEST( sfh.disk_sfrs()[3] == 0.4 );
   TEST( sfh.disk_sfrs()[4] == 0.5 );
   TEST( sfh.disk_sfrs()[5] == 0.6 );
   TEST( sfh.disk_sfrs()[6] == 0.7 );

   // Check bulge SFRs.
   TEST( sfh.bulge_sfrs().size() == 7 );
   TEST( sfh.bulge_sfrs()[0] == 0.8 );
   TEST( sfh.bulge_sfrs()[1] == 0.9 );
   TEST( sfh.bulge_sfrs()[2] == 1.0 );
   TEST( sfh.bulge_sfrs()[3] == 1.1 );
   TEST( sfh.bulge_sfrs()[4] == 1.2 );
   TEST( sfh.bulge_sfrs()[5] == 1.3 );
   TEST( sfh.bulge_sfrs()[6] == 1.4 );

   // Check disk SFR Zs.
   TEST( sfh.disk_metallicities().size() == 7 );
   TEST( sfh.disk_metallicities()[0] == 1.1 );
   TEST( sfh.disk_metallicities()[1] == 1.2 );
   TEST( sfh.disk_metallicities()[2] == 1.3 );
   TEST( sfh.disk_metallicities()[3] == 1.4 );
   TEST( sfh.disk_metallicities()[4] == 1.5 );
   TEST( sfh.disk_metallicities()[5] == 1.6 );
   TEST( sfh.disk_metallicities()[6] == 1.7 );

   // Check bulge SFR Zs.
   TEST( sfh.bulge_metallicities().size() == 7 );
   TEST( sfh.bulge_metallicities()[0] == 1.8 );
   TEST( sfh.bulge_metallicities()[1] == 1.9 );
   TEST( sfh.bulge_metallicities()[2] == 2.0 );
   TEST( sfh.bulge_metallicities()[3] == 2.1 );
   TEST( sfh.bulge_metallicities()[4] == 2.2 );
   TEST( sfh.bulge_metallicities()[5] == 2.3 );
   TEST( sfh.bulge_metallicities()[6] == 2.4 );

   // Check masses.
   TEST( sfh.masses().size() == 7 );
   TEST( sfh.masses()[0] == 4.1 );
   TEST( sfh.masses()[1] == 4.2 );
   TEST( sfh.masses()[2] == 4.3 );
   TEST( sfh.masses()[3] == 4.4 );
   TEST( sfh.masses()[4] == 4.5 );
   TEST( sfh.masses()[5] == 4.6 );
   TEST( sfh.masses()[6] == 4.7 );

   // Check table cache.
   TEST( sfh.tree_id() == 1 );
   TEST( sfh.root_galaxy_id() == 100 );
   TEST( sfh.root_galaxy_index() == 0 );
}

///
/// Check that _root is set correctly. I noticed
/// that subtrees can generate bad root values.
///
TEST_CASE( "load_tree_data/subtree" )
{
   tao::sfh sfh;
   sfh.load_tree_data( db->sql, "tree_1", 1, 103 );

   // Check descendants.
   TEST( sfh.descendants().size() == 3 );
   TEST( sfh.descendants()[0] == -1 );
   TEST( sfh.descendants()[1] == 0 );
   TEST( sfh.descendants()[2] == 0 );

   // Check snapshots.
   TEST( sfh.snapshots().size() == 3 );
   TEST( sfh.snapshots()[0] == 2 );
   TEST( sfh.snapshots()[1] == 1 );
   TEST( sfh.snapshots()[2] == 1 );

   // Check table cache.
   TEST( sfh.tree_id() == 1 );
   TEST( sfh.root_galaxy_id() == 103 );
   TEST( sfh.root_galaxy_index() == 0 );
}

TEST_CASE( "load_tree_data/invalid_gid" )
{
   tao::sfh sfh;
   THROWS_ANY( sfh.load_tree_data( db->sql, "tree_1", 1, 300 ) );
}

TEST_CASE( "load_tree_data/depth_first_order" )
{
   // TODO
}

TEST_CASE( "rebin/1-1" )
{
   tao::age_line<tao::real_type> snap_ages;
   {
      std::vector<tao::real_type> ages( 4 );
      ages[0] = 0.0;
      ages[1] = 3.0;
      ages[2] = 10.0;
      ages[3] = 21.0;
      snap_ages.set_ages( ages );
   }

   tao::stellar_population ssp;
   {
      std::vector<tao::real_type> mets( 3 );
      mets[0] = 0.1;
      mets[1] = 0.5;
      mets[2] = 0.9;
      ssp.set_metallicities( mets );

      std::vector<tao::real_type> ages( 4 );
      ages[0] = 0.0;
      ages[1] = 11.0;
      ages[2] = 18.0;
      ages[3] = 21.0;
      ssp.set_ages( ages );

      std::vector<tao::real_type> waves( 5 );
      std::iota( waves.begin(), waves.end(), 1.0 );
      ssp.set_wavelengths( waves );

      std::vector<tao::real_type> spec( 3*5 );
      std::fill( spec.begin(), spec.end(), 1.0 );
      ssp.set_spectra( spec );
   }

   std::vector<tao::real_type> disk_age_masses( ssp.age_masses_size() );
   std::vector<tao::real_type> bulge_age_masses( ssp.age_masses_size() );
   tao::sfh sfh;
   sfh.set_snapshot_ages( &snap_ages );

   sfh.load_tree_data( db->sql, "tree_5", 5, 500 );
   sfh.rebin<std::vector<tao::real_type>>( disk_age_masses, bulge_age_masses, ssp );

   TEST( disk_age_masses[0] == 5.5e9 );
   TEST( disk_age_masses[1] == 0 );
   TEST( disk_age_masses[2] == 0 );
   TEST( disk_age_masses[3] == 1.25e10 );
   TEST( disk_age_masses[4] == 0 );
   TEST( disk_age_masses[5] == 0 );
   TEST( disk_age_masses[6] == 1.15e10 );
   TEST( disk_age_masses[7] == 0 );
   TEST( disk_age_masses[8] == 0 );
   TEST( disk_age_masses[9] == 4.5e9 );
   TEST( disk_age_masses[10] == 0 );
   TEST( disk_age_masses[11] == 0 );

   TEST( bulge_age_masses[0] == 5.5e10 );
   TEST( bulge_age_masses[1] == 0 );
   TEST( bulge_age_masses[2] == 0 );
   TEST( bulge_age_masses[3] == 1.25e11 );
   TEST( bulge_age_masses[4] == 0 );
   TEST( bulge_age_masses[5] == 0 );
   TEST( bulge_age_masses[6] == 1.15e11 );
   TEST( bulge_age_masses[7] == 0 );
   TEST( bulge_age_masses[8] == 0 );
   TEST( bulge_age_masses[9] == 4.5e10 );
   TEST( bulge_age_masses[10] == 0 );
   TEST( bulge_age_masses[11] == 0 );
}

TEST_CASE( "rebin/1-many" )
{
   tao::age_line<tao::real_type> snap_ages;
   {
      std::vector<tao::real_type> ages( 4 );
      ages[0] = 0.0;
      ages[1] = 3.0;
      ages[2] = 10.0;
      ages[3] = 21.0;
      snap_ages.set_ages( ages );
   }

   tao::stellar_population ssp;
   {
      std::vector<tao::real_type> mets( 3 );
      mets[0] = 0.1;
      mets[1] = 0.5;
      mets[2] = 0.9;
      ssp.set_metallicities( mets );

      std::vector<tao::real_type> ages( 7 );
      ages[0] = 0.0;
      ages[1] = 5.5;
      ages[2] = 11.0;
      ages[3] = 14.5;
      ages[4] = 18.0;
      ages[5] = 19.5;
      ages[6] = 21.0;
      ssp.set_ages( ages );

      std::vector<tao::real_type> waves( 5 );
      std::iota( waves.begin(), waves.end(), 1.0 );
      ssp.set_wavelengths( waves );

      std::vector<tao::real_type> spec( 3*5 );
      std::fill( spec.begin(), spec.end(), 1.0 );
      ssp.set_spectra( spec );
   }

   std::vector<tao::real_type> disk_age_masses( ssp.age_masses_size() );
   std::vector<tao::real_type> bulge_age_masses( ssp.age_masses_size() );
   tao::sfh sfh;
   sfh.set_snapshot_ages( &snap_ages );

   sfh.load_tree_data( db->sql, "tree_5", 5, 500 );
   sfh.rebin<std::vector<tao::real_type>>( disk_age_masses, bulge_age_masses, ssp );

   TEST( disk_age_masses[0] == 2.75e9 );
   TEST( disk_age_masses[1] == 0 );
   TEST( disk_age_masses[2] == 0 );
   TEST( disk_age_masses[3] == 5.5e9 );
   TEST( disk_age_masses[4] == 0 );
   TEST( disk_age_masses[5] == 0 );
   TEST( disk_age_masses[6] == 6.25e9 );
   TEST( disk_age_masses[7] == 0 );
   TEST( disk_age_masses[8] == 0 );
   TEST( disk_age_masses[9] == 7.0e9 );
   TEST( disk_age_masses[10] == 0 );
   TEST( disk_age_masses[11] == 0 );
   TEST( disk_age_masses[12] == 5.75e9 );
   TEST( disk_age_masses[13] == 0 );
   TEST( disk_age_masses[14] == 0 );
   TEST( disk_age_masses[15] == 4.5e9 );
   TEST( disk_age_masses[16] == 0 );
   TEST( disk_age_masses[17] == 0 );
   TEST( disk_age_masses[18] == 2.25e9 );
   TEST( disk_age_masses[19] == 0 );
   TEST( disk_age_masses[20] == 0 );

   TEST( bulge_age_masses[0] == 2.75e10 );
   TEST( bulge_age_masses[1] == 0 );
   TEST( bulge_age_masses[2] == 0 );
   TEST( bulge_age_masses[3] == 5.5e10 );
   TEST( bulge_age_masses[4] == 0 );
   TEST( bulge_age_masses[5] == 0 );
   TEST( bulge_age_masses[6] == 6.25e10 );
   TEST( bulge_age_masses[7] == 0 );
   TEST( bulge_age_masses[8] == 0 );
   TEST( bulge_age_masses[9] == 7.0e10 );
   TEST( bulge_age_masses[10] == 0 );
   TEST( bulge_age_masses[11] == 0 );
   TEST( bulge_age_masses[12] == 5.75e10 );
   TEST( bulge_age_masses[13] == 0 );
   TEST( bulge_age_masses[14] == 0 );
   TEST( bulge_age_masses[15] == 4.5e10 );
   TEST( bulge_age_masses[16] == 0 );
   TEST( bulge_age_masses[17] == 0 );
   TEST( bulge_age_masses[18] == 2.25e10 );
   TEST( bulge_age_masses[19] == 0 );
   TEST( bulge_age_masses[20] == 0 );
}

TEST_CASE( "rebin/many-1" )
{
   tao::age_line<tao::real_type> snap_ages;
   {
      std::vector<tao::real_type> ages( 4 );
      ages[0] = 0.0;
      ages[1] = 3.0;
      ages[2] = 10.0;
      ages[3] = 21.0;
      snap_ages.set_ages( ages );
   }

   tao::stellar_population ssp;
   {
      std::vector<tao::real_type> mets( 3 );
      mets[0] = 0.1;
      mets[1] = 0.5;
      mets[2] = 0.9;
      ssp.set_metallicities( mets );

      std::vector<tao::real_type> ages( 2 );
      ages[0] = 0.0;
      ages[1] = 10.0;
      ssp.set_ages( ages );

      std::vector<tao::real_type> waves( 5 );
      std::iota( waves.begin(), waves.end(), 1.0 );
      ssp.set_wavelengths( waves );

      std::vector<tao::real_type> spec( 3*5 );
      std::fill( spec.begin(), spec.end(), 1.0 );
      ssp.set_spectra( spec );
   }

   std::vector<tao::real_type> disk_age_masses( ssp.age_masses_size() );
   std::vector<tao::real_type> bulge_age_masses( ssp.age_masses_size() );
   tao::sfh sfh;
   sfh.set_snapshot_ages( &snap_ages );

   sfh.load_tree_data( db->sql, "tree_5", 5, 500 );
   sfh.rebin<std::vector<tao::real_type>>( disk_age_masses, bulge_age_masses, ssp );

   TEST( disk_age_masses[0] == 5e9 );
   TEST( disk_age_masses[1] == 0 );
   TEST( disk_age_masses[2] == 0 );
   TEST( disk_age_masses[3] == 2.9e10 );
   TEST( disk_age_masses[4] == 0 );
   TEST( disk_age_masses[5] == 0 );

   TEST( bulge_age_masses[0] == 5e10 );
   TEST( bulge_age_masses[1] == 0 );
   TEST( bulge_age_masses[2] == 0 );
   TEST( bulge_age_masses[3] == 2.9e11 );
   TEST( bulge_age_masses[4] == 0 );
   TEST( bulge_age_masses[5] == 0 );
}

TEST_CASE( "rebin/mergers/minor" )
{
   tao::age_line<tao::real_type> snap_ages;
   {
      std::vector<tao::real_type> ages( 4 );
      ages[0] = 0.0;
      ages[1] = 3.0;
      ages[2] = 10.0;
      ages[3] = 21.0;
      snap_ages.set_ages( ages );
   }

   tao::stellar_population ssp;
   {
      std::vector<tao::real_type> mets( 3 );
      mets[0] = 0.1;
      mets[1] = 0.5;
      mets[2] = 0.9;
      ssp.set_metallicities( mets );

      std::vector<tao::real_type> ages( 2 );
      ages[0] = 0.0;
      ages[1] = 10.0;
      ssp.set_ages( ages );

      std::vector<tao::real_type> waves( 5 );
      std::iota( waves.begin(), waves.end(), 1.0 );
      ssp.set_wavelengths( waves );

      std::vector<tao::real_type> spec( 3*5 );
      std::fill( spec.begin(), spec.end(), 1.0 );
      ssp.set_spectra( spec );
   }

   std::vector<tao::real_type> disk_age_masses( ssp.age_masses_size() );
   std::vector<tao::real_type> bulge_age_masses( ssp.age_masses_size() );
   tao::sfh sfh;
   sfh.set_snapshot_ages( &snap_ages );

   sfh.load_tree_data( db->sql, "tree_5", 7, 508 );
   sfh.rebin<std::vector<tao::real_type>>( disk_age_masses, bulge_age_masses, ssp );

   TEST( disk_age_masses[0] == 5e9 );
   TEST( disk_age_masses[1] == 0 );
   TEST( disk_age_masses[2] == 0 );
   TEST( disk_age_masses[3] > 2.9e10 );
   TEST( disk_age_masses[4] == 0 );
   TEST( disk_age_masses[5] == 0 );

   TEST( bulge_age_masses[0] == 5e10 );
   TEST( bulge_age_masses[1] == 0 );
   TEST( bulge_age_masses[2] == 0 );
   TEST( bulge_age_masses[3] > 2.9e11 );
   TEST( bulge_age_masses[4] == 0 );
   TEST( bulge_age_masses[5] == 0 );
}

TEST_CASE( "rebin/mergers/major" )
{
   tao::age_line<tao::real_type> snap_ages;
   {
      std::vector<tao::real_type> ages( 4 );
      ages[0] = 0.0;
      ages[1] = 3.0;
      ages[2] = 10.0;
      ages[3] = 21.0;
      snap_ages.set_ages( ages );
   }

   tao::stellar_population ssp;
   {
      std::vector<tao::real_type> mets( 3 );
      mets[0] = 0.1;
      mets[1] = 0.5;
      mets[2] = 0.9;
      ssp.set_metallicities( mets );

      std::vector<tao::real_type> ages( 2 );
      ages[0] = 0.0;
      ages[1] = 10.0;
      ssp.set_ages( ages );

      std::vector<tao::real_type> waves( 5 );
      std::iota( waves.begin(), waves.end(), 1.0 );
      ssp.set_wavelengths( waves );

      std::vector<tao::real_type> spec( 3*5 );
      std::fill( spec.begin(), spec.end(), 1.0 );
      ssp.set_spectra( spec );
   }

   std::vector<tao::real_type> disk_age_masses( ssp.age_masses_size() );
   std::vector<tao::real_type> bulge_age_masses( ssp.age_masses_size() );
   tao::sfh sfh;
   sfh.set_snapshot_ages( &snap_ages );

   sfh.load_tree_data( db->sql, "tree_5", 8, 513 );
   sfh.rebin<std::vector<tao::real_type>>( disk_age_masses, bulge_age_masses, ssp );

   TEST( disk_age_masses[0] == 5e9 );
   TEST( disk_age_masses[1] == 0 );
   TEST( disk_age_masses[2] == 0 );
   TEST( disk_age_masses[3] == 2.9e10 );
   TEST( disk_age_masses[4] == 0 );
   TEST( disk_age_masses[5] == 0 );

   TEST( bulge_age_masses[0] == 5e10 );
   TEST( bulge_age_masses[1] == 0 );
   TEST( bulge_age_masses[2] == 0 );
   TEST( bulge_age_masses[3] > 2.9e11 );
   TEST( bulge_age_masses[4] == 0 );
   TEST( bulge_age_masses[5] == 0 );
}

TEST_CASE( "rebin/mergers/ics" )
{
   tao::age_line<tao::real_type> snap_ages;
   {
      std::vector<tao::real_type> ages( 4 );
      ages[0] = 0.0;
      ages[1] = 3.0;
      ages[2] = 10.0;
      ages[3] = 21.0;
      snap_ages.set_ages( ages );
   }

   tao::stellar_population ssp;
   {
      std::vector<tao::real_type> mets( 3 );
      mets[0] = 0.1;
      mets[1] = 0.5;
      mets[2] = 0.9;
      ssp.set_metallicities( mets );

      std::vector<tao::real_type> ages( 2 );
      ages[0] = 0.0;
      ages[1] = 10.0;
      ssp.set_ages( ages );

      std::vector<tao::real_type> waves( 5 );
      std::iota( waves.begin(), waves.end(), 1.0 );
      ssp.set_wavelengths( waves );

      std::vector<tao::real_type> spec( 3*5 );
      std::fill( spec.begin(), spec.end(), 1.0 );
      ssp.set_spectra( spec );
   }

   std::vector<tao::real_type> disk_age_masses( ssp.age_masses_size() );
   std::vector<tao::real_type> bulge_age_masses( ssp.age_masses_size() );
   tao::sfh sfh;
   sfh.set_snapshot_ages( &snap_ages );

   sfh.load_tree_data( db->sql, "tree_5", 6, 503 );
   sfh.rebin<std::vector<tao::real_type>>( disk_age_masses, bulge_age_masses, ssp );

   TEST( disk_age_masses[0] == 5e9 );
   TEST( disk_age_masses[1] == 0 );
   TEST( disk_age_masses[2] == 0 );
   TEST( disk_age_masses[3] == 2.9e10 );
   TEST( disk_age_masses[4] == 0 );
   TEST( disk_age_masses[5] == 0 );

   TEST( bulge_age_masses[0] == 5e10 );
   TEST( bulge_age_masses[1] == 0 );
   TEST( bulge_age_masses[2] == 0 );
   TEST( bulge_age_masses[3] == 2.9e11 );
   TEST( bulge_age_masses[4] == 0 );
   TEST( bulge_age_masses[5] == 0 );
}

TEST_CASE( "rebin/metallicity" )
{
   tao::age_line<tao::real_type> snap_ages;
   {
      std::vector<tao::real_type> ages( 4 );
      ages[0] = 0.0;
      ages[1] = 3.0;
      ages[2] = 10.0;
      ages[3] = 21.0;
      snap_ages.set_ages( ages );
   }

   tao::stellar_population ssp;
   {
      std::vector<tao::real_type> mets( 3 );
      mets[0] = 0.1;
      mets[1] = 0.5;
      mets[2] = 0.9;
      ssp.set_metallicities( mets );

      std::vector<tao::real_type> ages( 2 );
      ages[0] = 0.0;
      ages[1] = 10.0;
      ssp.set_ages( ages );

      std::vector<tao::real_type> waves( 5 );
      std::iota( waves.begin(), waves.end(), 1.0 );
      ssp.set_wavelengths( waves );

      std::vector<tao::real_type> spec( 3*5 );
      std::fill( spec.begin(), spec.end(), 1.0 );
      ssp.set_spectra( spec );
   }

   std::vector<tao::real_type> disk_age_masses( ssp.age_masses_size() );
   std::vector<tao::real_type> bulge_age_masses( ssp.age_masses_size() );
   tao::sfh sfh;
   sfh.set_snapshot_ages( &snap_ages );

   sfh.load_tree_data( db->sql, "tree_6", 10, 603 );
   sfh.rebin<std::vector<tao::real_type>>( disk_age_masses, bulge_age_masses, ssp );

   TEST( disk_age_masses[0] == 0 );
   TEST( disk_age_masses[1] == 5e9 );
   TEST( disk_age_masses[2] == 0 );
   TEST( disk_age_masses[3] == 0 );
   TEST( disk_age_masses[4] == 2.9e10 );
   TEST( disk_age_masses[5] == 0 );

   TEST( bulge_age_masses[0] == 0 );
   TEST( bulge_age_masses[1] == 5e10 );
   TEST( bulge_age_masses[2] == 0 );
   TEST( bulge_age_masses[3] == 0 );
   TEST( bulge_age_masses[4] == 2.9e11 );
   TEST( bulge_age_masses[5] == 0 );
}
