#ifndef tao_base_module_hh
#define tao_base_module_hh

#include <pugixml.hpp>
#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include <libhpc/options/xml_dict.hh>
#include "galaxy.hh"
#include "multidb.hh"

namespace tao {
   using namespace hpc;

   class module
   {
   public:

      typedef double real_type;

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
      tao::galaxy&
      galaxy();

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

      double
      time() const;

      double
      db_time() const;

   protected:

      void
      _read_db_options( const options::xml_dict& global_dict );

      void
      _db_connect();

      void
      _db_disconnect();

      bool
      _db_cycle();

   protected:

      string _name;
      unsigned long long _it;
      list<module*> _parents;
      bool _complete;

      pugi::xml_node _base;
      const options::xml_dict _dict;
      const options::xml_dict* _global_dict;
      bool _connected;
#ifdef MULTIDB
      multidb* _db;
#else
      soci::session _sql;
#endif
      unsigned _num_restart_its;
      unsigned _cur_restart_it;
      string _dbtype, _dbname, _dbhost, _dbport, _dbuser, _dbpass;
      string _tree_pre;
      unsigned _batch_size;

      profile::timer _timer;
      profile::timer _db_timer;
   };

}

#endif
