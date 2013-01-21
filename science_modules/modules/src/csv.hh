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

      csv( const string& filename="tao.output" );

      void
      initialise( const options::dictionary& dict,
		  const lightcone& lc );

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
