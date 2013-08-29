#ifndef tao_modules_sed_hh
#define tao_modules_sed_hh

#include "tao/base/base.hh"

// Forward declaration of test suites to allow direct access.
class sed_suite;

namespace tao {
   namespace modules {
      using namespace hpc;

      ///
      /// SED science module. The SED module is responsible for calculating the
      /// energy spectra of each galaxy.
      ///
      class sed
         : public module
      {
         friend class ::sed_suite;

      public:

         static
         module*
         factory( const string& name,
                  pugi::xml_node base );

      public:

         sed( const string& name = string(),
              pugi::xml_node base = pugi::xml_node() );

         ~sed();

         ///
         /// Initialise the module.
         ///
         virtual
         void
         initialise( const options::xml_dict& global_dict );

         ///
         /// Run the module.
         ///
         virtual
         void
         execute();

      protected:

         void
         _process_time( mpi::lindex time_idx,
                        unsigned gal_idx );

         void
         _sum_spectra( mpi::lindex time_idx,
                       real_type metal,
                       real_type sfh,
                       vector<real_type>::view galaxy_spectra );

         unsigned
         _interp_metal( real_type metal );

         void
         _read_ssp( const string& filename );

         void
         _read_options( const options::xml_dict& global_dict );

      protected:

         backends::multidb<real_type>* _be;
         simulation<real_type>* _sim;
         stellar_population _ssp;
         age_line<real_type> _snap_ages, _bin_ages;
         sfh<real_type> _sfh;
         vector<real_type> _age_masses, _bulge_age_masses;
         vector<real_type> _age_metals;
         unsigned _num_spectra, _num_metals;
         fibre<real_type> _disk_spectra, _bulge_spectra, _total_spectra;
      };

   }
}

#endif
