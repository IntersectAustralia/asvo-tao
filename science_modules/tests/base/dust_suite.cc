#include <fstream>
#include <libhpc/debug/unit_test_main.hh>
#include <libhpc/numerics/generators.hh>
#include <libhpc/system/stream_output.hh>
#include <libhpc/system/tmpfile.hh>
#include "tao/base/dust.hh"

using namespace hpc::test;

namespace {

   test_case<> ANON(
      "/tao/base/dust/calzetti",
      "",
      []()
      {
         std::vector<tao::real_type> spec( 10 ), res( 10 ), waves( 10 );
         hpc::numerics::gaussian( spec.begin(), 10, 1e10 );
         hpc::numerics::linear( waves.begin(), 10, 5000.0, 1000000.0 );
         tao::dust::calzetti( 1.0, spec.begin(), spec.end(), waves.begin(), res.begin() );
         tao::real_type vals[10] = { 2.96264e+09, 5.76439e+09, 7.8004e+09, 9.52412e+09, 1.05241e+10, 1.05309e+10, 9.54464e+09, 7.83624e+09, 5.82813e+09, 3.92677e+09 };
         for( unsigned ii = 0; ii < spec.size(); ++ii )
            DELTA( res[ii], vals[ii], 1e9 );
      }
      );

   test_case<> ANON(
      "/tao/base/dust/slab/constructor/default",
      "",
      []()
      {
         tao::dust::slab dust;
         TEST( dust.extinction().empty() == true );
         TEST( dust.albedo().empty() == true );
         TEST( dust.exponents().empty() == true );
      }
      );

   test_case<> ANON(
      "/tao/base/dust/slab/constructor/load",
      "",
      []()
      {
         hpc::tmpfile tmp;
         {
            std::ofstream file( tmp.filename().native() );
            file << "3\n"
               "1 3 5e-1 -5e-1\n"
               "3 2 3e-1 -3e-1\n"
               "5 1 1e-1 -1e-1\n";
         }
         std::vector<tao::real_type> waves( 5 );
	 hpc::numerics::linear( waves.begin(), 5, 1e4, 5e4 );
         tao::dust::slab dust( tmp.filename(), waves );
         DELTA( dust.extinction()[0], 3.0, 1e-1 );
         DELTA( dust.extinction()[1], 2.5, 1e-1 );
         DELTA( dust.extinction()[2], 2.0, 1e-1 );
         DELTA( dust.extinction()[3], 1.5, 1e-1 );
         DELTA( dust.extinction()[4], 1.0, 1e-1 );
         DELTA( dust.albedo()[0], 5e-1, 1e-2 );
         DELTA( dust.albedo()[1], 4e-1, 1e-2 );
         DELTA( dust.albedo()[2], 3e-1, 1e-2 );
         DELTA( dust.albedo()[3], 2e-1, 1e-2 );
         DELTA( dust.albedo()[4], 1e-1, 1e-2 );
         DELTA( dust.exponents()[0], 1.6 + -5e-1, 1e-2 );
         DELTA( dust.exponents()[1], 1.6 + -4e-1, 1e-2 );
         DELTA( dust.exponents()[2], 1.6 + -3e-1, 1e-2 );
         DELTA( dust.exponents()[3], 1.6 + -2e-1, 1e-2 );
         DELTA( dust.exponents()[4], 1.6 + -1e-1, 1e-2 );
      }
      );

   test_case<> ANON(
      "/tao/base/dust/slab",
      "",
      []()
      {
         tao::dust::slab dust;
         {
            std::vector<tao::real_type> ext( 10 ), alb( 10 ), exp( 10 );
            hpc::numerics::linear( ext.begin(), 10, 9.0, 1e-3 );
            hpc::numerics::linear( alb.begin(), 10, 4e-1, 0.0 );
            hpc::numerics::linear( exp.begin(), 10, -2e-1, 0.0 );
            dust.set_extinction( std::move( ext ), std::move( alb ), std::move( exp ) );
            TEST( ext.empty() == true );
            TEST( alb.empty() == true );
            TEST( exp.empty() == true );
         }
         std::vector<tao::real_type> spec( 10 ), res( 10 ), waves( 10 );
         hpc::numerics::gaussian( spec.begin(), 10, 1e10 );
         hpc::numerics::linear( waves.begin(), 10, 5000.0, 1000000.0 );
         dust( 0.73, 1.0, 1e10, 1e8, 1.0, spec.begin(), spec.end(), waves.begin(), res.begin() );
         tao::real_type vals[10] = { 8060.03, 1.31745e+04, 1.9866e+04, 2.77621e+04, 3.62184e+04, 4.46628e+04, 5.32989e+04, 6.4906e+04, 9.55588e+04, 6.3886e+07 };
         for( unsigned ii = 0; ii < 10; ++ii )
            DELTA( res[ii], vals[ii], pow( 10.0, int(log10( vals[ii] )) ) );

      }
      );

}
