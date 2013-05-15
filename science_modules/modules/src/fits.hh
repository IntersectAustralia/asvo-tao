#ifndef tao_modules_fits_hh
#define tao_modules_fits_hh

#include <fstream>
#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/galaxy.hh"
#include "lightcone.hh"
#include "fitsio.h"

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

      void _write_field( const tao::galaxy& galaxy,const string& field,unsigned idx, int ColIndex);
      void _write_table_header(const tao::galaxy& galaxy);

      void ReadFieldsInfo(const options::xml_dict& dict, optional<const string&> prefix = optional<const string&>());
   protected:
      bool _isfirstgalaxy;
      bool _istableopened;
      fitsfile* _file;
      string _fn;
      list<hpc::string> _fields;
	  list<hpc::string> _labels;
	  list<hpc::string> _units;
	  list<hpc::string> _desc;
      unsigned long long _records;

   };
}

#endif
