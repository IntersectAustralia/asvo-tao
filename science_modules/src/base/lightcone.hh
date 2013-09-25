#ifndef tao_base_lightcone_hh
#define tao_base_lightcone_hh

#include "simulation.hh"
#include "tile.hh"
#include "filter.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone_tile_iterator;

   ///
   /// Lightcone representation. Describes the geometry of a lightcone,
   /// including redshift distance mappings.
   ///
   template< class T >
   class lightcone
   {
      friend lightcone_tile_iterator<T>;

   public:

      typedef T real_type;
      typedef lightcone_tile_iterator<real_type> tile_iterator;

   public:

      lightcone( const tao::simulation<real_type>* sim = NULL )
         : _sim( NULL )
      {
         set_geometry( 0, 10, 0, 10, 0.06 );
         set_simulation( sim );
      }

      void
      set_simulation( const tao::simulation<real_type>* sim )
      {
         _sim = sim;
         _recalc();
      }

      void
      set_geometry( real_type ra_min,
                    real_type ra_max,
                    real_type dec_min,
                    real_type dec_max,
                    real_type z_max,
                    real_type z_min = 0 )
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

      const tao::simulation<real_type>*
      simulation() const
      {
         return _sim;
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

      tile_iterator
      tile_begin() const
      {
         return tile_iterator( *this );
      }

      tile_iterator
      tile_end() const
      {
         return tile_iterator();
      }

      template< class Backend >
      typename Backend::lightcone_galaxy_iterator
      galaxy_begin( query<real_type>& qry,
                    Backend& be,
                    tao::batch<real_type>* bat = 0,
                    filter const* filt = 0 )
      {
        return be.galaxy_begin( qry, *this, bat, filt );
      }

      template< class Backend >
      typename Backend::lightcone_galaxy_iterator
      galaxy_end( query<real_type>& qry,
                  Backend& be )
      {
         return be.galaxy_end( qry, *this );
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
         return _dist_bins;
      }

      const typename vector<real_type>::view
      distance_bins() const
      {
         return _dist_bins;
      }

      real_type
      distance_to_redshift( real_type dist ) const
      {
         return _dist_to_z[dist];
      }

   protected:

      void
      _recalc()
      {
         if( _sim )
         {
            LOGDLN( "Recalculating lightcone information.", setindent( 2 ) );

            _dist[0] = numerics::redshift_to_comoving_distance( _z[0], 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
            _dist[1] = numerics::redshift_to_comoving_distance( _z[1], 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );

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

<<<<<<< HEAD
	    // The distances I've calculated are all in Mpc. I really want them in Mpc/h.
	    std::transform( _dist_bins.begin(), _dist_bins.end(),
			    [this]( real_type d ) { d/this->_sim->h() } );

	    // Log to debugging stream.
=======
>>>>>>> fa30c41d3e1396b50c914895c470a5b76f7d228f
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
                  dists[ii] = numerics::redshift_to_comoving_distance( zs[ii], 1000, _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
               }

               // Transfer to interpolator.
               _dist_to_z.set_abscissa( dists );
               _dist_to_z.set_values( zs );
            }

            LOGD( setindent( -2 ) );
         }
      }

   protected:

      const tao::simulation<real_type>* _sim;
      array<real_type,2> _ra;
      array<real_type,2> _dec;
      array<real_type,2> _z;
      array<real_type,2> _dist;
      vector<real_type> _dist_bins;
      vector<unsigned> _snap_bins;
      numerics::interp<real_type> _dist_to_z;
   };

}

#endif
