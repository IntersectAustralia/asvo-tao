#include <cmath>
#include <boost/algorithm/string/trim.hpp>
#include <boost/tokenizer.hpp>
#include "filter.hh"

// Define the speed of light
// #define M_C 2.99792458e8 // m/s
#define M_C 2.99792458e18 // angstrom/s

using namespace hpc;

namespace tao {

   // Factory function used to create a new filter module.
   module*
   filter::factory( const string& name )
   {
      return new filter( name );
   }

   filter::filter( const string& name )
      : module( name )
   {
   }

   filter::~filter()
   {
   }

   ///
   /// Initialise the module.
   ///
   void
   filter::initialise( const options::xml_dict& dict,
                       optional<const string&> prefix )
   {
      LOG_ENTER();

      _read_options( dict, prefix );

      LOG_EXIT();
   }

   void
   filter::execute()
   {
      _timer.start();
      LOG_ENTER();
      ASSERT( parents().size() == 1 );

      // Grab the galaxy from the parent object.
      tao::galaxy& gal = parents().front()->galaxy();

      // Extract things from the galaxy object.
      fibre<real_type>& total_spectra = gal.vector_values<real_type>( "total_spectra" );
      fibre<real_type>& disk_spectra = gal.vector_values<real_type>( "disk_spectra" );
      fibre<real_type>& bulge_spectra = gal.vector_values<real_type>( "bulge_spectra" );

      // Perform the processing.
      process_galaxy( gal, total_spectra, disk_spectra, bulge_spectra );

      // Add values to the galaxy object.
      for( unsigned ii = 0; ii < _filter_names.size(); ++ii )
      {
	 gal.set_field<real_type>( _filter_names[ii] + "_apparent", _total_app_mags[ii] );
	 gal.set_field<real_type>( _filter_names[ii] + "_absolute", _total_abs_mags[ii] );
	 gal.set_field<real_type>( _filter_names[ii] + "_disk_apparent", _disk_app_mags[ii] );
	 gal.set_field<real_type>( _filter_names[ii] + "_disk_absolute", _disk_abs_mags[ii] );
	 gal.set_field<real_type>( _filter_names[ii] + "_bulge_apparent", _bulge_app_mags[ii] );
	 gal.set_field<real_type>( _filter_names[ii] + "_bulge_absolute", _bulge_abs_mags[ii] );
      }
      gal.set_field<real_type>( "total_luminosity", _total_lum );
      gal.set_field<real_type>( "disk_luminosity", _disk_lum );
      gal.set_field<real_type>( "bulge_luminosity", _bulge_lum );

      LOG_EXIT();
      _timer.stop();
   }

   void
   filter::process_galaxy( const tao::galaxy& galaxy,
                           const fibre<real_type>& total_spectra,
                           const fibre<real_type>& disk_spectra,
                           const fibre<real_type>& bulge_spectra )
   {
      _timer.start();
      LOG_ENTER();

      // Process each object individually to save space.
      for( unsigned ii = 0; ii < galaxy.batch_size(); ++ii )
      {
         // Calculate the distance/area for this galaxy. Use 1000
         // points.
         LOGDLN( "Using redshift of ", galaxy.values<real_type>( "redshift" )[ii], " to calculate distance." );
         real_type dist = numerics::redshift_to_luminosity_distance( galaxy.values<real_type>( "redshift" )[ii], 1000 );
         real_type area = log10( 4.0*M_PI ) + 2.0*log10( dist*3.08568025e24 ); // result in cm^2
         LOGDLN( "Distance: ", dist );
         LOGDLN( "Log area: ", area );

         // Process total, disk and bulge.
         _process_spectra( total_spectra[ii], area, _total_lum[ii], _total_app_mags, _total_abs_mags, ii );
         _process_spectra( disk_spectra[ii], area, _disk_lum[ii], _disk_app_mags, _bulge_abs_mags, ii );
         _process_spectra( bulge_spectra[ii], area, _bulge_lum[ii], _bulge_app_mags, _bulge_abs_mags, ii );
      }

      LOG_EXIT();
      _timer.stop();
   }

   void
   filter::_process_spectra( const vector<real_type>::view& spectra,
                             real_type area,
			     real_type& luminosity,
                             fibre<real_type>& apparent_mags,
                             fibre<real_type>& absolute_mags,
			     unsigned gal_idx )
   {
      LOGDLN( "Using spectra of: ", spectra );

      // Prepare the spectra.
      numerics::spline<real_type> spectra_spline;
      _prepare_spectra( spectra, spectra_spline );

      // Calculate luminosity.
      luminosity = _integrate( spectra_spline );

      // Loop over each filter band.
      for( unsigned ii = 0; ii < _filters.size(); ++ii )
      {
         real_type spec_int = _integrate( spectra_spline, _filters[ii] );
         LOGDLN( "For filter ", ii, " calculated F_\\nu of ", spec_int );

         // Need to check that there is in fact a spectra.
         if( !num::approx( spec_int, 0.0, 1e-12 ) &&
             !num::approx( _filt_int[ii], 0.0, 1e-12 ) )
         {
            apparent_mags[ii][gal_idx] = -2.5*(log10( spec_int ) - area - log10( _filt_int[ii] )) - 48.6;
            absolute_mags[ii][gal_idx] = -2.5*(log10( spec_int ) - log10( _filt_int[ii] )) - 48.6;
         }
         else
         {
            apparent_mags[ii][gal_idx] = 0.0;
            absolute_mags[ii][gal_idx] = 0.0;
         }
      }
   }

