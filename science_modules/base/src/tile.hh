#ifndef tao_base_tile_hh
#define tao_base_tile_hh

#include <libhpc/containers/array.hh>
#include "query.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone;

   template< class BGI >
   class tile_galaxy_iterator;

   template< class T >
   class tile
   {
   public:

      typedef T real_type;

   public:

      tile( tao::lightcone<real_type>& lc,
            const array<real_type,3>& offs = array<real_type,3>( 0, 0, 0 ),
            bool random = false )
         : _lc( lc ),
           _rand( random )
      {
         set_offset( offs );

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
      set_offset( const array<real_type,3>& offs )
      {
         _min = offs;
         for( unsigned ii = 0; ii < 3; ++ii )
            _max[ii] = _min[ii] + _lc.simulation().box_size();
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

      const tao::lightcone<real_type>&
      lightcone() const
      {
         return _lc;
      }

      template< class Backend >
      tile_galaxy_iterator<typename Backend::tile_galaxy_iterator>
      galaxy_begin( tao::query<real_type>& query,
                    Backend& be ) const
      {
         typedef typename Backend::tile_galaxy_iterator bgi_type;
         return tile_galaxy_iterator<bgi_type>( be.galaxy_begin( query, *this ) );
      }

      template< class Backend >
      tile_galaxy_iterator<typename Backend::tile_galaxy_iterator>
      galaxy_end( tao::query<real_type>& query,
                  Backend& be ) const
      {
         typedef typename Backend::tile_galaxy_iterator bgi_type;
         return tile_galaxy_iterator<bgi_type>( be.galaxy_end( query, *this ) );
      }

   protected:

      tao::lightcone<real_type>& _lc;
      array<real_type,3> _min, _max;
      bool _rand;
      array<unsigned,3> _rot;
      array<real_type,3> _trans;
   };

   template< class BGI >
   class tile_galaxy_iterator
      : public boost::iterator_facade< tile_galaxy_iterator<BGI>,
                                       typename BGI::value_type,
                                       std::forward_iterator_tag,
                                       typename BGI::reference_type >
   {
      friend class boost::iterator_core_access;

   public:

      typedef BGI backend_galaxy_iterator_type;
      typedef typename backend_galaxy_iterator_type::real_type real_type;
      typedef typename backend_galaxy_iterator_type::value_type value_type;
      typedef typename backend_galaxy_iterator_type::reference_type reference_type;

   public:

      tile_galaxy_iterator( const backend_galaxy_iterator_type& bgi )
          : _bgi( bgi )
      {
      }

      reference_type
      operator*()
      {
         return dereference();
      }

   protected:

      void
      increment()
      {
         ++_bgi;
      }

      bool
      equal( const tile_galaxy_iterator& op ) const
      {
         return _bgi == op._bgi;
      }

      reference_type
      dereference()
      {
         return *_bgi;
      }

   protected:

      backend_galaxy_iterator_type _bgi;
   };

}

#endif
