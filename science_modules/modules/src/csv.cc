#include "csv.hh"

using namespace hpc;

namespace tao {

   csv::csv( const string& filename )
   {
      string fn = filename + "." + to_string( mpi::comm::world.rank() );
      _file.open( fn, std::fstream::out | std::fstream::trunc );
   }

   void
   csv::process_galaxy( const tao::galaxy& galaxy,
			double app_mag )
   {
      _file << galaxy.x() << ", " << galaxy.y() << ", " << galaxy.z();
      _file << ", " << galaxy.redshift();
      _file << ", " << app_mag;
      _file << "\n";
   }
}
