#ifndef tao_base_lightcone_tile_iterator_hh
#define tao_base_lightcone_tile_iterator_hh

#include "simulation.hh"
#include "tile.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone_tile_iterator
      : public boost::iterator_facade< lightcone_tile_iterator<T>,
                                       tile<T>,
				       std::forward_iterator_tag,
                                       tile<T> >
   {
      friend class boost::iterator_core_access;

   public:

      typedef T real_type;
      typedef tile<real_type> value_type;
      typedef value_type reference_type;

      enum check_result
      {
         BELOW,
         ABOVE,
         ON
      };

   public:

      lightcone_tile_iterator()
         : _lc( NULL ),
           _done( true )
      {
      }

      lightcone_tile_iterator( const lightcone<real_type>& lc )
         : _lc( &lc ),
           _done( false )
      {
         std::fill( _cur.begin(), _cur.end(), 0 );
         if( _check() != ON )
            increment();
         _idx = 0;
      }

      bool
      done() const
      {
         return _done;
      }

      unsigned
      index() const
      {
         return _idx;
      }

   protected:

      void
      increment()
      {
         // Increment the index here. I do this because it's a little
         // easier than putting the increment on every return.
         ++_idx;

         real_type bs = _lc->simulation()->box_size();
         check_result res;
         do {
            do {
               do
               {
                  _cur[2] += bs;
                  res = _check();
                  if( res == ON )
                  {
                     return;
                  }
               }
               while( res == BELOW );

               _cur[1] += bs;
               _cur[2] = 0;
               res = _check();
               if( res == ON )
                  return;
            }
            while( res == BELOW );

            _cur[0] += bs;
            _cur[1] = 0;
            _cur[2] = 0;
            res = _check();
            if( res == ON )
               return;
         }
         while( res == BELOW );

         _done = true;
      }

      bool
      equal( const lightcone_tile_iterator& op ) const
      {
         return _done == op._done;
      }

      reference_type
      dereference() const
      {
         return tile<real_type>( _lc, _cur );
      }

      check_result
      _check()
      {
         real_type bs = _lc->_sim->box_size();

         // Check that the farthest corner of the box is greater than the
         // minimum distance.
         if( sqrt( pow( _cur[0] + bs, 2.0 ) + 
                   pow( _cur[1] + bs, 2.0 ) + 
                   pow( _cur[2] + bs, 2.0 ) ) < _lc->_dist[0] )
         {
            return BELOW;
         }

         // Check that the closest corner of the box is less than the
         // maximum distance.
         if( sqrt( pow( _cur[0], 2.0 ) + 
                   pow( _cur[1], 2.0 ) + 
                   pow( _cur[2], 2.0 ) ) > _lc->_dist[1] )
         {
            return ABOVE;
         }

         // We can check lower RA and DEC bounds by converting the (0, 1, 0)
         // vertex of the cube to ECS coordinates.
         real_type ra, dec;
         numerics::cartesian_to_ecs( _cur[0], _cur[1] + bs, _cur[2], ra, dec );
         if( ra < _lc->_ra[0] )
            return BELOW;

         // Similarly, we check the upper bounds by converting the (1, 0, 0)
         // vertex of the cube to ECS coordinates.
         numerics::cartesian_to_ecs( _cur[0] + bs, _cur[1], _cur[2], ra, dec );
         if( ra > _lc->_ra[1] )
            return ABOVE;

         // Similarly, we check the upper bounds by converting the (1, 0, 0)
         // vertex of the cube to ECS coordinates.
         numerics::cartesian_to_ecs( _cur[0], _cur[1], _cur[2] + bs, ra, dec );
         if( dec < _lc->_dec[0] )
            return BELOW;

         // We can check lower RA and DEC bounds by converting the (0, 1, 0)
         // vertex of the cube to ECS coordinates.
         numerics::cartesian_to_ecs( _cur[0] + bs, _cur[1] + bs, _cur[2], ra, dec );
         if( dec > _lc->_dec[1] )
            return ABOVE;

         // If we get here this box is in overlap.
         return ON;
      }

   protected:

      const lightcone<real_type>* _lc;
      array<real_type,3> _cur;
      bool _done;
      unsigned _idx;
   };

}

#endif
