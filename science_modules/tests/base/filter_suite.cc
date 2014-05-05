#include <string>
#include <vector>
#include <algorithm>
#include <libhpc/unit_test/main.hh>
#include "tao/base/filter.hh"

using tao::real_type;
using tao::batch;
using tao::filter;

void
make_batch( batch<real_type>& bat )
{
   bat.set_max_size( 10 );
   auto test1 = bat.set_scalar<real_type>( "test1" );
   auto test2 = bat.set_scalar<real_type>( "test2" );
   std::iota( test1.begin(), test1.end(), 0 );
   std::iota( test2.begin(), test2.end(), 100 );
   bat.set_size( 10 );
}

TEST_CASE( "/tao/base/filter/default_constructor" )
{
   filter filt;
   TEST( filt.field_name() == std::string() );
   TEST( filt.minimum<int>() == boost::none );
   TEST( filt.maximum<int>() == boost::none );
}

TEST_CASE( "/tao/base/filter/iterate" )
{
   // Construct a batch object.
   batch<real_type> bat;
   make_batch( bat );

   // Setup the filter.
   filter filt;
   filt.set_field( "test1", "3.5", "6.5" );
   filt.set_type( tao::batch<tao::real_type>::DOUBLE );

   // Check iteration values.
   {
      std::vector<unsigned> vals;
      std::copy( filt.begin( bat ), filt.end( bat ), std::back_insert_iterator<std::vector<unsigned>>( vals ) );
      TEST( vals.size() == 3 );
      TEST( vals[0] == 4 );
      TEST( vals[1] == 5 );
      TEST( vals[2] == 6 );
   }
}

TEST_CASE( "/tao/base/filter/iterate/no_maximum" )
{
   // Construct a batch object.
   batch<real_type> bat;
   make_batch( bat );

   // Setup the filter.
   filter filt;
   filt.set_field( "test1", "7.5", "" );
   filt.set_type( tao::batch<tao::real_type>::DOUBLE );
   TEST( (bool)filt.minimum<double>() == true );
   TEST( (bool)filt.maximum<double>() == false );
   DELTA( *filt.minimum<double>(), 7.5, 1e-6 );

   // Check iteration values.
   {
      std::vector<unsigned> vals;
      std::copy( filt.begin( bat ), filt.end( bat ), std::back_insert_iterator<std::vector<unsigned>>( vals ) );
      TEST( vals.size() == 2 );
      TEST( vals[0] == 8 );
      TEST( vals[1] == 9 );
   }
}

TEST_CASE( "/tao/base/filter/iterate/no_minimum" )
{
   // Construct a batch object.
   batch<real_type> bat;
   make_batch( bat );

   // Setup the filter.
   filter filt;
   filt.set_field( "test1", "", "3.5" );
   filt.set_type( tao::batch<tao::real_type>::DOUBLE );
   TEST( (bool)filt.minimum<double>() == false );
   TEST( (bool)filt.maximum<double>() == true );
   DELTA( *filt.maximum<double>(), 3.5, 1e-6 );

   // Check iteration values.
   {
      std::vector<unsigned> vals;
      std::copy( filt.begin( bat ), filt.end( bat ), std::back_insert_iterator<std::vector<unsigned>>( vals ) );
      TEST( vals.size() == 4 );
      TEST( vals[0] == 0 );
      TEST( vals[1] == 1 );
      TEST( vals[2] == 2 );
      TEST( vals[3] == 3 );
   }
}
