#ifndef tao_base_lightcone_galaxy_iterator_hh
#define tao_base_lightcone_galaxy_iterator_hh

#include "lightcone.hh"
#include "lightcone_tile_iterator.hh"
#include "batch.hh"

namespace tao {
   using namespace hpc;

   template< class Backend >
   class lightcone_galaxy_iterator
      : public boost::iterator_facade< lightcone_galaxy_iterator<Backend>,
                                       batch<typename Backend::real_type>&,
				       std::forward_iterator_tag,
                                       batch<typename Backend::real_type>& >
   {
      friend class boost::iterator_core_access;

   public:

      typedef Backend backend_type;
      typedef typename backend_type::real_type real_type;
      typedef typename lightcone<real_type>::tile_iterator tile_iterator;
      typedef typename backend_type::tile_galaxy_iterator tile_galaxy_iterator;
      typedef batch<real_type>& value_type;
      typedef value_type reference_type;

   public:

      lightcone_galaxy_iterator()
         : _done( true )
      {
      }

      lightcone_galaxy_iterator( const lightcone<real_type>& lc,
                                 backend_type& be,
                                 query<real_type>& qry )
         : _lc( &lc ),
           _be( &be ),
           _qry( &qry ),
           _done( false )
      {
         _tile_it = _lc->tile_begin();
         if( !_tile_it.done() )
         {
            _gal_it = _be->galaxy_begin( *_qry, *_tile_it );
            _settle();
         }
         else
            _done = true;
      }

      lightcone_galaxy_iterator&
      operator=( const lightcone_galaxy_iterator& op )
      {
         _lc = op._lc;
         _be = op._be;
         _qry = op._qry;
         _done = op._done;
         _tile_it = op._tile_it;
         _gal_it = op._gal_it;
         return *this;
      }

      reference_type
      operator*()
      {
         return *_gal_it;
      }

      bool
      done() const
      {
         return _done;
      }

   protected:

      void
      increment()
      {
         ++_gal_it;
         _settle();
      }

      bool
      equal( const lightcone_galaxy_iterator& op ) const
      {
         return _done == op._done;
      }

      reference_type
      dereference()
      {
         return *_gal_it;
      }

      void
      _settle()
      {
         if( _gal_it.done() )
         {
            do
            {
               ++_tile_it;
               if( _tile_it.done() )
               {
                  _done = true;
                  break;
               }
               _gal_it = _be->galaxy_begin( *_qry, *_tile_it );
            }
            while( _gal_it.done() );
         }
      }

   protected:

      const lightcone<real_type>* _lc;
      backend_type* _be;
      query<real_type>* _qry;
      tile_iterator _tile_it;
      tile_galaxy_iterator _gal_it;
      bool _done;
   };

}

#endif
