#ifndef tao_base_dust_hh
#define tao_base_dust_hh

#include <math.h>
#include <boost/filesystem.hpp>
#include <libhpc/containers/view.hh>
#include <libhpc/containers/assign.hh>
#include "types.hh"

namespace tao {
   namespace dust {
      namespace fs = boost::filesystem;

      ///
      /// Calculate dust according to Calzetti (?). TODO:
      /// need to provide a reference and more details.
      ///
      /// @tparam SpecIter Spectrum iterator type.
      /// @tparam WaveIter Wavelength iterator type.
      /// @tparam ResultIter Result iterator type.
      /// @param sfr Star formation rate of galaxy.
      /// @param spec_start Spectrum start iterator.
      /// @param spec_finish Spectrum finish iterator.
      /// @param wave_start Wavelength start iterator. The end of
      ///                   the wavelengths iteration is decided by
      ///                   end of the spectrum range.
      /// @param result_start Resulting spectrum.
      ///
      template< class SpecIter,
                class WaveIter,
                class ResultIter >
      void
      calzetti( real_type sfr,
                SpecIter spec_start,
                SpecIter const& spec_finish,
                WaveIter wave_start,
                ResultIter result_start )
      {
         static real_type const M_E_CU = M_E*M_E*M_E;
         static real_type const ALPHA  = M_E_CU - 1.0/M_E/M_E;

         // Calculate "adust", whatever that is...
         real_type adust;
         if( sfr > 0.05 )
         {
            // TODO: Explain the shit out of this.
            // TODO: Needs thorough checking.
            adust = 3.675*1.0/ALPHA*pow( sfr/1.479, 0.4 );
            adust += -1.0/ALPHA/M_E/M_E + 0.06;
         }
         else
            adust = 0.0;
         // LOGDLN( "adust: ", adust );

         // K-band unchanged by dust with this value (?).
         real_type rdust = 3.675;
         // LOGDLN( "rdust: ", rdust );
         ASSERT( adust/rdust >= 0.0, "Some dust problem... ?" );

         while( spec_start != spec_finish )
         {
            real_type wl = *wave_start++;

            // Why 6300.0?
            real_type kdust;
            if( wl <= 6300.0 )
            {
               kdust = 2.659*(-2.156 + 1.5098*1e4/wl - 0.198*1e8/wl/wl + 
                              0.011*1e12/wl/wl/wl) + rdust;
            }
            else
            {
               kdust = 2.659*(-1.857 + 1.040*1e4/wl) + rdust;
            }
            // LOGDLN( "kdust: ", kdust );

            real_type expdust;
            if( adust >= 0.0 )
               expdust = kdust*adust/rdust;
            else
               expdust = 0.0;
            // LOGDLN( "expdust: ", expdust );

            // Stomp on spectra.
            *result_start++ = (*spec_start++)*pow( 10.0, -0.4*expdust );
         }
      }

      ///
      /// Slab dust model.
      ///
      class slab
      {
      public:

         static real_type const default_sun_metallicity;

      public:

         slab();

         slab( fs::path const& ext_fn,
               hpc::view<std::vector<real_type>>::type const& waves );

         void
         load_extinction( fs::path const& ext_fn,
                          hpc::view<std::vector<real_type>>::type const& waves );

         template< class ExtSeq,
                   class AlbSeq,
                   class ExpSeq >
         void
         set_extinction( ExtSeq&& ext,
                         AlbSeq&& alb,
                         ExpSeq&& exp )
         {
            hpc::assign( _ext, std::forward<ExtSeq>( ext ) );
            hpc::assign( _alb, std::forward<AlbSeq>( alb ) );
            hpc::assign( _exp, std::forward<ExpSeq>( exp ) );
         }

         hpc::view<std::vector<real_type>>::type
         extinction() const;

         hpc::view<std::vector<real_type>>::type
         albedo() const;

         hpc::view<std::vector<real_type>>::type
         exponents() const;

         ///
         /// Calculate dust according to a slab model (?). TODO:
         /// need to provide a reference and more details.
         ///
         /// @tparam SpecIter Spectrum iterator type.
         /// @tparam WaveIter Wavelength iterator type.
         /// @tparam ResultIter Result iterator type.
         /// @param h Hubble constant divided by 100.
         /// @param redshift The cosmological redshift of the galaxy.
         /// @param cold_gas_mass Cold gas mass of galaxy.
         /// @param cold_gas_metal Cold gas metallicity of galaxy.
         /// @param disk_radius Disk radius of galaxy.
         /// @param spec_start Spectrum start iterator.
         /// @param spec_finish Spectrum finish iterator.
         /// @param wave_start Wavelength start iterator. The end of
         ///                   the wavelengths iteration is decided by
         ///                   end of the spectrum range.
         /// @param result_start Resulting spectrum.
         ///
         template< class SpecIter,
                   class WaveIter,
                   class ResultIter >
         void
         operator()( real_type h,
                     real_type redshift,
                     real_type cold_gas_mass,
                     real_type cold_gas_metal,
                     real_type disk_radius,
                     SpecIter spec_start,
                     SpecIter const& spec_finish,
                     WaveIter wave_start,
                     ResultIter result_start )
         {
            static real_type const nh_factor = 0.00059475488;
            real_type nh = 0.75*cold_gas_metal/(M_PI*pow( 3.0*disk_radius, 2.0 ));
            real_type metal = (cold_gas_mass > 0.0) ? cold_gas_metal/cold_gas_mass : -100.0;
            real_type cos_inc = 1.0;
            if( nh > 0.0 && metal > 0.0 )
            {
               nh *= nh_factor*h;
               auto ext_it = _ext.cbegin();
               auto alb_it = _alb.cbegin();
               auto exp_it = _exp.cbegin();
               while( spec_start != spec_finish )
               {
                  real_type tau_dust = _calc_tau( nh, metal, *ext_it++, *alb_it++, *exp_it++ );
                  tau_dust = tau_dust/cos_inc*1.0/(1.0 + redshift);
                  ASSERT( tau_dust > 0.0 );
                  real_type fesc = (1.0 - exp(-tau_dust))/tau_dust;
                  *result_start++ = (*spec_start++)*fesc;
               }
            }
            else
               std::copy( spec_start, spec_finish, result_start );
         }

      protected:

         real_type
         _calc_tau( real_type nh,
                    real_type metal,
                    real_type ext,
                    real_type alb,
                    real_type exp );

      protected:

         real_type _sun_metal;
         std::vector<real_type> _ext;
         std::vector<real_type> _alb;
         std::vector<real_type> _exp;
      };

   }
}

#endif
