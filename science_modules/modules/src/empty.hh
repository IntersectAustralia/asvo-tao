#ifndef tao_modules_empty_hh
#define tao_modules_empty_hh

#include "tao/base/base.hh"

namespace tao {

   class empty
      : public module
   {
   public:

      static
      module*
      factory( const string& name );

   public:

      empty( const string& name = string() );

      virtual
      void
      setup_options( options::dictionary& dict,
                     optional<const string&> prefix=optional<const string&>() );

      virtual
      void
      initialise( const options::dictionary& dict,
                  optional<const string&> prefix=optional<const string&>() );

      virtual
      void
      execute();

      virtual
      tao::galaxy&
      galaxy();
   };

}

#endif
