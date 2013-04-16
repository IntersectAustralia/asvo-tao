#ifndef tao_base_module_hh
#define tao_base_module_hh

#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include "galaxy.hh"
#include <libhpc/options/xml_dict.hh>


namespace tao {
   using namespace hpc;

   class module
   {
   public:

      typedef double real_type;

   public:

      module( const string& name = string() );

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
      initialise( const options::xml_dict& dict,
                  optional<const string&> prefix = optional<const string&>() ) = 0;

      void
      initialise( const options::xml_dict& dict,
                  const char* prefix );

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

      double
      time() const;

   protected:

      void
      _read_db_options( const options::xml_dict& dict );

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

      bool _connected;
      soci::session _sql;
      unsigned _num_restart_its;
      unsigned _cur_restart_it;
      string _dbtype, _dbname, _dbhost, _dbport, _dbuser, _dbpass;
      string _tree_pre;

      profile::timer _timer;
   };

}

#endif
