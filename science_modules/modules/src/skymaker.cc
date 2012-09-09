#include <cmath>
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
   skymaker::add_galaxy( soci::row& galaxy )
   {
      _params_file << galaxy.get<string>( "Pos0" ) << " ";
      _params_file << galaxy.get<string>( "Pos1" ) << " ";
      _params_file << galaxy.get<string>( "Pos2" ) << "\n";
   }

   void
   skymaker::_read_options( const options::dictionary& dict,
                            optional<const string&> prefix )
   {
      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;
   }
}
