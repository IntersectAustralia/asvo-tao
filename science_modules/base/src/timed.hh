#ifndef tao_base_timed_hh
#define tao_base_timed_hh

#include <libhpc/profile/timer.hh>

namespace tao {
   using namespace hpc;

   ///
   ///
   ///
   class timed
   {
   public:

      timed( profile::timer* timer = NULL,
             profile::timer* db_timer = NULL );

      void
      set_timer( profile::timer* timer );

      void
      set_db_timer( profile::timer* timer );

      void
      timer_start();

      void
      timer_stop();

      void
      db_timer_start();

      void
      db_timer_stop();

      double
      time() const;

      double
      db_time() const;

   protected:

      void
      _timer_start( profile::timer* timer );

      void
      _timer_stop( profile::timer* timer );

   protected:

      profile::timer* _db_timer;
      profile::timer* _timer;
   };

}

#endif
