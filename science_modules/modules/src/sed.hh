#ifndef tao_sed_sed_hh
#define tao_sed_sed_hh

#include "tao/base/module.hh"

namespace tao {

   ///
   /// SED science module.
   ///
   /// The SED module is responsible for calculating the
   /// energy spectra of each galaxy.
   ///
   class sed
      : public module
   {
   public:

      typedef double real_type;

      sed();

      ~sed();

      ///
      ///
      ///
      void
      setup_options( hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      ///
      ///
      ///
      void
      setup_options( hpc::options::dictionary& dict,
                     const char* prefix );

      ///
      /// Initialise the module.
      ///
      void
      initialise( const hpc::options::dictionary& dict,
                  hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      ///
      ///
      ///
      void
      initialise( const hpc::options::dictionary& dict,
                  const char* prefix );

      ///
      /// Run the module.
      ///
      void
      run();

      void
      process_galaxy( const tao::galaxy& galaxy );

      hpc::vector<real_type>::view
      disk_spectra();

      hpc::vector<real_type>::view
      bulge_spectra();

      hpc::vector<real_type>::view
      total_spectra();

   protected:

      void
      _process_time( hpc::mpi::lindex time_idx );

      void
      _sum_spectra( hpc::mpi::lindex time_idx,
                    real_type metal,
                    real_type sfh,
                    hpc::vector<real_type>::view galaxy_spectra );

      unsigned
      _interp_metal( real_type metal );

      void
      _rebin_info( unsigned flat_file,
                   unsigned flat_offset,
                   unsigned flat_length );

      void
      _gauss_quad( hpc::vector<real_type>::view crds,
                   hpc::vector<real_type>::view weights );

      void
      _update_flat_info( unsigned flat_file );

      void
      _read_ssp( const hpc::string& filename );

      void
      _read_options( const hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      void
      _read_flat_file( const hpc::string& base_filename,
                       unsigned flat_file );

   protected:

      hpc::vector<real_type> _ages;
      hpc::vector<real_type> _disk_age_masses, _bulge_age_masses;
      hpc::vector<real_type> _disk_age_metals, _bulge_age_metals;
      hpc::mpi::lindex _num_spectra, _num_metals;
      hpc::vector<real_type> _disk_spectra, _bulge_spectra, _total_spectra;
      hpc::vector<real_type> _ssp;

      hpc::h5::datatype _flat_mem_type, _flat_file_type;
      hpc::vector<flat_info<real_type>> _flat_data;
      int _cur_flat_file;
   };
}

#endif
