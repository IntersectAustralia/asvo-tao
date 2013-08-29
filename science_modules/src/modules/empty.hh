#ifndef tao_modules_empty_hh
#define tao_modules_empty_hh

#include "tao/base/base.hh"

namespace tao {
   namespace modules {

      ///
      /// Example science module.
      ///
      class empty
         : public module
      {
      public:

         ///
         /// Create an instance of the module.
         ///
         /// @param[in] name The unique name for the created module.
         ///
         static
         module*
         factory( const string& name,
                  pugi::xml_node base );

      public:

         ///
         /// Constructor.
         ///
         /// @param[in] name The unique name for this module.
         ///
         empty( const string& name = string(),
                pugi::xml_node base = (pugi::xml_node)0 );

         ///
         /// Read options, perform required setup.
         ///
         /// @param[in,out] dict Options dictionary to prepare.
         /// @param[in] prefix An optional prefix to apply to options.
         ///
         virtual
         void
         initialise( const options::xml_dict& global_dict );

         ///
         /// Execute.
         ///
         /// Retrieve galaxy information from parent(s) and
         /// perform processing.
         ///
         virtual
         void
         execute();
      };

   }
}

#endif
