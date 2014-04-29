#ifndef tao_base_module_hh
#define tao_base_module_hh

#include <list>
#include <string>
#include <boost/optional.hpp>
#include <pugixml.hpp>
#include "xml_dict.hh"
#include "batch.hh"
#include "multidb.hh"
#include "types.hh"

namespace tao {

   template< class Backend >
   class module
   {
   public:

      typedef Backend backend_type;

   public:

      module( const std::string& name = std::string(),
	      pugi::xml_node base = pugi::xml_node() )
         : _name( name ),
           _init( false ),
           _base( base ),
           _dict( base ),
           _global_dict( NULL ),
           _it( 0 ),
           _complete( false )
      {
      }

      virtual
      ~module()
      {
      }

      void
      add_parent( module& parent )
      {
         LOGILN( "Adding ", parent.name(), " to ", _name, ".", setindent( 2 ) );

         // Check that we don't already have this guy.
         ASSERT( std::find( _parents.begin(), _parents.end(), &parent ) == _parents.end(),
                 "Module's cannot add duplicate parents." );

         // Add it to the list.
         _parents.push_back( &parent );

         LOGILN( "Done.", setindent( -2 ) );
      }

      std::list<module*>&
      parents()
      {
         return _parents;
      }

      void
      process( unsigned long long iteration )
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

      virtual
      void
      initialise( const xml_dict& global_dict )
      {
         // Don't initialise if we're already doing so.
         if( _init )
            return;

         // Flag myself as having commenced initialisation.
         _init = true;
         _complete = false;

         // Initialise parents first.
         for( auto par : _parents )
            par->initialise( global_dict );

         // Store global dictionary.
         _global_dict = &global_dict;

         // Reset the iteration.
         _it = 0;
      }

      virtual
      void
      execute() = 0;

      virtual
      void
      finalise()
      {
      }

      virtual
      tao::batch<real_type>&
      batch()
      {
         // By default return the first parent.
         ASSERT( !_parents.empty(), "Cannot get batch of non-existant parent." );
         return _parents.front()->batch();
      }

      virtual
      backend_type*
      backend()
      {
         return 0;
      }

      virtual
      boost::optional<boost::any>
      find_attribute( const std::string& name )
      {
         // By default pass on to parents.
         for( auto par : _parents )
         {
            auto res = par->find_attribute( name );
            if( res )
               return res;
         }
         return boost::none;
      }

      template< class T >
      T
      attribute( const std::string& name )
      {
         auto res = find_attribute( name );
         EXCEPT( res, "Failed to locate attribute on module chain with name: ", name );
         return boost::any_cast<T>( *res );
      }

      virtual
      void
      log_metrics()
      {
         // LOGILN( _name, " runtime: ", time(), " (s)" );
         // LOGILN( _name, " db time: ", db_time(), " (s)" );
      }

      bool
      complete() const
      {
         return _complete;
      }

      const std::string&
      name() const
      {
         return _name;
      }

      const xml_dict&
      local_dict() const
      {
         return _dict;
      }

      pugi::xml_node
      local_xml_node()
      {
         return _base;
      }

   protected:

      std::string _name;
      unsigned long long _it;
      bool _init;
      std::list<module*> _parents;
      bool _complete;

      pugi::xml_node _base;
      const xml_dict _dict;
      const xml_dict* _global_dict;
   };

}

#endif
