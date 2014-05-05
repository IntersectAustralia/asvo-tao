#include <libhpc/unit_test/main.hh>
#include "tao/base/age_line.hh"
#include "../fixtures/db_fixture.hh"

using tao::age_line;
using tao::redshift_to_age;

TEST_CASE( "/base/age_line/default_constructor" )
{
   tao::age_line<double> al;
   TEST( al.size() == 0 );
}

TEST_CASE( "/base/age_line/load_constructor" )
{
   db_fixture db;

   // Construct.
   tao::age_line<double> al( db.be.session() );

   // Ages must be correct.
   TEST( al.size() == 5 );
   DELTA( al[0], redshift_to_age<double>( 127 ), 1e-3 );
   DELTA( al[1], redshift_to_age<double>( 80 ), 1e-3 );
   DELTA( al[2], redshift_to_age<double>( 63 ), 1e-3 );
   DELTA( al[3], redshift_to_age<double>( 20 ), 1e-3 );
   DELTA( al[4], redshift_to_age<double>( 0 ), 1e-3 );

   // Duals must be correct.
   DELTA( al.dual( 0 ), 0.5*(redshift_to_age<double>( 127 ) + redshift_to_age<double>( 80 )), 1e-3 );
   DELTA( al.dual( 1 ), 0.5*(redshift_to_age<double>( 80 ) + redshift_to_age<double>( 63 )), 1e-3 );
   DELTA( al.dual( 2 ), 0.5*(redshift_to_age<double>( 63 ) + redshift_to_age<double>( 20 )), 1e-3 );
   DELTA( al.dual( 3 ), 0.5*(redshift_to_age<double>( 20 ) + redshift_to_age<double>( 0 )), 1e-3 );
}

TEST_CASE( "/base/age_line/bin_location" )
{
   db_fixture db;

   // Construct.
   age_line<double> al( db.be.session() );

   // Test below/at minimum.
   TEST( al.find_bin( redshift_to_age<double>( 0 ) ) == 4 );

   // Test above maximum.
   TEST( al.find_bin( redshift_to_age<double>( 130 ) ) == 0 );

   // Bins.
   TEST( al.find_bin( 0.51*(redshift_to_age<double>( 127 ) + redshift_to_age<double>( 80 )) ) == 1 );
   TEST( al.find_bin( 0.51*(redshift_to_age<double>( 80 ) + redshift_to_age<double>( 63 )) ) == 2 );
   TEST( al.find_bin( 0.51*(redshift_to_age<double>( 63 ) + redshift_to_age<double>( 20 )) ) == 3 );
}
