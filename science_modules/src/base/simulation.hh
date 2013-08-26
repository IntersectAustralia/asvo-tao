#ifndef tao_base_simulation_hh
#define tao_base_simulation_hh

#include <stdarg.h>
#include <libhpc/containers/vector.hh>
#include <libhpc/logging/logging.hh>
#include "utils.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class simulation
   {
   public:

      typedef T real_type;

   public:

      simulation()
         : _box_size( 0 )
      {
      }

      simulation( real_type box_size,
                  real_type hubble,
                  real_type omega_m,
                  real_type omega_l,
                  unsigned num_snaps,
                  ... )
         : _box_size( box_size ),
           _zs( num_snaps )
      {
         set_cosmology( hubble, omega_m, omega_l );

         // Extract the expansion list and convert to redshifts.
         va_list vl;
         va_start( vl, num_snaps );
         for( unsigned ii = 0; ii < num_snaps; ++ii )
            _zs[ii] = expansion_to_redshift( va_arg( vl, real_type ) );

         // We really want these to be ordered by snapshots, and that
         // usually means oldest (largest redshifts) first.
#ifndef NDEBUG
         for( unsigned ii = 1; ii < _zs.size(); ++ii )
         {
            ASSERT( _zs[ii] < _zs[ii - 1],
                    "Expansion factor list must be supplied in snapshot order, "
                    "which must be oldest first." );
         }
#endif
      }

      void
      set_box_size( real_type box_size )
      {
         _box_size = box_size;
      }

      void
      set_cosmology( real_type hubble,
                     real_type omega_m,
                     real_type omega_l )
      {
         // LOGILN( "Setting simulation cosmology:", setindent( 2 ) );
         _hubble = hubble;
         // LOGILN( "Hubble: ", hubble );
         _h = _hubble/100;
         _omega_m = omega_m;
         // LOGILN( "Omega M: ", omega_m );
         _omega_l = omega_l;
         // LOGILN( "Omega L: ", omega_l );
         _omega_r = 4.165e-5/(_h*_h);
         // LOGILN( "Omega R: ", _omega_r );
         _omega_k = 1 - _omega_m - _omega_l - _omega_r;
         // LOGILN( "Omega K: ", _omega_k );
         // LOGILN( "Done.", setindent( -2 ) );
      }

      void
      set_snapshot_redshifts( vector<real_type>& redshifts )
      {
         _zs.deallocate();
         _zs.swap( redshifts );
      }

      real_type
      box_size() const
      {
         return _box_size;
      }

      real_type
      hubble() const
      {
         return _hubble;
      }

      real_type
      h() const
      {
         return _h;
      }

      real_type
      omega_m() const
      {
         return _omega_m;
      }

      real_type
      omega_l() const
      {
         return _omega_l;
      }

      unsigned
      num_snapshots() const
      {
         return _zs.size();
      }

      real_type
      redshift( unsigned snap ) const
      {
         return _zs[snap];
      }

      const typename vector<real_type>::view
      redshifts() const
      {
         return _zs;
      }

   protected:

      real_type _box_size;
      real_type _hubble;
      real_type _h;
      real_type _omega_m;
      real_type _omega_l;
      real_type _omega_r;
      real_type _omega_k;
      vector<real_type> _zs;
   };

}

#endif
