#ifndef tao_base_dust_hh
#define tao_base_dust_hh

#include <math.h>
#include <fstream>
#include <boost/filesystem.hpp>
#include <libhpc/debug/except.hh>
#include <libhpc/system/view.hh>
#include <libhpc/system/assign.hh>
#include <libhpc/system/filesystem.hh>
#include "types.hh"

namespace tao {
   namespace dust {

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

         template< class Seq >
         slab( hpc::fs::path const& ext_fn,
               typename hpc::type_traits<Seq>::reference waves )
         {
            load_extinction( ext_fn, waves );
         }

         template< class Seq >
         void
         load_extinction( hpc::fs::path const& ext_fn,
                          typename hpc::type_traits<Seq>::reference waves )
         {
            std::ifstream strm( ext_fn.native() );
            EXCEPT( strm.good(), "Failed to open extinction file: ", ext_fn );

            unsigned size;
            strm >> size;
            std::vector<real_type> ext_waves( size );
            std::vector<real_type> ext( size );
            std::vector<real_type> alb( size );
            std::vector<real_type> exp( size );
            for( unsigned ii = 0; ii < size; ++ii )
               strm >> ext_waves[ii] >> ext[ii] >> alb[ii] >> exp[ii];
            EXCEPT( strm.good(), "Failure reading extinction file: ", ext_fn );

            // Extinction wavelength scale needs to be altered.
            std::transform( ext_waves.begin(), ext_waves.end(), ext_waves.begin(),
                            []( real_type x ) { return 1e4*x; } );

            hpc::num::spline< real_type,
                              hpc::view<std::vector<real_type>>,
                              hpc::view<std::vector<real_type>> > spline;

            _ext.resize( waves.size() );
            spline.set_knot_points( ext_waves );
            spline.set_knot_values( ext );
            spline.update();
            for( unsigned ii = 0; ii < waves.size(); ++ii )
            {
               if( waves[ii] < ext_waves[0] )
                  _ext[ii] = ext[0];
               else if( waves[ii] > ext_waves[size - 1] )
                  _ext[ii] = ext[size - 1];
               else
               {
                  _ext[ii] = spline( waves[ii] );
                  if( _ext[ii] <= 0.0 )
                  {
                     unsigned poly = spline.poly( waves[ii] );
                     _ext[ii] = spline.values()[poly] + ((waves[ii] - spline.points()[poly])/(spline.points()[poly + 1] - spline.points()[poly]))*(spline.values()[poly + 1] - spline.values()[poly]);
                  }
               }
               ASSERT( _ext[ii] > 0.0 );
            }

            _alb.resize( waves.size() );
            spline.set_knot_values( alb );
            spline.update();
            for( unsigned ii = 0; ii < waves.size(); ++ii )
            {
               if( waves[ii] < ext_waves[0] )
                  _alb[ii] = alb[0];
               else if( waves[ii] > ext_waves[size - 1] )
                  _alb[ii] = alb[size - 1];
               else
                  _alb[ii] = spline( waves[ii] );
            }

            _exp.resize( waves.size() );
            spline.set_knot_values( exp );
            spline.update();
            for( unsigned ii = 0; ii < waves.size(); ++ii )
            {
               if( waves[ii] < ext_waves[0] )
                  _exp[ii] = exp[0];
               else if( waves[ii] > ext_waves[size - 1] )
                  _exp[ii] = exp[size - 1];
               else
                  _exp[ii] = spline( waves[ii] );
            }

            // Need to add 1.6 to the exponent.
            std::transform( _exp.begin(), _exp.end(), _exp.begin(),
                            []( real_type x ) { return x + 1.6; } );
         }

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

         hpc::view<std::vector<real_type>>
         extinction() const;

         hpc::view<std::vector<real_type>>
         albedo() const;

         hpc::view<std::vector<real_type>>
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
            real_type nh = 0.75*cold_gas_mass/(M_PI*pow( 3.0*disk_radius, 2.0 ));
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
                  ASSERT( ext_it != _ext.cend() );
                  ASSERT( alb_it != _alb.cend() );
                  ASSERT( exp_it != _exp.cend() );
                  real_type tau_dust = _calc_tau( nh, metal, *ext_it++, *alb_it++, *exp_it++ );
                  tau_dust = tau_dust/cos_inc*1.0/(1.0 + redshift);
                  ASSERT( tau_dust > 0.0 );
                  real_type fesc = (1.0 - exp( -tau_dust ))/tau_dust;
                  *result_start++ = (*spec_start++)*fesc;
               }
            }
            else
               std::copy( spec_start, spec_finish, result_start );
         }

         template< class ResultIter >
         void
         calc_transmission( real_type h,
                            real_type redshift,
                            real_type cold_gas_mass,
                            real_type cold_gas_metal,
                            real_type disk_radius,
                            ResultIter result_start,
                            ResultIter const& result_finish )
         {
            static real_type const nh_factor = 0.00059475488;
            real_type nh = 0.75*cold_gas_mass/(M_PI*pow( 3.0*disk_radius, 2.0 ));
            real_type metal = (cold_gas_mass > 0.0) ? cold_gas_metal/cold_gas_mass : -100.0;
            real_type cos_inc = 1.0;
            if( nh > 0.0 && metal > 0.0 )
            {
               nh *= nh_factor*h;
               auto ext_it = _ext.cbegin();
               auto alb_it = _alb.cbegin();
               auto exp_it = _exp.cbegin();
               while( result_start != result_finish )
               {
                  ASSERT( ext_it != _ext.cend() );
                  ASSERT( alb_it != _alb.cend() );
                  ASSERT( exp_it != _exp.cend() );
                  real_type tau_dust = _calc_tau( nh, metal, *ext_it++, *alb_it++, *exp_it++ );
                  tau_dust = tau_dust/cos_inc*1.0/(1.0 + redshift);
                  ASSERT( tau_dust > 0.0 );
                  *result_start++ = (1.0 - exp( -tau_dust ))/tau_dust;
               }
            }
            else
               std::fill( result_start, result_finish, 1.0 );
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
