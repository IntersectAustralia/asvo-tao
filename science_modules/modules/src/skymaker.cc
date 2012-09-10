#include <cmath>
#include <fstream>
#include <boost/algorithm/string/trim.hpp>
#include <boost/tokenizer.hpp>
#include "skymaker.hh"

using namespace hpc;

namespace tao {

   skymaker::skymaker()
   {
   }

   skymaker::~skymaker()
   {
   }

   ///
   ///
   ///
   void
   skymaker::setup_options( options::dictionary& dict,
                            optional<const string&> prefix )
   {
   }

   ///
   ///
   ///
   void
   skymaker::setup_options( hpc::options::dictionary& dict,
                            const char* prefix )
   {
   }

   ///
   /// Initialise the module.
   ///
   void
   skymaker::initialise( const options::dictionary& dict,
                         optional<const string&> prefix )
   {
      LOG_ENTER();

      _read_options( dict, prefix );
      _setup_params();

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   skymaker::initialise( const hpc::options::dictionary& dict,
                         const char* prefix )
   {
      initialise( dict, string( prefix ) );
   }

   void
   skymaker::run()
   {
      // Close the parameter file.
      _params_file.close();

      // Launch the external command.
      // TODO: Need a library call.
      ::system( (string( "sky " ) + _params_filename).c_str() );
   }

   void
   skymaker::add_galaxy( const soci::row& galaxy,
                         real_type magnitude )
   {
      _params_file << "100" << " "; // 100 = star, 200 = galaxy

      // Convert the cartesian coordiantes to right-ascension and
      // declination.
      real_type ra, dec;
      numerics::cartesian_to_ecs( galaxy.get<real_type>( "Pos1" ),
                                  galaxy.get<real_type>( "Pos2" ),
                                  galaxy.get<real_type>( "Pos3" ),
                                  ra, dec );
      LOGLN( "Converted to (", ra, ", ", dec, ")" );

      // Now convert to pixel coordinates.
      real_type x, y;
      numerics::gnomonic_projection( ra, dec,
                                     0.25*M_PI, 0.25*M_PI,
                                     x, y );
      LOGLN( "Now to (", x, ", ", y, ")" );

      // Now, convert to pixel coordinates.
      // TODO: Do this properly.
      x *= 1024.0;
      x += 512.0;
      y *= 1024.0;
      y += 512.0;

      // Write to file.
      _params_file << x << " " << y << " " << magnitude << "\n";

      // TODO: Include all the disk/bulge information.
   }

   void
   skymaker::_read_options( const options::dictionary& dict,
                            optional<const string&> prefix )
   {
      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;
   }

   void
   skymaker::_setup_params()
   {
      _params_filename = tmpnam( NULL );
      LOGLN( "Opening parameter file: ", _params_filename );
      _params_file.open( _params_filename, std::ios::out );
   }
}
