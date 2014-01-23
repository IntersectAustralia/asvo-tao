#ifndef tao_base_lightcone_hh
#define tao_base_lightcone_hh

#include "simulation.hh"
#include "filter.hh"
#include "query.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone_tile_iterator;

   ///
   /// Lightcone representation. Describes the geometry of a lightcone,
   /// including redshift distance mappings.
   ///
   class lightcone
   {
      friend lightcone_tile_iterator<real_type>;

   public:

      typedef lightcone_tile_iterator<real_type> tile_iterator;

   public:

      ///
      /// Constructor.
      /// @param[in] sim  Simulation for the lightcone.
      ///
      lightcone( tao::simulation<real_type> const* sim = nullptr );

      ///
      /// Set lightcone simulation.
      /// @param[in] sim  Simulation for the lightcone.
      ///
      void
      set_simulation( tao::simulation<real_type> const* sim );

      ///
      /// Get lightcone simulation.
      /// @returns Simulation.
      ///
      tao::simulation<real_type> const*
      simulation() const;

      ///
      /// Set lightcone geometry.
      /// @param[in] ra_min  Minimum right-ascension.
      /// @param[in] ra_max  Maximum right-ascension.
      /// @param[in] dec_min  Minimum declination.
      /// @param[in] dec_max  Maximum declination.
      /// @param[in] z_min  Minimum redshift.
      /// @param[in] z_max  Maximum redshift.
      ///
      void
      set_geometry( real_type ra_min,
                    real_type ra_max,
                    real_type dec_min,
                    real_type dec_max,
                    real_type z_max,
                    real_type z_min = 0 );

      void
      set_min_ra( real_type ra_min );

      void
      set_max_ra( real_type ra_max );

      void
      set_min_dec( real_type dec_min );

      void
      set_max_dec( real_type dec_max );

      void
      set_min_redshift( real_type z_min );

      void
      set_max_redshift( real_type z_max );

      real_type
      min_ra() const;

      real_type
      max_ra() const;

      real_type
      min_dec() const;

      real_type
      max_dec() const;

      real_type
      min_redshift() const;

      real_type
      max_redshift() const;

      real_type
      min_dist() const;

      real_type
      max_dist() const;

      ///
      /// Set randomised lightcone. Lightcones will pass through a
      /// number of tiles, typically. These tiles can be optionally
      /// randomly rotated and shifted.
      /// @param[in] rand  Flag indicating randomness on or off.
      /// @param[in] engine  The random engine to use.
      ///
      void
      set_random( bool rand,
		  engine_type* engine = &hpc::engine );

      ///
      /// Get lightcone random state.
      /// @returns Lightcone random state.
      ///
      bool
      random() const;

      ///
      /// Set viewing inclination angle. This angle decides an right-
      /// ascension offset used in calculating unique cones.
      /// @param[in] angle  Viewing offset angle.
      ///
      void
      set_viewing_angle( real_type angle );

      ///
      /// Get viewing angle.
      /// @returns Viewing inclination angle.
      ///
      real_type
      viewing_angle() const;

      ///
      /// Set lightcone origin.
      /// @param orig  Lightcone origin.
      ///
      void
      set_origin( std::array<real_type,3> const& orig );

      ///
      /// Get lightcone origin.
      /// @returns Lightcone origin.
      ///
      std::array<real_type,3> const&
      origin() const;

      tile_iterator
      tile_begin() const;

      tile_iterator
      tile_end() const;

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

      typename vector<unsigned>::view const
      snapshot_bins() const;

      typename vector<real_type>::view const
      distance_bins() const;

      real_type
      distance_to_redshift( real_type dist ) const;

      engine_type*
      rng_engine() const;

   protected:

      void
      _recalc();

   protected:

      const tao::simulation<real_type>* _sim;
      array<real_type,2> _ra;
      array<real_type,2> _dec;
      array<real_type,2> _z;
      array<real_type,2> _dist;
      vector<real_type> _dist_bins;
      vector<unsigned> _snap_bins;
      numerics::interp<real_type> _dist_to_z;
      bool _rand;
      real_type _view_angle;
      std::array<real_type,3> _orig;
      engine_type* _eng;
   };

}

#endif
