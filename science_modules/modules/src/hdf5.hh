#ifndef tao_modules_hdf5_hh
#define tao_modules_hdf5_hh

#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/galaxy.hh"

namespace tao {
   using namespace hpc;

   class hdf5
      : public module
   {
   public:

      static
      module*
      factory( const string& name,
	       pugi::xml_node base );

   public:

      hdf5( const string& name = string(),
	    pugi::xml_node base = pugi::xml_node() );

      virtual
      ~hdf5();

      ///
      ///
      ///
      virtual
      void
      initialise( const options::xml_dict& global_dict );

      ///
      ///
      ///
      virtual
      void
      execute();

      void
      open();

      void
      process_galaxy( tao::galaxy& galaxy );

      virtual
      void
      log_metrics();

   protected:

      h5::datatype
      _field_type( const tao::galaxy& galaxy,
		   const string& field );

      void
      _write_field( const tao::galaxy& galaxy,
		    const string& field,
		    h5::dataset& dset,
		    h5::dataspace& dspace );

   protected:

      h5::file _file;
      string _fn;
      list<string> _fields;
      unsigned long long _records;
      list<scoped_ptr<h5::dataset>> _dsets;
      hsize_t _chunk_size;
      bool _ready;
   };
}

#endif
