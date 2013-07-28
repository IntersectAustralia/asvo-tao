#include "integration.hh"

namespace tao {
   namespace integ {

      void
      gaussian_quadrature_4( vector<real_type>::view crds,
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

      real_type
      integrate( const numerics::spline<real_type>& spectra,
                 const numerics::spline<real_type>& filter )
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
         gaussian_quadrature_4( crds, weights );

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
      integrate( const numerics::spline<real_type>& spectra )
      {
         vector<real_type> crds( 4 ), weights( 4 );
         gaussian_quadrature_4( crds, weights );

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

   }
}
