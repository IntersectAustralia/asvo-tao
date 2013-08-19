#ifndef tao_modules_votable_hh
#define tao_modules_votable_hh

#include <fstream>
#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/galaxy.hh"
#include "lightcone.hh"

namespace tao {
   using namespace hpc;

   class votable
      : public module
   {
   public:

      static module* factory( const string& name,
			      pugi::xml_node base );

   public:

      votable( const string& name = string(),
	       pugi::xml_node base = pugi::xml_node() );

      virtual ~votable();

      ///
      ///
      ///
      virtual
      void
      initialise( const options::xml_dict& global_dict );

      ///
      ///
      ///
      virtual void execute();


      virtual void finalise();

      void open();

      void process_galaxy( tao::galaxy& galaxy );

      virtual void log_metrics();

   protected:
      string _xml_encode(string _toencode_string);
      string _xml_encode_fieldName(string _toencode_string);
      void _write_field( const tao::galaxy& galaxy,const string& field);
      void _write_file_header(const string& ResourceName,const string& TableName );
      void _write_footer();

      void _write_table_header(const tao::galaxy& galaxy);
      void _start_table();
      void _end_table();
      void ReadFieldsInfo(const options::xml_dict& dict );
   protected:
      bool _isfirstgalaxy;
      bool _istableopened;
      std::ofstream _file;
      string _fn;
      list<hpc::string> _fields;
      list<hpc::string> _labels;
      list<hpc::string> _units;
      list<hpc::string> _desc;
      unsigned long long _records;

   };
}

#endif
