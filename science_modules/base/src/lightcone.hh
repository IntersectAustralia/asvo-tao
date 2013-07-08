#ifndef tao_base_lightcone_hh
#define tao_base_lightcone_hh

#include "simulation.hh"
#include "box.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone_box_iterator;

   template< class T >
   class lightcone
   {
      friend lightcone_box_iterator<T>;

   public:

      typedef T real_type;
      typedef lightcone_box_iterator<real_type> box_iterator;

   public:

      lightcone()
         : _is_set( false )
      {
         set_simulation( NULL );
      }

      lightcone( tao::simulation<real_type>* )
         : _is_set( false )
      {
         set_simulation( NULL );
      }

      void
      set_simulation( tao::simulation<real_type>* sim )
      {
         _sim = sim;

         // Setting the simulation requires recalculation of
         // the dependant parts of the lightcone.
         _recalc();
      }

      void
      set_geometry( real_type ra_min,
                    real_type ra_max,
                    real_type dec_min,
                    real_type dec_max,
                    real_type z_max,
                    real_type z_min = 0,
                    optional<real_type> ra_ori = optional<real_type>(),
                    optional<real_type> dec_ori = optional<real_type>() )
      {
         // Check values make sense.
         ASSERT( ra_min >= 0.0 && ra_min <= 90.0,
                 "Minimum RA cannot be less than zero or greater than 90 degrees." );
         ASSERT( ra_max >= 0.0 && ra_max <= 90.0,
                 "Maximum RA cannot be less than zero or greater than 90 degrees." );
         ASSERT( ra_min < ra_max,
                 "Minimum RA must be less than maximum RA." );
         ASSERT( dec_min >= 0.0 && dec_min <= 90.0,
                 "Minimum DEC cannot be less than zero or greater than 90 degrees." );
         ASSERT( dec_max >= 0.0 && dec_max <= 90.0,
                 "Maximum DEC cannot be less than zero or greater than 90 degrees." );
         ASSERT( dec_min < dec_max,
                 "Minimum DEC must be less than maximum DEC." );
         ASSERT( z_min >= 0.0,
                 "Minimum redshift must be greater than or equal to zero." );
         ASSERT( z_min < z_max,
                 "Minimum redshift must be less than maximum redshift." );

         // Set values.
         _ra[0] = to_radians( ra_min );
         _ra[1] = to_radians( ra_max );
         _dec[0] = to_radians( dec_min );
         _dec[1] = to_radians( dec_max );
         _ori[0] = ra_ori.get_value_or( 0.5*(_ra[0] + _ra[1]) );
         _ori[1] = dec_ori.get_value_or( 0.5*(_dec[0] + _dec[1]) );
         _z[0] = z_min;
         _z[1] = z_max;
         _is_set = true;
         _recalc();
      }

      const tao::simulation<real_type>&
      simulation() const
      {
         ASSERT( _sim, "No simulation set." );
         return *_sim;
      }

      box_iterator
      box_begin()
      {
         if( _is_set )
            return box_iterator( *this, false );
         else
            return box_end();
      }

      box_iterator
      box_end()
      {
         return box_iterator( *this, true );
      }

   protected:

      void
      _recalc()
      {
         if( _is_set )
         {
            ASSERT( _sim, "No simulation set." );
            _dist[0] = numerics::redshift_to_comoving_distance( _z[0], 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
            _dist[1] = numerics::redshift_to_comoving_distance( _z[1], 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
         }
      }

   protected:

      tao::simulation<real_type>* _sim;
      array<real_type,2> _ra;
      array<real_type,2> _dec;
      array<real_type,2> _ori;
      array<real_type,2> _z;
      array<real_type,2> _dist;
      bool _is_set;
   };

   template< class T >
   class lightcone_box_iterator
      : public boost::iterator_facade< lightcone_box_iterator<T>,
                                       box<T>,
				       std::forward_iterator_tag,
                                       box<T> >
   {
      friend class boost::iterator_core_access;

   public:

      typedef T real_type;
      typedef box<real_type> value_type;
      typedef value_type reference_type;

      enum check_result
      {
         BELOW,
         ABOVE,
         ON
      };

   public:

      lightcone_box_iterator( lightcone<real_type>& lc,
                              bool done )
         : _lc( lc ),
           _done( done )
      {
         std::fill( _cur.begin(), _cur.end(), 0 );
         if( _check() != ON )
            increment();
      }

   protected:

      void
      increment()
      {
         real_type bs = _lc.simulation().box_size();
         check_result res;
         do {
            do {
               do
               {
                  _cur[2] += bs;
                  res = _check();
                  if( res == ON )
                     return;
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
      equal( const lightcone_box_iterator& op ) const
      {
         return _done == op._done;
      }

      reference_type
      dereference() const
      {
         return box<real_type>( _lc, _cur );
      }

      check_result
      _check()
      {
         real_type bs = _lc._sim->box_size();

         // Check that the farthest corner of the box is greater than the
         // minimum distance.
         if( sqrt( pow( _cur[0] + bs, 2.0 ) + 
                   pow( _cur[1] + bs, 2.0 ) + 
                   pow( _cur[2] + bs, 2.0 ) ) < _lc._dist[0] )
         {
            return BELOW;
         }

         // Check that the closest corner of the box is less than the
         // maximum distance.
         if( sqrt( pow( _cur[0], 2.0 ) + 
                   pow( _cur[1], 2.0 ) + 
                   pow( _cur[2], 2.0 ) ) > _lc._dist[1] )
         {
            return ABOVE;
         }

         // We can check lower RA and DEC bounds by converting the (0, 1, 0)
         // vertex of the cube to ECS coordinates.
         real_type ra, dec;
         numerics::cartesian_to_ecs( _cur[0], _cur[1] + bs, _cur[2], ra, dec );
         if( ra < _lc._ra[0] )
            return BELOW;

         // Similarly, we check the upper bounds by converting the (1, 0, 0)
         // vertex of the cube to ECS coordinates.
         numerics::cartesian_to_ecs( _cur[0] + bs, _cur[1], _cur[2], ra, dec );
         if( ra > _lc._ra[1] )
            return ABOVE;

         // Similarly, we check the upper bounds by converting the (1, 0, 0)
         // vertex of the cube to ECS coordinates.
         numerics::cartesian_to_ecs( _cur[0], _cur[1], _cur[2] + bs, ra, dec );
         if( dec < _lc._dec[0] )
            return BELOW;

         // We can check lower RA and DEC bounds by converting the (0, 1, 0)
         // vertex of the cube to ECS coordinates.
         numerics::cartesian_to_ecs( _cur[0] + bs, _cur[1] + bs, _cur[2], ra, dec );
         if( dec > _lc._dec[1] )
            return ABOVE;

         // If we get here this box is in overlap.
         return ON;
      }

   protected:

      lightcone<real_type>& _lc;
      array<real_type,3> _cur;
      bool _done;
   };

}

#endif
