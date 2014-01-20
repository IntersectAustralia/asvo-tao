#ifndef tao_base_factory_hh
#define tao_base_factory_hh

#include <boost/iterator/transform_iterator.hpp>
#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include "module.hh"

namespace tao {
   using namespace hpc;

   template< class Backend >
   class factory
   {
   public:

      typedef Backend backend_type;
      typedef module<backend_type> module_type;
      typedef module_type* (*factory_create_type)( const string& name, 
                                                   pugi::xml_node base );
      typedef typename list<module_type*>::iterator iterator;

   public:

      factory()
      {
      }

      ~factory()
      {
         for( auto mod : _mods )
            delete mod;
      }

      void
      register_module( const string& name,
                       factory_create_type create )
      {
         EXCEPT( !_facs.has( name ), "Cannot add new science module factory, ID already exists: ", name );
         _facs.insert( name, create );
      }

      module_type&
      create_module( const string& name,
                     const string& inst_name = string(),
		     pugi::xml_node base = (pugi::xml_node)0 )
      {
         string _in;
         if( inst_name.empty() )
            _in = name;
         else
            _in = inst_name;
#ifndef NEXCEPT
         for( auto mod : _mods )
            EXCEPT( mod->name() != _in, "Science module with name already exists: ", _in );
#endif
         EXCEPT( _facs.has( name ), "No science module exists with ID: ", name );
         module_type* mod = _facs.get( name )( _in, base );
         _mods.push_back( mod );
         LOGDLN( "Created module ", name, " with name ", _in );
         return *mod;
      }

      iterator
      begin()
      {
         return _mods.begin();
      }

      iterator
      end()
      {
         return _mods.end();
      }

      module_type*
      operator[]( const string& name )
      {
         for( auto mod : _mods )
         {
            if( mod->name() == name )
               return mod;
         }
         ASSERT( 0 );
      }

   protected:

      map<string,factory_create_type> _facs;
      list<module_type*> _mods;
   };

}

#endif
