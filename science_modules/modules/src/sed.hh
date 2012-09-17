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
      _read_ssp( const hpc::string& filename );

      void
      _read_options( const hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

   protected:

      hpc::mpi::lindex _num_times, _num_spectra, _num_metals;
      hpc::vector<real_type> _disk_sfh, _disk_metals;
      hpc::vector<real_type> _bulge_sfh, _bulge_metals;
      hpc::vector<real_type> _disk_spectra, _bulge_spectra, _total_spectra;
      hpc::vector<real_type> _ssp;

      hpc::h5::datatype _flat_mem_type, _flat_file_type;
      hpc::vector<flat_info> _flat_data;
      int _cur_flat_file;
   };
}

#endif
