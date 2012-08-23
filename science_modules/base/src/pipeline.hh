#ifndef tao_base_pipeline_hh
#define tao_base_pipeline_hh

namespace tao {

   class pipeline
   {
   public:

      void
      setup_options( hpc::options::dictionary& dict );

      void
      initialise( const hpc::options::dictionary& dict );

      void
      run();
   };
}

#endif
