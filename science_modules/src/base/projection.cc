#include <math.h>
#include <libhpc/numerics/coords.hh>
#include "projection.hh"

namespace tao {

   projection::projection()
   {
   }

   projection::projection( const lightcone<real_type>& lc,
                           unsigned width,
                           unsigned height )
      : _dim{ { width, height } }
   {
      _fov[0] = lc.max_ra() - lc.min_ra();
      _fov[1] = lc.max_dec() - lc.min_dec();
      _org[0] = lc.min_ra() + 0.5*_fov[0];
      _org[1] = lc.min_dec() + 0.5*_fov[1];
      _calc_scale();
   }

   void
   projection::project( real_type gal_x,
                        real_type gal_y,
                        real_type gal_z,
                        real_type& img_x,
                        real_type& img_y ) const
   {
      // Convert the cartesian coordiantes to right-ascension and
      // declination.
      real_type ra, dec;
      numerics::cartesian_to_ecs( gal_x, gal_y, gal_z,
                                  ra, dec );

      // Filter out any RA or DEC outside our FoV.
      if( fabs( ra - _org[0] ) <= 0.5*_fov[0] && fabs( dec - _org[1] ) <= 0.5*_fov[1] )
      {
         // Now convert to pixel coordinates.
         numerics::gnomonic_projection<real_type>( ra, dec, _org[0], _org[1], img_x, img_y );

         // To convert to pixel coordinates use the scaling factor
         // in each dimension and offset by half image size.
         img_x = img_x*_scale[0] + 0.5*_dim[0];
         img_y = img_y*_scale[1] + 0.5*_dim[1];
      }
   }

   projection::iterator
   projection::begin( const batch<real_type>& batch )
   {
      return iterator( *this, batch );
   }

   projection::iterator
   projection::end( const batch<real_type>& batch )
   {
      return iterator( batch );
   }

   void
   projection::_calc_scale()
   {
      // Calculate the required scale factors.
      _scale[0] = 0.5*_dim[0]/tan( 0.5*_fov[0] );
      _scale[1] = 0.5*_dim[1]/tan( 0.5*_fov[1] );
   }

   projection_iterator::projection_iterator( const batch<real_type>& bat )
      : _proj( NULL ),
        _bat( &bat )
   {
   }

   projection_iterator::projection_iterator( const projection& proj,
                                             const batch<real_type>& bat )
      : _proj( &proj ),
        _bat( &bat ),
        _gal_idx( 0 )
   {
      _x = _bat->scalar<real_type>( "pos_x" );
      _y = _bat->scalar<real_type>( "pos_y" );
      _z = _bat->scalar<real_type>( "pos_z" );
      // _mag = &_bat->scalar<real_type>( _proj->magnitude_field() );
   }

   bool
   projection_iterator::done() const
   {
      return _gal_idx == _bat->size();
   }

   projection_iterator::reference_type
   projection_iterator::operator*()
   {
      _proj->project( _x[_gal_idx], _y[_gal_idx], _z[_gal_idx], _pos[0], _pos[1] );
      return _pos;
   }

   real_type
   projection_iterator::magnitude() const
   {
      return _mag[_gal_idx];
   }

   unsigned
   projection_iterator::index() const
   {
      return _gal_idx;
   }

   void
   projection_iterator::increment()
   {
      ++_gal_idx;
   }

   bool
   projection_iterator::equal( const projection_iterator& op ) const
   {
      return done();
   }

   projection_iterator::reference_type
   projection_iterator::dereference() const
   {
      ASSERT( 0 );
      return _pos;
   }

}
