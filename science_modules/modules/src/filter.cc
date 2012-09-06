#include <cmath>
#include <boost/algorithm/string/trim.hpp>
#include <boost/tokenizer.hpp>
#include "filter.hh"

// Define the speed of light (m/s).
#define M_C 299792458.0

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

   filter::real_type
   filter::process_galaxy( const soci::row& galaxy,
                           vector<real_type>::view spectra )
   {
      // Prepare the spectra.
      numerics::spline<real_type> spectra_spline;
      _prepare_spectra( spectra, spectra_spline );

      // Loop over each filter band.
      for( unsigned ii = 0; ii < _filters.size(); ++ii )
         _process_filter( spectra_spline, _filters[ii], _filt_int[ii], _vega_int[ii] );
   }

   void
   filter::_process_filter( const numerics::spline<real_type>& spectra,
                            const numerics::spline<real_type>& filter,
                            real_type filter_int,
                            real_type vega_int )
   {
      real_type spec_int = _integrate( spectra, filter );
      _apparant_magnitude( spec_int, filter_int, vega_int, 1.0 ); // TODO: distance
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
      auto it = make_interp_iterator(
         boost::make_transform_iterator( filter.knots().begin(), take_first ),
         boost::make_transform_iterator( filter.knots().end(), take_first ),
         boost::make_transform_iterator( spectra.knots().begin(), take_first ),
         boost::make_transform_iterator( spectra.knots().end(), take_first ),
         1e-7
         );

      range<real_type> fi_rng( filter.knots().front()[0], filter.knots().back()[0] );
      range<real_type> sp_rng( spectra.knots().front()[0], spectra.knots().back()[0] );
      real_type low = std::max( fi_rng.start(), sp_rng.start() );
      real_type upp = std::min( fi_rng.finish(), sp_rng.finish() );

      while( !num::approx( *it, low, 1e-7 ) )
         ++it;

      vector<real_type> crds( 4 ), weights( 4 );
      _gauss_quad( crds, weights );

      real_type sum = 0.0;

      while( !num::approx( *it++, upp, 1e-7 ) )
      {
         real_type w = *it - low;
         real_type jac_det = 0.5*w;
         unsigned fi_poly = it.indices()[0] - 1;
         unsigned sp_poly = it.indices()[1] - 1;
         for( unsigned ii = 0; ii < 4; ++ii )
         {
            real_type x = low + w*0.5*(1.0 + crds[ii]);
            sum += jac_det*weights[ii]*filter( x, fi_poly )*spectra( x, sp_poly )*x*x/(M_C*1e10); // TODO: generalise
            std::cout << x << ": " << filter( x, fi_poly )*spectra( x, sp_poly ) << "\n";
         }
         low = *it;
      }

      exit( 1 );

      return sum;
   }

   // filter::real_type
   // filter::_integrate( const numerics::spline<real_type>& spectra )
   // {
   //    vector<real_type> crds( 4 ), weights( 4 );
   //    _gauss_quad( crds, weights );

   //    real_type sum = 0.0;

   //    for( unsigned ii = 0; ii < spectra.num_segments(); ++ii )
   //    {
   //       real_type low = spectra.segment_start( ii );
   //       real_type w = spectra.segment_width( ii );
   //       real_type jac_det = 0.5*w;
   //       for( unsigned ii = 0; ii < 4; ++ii )
   //       {
   //          real_type x = low + w*0.5*(1.0 + crds[ii]);
   //          sum += weights[ii]*spectra( x, ii )*jac_det;
   //       }
   //    }

   //    return sum;
   // }

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

         // Load each filter into memory.
         for( const auto& fn : filenames )
            _load_filter( fn );
      }

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
   }

   void
   filter::_process_vega( const string& filename )
   {
      std::ifstream file( filename );
      ASSERT( file.is_open() );

      // The Vega file is a spectrum. First column is wavelength and
      // second column is flux (?).
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
         file >> knots(ii,0);
         file >> knots(ii,1);

         // Scale the values by 2e-17.
         knots(ii,1) *= 2e-17;
      }

      // Convert the spectrum to a spline and convolve with each
      // filter.
      numerics::spline<real_type> spline;
      spline.set_knots( knots );
      LOGLN( "Calculating vega integrals with respect to filters.", setindent( 2 ) );
      for( unsigned ii = 0; ii < _filters.size(); ++ii )
      {
         _vega_int[ii] = _integrate( spline, _filters[ii] );
         LOGLN( indent, ii, ": ", _vega_int[ii] );
      }
      LOG( setindent( -2 ) );
   }
}
