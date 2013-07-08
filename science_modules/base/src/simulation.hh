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

      simulation( real_type box_size = 500,
                  real_type hubble = 73,
                  real_type omega_m = 0.25,
                  real_type omega_l = 0.75 )
         : _box_size( box_size )
      {
         set_cosmology( hubble, omega_m, omega_l );
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
      omega_m() const
      {
         return _omega_m;
      }

      real_type
      omega_l() const
      {
         return _omega_l;
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
