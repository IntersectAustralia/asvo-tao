#include <cmath>
#include <boost/algorithm/string/trim.hpp>
#include <boost/tokenizer.hpp>
#include "filter.hh"

// Define the speed of light
// #define M_C 2.99792458e8 // m/s
#define M_C 2.99792458e18 // angstrom/s

using namespace hpc;

namespace tao {

   filter::filter()
   {
   }

   filter::~filter()
   {
   }

   ///
   ///
   ///
   void
   filter::setup_options( options::dictionary& dict,
                          optional<const string&> prefix )
   {
      dict.add_option( new options::string( "waves_filename" ), prefix );
      dict.add_option( new options::string( "filter_filenames" ), prefix );
      dict.add_option( new options::string( "vega_filename" ), prefix );
   }

   ///
   ///
   ///
   void
   filter::setup_options( hpc::options::dictionary& dict,
                          const char* prefix )
   {
      setup_options( dict, string( prefix ) );
   }

   ///
   /// Initialise the module.
   ///
   void
   filter::initialise( const options::dictionary& dict,
                       optional<const string&> prefix )
   {
      LOG_ENTER();

      _read_options( dict, prefix );

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   filter::initialise( const hpc::options::dictionary& dict,
                       const char* prefix )
   {
      initialise( dict, string( prefix ) );
   }

   void
   filter::run()
   {
   }

   void
   filter::process_galaxy( const soci::row& galaxy,
                           vector<real_type>::view spectra )
   {
      // Prepare the spectra.
      numerics::spline<real_type> spectra_spline;
      _prepare_spectra( spectra, spectra_spline );

      // Calculate the distance/area for this galaxy. Use 10000
      // points.
      real_type dist = numerics::redshift_to_distance( 0.02, 10000 )*1e-3;
      real_type area = log10( 4.0*M_PI ) + 2.0*log10( dist*3.08568025e24 );

      // Loop over each filter band.
      for( unsigned ii = 0; ii < _filters.size(); ++ii )
      {
         real_type spec_int = _integrate( spectra_spline, _filters[ii] );
         _mags[ii] = -2.5*(log10( spec_int ) - area - log10( _filt_int[ii] )) - 48.6;
      }
      LOGLN( "Band magnitudes: ", _mags );
   }

   ///
   ///
   ///
   const hpc::vector<filter::real_type>::view
   filter::magnitudes() const
   {
      return _mags;
   }

   filter::real_type
   filter::_apparant_magnitude( real_type spectra,
                                real_type filter,
                                real_type vega,
                                real_type distance )
   {
      real_type area = log10( 4.0*M_PI ) + 2.0*log10( distance*3.08568025e24 );
      real_type spec_filt = -2.5*(log10( spectra ) + 20.0 - area - log10( filter )) - 48.6;
      real_type spec_vega = -2.5*(log10( spectra ) + 20.0 - area - log10( vega ));
      real_type vega_filt = -2.5*(log10( vega ) - log10( filter )) - 48.6;
   }

   void
   filter::_prepare_spectra( const vector<real_type>::view& spectra,
                             numerics::spline<real_type>& spline )
   {
      ASSERT( spectra.size() == _waves.size() );
      fibre<real_type> knots( 2, spectra.size() );
      for( unsigned ii = 0; ii < _waves.size(); ++ii )
      {
         knots(ii,0) = _waves[ii];
         knots(ii,1) = spectra[ii];
      }
      spline.set_knots( knots );
   }

   filter::real_type
   filter::_integrate( const numerics::spline<real_type>& spectra,
                       const numerics::spline<real_type>& filter )
                       
   {
      typedef vector<real_type>::view array_type;
      element<array_type> take_first( 0 );

      range<real_type> fi_rng( filter.knots().front()[0], filter.knots().back()[0] );
      range<real_type> sp_rng( spectra.knots().front()[0], spectra.knots().back()[0] );
      real_type low = std::max( fi_rng.start(), sp_rng.start() );
      real_type upp = std::min( fi_rng.finish(), sp_rng.finish() );

      auto it = make_interp_iterator(
         boost::make_transform_iterator( filter.knots().begin(), take_first ),
         boost::make_transform_iterator( filter.knots().end(), take_first ),
         boost::make_transform_iterator( spectra.knots().begin(), take_first ),
         boost::make_transform_iterator( spectra.knots().end(), take_first ),
         1e-7
         );

      while( !num::approx( *it, low, 1e-7 ) )
         ++it;

      vector<real_type> crds( 4 ), weights( 4 );
      _gauss_quad( crds, weights );

      real_type sum = 0.0;

      while( !num::approx( *it++, upp, 1e-7 ) )
      {
         real_type w = *it - low;
         real_type jac_det = 0.5*(M_C/low - M_C/(*it));
         unsigned fi_poly = it.indices()[0] - 1;
         unsigned sp_poly = it.indices()[1] - 1;
         for( unsigned ii = 0; ii < 4; ++ii )
         {
            real_type x = low + w*0.5*(1.0 + crds[ii]);

            // This integral looks like this because of a change of variable
            // frome wavelength to frequency. Do the math!
            // sum += jac_det*weights[ii]*filter( x, fi_poly )*spectra( x, sp_poly )*x*x*x*x*2.0/(2.9979*M_C);
            sum += jac_det*weights[ii]*filter( x, fi_poly )*spectra( x, sp_poly )*x*x*x*x/(M_C*M_C);
         }
         low = *it;
      }

      return sum;
   }

   filter::real_type
   filter::_integrate( const numerics::spline<real_type>& spectra )
   {
      vector<real_type> crds( 4 ), weights( 4 );
      _gauss_quad( crds, weights );

      real_type sum = 0.0;
      for( unsigned ii = 0; ii < spectra.num_segments(); ++ii )
      {
         real_type low = spectra.segment_start( ii );
         real_type w = spectra.segment_width( ii );
         real_type jac_det = 0.5*w;
         for( unsigned jj = 0; jj < 4; ++jj )
         {
            real_type x = low + w*0.5*(1.0 + crds[jj]);

            // Note that this integral does not require a change of
            // variable, as it is not a convolution.
            sum += jac_det*weights[jj]*spectra( x, ii );
         }
      }

      return sum;
   }

   void
   filter::_gauss_quad( vector<real_type>::view crds,
                        vector<real_type>::view weights )
   {
      real_type v0 = sqrt( (3.0 - 2.0*sqrt( 6.0/5.0 ))/7.0 );
      real_type v1 = sqrt( (3.0 + 2.0*sqrt( 6.0/5.0 ))/7.0 );
      crds[0] = -v1;
      crds[1] = -v0;
      crds[2] = v0;
      crds[3] = v1;
      weights[0] = (18.0 - sqrt( 30.0 ))/36.0;
      weights[1] = (18.0 + sqrt( 30.0 ))/36.0;
      weights[2] = (18.0 + sqrt( 30.0 ))/36.0;
      weights[3] = (18.0 - sqrt( 30.0 ))/36.0;
   }

   void
   filter::_read_options( const options::dictionary& dict,
                          optional<const string&> prefix )
   {
      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      {
         // Get the wavelengths filename.
         string filename = sub.get<string>( "waves_filename" );
         LOGLN( "Using wavelengths filename \"", filename, "\"" );

         // Load the wavelengths.
         _read_wavelengths( filename );
      }

      {
         // Split out the filter filenames.
         list<string> filenames;
         {
            string filters_str = sub.get<string>( "filter_filenames" );
            boost::tokenizer<boost::char_separator<char> > tokens( filters_str, boost::char_separator<char>( "," ) );
            for( const auto& fn : tokens )
               filenames.push_back( boost::trim_copy( fn ) );
         }

         // Allocate room for the filters.
         _filters.reallocate( filenames.size() );
         _filters.resize( 0 );
         _filt_int.reallocate( filenames.size() );
         _filt_int.resize( 0 );
         _mags.reallocate( filenames.size() );

         // Load each filter into memory.
         for( const auto& fn : filenames )
            _load_filter( fn );
      }
      LOGLN( "Filter integrals: ", _filt_int );

      // Get the Vega filename and perform processing.
      _process_vega( sub.get<string>( "vega_filename" ) );
   }

   void
   filter::_read_wavelengths( const string& filename )
   {
      LOG_ENTER();

      // Open the file.
      std::ifstream file( filename );
      ASSERT( file.is_open() );

      // Need to get number of lines in file first.
      unsigned num_waves = 0;
      {
         string line;
         while( !file.eof() )
         {
            std::getline( file, line );
            if( boost::trim_copy( line ).length() )
               ++num_waves;
         }
      }

      // Allocate. Note that the ordering goes time,spectra,metals.
      _waves.reallocate( num_waves );

      // Read in the file in one big go.
      file.clear();
      file.seekg( 0 );
      for( unsigned ii = 0; ii < _waves.size(); ++ii )
         file >> _waves[ii];

      LOG_EXIT();
   }

   void
   filter::_load_filter( const string& filename )
   {
      std::ifstream file( filename, std::ios::in );
      ASSERT( file.is_open() );

      // First entry is number of spectral bands.
      unsigned num_spectra;
      file >> num_spectra;

      // Allocate for this filter.
      unsigned cur_filter = _filters.size();
      _filters.resize( cur_filter + 1 );
      numerics::spline<real_type>& filter = _filters[cur_filter];

      // Read in all the values.
      fibre<real_type> knots( 2, num_spectra );
      for( unsigned ii = 0; ii < num_spectra; ++ii )
      {
         file >> knots(ii,0);
         file >> knots(ii,1);
      }

      // Setup the spline.
      filter.set_knots( knots );

      // Integrate the filter and cache the result.
      _filt_int.resize( _filt_int.size() + 1 );
      _filt_int.back() = _integrate( filter );
   }

   void
   filter::_process_vega( const string& filename )
   {
      std::ifstream file( filename );
      ASSERT( file.is_open() );

      // The Vega file is a spectrum. First column is wavelength and
      // second column is luminosity density.
      unsigned num_waves = 0;
      while( !file.eof() )
      {
         string line;
         std::getline( file, line );
         if( boost::trim_copy( line ).length() )
            ++num_waves;
      }

      // Allocate.
      _vega_int.reallocate( _filters.size() );
      fibre<real_type> knots( 2, num_waves );

      // Reset the file position and go again.
      file.clear();
      file.seekg( 0, std::ios_base::beg );
      for( unsigned ii = 0; ii < num_waves; ++ii )
      {
         file >> knots(ii,0); // angstroms
         file >> knots(ii,1); // 2e17*erg/s/angstrom

         // I first need to multiply by 2e-17 to get to erg/s/angstrom.
         knots(ii,1) *= 2e-17;
      }

      // Convert the spectrum to a spline and convolve with each
      // filter.
      numerics::spline<real_type> spline;
      spline.set_knots( knots );
      for( unsigned ii = 0; ii < _filters.size(); ++ii )
         _vega_int[ii] = _integrate( spline, _filters[ii] );
      LOGLN( "Vega integrals: ", _vega_int );

      // Calculate the Vega magnitudes.
      _vega_mag.reallocate( _filters.size() );
      for( unsigned ii = 0; ii < _filters.size(); ++ii )
         _vega_mag[ii] = -2.5*log10( _vega_int[ii]/_filt_int[ii] ) - 48.6;
      LOGLN( "Vega magnitudes: ", _vega_mag );
   }
}
