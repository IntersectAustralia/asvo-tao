#include <cstdlib>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>
#include <tao/modules/filter.hh>

using namespace hpc;

void
open_file( const string& filename,
           std::ifstream& file )
{
   file.open( filename );
   if( !file )
   {
      std::cout << "Failed to open '" << filename << "'.\n";
      exit( 1 );
   }
}

int
main( int argc,
      char* argv[] )
{
   // Load the filters.
   tao::filter filt;
   filt._read_wavelengths( "wavelength.sed" );
   filt._load_filter( "b.dat" );
   filt._load_filter( "k.dat" );
   filt._load_filter( "v.dat" );
   filt._process_vega( "vega.sed" );
   unsigned num_waves = filt._waves.size();

   // // Dump some vega stuff.
   // std::cout << "Vega B magnitude = " << filt._vega_mag[0] << "\n";
   // std::cout << "Vega K magnitude = " << filt._vega_mag[1] << "\n";
   // std::cout << "Vega V magnitude = " << filt._vega_mag[2] << "\n";

   // Open the catalogue.
   std::ifstream cat;
   open_file( "catalogue.sed", cat );
   vector<tao::real_type> sed( num_waves );
   unsigned idx = 0;
   while( cat )
   {
      for( unsigned ii = 0; ii < num_waves; ++ii )
      {
         cat >> sed[ii];
      }
      numerics::spline<tao::real_type> spline;
      filt._prepare_spectra( sed, spline );
      std::cout << "Index: " << idx << "\n";
      for( unsigned jj = 0; jj < 3; ++jj )
      {
         tao::real_type Fv = filt._integrate( spline, filt._filters[jj] );
         tao::real_type Rv = filt._filt_int[jj];
         tao::real_type vega = -2.5*log10( Fv/filt._vega_int[jj] );
         tao::real_type ab = -2.5*log10( Fv/Rv ) - 48.6;
         if( jj == 0 )
         {
            std::cout << "  Bvega=" << vega << "\n";
            std::cout << "  Bab  =" << ab << "\n";
         }
         else if( jj == 1 )
         {
            std::cout << "  Kvega=" << vega << "\n";
            std::cout << "  Kab  =" << ab << "\n";
         }
         else
         {
            std::cout << "  Vvega=" << vega << "\n";
            std::cout << "  Vab  =" << ab << "\n";
         }
      }
      ++idx;
   }

   return EXIT_SUCCESS;
}
