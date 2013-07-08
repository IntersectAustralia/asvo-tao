#ifndef tao_base_simulation_hh
#define tao_base_simulation_hh

namespace tao {
   using namespace hpc;

   template< class T >
   class simulation
   {
   public:

      typedef T real_type;

   public:

      simulation()
         : _box_size( 500 )
      {
         set_cosmology( 73, 0.25, 0.75 );
      }

      void
      set_cosmology( real_type hubble,
                     real_type omega_m,
                     real_type omega_l )
      {
         _hubble = hubble;
         _h = _hubble/100;
         _omega_m = omega_m;
         _omega_l = omega_l;
         _omega_r = 4.165e-5/(_h*_h);
         _omega_k = 1 - _omega_m - _omega_l - _omega_r;
      }

   protected:

      real_type _box_size;
      real_type _hubble;
      real_type _h;
      real_type _omega_m;
      real_type _omega_l;
      real_type _omega_r;
      real_type _omega_k;
   };

}

#endif
