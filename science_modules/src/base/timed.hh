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

      profile::timer::handle
      timer_start( profile::timer::handle::stop_type stop = profile::timer::handle::NORMAL );

      profile::timer::handle
      db_timer_start( profile::timer::handle::stop_type stop = profile::timer::handle::NORMAL );

      double
      time() const;

      double
      db_time() const;

   protected:

      profile::timer::handle
      _timer_start( profile::timer* timer,
                    profile::timer::handle::stop_type stop );

      profile::timer::handle
      _db_timer_start( profile::timer* timer,
                       profile::timer::handle::stop_type stop );

   protected:

      profile::timer* _db_timer;
      profile::timer* _timer;
   };

}

#endif
