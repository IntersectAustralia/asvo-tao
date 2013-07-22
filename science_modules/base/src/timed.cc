#include "timed.hh"

using namespace hpc;

namespace tao {

   timed::timed()
      : _timer( NULL ),
        _db_timer( NULL )
   {
   }

   void
   timed::set_timer( profile::timer* timer )
   {
      _timer = timer;
   }

   void
   timed::set_db_timer( profile::timer* timer )
   {
      _db_timer = timer;
   }

   void
   timed::timer_start()
   {
      _timer_start( _timer );
   }

   void
   timed::timer_stop()
   {
      _timer_stop( _timer );
   }

   void
   timed::db_timer_start()
   {
      _timer_start( _db_timer );
   }

   void
   timed::db_timer_stop()
   {
      _timer_stop( _db_timer );
   }

   void
   timed::_timer_start( profile::timer* timer )
   {
      if( timer )
         timer->start();
   }

   void
   timed::_timer_stop( profile::timer* timer )
   {
      if( timer )
         timer->stop();
   }

}
