#include "lightcone.hh"
#include "lightcone_tile_iterator.hh"

namespace tao {

   lightcone::lightcone( const tao::simulation* sim )
      : _sim( NULL ),
        _rand( false ),
        _view_angle( 0.0 ),
        _orig{ { 0.0, 0.0, 0.0 } },
        _sng_snap( false ),
        _snap( 0 ),
        _eng( &hpc::engine )
        {
           set_geometry( 0, 10, 0, 10, 0.06 );
           set_simulation( sim );
        }

   void
   lightcone::set_simulation( const tao::simulation* sim )
   {
      _sim = sim;
      _recalc();
   }

   void
   lightcone::set_geometry( real_type ra_min,
                            real_type ra_max,
                            real_type dec_min,
                            real_type dec_max,
                            real_type z_max,
                            real_type z_min )
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
      _z[0] = z_min;
      _z[1] = z_max;
      _recalc();
   }

   void
   lightcone::set_random( bool rand,
                          engine_type* engine )
   {
      _rand = rand;
      _eng = engine;
   }

   void
   lightcone::set_viewing_angle( real_type angle )
   {
      _view_angle = angle;
   }

   real_type
   lightcone::viewing_angle() const
   {
      return _view_angle;
   }

   void
   lightcone::set_origin( std::array<real_type,3> const& orig )
   {
      _orig = orig;
   }

   std::array<real_type,3> const&
   lightcone::origin() const
   {
      return _orig;
   }

   void
   lightcone::set_single_snapshot( bool state )
   {
      _sng_snap = state;
   }

   bool
   lightcone::single_snapshot() const
   {
      return _sng_snap;
   }

   void
   lightcone::set_snapshot( unsigned snap )
   {
      _snap = snap;
   }

   unsigned
   lightcone::snapshot() const
   {
      return _snap;
   }

   const tao::simulation*
   lightcone::simulation() const
   {
      return _sim;
   }

   void
   lightcone::set_min_ra( real_type ra_min )
   {
      ASSERT( ra_min >= 0.0 && ra_min <= 90.0,
              "Minimum RA cannot be less than zero or greater than 90 degrees." );
      ASSERT( to_radians( ra_min ) < _ra[1],
              "Minimum RA must be less than maximum RA." );
      _ra[0] = to_radians( ra_min );
      _recalc();
   }

   void
   lightcone::set_max_ra( real_type ra_max )
   {
      ASSERT( ra_max >= 0.0 && ra_max <= 90.0,
              "Maximum RA cannot be less than zero or greater than 90 degrees." );
      ASSERT( to_radians( ra_max ) > _ra[0],
              "Minimum RA must be less than maximum RA." );
      _ra[1] = to_radians( ra_max );
      _recalc();
   }

   void
   lightcone::set_min_dec( real_type dec_min )
   {
      ASSERT( dec_min >= 0.0 && dec_min <= 90.0,
              "Minimum DEC cannot be less than zero or greater than 90 degrees." );
      ASSERT( to_radians( dec_min ) < _dec[1],
              "Minimum DEC must be less than maximum DEC." );
      _dec[0] = to_radians( dec_min );
      _recalc();
   }

   void
   lightcone::set_max_dec( real_type dec_max )
   {
      ASSERT( dec_max >= 0.0 && dec_max <= 90.0,
              "Maximum DEC cannot be less than zero or greater than 90 degrees." );
      ASSERT( to_radians( dec_max ) > _dec[0],
              "Minimum DEC must be less than maximum DEC." );
      _dec[1] = to_radians( dec_max );
      _recalc();
   }

   void
   lightcone::set_min_redshift( real_type z_min )
   {
      ASSERT( z_min >= 0.0,
              "Minimum redshift must be greater than or equal to zero." );
      ASSERT( z_min < _z[1],
              "Minimum redshift must be less than maximum redshift." );
      _z[0] = z_min;
      _recalc();
   }

   void
   lightcone::set_max_redshift( real_type z_max )
   {
      ASSERT( _z[0] < z_max,
              "Minimum redshift must be less than maximum redshift." );
      _z[1] = z_max;
      _recalc();
   }

   lightcone::tile_iterator
   lightcone::tile_begin() const
   {
      return tile_iterator( *this );
   }

   lightcone::tile_iterator
   lightcone::tile_end() const
   {
      return tile_iterator();
   }

   real_type
   lightcone::min_ra() const
   {
      return _ra[0];
   }

   real_type
   lightcone::max_ra() const
   {
      return _ra[1];
   }

   real_type
   lightcone::min_dec() const
   {
      return _dec[0];
   }

   real_type
   lightcone::max_dec() const
   {
      return _dec[1];
   }

   real_type
   lightcone::min_redshift() const
   {
      return _z[0];
   }

   real_type
   lightcone::max_redshift() const
   {
      return _z[1];
   }

   real_type
   lightcone::min_dist() const
   {
      return _dist[0];
   }

   real_type
   lightcone::max_dist() const
   {
      return _dist[1];
   }

   const typename vector<unsigned>::view
   lightcone::snapshot_bins() const
   {
      return _snap_bins;
   }

   const typename vector<real_type>::view
   lightcone::distance_bins() const
   {
      return _dist_bins;
   }

   real_type
   lightcone::distance_to_redshift( real_type dist ) const
   {
      return _dist_to_z[dist];
   }

   bool
   lightcone::random() const
   {
      return _rand;
   }

   engine_type*
   lightcone::rng_engine() const
   {
      return _eng;
   }

   void
   lightcone::_recalc()
   {
      if( _sim )
      {
         LOGDLN( "Recalculating lightcone information.", setindent( 2 ) );

         _dist[0] = numerics::redshift_to_comoving_distance( _z[0], 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() )*_sim->h();
         _dist[1] = numerics::redshift_to_comoving_distance( _z[1], 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() )*_sim->h();
         LOGDLN( "Distance range: [", _dist[0], ", ", _dist[1], ")" );

         // Prepare the redshift distance bins. Note that I will incorporate the
         // minimum and maximum redshift here. First calculate the
         // number of bins in the redshift range.
         _dist_bins.deallocate();
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
         _dist_bins.reallocate( last - first + 1 );
         _snap_bins.reallocate( last - first );
         _dist_bins.back() = numerics::redshift_to_comoving_distance( std::min( _sim->redshift( 0 ), _z[0] ), 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
         _dist_bins.front() = numerics::redshift_to_comoving_distance( std::max( _sim->redshift( _sim->num_snapshots() - 1 ), _z[1] ), 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
         for( unsigned ii = 1; ii < _dist_bins.size() - 1; ++ii )
            _dist_bins[ii] = numerics::redshift_to_comoving_distance( _sim->redshift( first + ii - 1 ), 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
         for( unsigned ii = 0; ii < _snap_bins.size(); ++ii )
            _snap_bins[ii] = first + ii;

         // The distances I've calculated are all in Mpc. I really want them in Mpc/h.
         std::transform( _dist_bins.begin(), _dist_bins.end(), _dist_bins.begin(),
                         [this]( real_type d ) { return d*this->_sim->h(); } );

         // Log to debugging stream.
         LOGDLN( "Distance bins: ", _dist_bins );
         LOGDLN( "Snapshot bins: ", _snap_bins );

         // Build the distance to redshift interpolator.
         {
            // How many points do I need?
            unsigned num_points = std::max<unsigned>( (unsigned)((_z[1] - _z[0])/0.001), 2 );

            // Setup arrays.
            vector<real_type> dists( num_points );
            vector<real_type> zs( num_points );
            for( unsigned ii = 0; ii < num_points; ++ii )
            {
               zs[ii] = _z[0] + (_z[1] - _z[0])*((real_type)ii/(real_type)(num_points - 1));
               dists[ii] = numerics::redshift_to_comoving_distance( zs[ii], 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() )*_sim->h(); // don't forget to put in Mpc/h
            }

            // Transfer to interpolator.
            _dist_to_z.set_abscissa( dists );
            _dist_to_z.set_values( zs );
         }

         LOGD( setindent( -2 ) );
      }
   }

}
