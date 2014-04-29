#ifndef tao_base_tile_hh
#define tao_base_tile_hh

#include <array>
#include "box.hh"
#include "query.hh"
#include "lightcone.hh"

namespace tao {
   using namespace hpc;

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

      tile( const tao::lightcone* lc = 0,
            std::array<real_type,3> offs = { { 0, 0, 0 } } )
         : box<T>( 0 ),
           _lc( 0 )
      {
	 set_lightcone( lc, offs );
      }

      void
      set_lightcone( const lightcone* lc,
                     std::array<real_type,3> offs = { { 0, 0, 0 } } )
      {
         if( lc )
         {
            _lc = lc;
            this->set_simulation( lc->simulation() );
            set_offset( offs );
	    this->set_random( _lc->random(), _lc->rng_engine() );
            this->set_origin( _lc->origin() );
         }
         else
            this->set_simulation( 0 );
      }

      void
      set_offset( const std::array<real_type,3>& offs )
      {
         this->_min = offs;
         for( unsigned ii = 0; ii < 3; ++ii )
            this->_max[ii] = this->_min[ii] + _lc->simulation()->box_size();
      }

      const tao::lightcone*
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

      tao::lightcone const* _lc;
   };

}

#endif
