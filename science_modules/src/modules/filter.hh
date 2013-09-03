#ifndef tao_modules_filter_hh
#define tao_modules_filter_hh

#include "tao/base/base.hh"

#define M_C 2.99792458e18 // angstrom/s

namespace tao {
   namespace modules {
      using namespace hpc;

      template< class Backend >
      class filter
         : public module<Backend>
      {
      public:

         typedef Backend backend_type;
         typedef module<backend_type> module_type;

         static
         module_type*
         factory( const string& name,
                  pugi::xml_node base )
         {
            return new filter( name, base );
         }

      public:

         filter( const string& name = string(),
                 pugi::xml_node base = pugi::xml_node() )
            : module_type( name, base )
         {
         }

         virtual
         ~filter()
         {
         }

         ///
         /// Initialise the module.
         ///
         virtual
         void
         initialise( const options::xml_dict& global_dict )
         {
            // Don't initialise if we're already doing so.
            if( this->_init )
               return;
            module_type::initialise( global_dict );

            auto timer = this->timer_start();
            LOGILN( "Initialising filter module.", setindent( 2 ) );

            // Find the wavelengths from my parents.
            _waves = this->template attribute<const vector<real_type>*>( "wavelengths" );

            _read_options( global_dict );

            // Prepare the batch object.
            ASSERT( this->parents().size() == 1, "Must have at least one parent defined." );
            tao::batch<real_type>& bat = this->parents().front()->batch();
            for( unsigned ii = 0; ii < _filter_names.size(); ++ii )
            {
               _total_app_mags[ii] = bat.set_scalar<real_type>( _filter_names[ii] + "_apparent" );
               _total_abs_mags[ii] = bat.set_scalar<real_type>( _filter_names[ii] + "_absolute" );
               _disk_app_mags[ii] = bat.set_scalar<real_type>( _filter_names[ii] + "_disk_apparent" );
               _disk_abs_mags[ii] = bat.set_scalar<real_type>( _filter_names[ii] + "_disk_absolute" );
               _bulge_app_mags[ii] = bat.set_scalar<real_type>( _filter_names[ii] + "_bulge_apparent" );
               _bulge_abs_mags[ii] = bat.set_scalar<real_type>( _filter_names[ii] + "_bulge_absolute" );
            }
            _total_lum = bat.set_scalar<real_type>( "total_luminosity" );
            _disk_lum = bat.set_scalar<real_type>( "disk_luminosity" );
            _bulge_lum = bat.set_scalar<real_type>( "bulge_luminosity" );

            // Extract things from the batch object.
            _redshift = bat.scalar<real_type>( "redshift" );
            _total_spectra = &bat.vector<real_type>( "total_spectra" );
            _disk_spectra = &bat.vector<real_type>( "disk_spectra" );
            _bulge_spectra = &bat.vector<real_type>( "bulge_spectra" );
         }

         ///
         /// Run the module.
         ///
         virtual
         void
         execute()
         {
            auto timer = this->timer_start();

            // Grab the batch from the parent object.
            tao::batch<real_type>& bat = this->parents().front()->batch();

            // Perform the processing.
            process_batch( bat, *_total_spectra, *_disk_spectra, *_bulge_spectra );
         }

         ///
         ///
         ///
         void
         process_batch( const tao::batch<real_type>& bat,
                        const fibre<real_type>& total_spectra,
                        const fibre<real_type>& disk_spectra,
                        const fibre<real_type>& bulge_spectra )
         {
            auto timer = this->timer_start();

            // Process each object individually to save space.
            for( unsigned ii = 0; ii < bat.size(); ++ii )
            {
               // Calculate the distance/area for this galaxy. Use 1000
               // points.
               LOGDLN( "Using redshift of ", _redshift[ii], " to calculate distance." );
               real_type dist = numerics::redshift_to_luminosity_distance( _redshift[ii], 1000 );
               if( dist < 1e-5 )  // Be careful! If dist is zero (which it can be) then resort to absolute
                  dist = 1e-5;    // magnitudes.
               real_type area = log10( 4.0*M_PI ) + 2.0*log10( dist*3.08568025e24 ); // result in cm^2
               LOGDLN( "Distance: ", dist );
               LOGDLN( "Log area: ", area );

               // Process total, disk and bulge.
               _process_spectra( total_spectra[ii], area, _total_lum[ii], _total_app_mags, _total_abs_mags, ii );
               _process_spectra( disk_spectra[ii], area, _disk_lum[ii], _disk_app_mags, _bulge_abs_mags, ii );
               _process_spectra( bulge_spectra[ii], area, _bulge_lum[ii], _bulge_app_mags, _bulge_abs_mags, ii );
            }
         }

      protected:

         void
         _process_spectra( const vector<real_type>::view& spectra,
                           real_type area,
                           real_type& luminosity,
                           vector<vector<real_type>::view>& apparent_mags,
                           vector<vector<real_type>::view>& absolute_mags,
                           unsigned gal_idx )
         {
            LOGTLN( "Using spectra of: ", spectra );

            // TODO: Shift this elsewhere to save some time.
            real_type abs_area = log10( 4.0*M_PI ) + 2.0*log10( (10.0/1e6)*3.08568025e24 ); // result in cm^2

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
                  absolute_mags[ii][gal_idx] = -2.5*(log10( spec_int ) - abs_area - log10( _filt_int[ii] )) - 48.6;
               }
               else
               {
                  apparent_mags[ii][gal_idx] = 0.0;
                  absolute_mags[ii][gal_idx] = 0.0;
               }

               // Make sure these are sane.
               ASSERT( apparent_mags[ii][gal_idx] == apparent_mags[ii][gal_idx], "NaN" );
               ASSERT( absolute_mags[ii][gal_idx] == absolute_mags[ii][gal_idx], "NaN" );
            }
         }

