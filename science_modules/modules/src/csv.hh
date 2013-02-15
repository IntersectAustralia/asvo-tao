#ifndef tao_modules_csv_hh
#define tao_modules_csv_hh

#include <fstream>
#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/galaxy.hh"
#include "lightcone.hh"

namespace tao {
   using namespace hpc;

   class csv
      : public module
   {
   public:

      csv( const string& name = string() );

      ///
      ///
      ///
      virtual
      void
      setup_options( options::dictionary& dict,
                     optional<const string&> prefix = optional<const string&>() );

      ///
      ///
      ///
      virtual
      void
      initialise( const options::dictionary& dict,
                  optional<const string&> prefix = optional<const string&>() );

      ///
      ///
      ///
      virtual
      void
      execute();

      ///
      ///
      ///
      virtual
      tao::galaxy&
      galaxy();

      void
      set_filename( const string& filename );

      void
      open();

      void
      process_galaxy( const tao::galaxy& galaxy,
		      double app_mag=0.0 );

   protected:

      void
      _write_field( const tao::galaxy& galaxy,
		    const string& field );

   protected:

      std::ofstream _file;
      string _fn;
      const lightcone* _lc;
   };
}

#endif
