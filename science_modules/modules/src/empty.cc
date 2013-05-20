#include "empty.hh"

namespace tao {

   module*
   empty::factory( const string& name )
   {
      return new empty( name );
   }

   empty::empty( const string& name )
      : module( name )
   {
   }

   void
   empty::setup_options( options::xml_dict& dict,
                         optional<const string&> prefix )
   {
   }

   void
   empty::initialise( const options::xml_dict& dict,
                      optional<const string&> prefix )
   {
   }

   void
   empty::execute()
   {
   }

}
