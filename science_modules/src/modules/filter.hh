#ifndef tao_modules_filter_hh
#define tao_modules_filter_hh

#include "tao/base/base.hh"

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
            _waves = this->template attribute<const vector<real_type>::view>( "wavelengths" );

            _read_options( global_dict );

            // Allocate for batch references.
            _total_app_mags.resize( _bpf_names.size() );
            _total_abs_mags.resize( _bpf_names.size() );
            _disk_app_mags.resize( _bpf_names.size() );
            _disk_abs_mags.resize( _bpf_names.size() );
            _bulge_app_mags.resize( _bpf_names.size() );
            _bulge_abs_mags.resize( _bpf_names.size() );

            // Prepare the batch object.
            ASSERT( this->parents().size() == 1, "Must have at least one parent defined." );
            tao::batch<real_type>& bat = this->parents().front()->batch();
            for( unsigned ii = 0; ii < _bpf_names.size(); ++ii )
            {
               _total_app_mags[ii] = bat.set_scalar<real_type>( _bpf_names[ii] + "_apparent" );
               _total_abs_mags[ii] = bat.set_scalar<real_type>( _bpf_names[ii] + "_absolute" );
               _disk_app_mags[ii] = bat.set_scalar<real_type>( _bpf_names[ii] + "_disk_apparent" );
               _disk_abs_mags[ii] = bat.set_scalar<real_type>( _bpf_names[ii] + "_disk_absolute" );
               _bulge_app_mags[ii] = bat.set_scalar<real_type>( _bpf_names[ii] + "_bulge_apparent" );
               _bulge_abs_mags[ii] = bat.set_scalar<real_type>( _bpf_names[ii] + "_bulge_absolute" );
            }
            _total_lum = bat.set_scalar<real_type>( "total_luminosity" );
            _disk_lum = bat.set_scalar<real_type>( "disk_luminosity" );
            _bulge_lum = bat.set_scalar<real_type>( "bulge_luminosity" );

            // Extract things from the batch object.
            _redshift = bat.scalar<real_type>( "redshift_cosmological" );
            _total_spectra = &bat.vector<real_type>( "total_spectra" );
            _disk_spectra = &bat.vector<real_type>( "disk_spectra" );
            _bulge_spectra = &bat.vector<real_type>( "bulge_spectra" );

            LOGILN( "Done.", setindent( -2 ) );
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
               LOGDLN( "Using redshift of ", _redshift[ii], " to calculate area." );
               real_type area = calc_area( _redshift[ii] );

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
            // Prepare the SED.
            typedef hpc::view<std::vector<real_type>>::type view_type;
            typedef numerics::spline<real_type,view_type,view_type> spline_type;
            tao::sed<spline_type> sed( (const view<std::vector<real_type>>::type&)_waves, (const vector_view<std::vector<real_type>>&)spectra );

            // Calculate luminosity.
            luminosity = integrate( sed.spectrum() );

            // Loop over each filter band.
            for( unsigned ii = 0; ii < _bpfs.size(); ++ii )
            {
               apparent_mags[ii][gal_idx] = apparent_magnitude( sed, _bpfs[ii], area );
               absolute_mags[ii][gal_idx] = absolute_magnitude( sed, _bpfs[ii] );

               // Make sure these are sane.
               ASSERT( apparent_mags[ii][gal_idx] == apparent_mags[ii][gal_idx],
                       "Produced NaN for apparent magnitude." );
               ASSERT( absolute_mags[ii][gal_idx] == absolute_mags[ii][gal_idx],
                       "Produced NaN for absolute magnitude." );
            }
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
            _bpfs.reallocate( filenames.size() );
            _bpf_names.reallocate( filenames.size() );

            // Load each filter into memory.
            unsigned ii = 0;
            for( const auto& fn : filenames )
            {
               _bpfs[ii].load( path/fn );

               // Store the field names.
               _bpf_names[ii] = fn;
               LOGDLN( "Adding filter by the name: ", _bpf_names[ii] );
               ++ii;
            }

            // Get the Vega filename and perform processing.
            path = data_prefix()/"spectra";
            _process_vega( path/dict.get<string>( "vega-spectrum", "A0V_KUR_BB.SED" ) );
         }

         void
         _process_vega( const fs::path& filename )
         {
            LOGILN( "Processing Vega spectrum from: ", filename, setindent( 2 ) );

            // Load the Vega spectrum.
            tao::sed<> vega( filename );

            // Integrate against each of the filters.
            _vega_int.reallocate( _bpfs.size() );
            for( unsigned ii = 0; ii < _bpfs.size(); ++ii )
               _vega_int[ii] = vega.integrate( _bpfs[ii] );
            LOGDLN( "Vega integrals: ", _vega_int );

            // Calculate the Vega magnitudes. I'm pretty sure that the
            // SED we read for Vega is already in erg.s^-1.cm^-2.Hz^-1,
            // it is already a flux density. So, we don't need any
            // distance information.
            _vega_mag.reallocate( _bpfs.size() );
            for( unsigned ii = 0; ii < _bpfs.size(); ++ii )
               _vega_mag[ii] = -2.5*log10( _vega_int[ii]/_bpfs[ii].integral() ) - 48.6;
            LOGDLN( "Vega magnitudes: ", _vega_mag );

            LOGILN( "Done.", setindent( -2 ) );
         }

      protected:

         vector<real_type>::view _waves;

         vector<real_type>::view _spec;
         vector<bandpass> _bpfs;
         vector<string> _bpf_names;
         vector<real_type> _vega_int;
         vector<real_type> _vega_mag;

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
