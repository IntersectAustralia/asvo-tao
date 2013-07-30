#include "empty.hh"

namespace tao {
   namespace modules {

      module*
      empty::factory( const string& name,
                      pugi::xml_node base )
      {
         return new empty( name, base );
      }

      empty::empty( const string& name,
                    pugi::xml_node base )
         : module( name, base )
      {
      }

      void
      empty::initialise( const options::xml_dict& global_dict )
      {
      }

      void
      empty::execute()
      {
      }

   }
}
