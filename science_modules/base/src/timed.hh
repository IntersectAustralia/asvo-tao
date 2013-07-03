#ifndef tao_base_timed_hh
#define tao_base_timed_hh

namespace tao {
   using namespace hpc;

   ///
   /// Star-formation History. Responsible for rebinning star-formation
   /// history data into appropriate time bins.
   ///
   class timed
   {
   public:

      timed();

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
