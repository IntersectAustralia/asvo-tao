#ifndef tao_filter_filter_hh
#define tao_filter_filter_hh

namespace tao {

   ///
   ///
   ///
   class filter
   {
   public:

      filter();

      ~filter();

      ///
      /// Run the module.
      ///
      void
      run();

   protected:

      void
      _process_filter();

   protected:
   };
}

#endif
