#include "timed.hh"

using namespace hpc;

namespace tao {

   timed::timed( profile::timer* timer,
                 profile::timer* db_timer )
      : _timer( timer ),
        _db_timer( db_timer )
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

   profile::timer::handle
   timed::timer_start( profile::timer::handle::stop_type stop )
   {
      return _timer_start( _timer, stop );
   }

   profile::timer::handle
   timed::db_timer_start( profile::timer::handle::stop_type stop )
   {
      return _timer_start( _db_timer, stop );
   }

   double
   timed::time() const
   {
      return _timer->total();
   }

   double
   timed::db_time() const
   {
      return _db_timer->total();
   }

   profile::timer::handle
   timed::_timer_start( profile::timer* timer,
                        profile::timer::handle::stop_type stop )
   {
      if( timer )
         return timer->start( stop );
      else
         return profile::timer::handle();
   }

}
