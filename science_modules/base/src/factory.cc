#include "factory.hh"

namespace tao {
   using namespace hpc;

   factory_type factory;

   factory_type::factory_type()
   {
   }

   void
   factory_type::register_module( const string& name,
                                  factory_create_type create )
   {
      ASSERT( !_facs.has( name ), "Science module name already exists." );
      _facs.insert( name, create );
   }

   module&
   factory_type::create_module( const string& name,
                                const string& inst_name )
   {
      string _in;
      if( inst_name.empty() )
         _in = name;
      else
         _in = inst_name;
#ifndef NDEBUG
      for( auto mod : _mods )
         ASSERT( mod->name() != _in, "Module with that instance name already exists." );
#endif
      module* mod = _facs.get( name )( _in );
      _mods.push_back( mod );
      LOGDLN( "Created module ", name, " with name ", inst_name );
      return *mod;
   }

   factory_type::iterator
   factory_type::begin()
   {
      return _mods.begin();
   }

   factory_type::iterator
   factory_type::end()
   {
      return _mods.end();
   }

   module*
   factory_type::operator[]( const string& name )
   {
      for( auto mod : _mods )
      {
         if( mod->name() == name )
            return mod;
      }
      ASSERT( 0 );
   }

}
