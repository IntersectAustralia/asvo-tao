#ifndef tao_lightcone_lightcone_hh
#define tao_lightcone_lightcone_hh

#include "tao/base/base.hh"

// Forward declaration of test suites to allow direct access.
class lightcone_suite;

namespace tao {
   namespace modules {
      using namespace hpc;

      ///
      /// Lightcone science module.
      ///
      class lightcone
         : public module
      {
         friend class ::lightcone_suite;

      public:

         // Factory function used to create a new module.
         static
         module*
         factory( const string& name,
                  pugi::xml_node base );

         // Type of geometry to use.
         enum geometry_type
         {
            CONE,
            BOX
         };

      public:

         lightcone( const string& name = string(),
                    pugi::xml_node base = pugi::xml_node() );

         ///
         ///
         ///
         virtual
         void
         initialise( const options::xml_dict& global_dict );

         ///
         /// Run the module.
         ///
         virtual
         void
         execute();

         ///
         ///
         ///
         virtual
         tao::batch<real_type>&
         batch();

         const set<string>&
         output_fields() const;

         unsigned
         num_boxes() const;

         virtual
         void
         log_metrics();

      protected:

         void
         _read_options( const options::xml_dict& global_dict );

      protected:

         geometry_type _geom;
         real_type _box_size;
         int _rng_seed;
         uniform_generator<real_type> _real_rng;
         uniform_generator<int> _int_rng;

         tao::simulation<real_type> _sim;
         tao::query<real_type> _qry;
         tao::lightcone<real_type> _lc;
         tao::box<real_type> _box;
         tao::backends::soci<real_type> _be;
         tao::backends::soci<real_type>::lightcone_galaxy_iterator _c_it;
         tao::backends::soci<real_type>::box_galaxy_iterator _b_it;

         profile::progress _prog;
      };

   }
}

#endif