   ///
   ///
   ///
   const hpc::vector<filter::real_type>::view
   filter::magnitudes() const
   {
      return _total_app_mags;
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
      LOGDLN( "fi_rng = ", fi_rng );
      LOGDLN( "sp_rng = ", sp_rng );
      LOGDLN( "low = ", low );
      LOGDLN( "upp = ", upp );

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
         // real_type jac_det = 0.5*(M_C/low - M_C/(*it));
         real_type jac_det = 0.5*w;
         unsigned fi_poly = it.indices()[0] - 1;
         unsigned sp_poly = it.indices()[1] - 1;
         LOGDLN( "w = ", w );
         LOGDLN( "jac_det = ", jac_det );
         for( unsigned ii = 0; ii < 4; ++ii )
         {
            real_type x = low + w*0.5*(1.0 + crds[ii]);
            LOGDLN( "Current x: ", x );
            LOGDLN( "Filter: ", filter( x, fi_poly ) );
            LOGDLN( "Spectra: ", spectra( x, sp_poly ) );

            // This integral looks like this because of a change of variable
            // frome wavelength to frequency. Do the math!
            // sum += jac_det*weights[ii]*filter( x, fi_poly )*spectra( x, sp_poly )*x*x*x*x*2.0/(2.9979*M_C);
            // sum += jac_det*weights[ii]*filter( x, fi_poly )*spectra( x, sp_poly )*x*x*x*x/(M_C*M_C);
            // sum += jac_det*weights[ii]*filter( x, fi_poly )*spectra( x, sp_poly )*x*x/M_C;
            sum += jac_det*weights[ii]*filter( x, fi_poly )*spectra( x, sp_poly );
            LOGDLN( "Partial sum is ", sum );
         }
         low = *it;
      }

      LOGDLN( "Integrated to ", sum );
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
            sum += jac_det*weights[jj]*spectra( x, ii )*M_C/(x*x);
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
   filter::_read_options( const options::xml_dict& dict,
                          optional<const string&> prefix )
   {
      LOG_ENTER();

      // Must perform the module read to get batch size.
      _read_db_options( dict );

      {
         // Get the wavelengths filename.
         string filename = dict.get<string>( prefix.get()+":wavelengths","wavelengths.dat" );
         LOGDLN( "Using wavelengths filename \"", filename, "\"" );

         // Load the wavelengths.
         _read_wavelengths( filename );
      }

      {
         // Split out the filter filenames.
	 list<string> filenames = dict.get_list<string>( prefix.get()+":bandpass-filters" );

         // Allocate room for the filters.
         _filters.reallocate( filenames.size() );
         _filters.resize( 0 );
         _filt_int.reallocate( filenames.size() );
         _filt_int.resize( 0 );
	 _filter_names.reallocate( filenames.size() );
         _total_app_mags.reallocate( _batch_size, filenames.size() );
         _total_abs_mags.reallocate( _batch_size, filenames.size() );
         _disk_app_mags.reallocate( _batch_size, filenames.size() );
         _disk_abs_mags.reallocate( _batch_size, filenames.size() );
         _bulge_app_mags.reallocate( _batch_size, filenames.size() );
         _bulge_abs_mags.reallocate( _batch_size, filenames.size() );
         _total_lum.reallocate( _batch_size );
         _disk_lum.reallocate( _batch_size );
         _bulge_lum.reallocate( _batch_size );

         // Load each filter into memory.
	 unsigned ii = 0;
	 for( const auto fn : filenames )
	 {
            _load_filter( fn );

	    // Store the field names.
	    auto it = std::find( fn.rbegin(), fn.rend(), '.' );
	    it++;
	    _filter_names[ii] = string( fn.begin(), it.base() );
	    LOGDLN( "Adding filter by the name: ", _filter_names[ii] );
	    ++ii;
	 }
      }
      LOGDLN( "Filter integrals: ", _filt_int );

      // Get the Vega filename and perform processing.
      _process_vega( dict.get<string>( prefix.get()+":vega-spectrum","A0V_KUR_BB.SED" ) );

      LOG_EXIT();
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
      LOGDLN( "Vega integrals: ", _vega_int );

      // Calculate the Vega magnitudes. I'm pretty sure that the
      // SED we read for Vega is already in erg.s^-1.cm^-2.Hz^-1,
      // it is already a flux density. So, we don't need any
      // distance information.
      _vega_mag.reallocate( _filters.size() );
      for( unsigned ii = 0; ii < _filters.size(); ++ii )
         _vega_mag[ii] = -2.5*log10( _vega_int[ii]/_filt_int[ii] ) - 48.6;
      LOGDLN( "Vega magnitudes: ", _vega_mag );
   }
}
