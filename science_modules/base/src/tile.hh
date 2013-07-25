#ifndef tao_base_tile_hh
#define tao_base_tile_hh

#include <libhpc/containers/array.hh>
#include "query.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone;

   ///
   ///
   ///
   template< class T >
   class tile
      : public box<T>
   {
   public:

      typedef T real_type;

   public:

      tile( const tao::lightcone<real_type>* lc,
            array<real_type,3> offs = array<real_type,3>( 0, 0, 0 ),
            bool random = false )
         : box<T>( NULL, random ),
           _lc( lc ),
           _rand( random )
      {
         if( _lc )
            set_simulation( _lc->simulation() ):
         set_offset( offs );
      }

      void
      set_offset( const array<real_type,3>& offs )
      {
         _min = offs;
         for( unsigned ii = 0; ii < 3; ++ii )
            _max[ii] = _min[ii] + _lc->simulation()->box_size();
      }

      const tao::lightcone<real_type>*
      lightcone() const
      {
         return _lc;
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

      tao::lightcone<real_type>* _lc;
      array<real_type,3> _min, _max;
      bool _rand;
      array<unsigned,3> _rot;
      array<real_type,3> _trans;
   };

}

#endif