         void
         _prepare_spectra( const vector<real_type>::view& spectra,
                           numerics::spline<real_type>& spline )
         {
            ASSERT( spectra.size() == _waves->size() );
            fibre<real_type> knots( 2, spectra.size() );
            for( unsigned ii = 0; ii < _waves->size(); ++ii )
            {
               knots(ii,0) = (*_waves)[ii];
               knots(ii,1) = spectra[ii];
            }
            spline.set_knots( knots );
         }

         real_type
         _integrate( const numerics::spline<real_type>& filter,
                     const numerics::spline<real_type>& spectra )
         {
            typedef vector<real_type>::view array_type;
            element<array_type> take_first( 0 );

            range<real_type> fi_rng( filter.knots().front()[0], filter.knots().back()[0] );
            range<real_type> sp_rng( spectra.knots().front()[0], spectra.knots().back()[0] );
            real_type low = std::max( fi_rng.start(), sp_rng.start() );
            real_type upp = std::min( fi_rng.finish(), sp_rng.finish() );

            // If there is no overlap, return 0.
            if( upp <= low )
               return 0.0;

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
               real_type jac_det = 0.5*w;
               unsigned fi_poly = it.indices()[0] - 1;
               unsigned sp_poly = it.indices()[1] - 1;
               for( unsigned ii = 0; ii < 4; ++ii )
               {
                  real_type x = low + w*0.5*(1.0 + crds[ii]);
                  sum += jac_det*weights[ii]*filter( x, fi_poly )*spectra( x, sp_poly );
               }
               low = *it;
            }

            return sum;
         }

         real_type
         _integrate( const numerics::spline<real_type>& spectra )
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
                  sum += jac_det*weights[jj]*spectra( x, ii )*M_C/(x*x);
               }
            }

            return sum;
         }

         void
         _gauss_quad( vector<real_type>::view crds,
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
         _read_options( const options::xml_dict& global_dict )
         {
            // Cache the dictionary.
            const options::xml_dict& dict = this->_dict;

            // Read the prefix of the bandpass filters.
            auto path = data_prefix()/"bandpass_filters";

            // Split out the filter filenames.
            list<string> filenames = dict.get_list<string>( "bandpass-filters" );

            // Allocate room for the filters.
            _filters.reallocate( filenames.size() );
            _filters.resize( 0 );
            _filt_int.reallocate( filenames.size() );
            _filt_int.resize( 0 );
            _filter_names.reallocate( filenames.size() );

            // Load each filter into memory.
            unsigned ii = 0;
            for( const auto& fn : filenames )
            {
               _load_filter( path/fn );

               // Store the field names.
               _filter_names[ii] = fn;
               LOGDLN( "Adding filter by the name: ", _filter_names[ii] );
               ++ii;
            }
            LOGDLN( "Filter integrals: ", _filt_int );

            // Get the Vega filename and perform processing.
            path = data_prefix()/"vega";
            _process_vega( path/dict.get<string>( "vega-spectrum", "A0V_KUR_BB.SED" ) );
         }

         void
         _load_filter( const fs::path& filename )
         {
            LOGILN( "Loading bandpass filter from: ", filename, setindent( 2 ) );

            std::ifstream file( filename.c_str(), std::ios::in );
            EXCEPT( file.is_open(), "Failed to find file: ", filename );

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

            LOGILN( "Done.", setindent( -2 ) );
         }

         void
         _process_vega( const fs::path& filename )
         {
            LOGILN( "Processing Vega spectrum from: ", filename, setindent( 2 ) );

            std::ifstream file( filename.c_str() );
            EXCEPT( file.is_open(), "Failed to find Vega spectrum: ", filename );

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

            LOGILN( "Done.", setindent( -2 ) );
         }

      protected:

         const vector<real_type>* _waves;

         vector<real_type>::view _spec;
         vector<numerics::spline<real_type>> _filters;
         vector<real_type> _filt_int;
         vector<real_type> _vega_int;
         vector<real_type> _vega_mag;
         vector<string> _filter_names;

         vector<vector<real_type>::view> _total_app_mags, _total_abs_mags;
         vector<vector<real_type>::view> _disk_app_mags, _disk_abs_mags;
         vector<vector<real_type>::view> _bulge_app_mags, _bulge_abs_mags;
         vector<real_type>::view _total_lum, _disk_lum, _bulge_lum;
         vector<real_type>::view _redshift;
         fibre<real_type> *_total_spectra, *_disk_spectra, *_bulge_spectra;
      };

   }
}

#endif
