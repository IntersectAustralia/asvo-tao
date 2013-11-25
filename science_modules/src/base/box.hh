#ifndef tao_base_box_hh
#define tao_base_box_hh

#include <libhpc/containers/array.hh>
#include <libhpc/containers/random.hh>
#include "query.hh"
#include "batch.hh"
#include "filter.hh"

namespace tao {
   using namespace hpc;

   template< class T >
   class simulation;

   template< class T >
   class box
   {
   public:

      typedef T real_type;

   public:

      box( const tao::simulation<real_type>* sim = 0 )
         : _sim( sim ),
           _snap( 0 ),
           _rand( false ),
	   _eng( 0 ),
           _orig{ { 0.0, 0.0, 0.0 } }
      {
         _update();
      }

      void
      set_simulation( const tao::simulation<real_type>* sim )
      {
         _sim = sim;
         _update();
      }

      void
      set_size( real_type size )
      {
         std::fill( _min.begin(), _min.end(), 0.0 );
         std::fill( _max.begin(), _max.end(), size );
      }

      void
      set_snapshot( unsigned snap )
      {
         _snap = snap;
      }

      void
      set_random( bool rand,
		  engine_type* engine = &hpc::engine )
      {
	 _rand = rand;
	 _eng = engine;
	 _update_random();
      }

      void
      set_origin( std::array<real_type,3> const& orig )
      {
         _orig = orig;
      }

      std::array<real_type,3> const&
      origin() const
      {
         return _orig;
      }

      const tao::simulation<real_type>*
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

      unsigned
      snapshot() const
      {
         return _snap;
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
      typename Backend::box_galaxy_iterator
      galaxy_begin( tao::query<real_type>& query,
                    Backend& be,
                    tao::batch<real_type>* bat = 0,
                    tao::filter const* filt = 0 )
      {
         return be.galaxy_begin( query, *this, bat, filt );
      }

      template< class Backend >
      typename Backend::box_galaxy_iterator
      galaxy_end( tao::query<real_type>& query,
                  Backend& be ) const
      {
         return be.galaxy_end( query, *this );
      }

      void
      randomise()
      {
         // Only do this if we have a simulation set.
         if( _sim )
         {
            LOGDLN( "Randomising box.", setindent( 2 ) );

            // Generate translation.
            for( unsigned ii = 0; ii < 3; ++ii )
               _trans[ii] = generate_uniform<real_type>( 0.0, _sim->box_size(), *_eng );
            LOGDLN( "Translation: ", _trans );

            // Generate rotations.
            int rnd = generate_uniform<int>( 0, 5, *_eng );
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
            LOGDLN( "Rotation: ", _rot );

            LOGDLN( "Done.", setindent( -2 ) );
         }
      }

   protected:

      void
      _update()
      {
	 _update_random();

         // If simulation is set, update min and max.
         if( _sim )
         {
            std::fill( _min.begin(), _min.end(), 0 );
            std::fill( _max.begin(), _max.end(), _sim->box_size() );
         }
      }

      void
      _update_random()
      {
         // If randomised, then randomise!
         if( _rand )
         {
            randomise();
         }
         else
         {
            std::iota( _rot.begin(), _rot.end(), 0 );
            std::fill( _trans.begin(), _trans.end(), 0 );
         }
      }

   protected:

      const tao::simulation<real_type>* _sim;
      array<real_type,3> _min, _max;
      bool _rand;
      engine_type* _eng;
      array<unsigned,3> _rot;
      array<real_type,3> _trans;
      std::array<real_type,3> _orig;
      unsigned _snap;
   };

}

#endif
