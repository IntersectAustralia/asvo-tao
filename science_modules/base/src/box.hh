#ifndef tao_base_tile_hh
#define tao_base_tile_hh

#include <libhpc/containers/array.hh>
#include "query.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone;

   template< class T >
   class box
   {
   public:

      typedef T real_type;

   public:

      box( const simulation<real_type>* sim = NULL,
           bool random = false )
         : _sim( sim ),
           _rand( random )
      {
         // If randomised, then randomise!
         if( _rand )
         {
            // Generate translation.
            for( unsigned ii = 0; ii < 3; ++ii )
               _trans[ii] = generate_uniform<real_type>( 0.0, lc.simulation().box_size() );

            // Generate rotations.
            int rnd = generate_uniform<int>( 0, 5 );
            switch( rnd )
            {
               case 0:
                  _rot[0] = 0;
                  _rot[1] = 1;
                  _rot[2] = 2;
                  break;
               case 1:
                  _rot[0] = 2;
                  _rot[1] = 0;
                  _rot[2] = 1;
                  break;
               case 2:
                  _rot[0] = 1;
                  _rot[1] = 2;
                  _rot[2] = 0;
                  break;
               case 3:
                  _rot[0] = 0;
                  _rot[1] = 2;
                  _rot[2] = 1;
                  break;
               case 4:
                  _rot[0] = 1;
                  _rot[1] = 0;
                  _rot[2] = 2;
                  break;
               case 5:
                  _rot[0] = 2;
                  _rot[1] = 1;
                  _rot[2] = 0;
                  break;
            };
         }
         else
         {
            std::iota( _rot.begin(), _rot.end(), 0 );
            std::fill( _trans.begin(), _trans.end(), 0 );
         }
      }

      void
      set_simulation( const simulation<real_type>* sim )
      {
         _sim = sim;
      }

      const simulation<real_type>*
      simulation() const
      {
         return _sim;
      }

      const array<real_type,3>&
      min() const
      {
         return _min;
      }

      const array<real_type,3>&
      max() const
      {
         return _max;
      }

      bool
      random() const
      {
         return _rand;
      }

      const array<unsigned,3>&
      rotation() const
      {
         return _rot;
      }

      const array<real_type,3>&
      translation() const
      {
         return _trans;
      }

      template< class Backend >
      typename Backend::tile_galaxy_iterator
      galaxy_begin( tao::query<real_type>& query,
                    Backend& be ) const
      {
         return be.galaxy_begin( query, *this );
      }

      template< class Backend >
      typename Backend::tile_galaxy_iterator
      galaxy_end( tao::query<real_type>& query,
                  Backend& be ) const
      {
         return be.galaxy_end( query, *this );
      }

   protected:

      simulation<real_type>* _sim;
      array<real_type,3> _min, _max;
      bool _rand;
      array<unsigned,3> _rot;
      array<real_type,3> _trans;
   };

}

#endif
