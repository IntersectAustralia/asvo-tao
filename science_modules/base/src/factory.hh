#ifndef tao_base_factory_hh
#define tao_base_factory_hh

#include <boost/iterator/transform_iterator.hpp>
#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include "galaxy.hh"
#include "module.hh"

namespace tao {
   using namespace hpc;

   class factory_type;

   extern factory_type factory;

   class factory_type
   {
   public:

      typedef module* (*factory_create_type)( const string& name );
      typedef list<module*>::iterator iterator;

   public:

      factory_type();

      ~factory_type();

      void
      register_module( const string& name,
                       factory_create_type create );

      module&
      create_module( const string& name,
                     const string& inst_name = string() );

      iterator
      begin();

      iterator
      end();

      module*
      operator[]( const string& name );

   protected:

      map<string,factory_create_type> _facs;
      list<module*> _mods;
   };

}

#endif
