#include "module.hh"

using namespace hpc;

namespace tao {

   module::module( const string& name,
		   pugi::xml_node base )
      : timed(),
        _name( name ),
	_base( base ),
	_dict( base ),
	_global_dict( NULL ),
        _it( 0 )
   {
      set_timer( &_my_timer );
      set_db_timer( &_my_db_timer );
   }

   module::~module()
   {
   }

   void
   module::add_parent( module& parent )
   {
      LOGILN( "Adding ", parent.name(), " to ", _name, ".", setindent( 2 ) );

      // Check that we don't already have this guy.
      ASSERT( std::find( _parents.begin(), _parents.end(), &parent ) == _parents.end(),
              "Module's cannot add duplicate parents." );

      // Add it to the list.
      _parents.push_back( &parent );

      LOGILN( "Done.", setindent( -2 ) );
   }

   list<module*>&
   module::parents()
   {
      return _parents;
   }

   void
   module::process( unsigned long long iteration )
   {
      // Iteration should never be lower than my current.
      ASSERT( iteration >= _it );

      // If we have not already processed this round, launch
      // the execute routine.
      if( iteration > _it )
      {
         // Should only ever be greater by one.
         ASSERT( iteration == _it + 1 );

         // Process all parents.
         bool all_complete = !_parents.empty();
         for( auto& parent : _parents )
         {
            parent->process( iteration );
            if( !parent->complete() )
               all_complete = false;
         }

         // Call the user-defined execute routine.
         if( !all_complete )
            execute();
         else
         {
            LOGDLN( "Module ", _name, ": All parents are complete, marking myself as complete." );
            _complete = true;
         }

         // Update my iteration counter.
         _it = iteration;
      }
   }

   void
   module::initialise( const options::xml_dict& global_dict )
   {
      // Store global dictionary.
      _global_dict = &global_dict;

      // Reset timers.
      _my_timer.reset();
      _my_db_timer.reset();

      // Reset the iteration.
      _it = 0;
   }

   void
   module::finalise()
   {
   }

   tao::batch<real_type>&
   module::batch()
   {
      // By default return the first parent.
      ASSERT( !_parents.empty(), "Cannot get batch of non-existant parent." );
      return _parents.front()->batch();
   }

   void
   module::log_metrics()
   {
      LOGILN( _name, " runtime: ", time(), " (s)" );
      LOGILN( _name, " db time: ", db_time(), " (s)" );
   }

   bool
   module::complete() const
   {
      return _complete;
   }

   const string&
   module::name() const
   {
      return _name;
   }

   const options::xml_dict&
   module::local_dict() const
   {
      return _dict;
   }

   pugi::xml_node
   module::local_xml_node()
   {
      return _base;
   }

}
