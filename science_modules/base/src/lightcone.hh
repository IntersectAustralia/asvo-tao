#ifndef tao_base_lightcone_hh
#define tao_base_lightcone_hh

#include "simulation.hh"
#include "tile.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone_tile_iterator;

   template< class T >
   class lightcone
   {
      friend lightcone_tile_iterator<T>;

   public:

      typedef T real_type;
      typedef lightcone_tile_iterator<real_type> tile_iterator;

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

      void
      set_min_ra( real_type ra_min )
      {
         ASSERT( ra_min >= 0.0 && ra_min <= 90.0,
                 "Minimum RA cannot be less than zero or greater than 90 degrees." );
         ASSERT( to_radians( ra_min ) < _ra[1],
                 "Minimum RA must be less than maximum RA." );
         _ra[0] = to_radians( ra_min );
         _recalc();
      }

      void
      set_max_ra( real_type ra_max )
      {
         ASSERT( ra_max >= 0.0 && ra_max <= 90.0,
                 "Maximum RA cannot be less than zero or greater than 90 degrees." );
         ASSERT( to_radians( ra_max ) > _ra[0],
                 "Minimum RA must be less than maximum RA." );
         _ra[1] = to_radians( ra_max );
         _recalc();
      }

      void
      set_min_dec( real_type dec_min )
      {
         ASSERT( dec_min >= 0.0 && dec_min <= 90.0,
                 "Minimum DEC cannot be less than zero or greater than 90 degrees." );
         ASSERT( to_radians( dec_min ) < _dec[1],
                 "Minimum DEC must be less than maximum DEC." );
         _dec[0] = to_radians( dec_min );
         _recalc();
      }

      void
      set_max_dec( real_type dec_max )
      {
         ASSERT( dec_max >= 0.0 && dec_max <= 90.0,
                 "Maximum DEC cannot be less than zero or greater than 90 degrees." );
         ASSERT( to_radians( dec_max ) > _dec[0],
                 "Minimum DEC must be less than maximum DEC." );
         _dec[1] = to_radians( dec_max );
         _recalc();
      }

      void
      set_min_redshift( real_type z_min )
      {
         ASSERT( z_min >= 0.0,
                 "Minimum redshift must be greater than or equal to zero." );
         ASSERT( z_min < _z[1],
                 "Minimum redshift must be less than maximum redshift." );
         _z[0] = z_min;
         _recalc();
      }

      void
      set_max_redshift( real_type z_max )
      {
         ASSERT( _z[0] < z_max,
                 "Minimum redshift must be less than maximum redshift." );
         _z[1] = z_max;
         _recalc();
      }

      const tao::simulation<real_type>&
      simulation() const
      {
         ASSERT( _sim, "No simulation set." );
         return *_sim;
      }

      tile_iterator
      tile_begin()
      {
         if( _is_set )
            return tile_iterator( *this, false );
         else
            return tile_end();
      }

      tile_iterator
      tile_end()
      {
         return tile_iterator( *this, true );
      }

      real_type
      min_ra() const
      {
         return _ra[0];
      }

      real_type
      max_ra() const
      {
         return _ra[1];
      }

      real_type
      min_dec() const
      {
         return _dec[0];
      }

      real_type
      max_dec() const
      {
         return _dec[1];
      }

      real_type
      min_redshift() const
      {
         return _z[0];
      }

      real_type
      max_redshift() const
      {
         return _z[1];
      }

      real_type
      min_dist() const
      {
         return _dist[0];
      }

      real_type
      max_dist() const
      {
         return _dist[1];
      }

      const typename vector<real_type>::view
      snapshot_bins() const
      {
         return _z_bins;
      }

   protected:

      void
      _recalc()
      {
         if( _is_set )
         {
            LOGDLN( "Recalculating lightcone information.", setindent( 2 ) );

            ASSERT( _sim, "No simulation set." );
            _dist[0] = numerics::redshift_to_comoving_distance( _z[0], 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
            _dist[1] = numerics::redshift_to_comoving_distance( _z[1], 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );

            // Prepare the redshift distance bins. Note that I will incorporate the
            // minimum and maximum redshift here. First calculate the
            // number of bins in the redshift range.
            _z_bins.deallocate();
            _snap_bins.deallocate();
            unsigned first, last;
            {
               unsigned ii = 0;
               unsigned ns = _sim->num_snapshots();
               while( ii < ns && _sim->redshift( ii ) > _z[1] )
                  ++ii;
               first = ii;
               while( ii < ns && _sim->redshift( ii ) > _z[0] )
                  ++ii;
               last = ii + 1;
            }

            // Store the distances.
            _z_bins.reallocate( last - first + 1 );
            _snap_bins.reallocate( last - first );
            _z_bins.back() = numerics::redshift_to_comoving_distance( std::min( _sim->redshift( 0 ), _z[0] ), 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
            _z_bins.front() = numerics::redshift_to_comoving_distance( std::max( _sim->redshift( _sim->num_snapshots() - 1 ), _z[1] ), 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
            for( unsigned ii = 1; ii < _z_bins.size() - 1; ++ii )
               _z_bins[ii] = numerics::redshift_to_comoving_distance( _sim->redshift( first + ii - 1 ), 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
            for( unsigned ii = 0; ii < _snap_bins.size(); ++ii )
               _snap_bins[ii] = first + ii;

            LOGDLN( "Distance bins: ", _z_bins );
            LOGDLN( "Snapshot bins: ", _snap_bins );
         }
      }

   protected:

      tao::simulation<real_type>* _sim;
      array<real_type,2> _ra;
      array<real_type,2> _dec;
      array<real_type,2> _ori;
      array<real_type,2> _z;
      array<real_type,2> _dist;
      vector<real_type> _z_bins;
      vector<unsigned> _snap_bins;
      bool _is_set;
   };

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

      lightcone_tile_iterator( lightcone<real_type>& lc,
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
