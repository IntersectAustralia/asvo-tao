#ifndef tao_sed_sed_hh
#define tao_sed_sed_hh

namespace tao {

   ///
   /// SED science module.
   ///
   /// The SED module is responsible for calculating the
   /// energy spectra of each galaxy.
   ///
   class sed
   {
   public:

      sed();

      ~sed();

      ///
      /// Run the module.
      ///
      void
      run();

   protected:
   };
}

#endif
