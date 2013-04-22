#ifndef tao_modules_fits_hh
#define tao_modules_fits_hh

#include <fstream>
#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/galaxy.hh"
#include "lightcone.hh"

namespace tao {
   using namespace hpc;

   class fits
      : public module
   {
   public:

      static module* factory( const string& name );

   public:

      fits( const string& name = string() );

      virtual ~fits();

      ///
      ///
      ///
      virtual
      void
      initialise( const options::xml_dict& dict, optional<const string&> prefix = optional<const string&>() );

      ///
      ///
      ///
      virtual void execute();


      virtual void finalise();

      void open();

      void process_galaxy( const tao::galaxy& galaxy );

      virtual void log_metrics();

   protected:

      void _write_field( const tao::galaxy& galaxy,const string& field );
      void _write_file_header(const string& ResourceName,const string& TableName );
      void _write_footer();

      void _write_table_header(const tao::galaxy& galaxy);
      void _start_table();
      void _end_table();
   protected:
      bool _isfirstgalaxy;
      bool _istableopened;
      std::ofstream _file;
      string _fn;
      list<string> _fields;
      unsigned long long _records;

   };
}

#endif
