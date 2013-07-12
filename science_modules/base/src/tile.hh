#ifndef tao_base_tile_hh
#define tao_base_tile_hh

#include <libhpc/containers/array.hh>

namespace tao {
   using namespace hpc;

   template< class T >
   class lightcone;

   template< class T >
   class tile
   {
   public:

      typedef T real_type;

   public:

      tile( lightcone<real_type>& lc,
            const array<real_type,3>& offs )
         : _lc( lc ),
           _offs( offs )
      {
      }

      array<real_type,3>
      min() const
      {
         return _offs;
      }

      array<real_type,3>
      max() const
      {
         real_type bs = _lc.simulation().box_size();
         return array<real_type,3>( _offs[0] + bs, _offs[1] + bs, _offs[2] + bs );
      }

      template< class Backend >
      tile_galaxy_iterator<typename Backend::galaxy_iterator>
      galaxy_begin( Backend& be ) const
      {
         typedef typename Backend::galaxy_iterator bgi_type;
         return tile_galaxy_iterator<bgi_type>( be.galaxy_begin( *this ) );
      }

      template< class Backend >
      tile_galaxy_iterator<typename Backend::galaxy_iterator>
      galaxy_end( Backend& be ) const
      {
         typedef typename Backend::galaxy_iterator bgi_type;
         return tile_galaxy_iterator<bgi_type>( be.galaxy_end() );
      }

   protected:

      lightcone<real_type>& _lc;
      array<real_type,3> _offs;
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

   protected:

      void
      increment()
      {
         ++_bgi;
      }

      bool
      equal( const galaxy_iterator& op ) const
      {
         return _bgi == op._bgi;
      }

      reference_type
      dereference() const
      {
         return *_bgi;
      }

   protected:

      backend_galaxy_iterator_type _bgi;
   };

}

#endif
