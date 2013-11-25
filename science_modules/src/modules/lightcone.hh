#ifndef tao_modules_lightcone_hh
#define tao_modules_lightcone_hh

#include "tao/base/base.hh"

namespace tao {
   namespace modules {
      using namespace hpc;

      ///
      /// Lightcone science module.
      ///
      template< class Backend >
      class lightcone
         : public module<Backend>
      {
      public:

         typedef Backend backend_type;
         typedef module<backend_type> module_type;

         // Type of geometry to use.
         enum geometry_type
         {
            CONE,
            BOX
         };

         // Factory function used to create a new module.
         static
         module_type*
         factory( const string& name,
                  pugi::xml_node base )
         {
            return new lightcone( name, base );
         }

      public:

         lightcone( const string& name = string(),
                    pugi::xml_node base = pugi::xml_node() )
            : module_type( name, base ),
              _my_be( false ),
              _be( 0 )
         {
         }

         virtual
         ~lightcone()
         {
            if( _my_be )
               delete _be;
         }

         void
         set_backend( backend_type* be )
         {
            _my_be = (be == 0);
            _be = be;
         }

         ///
         ///
         ///
         virtual
         void
         initialise( const options::xml_dict& global_dict )
         {
            // Don't initialise if we're already doing so.
            if( this->_init )
               return;
            module_type::initialise( global_dict );

            auto timer = this->timer_start();
            LOGILN( "Initialising lightcone module.", setindent( 2 ) );

            // If we have been given an existing backend then use that.
            if( !_be )
            {
               _my_be = true;
               auto db_timer = this->db_timer_start();
               _be = new backend_type;
               _be->connect( global_dict );
            }

            // Read all my options.
            _read_options( global_dict );

            // We need to calculate the total number of tiles in the
            // cone that we will be querying so we can give a meaningful
            // progress indicator (I say meaningful...).
            if( _geom == CONE )
            {
               _num_tiles = 0;
               for( auto it = _lc.tile_begin(); it != _lc.tile_end(); ++it )
                  ++_num_tiles;
            }
            else
               _num_tiles = 1;

            // Make sure the local batch object is prepared. I need to
            // do this here because other modules will likely need
            // to access and cache values.
            _be->init_batch( _bat, _qry );

	    // Set the random seed now, so that we actually start from
	    // the seed given.
            _eng.seed( _rng_seed );

	    // Show in the logs what we're querying.
	    LOGILN( "Querying the following fields: ", _qry.output_fields() );

	    // If we have been built to be a preprocessing version,
	    // dump each tile/box to be used and the tables in each.
#ifdef PREPROCESSING
	    LOG( logging::pushlevel( 100 ) );
	    if( _geom == CONE )
            {
	       LOG( "Boxes:[" );
	       bool first = true;
               for( auto it = _lc.tile_begin(); it != _lc.tile_end(); ++it )
	       {
		  if( !first )
		     LOG( ", " );
		  LOG( it->min() );
		  first = false;
	       }
	       LOGLN( "]" );

               for( auto it = _lc.tile_begin(); it != _lc.tile_end(); ++it )
	       {
		  LOGLN( "Using box:", it->min() );
		  LOG( "Tables:[" );
		  bool first = true;
		  for( auto tbl_it = _be->table_begin( *it ); tbl_it != _be->table_end( *it ); ++tbl_it )
		  {
		     if( !first )
			LOG( ", " );
		     LOG( tbl_it->name() );
		     first = false;
		  }
		  LOGLN( "]" );
	       }
            }
            else
	    {
	       LOGLN( "Boxes:[(0, 0, 0)]" );
	       LOGLN( "Using box:[(0, 0, 0)]" );
	    }
	    LOG( logging::poplevel );
#endif

            LOGILN( "Done.", setindent( -2 ) );
         }

         ///
         /// Run the module.
         ///
         virtual
         void
         execute()
         {
#ifndef PREPROCESSING
            auto timer = this->timer_start();

            // Is this my first time through? If so begin iterating.
            if( this->_it == 0 )
            {
               {
                  auto db_timer = this->db_timer_start();
                  if( _geom == CONE )
                     _c_it = _lc.galaxy_begin( _qry, *_be, &_bat, &_filt );
                  else
                     _b_it = _box.galaxy_begin( _qry, *_be, &_bat, &_filt );
               }

               // Initialise the tile index.
               _tile_idx = std::numeric_limits<unsigned>::max();
            }
            else
            {
               if( _geom == CONE )
               {
                  {
                     auto db_timer = this->db_timer_start();
                     ++_c_it;
                  }

                  // Dump updates about how many tiles we've completed.
                  // TODO: This is only dumping for rank 0. We should
                  // probably come up with a better way of handling
                  // distributed progress.
                  if( _c_it.tile_index() != _tile_idx )
                  {
                     _tile_idx = _c_it.tile_index();
                     if( _tile_idx != _num_tiles )
                     {
                        LOG_PUSH_TAG( "progress" );
                        LOGILN( runtime(), ",", (float)_tile_idx*100.0/(float)_num_tiles, "%" );
                        LOG_POP_TAG( "progress" );
                     }
                  }
               }
               else
               {
                  auto db_timer = this->db_timer_start();
                  ++_b_it;
               }
            }

            // Check for completion.
            if( _geom == CONE )
            {
               if( _c_it == _lc.galaxy_end( _qry, *_be ) )
                  this->_complete = true;
            }
            else if( _b_it == _box.galaxy_end( _qry, *_be ) )
            {
               this->_complete = true;
            }
#endif
         }

         ///
         ///
         ///
         virtual
         tao::batch<real_type>&
         batch()
         {
            return _bat;
         }

         virtual
         backend_type*
         backend()
         {
            return _be;
         }

         virtual
         optional<boost::any>
         find_attribute( const string& name )
         {
            if( name == "simulation" )
               return boost::any( &((const simulation<real_type>&)_sim) );
            else if( name == "filter" )
               return boost::any( &((filter const&)_filt) );
            else
               return module_type::find_attribute( name );
         }

         geometry_type
         geometry() const
         {
            return _geom;
         }

         int
         random_seed() const
         {
            return _rng_seed;
         }

         bool
         tile_repetition_random() const
         {
            return !_unique;
         }

         const tao::lightcone<real_type>&
         base_lightcone() const
         {
            return _lc;
         }

         real_type
         box_size() const
         {
            return _box_size;
         }

         real_type
         box_redshift() const
         {
            return _box_z;
         }

         virtual
         void
         log_metrics()
         {
            module_type::log_metrics();
            LOGILN( this->_name, " number of tiles: ", _num_tiles );
         }

      protected:

         void
         _read_options( const options::xml_dict& global_dict )
         {
            // Cache the local dictionary.
            const options::xml_dict& dict = this->_dict;

            // Simulation box size comes from backend.
            _sim.set_box_size( _be->box_size() );

            // Cosmological values.
            real_type hubble = dict.get<real_type>( "hubble", 73.0 );
            real_type omega_m = dict.get<real_type>( "omega_m", 0.25 );
            real_type omega_l = dict.get<real_type>( "omega_l", 0.75 );
            _sim.set_cosmology( hubble, omega_m, omega_l );

            // Extract the list of redshift snapshots from the backend to
            // be set on the simulation.
            {
               vector<real_type> snap_zs;
               {
                  auto db_timer = this->db_timer_start();
                  _be->snapshot_redshifts( snap_zs );
               }
               _sim.set_snapshot_redshifts( snap_zs );
            }

            // Now set the simulation on the backend.
            {
               auto db_timer = this->db_timer_start();
               _be->set_simulation( &_sim );
            }

            // Extract the random number generator seed and set it.
            optional<int> rng_seed = dict.opt<int>( "rng-seed" );
            if( rng_seed )
               _rng_seed = *rng_seed;
            else
            {
               ::srand( ::time( NULL ) );
               _rng_seed = rand();
            }
            mpi::comm::world.bcast<int>( _rng_seed, 0 );
            LOGILN( "Random seed: ", _rng_seed );

	    // Get tile repetition type.
	    string tile_repeat = dict.get<string>( "box-repetition", "unique" );
	    to_lower( tile_repeat );
	    LOGILN( "Tile/box repetition type: ", tile_repeat );
	    _unique = (tile_repeat == "unique");

            // Get box type.
            string box_type = dict.get<string>( "geometry", "light-cone" );
            to_lower( box_type );
            LOGILN( "Box type: ", box_type );
            if( box_type == "light-cone" )
            {
               _geom = CONE;

               // Redshift ranges.
               real_type snap_z_max = _sim.redshifts().front();
               real_type snap_z_min = _sim.redshifts().back();
               real_type max_z = std::min( dict.get<real_type>( "redshift-max", snap_z_max ), snap_z_max );
               real_type min_z = std::max( dict.get<real_type>( "redshift-min", snap_z_min ), snap_z_min );
               LOGILN( "Redshift range: [", min_z, ", ", max_z, ")" );

               // Right ascension.
               real_type min_ra = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "ra-min", 0.0 ), 0.0 ), 90.0 );
               real_type max_ra = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "ra-max", 10.0 ), 0.0 ), 90.0 );
               min_ra = std::min<real_type>( min_ra, max_ra );
               LOGILN( "Right ascension range: [", min_ra, ", ", max_ra, ")" );

               // Declination.
               real_type min_dec = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "dec-min", 0.0 ), 0.0 ), 90.0 );
               real_type max_dec = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "dec-max", 10.0 ), 0.0 ), 90.0 );
               min_dec = std::min<real_type>( min_dec, max_dec );
               LOGILN( "Declination range: [", min_dec, ", ", max_dec, ")" );

               // Prepare the lightcone object.
               _lc.set_simulation( &_sim );
               _lc.set_geometry( min_ra, max_ra, min_dec, max_dec, max_z, min_z );
	       _lc.set_random( !_unique, &_eng );

	       // Prepare the origin if we're running a unique cone.
	       if( _unique )
		 _calc_origin( global_dict );
            }
            else
            {
               _geom = BOX;

               // Box size.
               _box_size = dict.get<real_type>( "query-box-size", _sim.box_size() );
               LOGILN( "Box size: ", _box_size );

               // Snapshot.
               _box_z = dict.get<real_type>( "redshift", _sim.redshifts().front() );
               LOGILN( "Redshift: ", _box_z );

               // Try to coerce the redshift into a snapshot index.
               unsigned ii = 0;
               for( ; ii < _sim.redshifts().size(); ++ii )
               {
                  if( num::approx( _box_z, _sim.redshifts()[ii], 1e-3 ) )
                     break;
               }
               EXCEPT( ii < _sim.redshifts().size(),
                       "Unable to match specified box redshift, ", _box_z, ", to snapshot.\n"
                       "Available redshifts for selected simulation are: ", _sim.redshifts() );
               LOGILN( "Matched redshift to snapshot: ", ii );

               // Prepare box object.
               _box.set_simulation( &_sim );
               _box.set_size( _box_size );
               _box.set_snapshot( ii );
               _box.set_random( !_unique, &_eng );
            }

            // Output field information.
            {
               list<string> _fields = dict.get_list<string>( "output-fields" );
               for( const auto& field : _fields )
                  _qry.add_output_field( field );
            }
            LOGILN( "Extracting fields: ", _qry.output_fields() );

            // Filter information.
            {
               string filt_field = global_dict.get<string>( "workflow:record-filter:filter:filter-attribute", "" );
               // to_lower( filt_field );
               string filt_min = global_dict.get<string>( "workflow:record-filter:filter:filter-min", "" );
               string filt_max = global_dict.get<string>( "workflow:record-filter:filter:filter-max", "" );
               if( !filt_field.empty() && filt_field != "" )
               {
                  _filt.set_field_name( filt_field );
                  try
                  {
                     real_type val = boost::lexical_cast<real_type>( filt_min );
                     _filt.set_minimum( val );
                  }
                  catch( const boost::bad_lexical_cast& ex ) {}
                  try
                  {
                     real_type val = boost::lexical_cast<real_type>( filt_max );
                     _filt.set_maximum( val );
                  }
                  catch( const boost::bad_lexical_cast& ex ) {}
                  LOGILN( "Filter name: ", filt_field );
                  LOGILN( "Filter range: [", filt_min, ", ", filt_max, ")" );
               }
            }
         }

         void
         _calc_origin( const options::xml_dict& global_dict )
         {
            EXCEPT( _lc.min_ra() == 0.0, "Cannot compute multiple unique cones when "
                    "minimum RA is not 0." );
            EXCEPT( _lc.min_dec() == 0.0, "Cannot compute multiple unique cones when "
                    "minimum DEC is not 0." );

            // Get the subjobindex.
            unsigned sub_idx = global_dict.get<unsigned>( "subjobindex" );

	    // Check this index is okay.
	    unsigned max_subcones = tao::calc_max_subcones( _lc );
	    EXCEPT( sub_idx < max_subcones, "Subcone with index ", sub_idx,
		    " is outside the maximum range of ", max_subcones );

	    // Calculate subcone origin.
	    std::array<real_type,3> ori = tao::calc_subcone_origin<real_type>( _lc, sub_idx );

	    // Set origin.
            _lc.set_origin( ori );
            LOGILN( "Origin set to: (", ori[0], ", ", ori[1], ", ", ori[2], ")" );
         }

      protected:

         geometry_type _geom;
         real_type _box_size;
         real_type _box_z;
         int _rng_seed;
         engine_type _eng;
         bool _unique;

         simulation<real_type> _sim;
         query<real_type> _qry;
         filter _filt;
         tao::lightcone<real_type> _lc;
         box<real_type> _box;
         bool _my_be;
         backend_type* _be;
         typename backend_type::lightcone_galaxy_iterator _c_it;
         typename backend_type::box_galaxy_iterator _b_it;
         tao::batch<real_type> _bat;

         unsigned _tile_idx;
         unsigned _num_tiles;
         // profile::progress _prog;
      };

   }
}

#endif
