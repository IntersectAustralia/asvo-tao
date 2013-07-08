#ifndef tao_base_lightcone_hh
#define tao_base_lightcone_hh

#include "simulation.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone
   {
   public:

      typedef T real_type;

   public:

      lightcone()
         : _is_set( false )
      {
         set_simulation( NULL );
      }

      void
      set_simulation( simulation<real_type>* sim )
      {
         if( sim )
            _sim = sim;
         else
            _sim = new simulation<real_type>();

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
         _ra[0] = ra_min;
         _ra[1] = ra_max;
         _dec[0] = dec_min;
         _dec[1] = dec_max;
         _ori[0] = ra_ori.get_value_or( 0.5*(_ra[0] + _ra[1]) );
         _ori[1] = dec_ori.get_value_or( 0.5*(_dec[0] + _dec[1]) );
         _z[0] = z_min;
         _z[1] = z_max;
         _is_set = true;
         _recalc();
      }

      const simulation<real_type>&
      simulation() const
      {
         return *_sim;
      }

   protected:

      void
      _recalc()
      {
         if( _is_set )
         {
            _dist[0] = numerics::redshift_to_comoving( _z[0], _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
            _dist[1] = numerics::redshift_to_comoving( _z[1], _sim->hubble(), _sim->omega_l(), _sim->omega_m() );
         }
      }

   protected:

      shared_ptr<simulation<real_type>> _sim;
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
                                       const array<T,3>&,
				       std::forward_iterator_tag >
   {
      friend class boost::iterator_core_access;

   public:

      typedef T real_type;
      typedef const array<real_type,3>& value_type;
      typedef value_type reference_type;

      lightcone_box_iterator()
      {
         std::fill( _cur.begin(), _cur.end(), 0 );
         _settle();
      }

   protected:

      void
      increment()
      {
	 ++_it;
      }

      bool
      _check()
      {
         real_type bs = _sim->box_size();

         // Check that the farthest corner of the box is greater than the
         // minimum distance.
         if( sqrt( pow( _cur[0] + bs, 2.0 ) + 
                   pow( _cur[1] + bs, 2.0 ) + 
                   pow( _cur[2] + bs, 2.0 ) ) < _dist[0] )
         {
            return false;
         }

         // 

         if( 
             (((_cur[0] + bs)/sqrt( pow( _cur[0] + bs, 2.0 ) + 
                                    pow( _cur[1], 2.0 ) )) > cos( _ra[1] )) &&
             (_cur[0]/sqrt( pow( _cur[0], 2.0 ) + pow( _cur[1] + bs, 2.0 ) ) < cos( _ra[0] )) &&
             ((sqrt( pow( _cur[0] + bs, 2.0 ) + pow( _cur[1] + bs, 2.0 )))/sqrt( pow( _cur[0] + bs +, 2.0 ) + pow( _cur[1] + bs, 2.0 ) + pow( _cur[2], 2.0 ) ) > cos( _dec[1] )) &&
             ((sqrt( pow( _cur[0], 2.0 ) + pow( _cur[1], 2.0 )))/sqrt( pow( _cur[0], 2.0 ) + pow( _cur[1], 2.0 ) + pow( _cur[2] + bs, 2.0 ) ) < cos( _dec[0] )) )
         {
         }
      }

   protected:

      array<real_type,3> _cur;
   };

}

#endif
