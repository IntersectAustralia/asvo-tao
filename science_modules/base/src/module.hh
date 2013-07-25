#ifndef tao_base_module_hh
#define tao_base_module_hh

#include <pugixml.hpp>
#include <libhpc/options/xml_dict.hh>
#include "batch.hh"
#include "multidb.hh"
#include "timed.hh"
#include "types.hh"

namespace tao {
   using namespace hpc;

   class module
      : public timed
   {
   public:

      module( const string& name = string(),
	      pugi::xml_node base = pugi::xml_node() );

      virtual
      ~module();

      void
      add_parent( module& parent );

      list<module*>&
      parents();

      void
      process( unsigned long long iteration );

      virtual
      void
      initialise( const options::xml_dict& global_dict );

      virtual
      void
      execute() = 0;

      virtual
      void
      finalise();

      virtual
      tao::batch<real_type>&
      batch();

      virtual
      void
      log_metrics();

      bool
      complete() const;

      const string&
      name() const;

      const options::xml_dict&
      local_dict() const;

      pugi::xml_node
      local_xml_node();

   protected:

      string _name;
      unsigned long long _it;
      list<module*> _parents;
      bool _complete;

      pugi::xml_node _base;
      const options::xml_dict _dict;
      const options::xml_dict* _global_dict;

      profile::timer _my_timer;
      profile::timer _my_db_timer;
   };

}

#endif
