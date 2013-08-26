#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <cxxtest/GlobalFixture.h>
#include "tao/modules/skymaker.hh"

using namespace hpc;
using namespace tao;

#include "mpi_fixture.hh"

///
/// Skymaker test suite.
///
class skymaker_suite : public CxxTest::TestSuite
{
public:

   typedef skymaker::real_type real_type;

   ///
   /// Test default constructor.
   ///
   void test_default_constructor()
   {
      tao::skymaker sky;
   }

   ///
   /// Test image constructor.
   ///
   void test_image_constructor()
   {
      unsigned sub_cone = 1;
      string format = "FITS", mag_field = "field";
      real_type min_mag = 3, z_min = 4, z_max = 5;
      real_type origin_ra = 6, origin_dec = 7;
      real_type fov_ra = 90, fov_dec = 90;
      unsigned width = 10, height = 11;
      tao::skymaker::image img( 0,
				sub_cone, format, mag_field,
				min_mag, z_min, z_max,
				origin_ra, origin_dec,
				fov_ra, fov_dec,
				width, height );

      // Values are set correctly.
      TS_ASSERT_EQUALS( img._sub_cone, sub_cone );
      TS_ASSERT_EQUALS( img._format, format );
      TS_ASSERT_EQUALS( img._mag_field, mag_field );
      TS_ASSERT_EQUALS( img._min_mag, min_mag );
      TS_ASSERT_EQUALS( img._z_min, z_min );
      TS_ASSERT_EQUALS( img._z_max, z_max );
      TS_ASSERT_EQUALS( img._origin_ra, to_radians( origin_ra ) );
      TS_ASSERT_EQUALS( img._origin_dec, to_radians( origin_dec ) );
      TS_ASSERT_EQUALS( img._fov_ra, to_radians( fov_ra ) );
      TS_ASSERT_EQUALS( img._fov_dec, to_radians( fov_dec ) );
      TS_ASSERT_EQUALS( img._width, width );
      TS_ASSERT_EQUALS( img._height, height );
      TS_ASSERT_EQUALS( img._cnt, 0 );

      // Scale factors are correctly set.
      TS_ASSERT_DELTA( img._scale_x, 0.5*width, 1e-3 );
      TS_ASSERT_DELTA( img._scale_y, 0.5*height, 1e-3 );
   }
};
