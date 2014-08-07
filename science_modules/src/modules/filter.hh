#ifndef tao_modules_filter_hh
#define tao_modules_filter_hh

#include <libhpc/system/assign.hh>
#include "tao/base/base.hh"

namespace tao {
   namespace modules {

      template< class Backend >
      class filter
         : public module<Backend>
      {
      public:

         typedef Backend backend_type;
         typedef module<backend_type> module_type;

         static
         module_type*
         factory( const std::string& name,
                  pugi::xml_node base )
         {
            return new filter( name, base );
         }

      public:

         filter( const std::string& name = std::string(),
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
         initialise( const xml_dict& global_dict )
         {
            // Don't initialise if we're already doing so.
            if( this->_init )
               return;
            module_type::initialise( global_dict );

            LOGILN( "Initialising filter module.", setindent( 2 ) );

            // Find the wavelengths and simulation from my parents.
            hpc::assign( _waves, this->template attribute<hpc::view<std::vector<real_type> const>>( "wavelengths" ) );
            _sim = this->template attribute<tao::simulation const*>( "simulation" );

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
            hpc::assign( _redshift, bat.scalar<real_type>( "redshift_cosmological" ) );
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
            // Grab the batch from the parent object.
            tao::batch<real_type>& bat = this->parents().front()->batch();

            // Perform the processing.
            process_batch( bat, *_total_spectra, *_disk_spectra, *_bulge_spectra );
         }

         ///
         ///
         ///
         void
         process_batch( tao::batch<real_type> const& bat,
                        const hpc::matrix<real_type>& total_spectra,
                        const hpc::matrix<real_type>& disk_spectra,
                        const hpc::matrix<real_type>& bulge_spectra )
         {
	    LOGBLOCKD( "Processing batch in filter module." );

#ifndef NLOGDEBUG
	    auto ids = bat.scalar<long long>( "globalindex" );
#endif

            // Process each object individually to save space.
            for( unsigned ii = 0; ii < bat.size(); ++ii )
            {
	       LOGDLN( "Galaxy global index: ", ids[ii] );

               // Calculate the distance/area for this galaxy. Use 1000
               // points.
               LOGDLN( "Using redshift of ", _redshift[ii], " to calculate area." );
               real_type area = calc_area( _redshift[ii], *_sim );
	       LOGDLN( "Calculated area: ", area );

               // Process total, disk and bulge.
               {
                  LOGBLOCKD( "Processing total spectra:" );
                  _process_spectra( total_spectra[ii], _redshift[ii], area, _total_lum[ii], _total_app_mags, _total_abs_mags, ii );
               }
               {
                  LOGBLOCKD( "Processing disk spectra:" );
                  _process_spectra( disk_spectra[ii], _redshift[ii], area, _disk_lum[ii], _disk_app_mags, _bulge_abs_mags, ii );
               }
               {
                  LOGBLOCKD( "Processing bulge spectra:" );
                  _process_spectra( bulge_spectra[ii], _redshift[ii], area, _bulge_lum[ii], _bulge_app_mags, _bulge_abs_mags, ii );
               }

#if 0
	       // Dump some stuff.
	       std::ofstream outf( boost::lexical_cast<std::string>( ids[ii] ) + ".dat", std::ios::app );
	       outf << "REDSHIFT (COSMOLOGICAL): " << _redshift[ii] << "\n";
	       outf << "APPARENT MAGNITUDE: " << _total_app_mags[0][ii] << "\n";
	       outf << "ABSOLUTE MAGNITUDE: " << _total_abs_mags[0][ii] << "\n";
#endif
            }
         }

      protected:

         void
         _process_spectra( hpc::view<std::vector<real_type> const> const& spectra,
                           real_type redshift,
                           real_type area,
                           real_type& luminosity,
                           std::vector<hpc::view<std::vector<real_type>>>& apparent_mags,
                           std::vector<hpc::view<std::vector<real_type>>>& absolute_mags,
                           unsigned gal_idx )
         {
            typedef hpc::view<std::vector<real_type>> view_type;
            typedef hpc::num::spline<real_type,view_type,view_type> spline_type;

	    LOGDLN( "Spectra: ", spectra );

            // Calculate absolute magnitudes.
            {
               // Prepare the normal SED.
               tao::sed<spline_type> sed( (const hpc::view<std::vector<real_type>>&)_waves,
                                          (const hpc::view<std::vector<real_type>>&)spectra );

               // Calculate luminosity.
               luminosity = integrate( sed.spectrum() );

               // Each bandpass filter.
               for( unsigned ii = 0; ii < _bpfs.size(); ++ii )
               {
                  absolute_mags[ii][gal_idx] = absolute_magnitude( sed, _bpfs[ii] );
                  ASSERT( absolute_mags[ii][gal_idx] == absolute_mags[ii][gal_idx],
                          "Produced NaN for absolute magnitude." );
		  LOGDLN( "Absolute magnitude: ", absolute_mags[ii][gal_idx] );
               }
            }

            // Now to calculate apparent magnitudes.
            if( _k_cor )
            {
               // Transform the spectra.
               std::vector<real_type> new_spec( spectra.size() );
               std::transform(
                  spectra.begin(), spectra.end(), new_spec.begin(),
                  [redshift]( real_type val )
                  {
                     return val/(1.0 + redshift);
                  }
                  );

               // Transform the wavelengths.
               std::vector<real_type> new_waves( _waves.size() );
               std::transform(
                  _waves.begin(), _waves.end(), new_waves.begin(),
                  [redshift]( real_type val )
                  {
                     return val*(1.0 + redshift);
                  }
                  );

               // Prepare new SED.
               tao::sed<> sed( new_waves, new_spec );

               // Each bandpass filter.
               for( unsigned ii = 0; ii < _bpfs.size(); ++ii )
               {
                  apparent_mags[ii][gal_idx] = apparent_magnitude( sed, _bpfs[ii], area );
                  ASSERT( apparent_mags[ii][gal_idx] == apparent_mags[ii][gal_idx],
                          "Produced NaN for apparent magnitude." );
		  LOGDLN( "Apparent magnitude: ", apparent_mags[ii][gal_idx] );
               }
            }
            else
            {
               // Prepare the normal SED.
               tao::sed<spline_type> sed( (const hpc::view<std::vector<real_type>>&)_waves,
                                          (const hpc::view<std::vector<real_type>>&)spectra );

               // Each bandpass filter.
               for( unsigned ii = 0; ii < _bpfs.size(); ++ii )
               {
                  apparent_mags[ii][gal_idx] = apparent_magnitude( sed, _bpfs[ii], area );
                  ASSERT( apparent_mags[ii][gal_idx] == apparent_mags[ii][gal_idx],
                          "Produced NaN for apparent magnitude." );
		  LOGDLN( "Apparent magnitude: ", apparent_mags[ii][gal_idx] );
               }
            }
         }

         void
         _read_options( const xml_dict& global_dict )
         {
            // Cache the dictionary.
            xml_dict const& dict = this->_dict;

            // Read the prefix of the bandpass filters.
            auto path = data_prefix()/"bandpass_filters";

            // Split out the filter filenames.
            std::list<std::string> filenames = dict.get_list<std::string>( "bandpass-filters" );

            // Allocate room for the filters.
            hpc::reallocate( _bpfs, filenames.size() );
            hpc::reallocate( _bpf_names, filenames.size() );

            // Load each filter into memory.
            unsigned ii = 0;
            for( const auto& fn : filenames )
            {
               _bpfs[ii].load( path/fn );

               // Store the field names.
               _bpf_names[ii] = fn;
	       hpc::to_lower( (std::string&)_bpf_names[ii] );
               LOGDLN( "Adding filter by the name: ", _bpf_names[ii] );
               ++ii;
            }

            // Get the Vega filename and perform processing.
            path = data_prefix()/"spectra";
            _process_vega( path/dict.get<std::string>( "vega-spectrum", "A0V_KUR_BB.SED" ) );

            // Read k-correction.
            _k_cor = dict.get<bool>( "k-correction", true );
            LOGILN( "Using inverse k-correction: ", (_k_cor ? "yes" : "no") );
         }

         void
         _process_vega( const fs::path& filename )
         {
            LOGILN( "Processing Vega spectrum from: ", filename, setindent( 2 ) );

            // Load the Vega spectrum.
            tao::sed<> vega( filename );

            // Integrate against each of the filters.
            hpc::reallocate( _vega_int, _bpfs.size() );
            for( unsigned ii = 0; ii < _bpfs.size(); ++ii )
               _vega_int[ii] = vega.integrate( _bpfs[ii] );
            LOGDLN( "Vega integrals: ", _vega_int );

            // Calculate the Vega magnitudes. I'm pretty sure that the
            // SED we read for Vega is already in erg.s^-1.cm^-2.Hz^-1,
            // it is already a flux density. So, we don't need any
            // distance information.
            hpc::reallocate( _vega_mag, _bpfs.size() );
            for( unsigned ii = 0; ii < _bpfs.size(); ++ii )
               _vega_mag[ii] = -2.5*log10( _vega_int[ii]/_bpfs[ii].integral() ) - 48.6;
            LOGDLN( "Vega magnitudes: ", _vega_mag );

            LOGILN( "Done.", setindent( -2 ) );
         }

      protected:

	 tao::simulation const* _sim;
         hpc::view<std::vector<real_type> const> _waves;

         hpc::view<std::vector<real_type> const> _spec;
         std::vector<bandpass> _bpfs;
         std::vector<std::string> _bpf_names;
         std::vector<real_type> _vega_int;
         std::vector<real_type> _vega_mag;
         bool _k_cor;

         std::vector<hpc::view<std::vector<real_type>>> _total_app_mags, _total_abs_mags;
         std::vector<hpc::view<std::vector<real_type>>> _disk_app_mags, _disk_abs_mags;
         std::vector<hpc::view<std::vector<real_type>>> _bulge_app_mags, _bulge_abs_mags;
         hpc::view<std::vector<real_type>> _total_lum, _disk_lum, _bulge_lum;
         hpc::view<std::vector<real_type> const> _redshift;
         hpc::matrix<real_type> *_total_spectra, *_disk_spectra, *_bulge_spectra;
      };

   }
}

#endif
