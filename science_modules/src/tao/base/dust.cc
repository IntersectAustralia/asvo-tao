#include <fstream>
#include <libhpc/numerics/spline.hh>
#include "dust.hh"

namespace tao {
   namespace dust {

      real_type const slab::default_sun_metallicity = 0.019;

      slab::slab()
         : _sun_metal( default_sun_metallicity )
      {
      }

      slab::slab( fs::path const& ext_fn,
                  hpc::view<std::vector<real_type>>::type const& waves )
         : _sun_metal( default_sun_metallicity )
      {
         load_extinction( ext_fn, waves );
      }

      void
      slab::load_extinction( fs::path const& ext_fn,
                             hpc::view<std::vector<real_type>>::type const& waves )
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

         hpc::numerics::spline< real_type,
                                hpc::view<std::vector<real_type>>::type,
                                hpc::view<std::vector<real_type>>::type > spline;

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
            _exp[ii] += 1.6; // TODO: Explain this.
         }
      }

      hpc::view<std::vector<real_type>>::type
      slab::extinction() const
      {
         return _ext;
      }

      hpc::view<std::vector<real_type>>::type
      slab::albedo() const
      {
         return _alb;
      }

      hpc::view<std::vector<real_type>>::type
      slab::exponents() const
      {
         return _exp;
      }

      real_type
      slab::_calc_tau( real_type nh,
                       real_type metal,
                       real_type ext,
                       real_type alb,
                       real_type exp )
      {
         ASSERT( ext >= 0.0 );
         real_type tau = ext*nh*pow( metal/_sun_metal, exp );
         return tau*sqrt( 1.0 - alb );
      }

   }
}
