#ifndef tao_dust_dust_hh
#define tao_dust_dust_hh

namespace tao {

   ///
   /// SED science module.
   ///
   /// The SED module is responsible for calculating the
   /// energy spectra of each galaxy.
   ///
   class dust
   {
   public:

      dust();

      ~dust();

      ///
      /// Run the module.
      ///
      void
      run();

   protected:
   };
}

#endif
