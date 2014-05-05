#ifndef tao_modules_lightcone_hh
#define tao_modules_lightcone_hh

#include <libhpc/system/math.hh>
#include "tao/base/base.hh"

namespace tao {
   namespace modules {

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
         initialise( xml_dict const& global_dict )
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
               _num_tbls = 0;
               for( auto it = _lc.tile_begin(); it != _lc.tile_end(); ++it )
	       {
		  ++_num_tiles;
		  for( auto tbl_it = _be->table_begin( *it ); tbl_it != _be->table_end( *it ); ++tbl_it )
		     ++_num_tbls;
	       }
            }
            else
	    {
	       _num_tiles = 1;
	       for( auto tbl_it = _be->table_begin( _box ); tbl_it != _be->table_end( _box ); ++tbl_it )
		  ++_num_tbls;
	    }

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
	       // First of all, fix up my filter. I need to postpone it until
	       // here because the batch object is only full of all the possible
	       // fields now.
	       if( !_filt.field_name().empty() )
		  _filt.set_type( _bat.get_field_type( _filt.field_name() ) );

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
		     _tile_idx = _c_it.tile_index();
		  if( _c_it.table_index() != _num_tbls )
		  {
		     LOG_PUSH_TAG( "progress" );
		     LOGILN( runtime(), ",", (float)_c_it.table_index()*100.0/(float)_num_tbls, "%" );
		     LOG_POP_TAG( "progress" );
		  }
               }
               else
               {
                  auto db_timer = this->db_timer_start();
                  ++_b_it;
		  if( _b_it.table_index() != _num_tbls )
		  {
		     LOG_PUSH_TAG( "progress" );
		     LOGILN( runtime(), ",", (float)_b_it.table_index()*100.0/(float)_num_tbls, "%" );
		     LOG_POP_TAG( "progress" );
		  }
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
#else
            this->_complete = true;
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
               return boost::any( (const simulation*)_sim );
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

         const tao::lightcone&
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
         _read_options( xml_dict const& global_dict )
         {
            // Cache the local dictionary.
            const xml_dict& dict = this->_dict;

	    // Load simulation information from database.
            _sim = _be->load_simulation();

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
               real_type snap_z_max = _sim->redshifts().front();
               real_type snap_z_min = _sim->redshifts().back();
               real_type max_z = std::min( dict.get<real_type>( "redshift-max", snap_z_max ), snap_z_max );
               real_type min_z = std::max( dict.get<real_type>( "redshift-min", snap_z_min ), snap_z_min );
               LOGILN( "Redshift range: [", min_z, ", ", max_z, ")" );

               // Right ascension.
               real_type min_ra = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "ra-min", 0.0 ), 0.0 ), 89.99 );
               real_type max_ra = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "ra-max", 10.0 ), 0.0 ), 89.99 );
               min_ra = std::min<real_type>( min_ra, max_ra );
               LOGILN( "Right ascension range: [", min_ra, ", ", max_ra, ")" );

               // Declination.
               real_type min_dec = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "dec-min", 0.0 ), 0.0 ), 89.99 );
               real_type max_dec = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "dec-max", 10.0 ), 0.0 ), 89.99 );
               min_dec = std::min<real_type>( min_dec, max_dec );
               LOGILN( "Declination range: [", min_dec, ", ", max_dec, ")" );

               // Check for single snapshot.
               auto sng_snap = dict.opt<unsigned>( "single-snapshot" );
               if( sng_snap )
                  LOGILN( "Single snapshot: ", *sng_snap );

               // Prepare the lightcone object.
               _lc.set_simulation( _sim );
               _lc.set_geometry( min_ra, max_ra, min_dec, max_dec, max_z, min_z );
	       _lc.set_random( !_unique, &_eng );
               if( sng_snap )
               {
                  _lc.set_single_snapshot( true );
                  _lc.set_snapshot( *sng_snap );
               }

	       // Prepare the origin if we're running a unique cone.
	       if( _unique )
		 _calc_origin( global_dict );
            }
            else
            {
               _geom = BOX;

               // Box size.
               _box_size = dict.get<real_type>( "query-box-size", _sim->box_size() );
               LOGILN( "Box size: ", _box_size );

               // Snapshot.
               _box_z = dict.get<real_type>( "redshift", _sim->redshifts().front() );
               LOGILN( "Redshift: ", _box_z );

               // Try to coerce the redshift into a snapshot index.
               unsigned ii = 0;
               for( ; ii < _sim->redshifts().size(); ++ii )
               {
                  if( hpc::approx( _box_z, _sim->redshifts()[ii], 1e-3 ) )
                     break;
               }
               EXCEPT( ii < _sim->redshifts().size(),
                       "Unable to match specified box redshift, ", _box_z, ", to snapshot.\n"
                       "Available redshifts for selected simulation are: ", _sim->redshifts() );
               LOGILN( "Matched redshift to snapshot: ", ii );

               // Prepare box object.
               _box.set_simulation( _sim );
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
               string filt_min = global_dict.get<string>( "workflow:record-filter:filter:filter-min", "" );
               string filt_max = global_dict.get<string>( "workflow:record-filter:filter:filter-max", "" );
               if( !filt_field.empty() && filt_field != "" && filt_field != "none" && filt_field != "NONE" && filt_field != "None" )
               {
		 _filt.set_field( filt_field, filt_min, filt_max );
                  LOGILN( "Filter name: ", filt_field );
                  LOGILN( "Filter range: [", filt_min, ", ", filt_max, ")" );
               }
            }
         }

         void
         _calc_origin( const xml_dict& global_dict )
         {
            EXCEPT( _lc.min_ra() == 0.0, "Cannot compute multiple unique cones when "
                    "minimum RA is not 0." );
            EXCEPT( _lc.min_dec() == 0.0, "Cannot compute multiple unique cones when "
                    "minimum DEC is not 0." );

            // Get the subjobindex.
            unsigned sub_idx = global_dict.get<unsigned>( "subjobindex" );
	    LOGILN( "Subcone inde: ", sub_idx );

	    // Check this index is okay.
	    unsigned max_subcones = tao::calc_max_subcones( _lc );
	    EXCEPT( sub_idx < max_subcones, "Subcone with index ", sub_idx,
		    " is outside the maximum range of ", max_subcones );

	    // Calculate subcone viewing angle and origin.
            real_type view_angle = *tao::calc_subcone_angle( _lc );
	    std::array<real_type,3> ori = tao::calc_subcone_origin<real_type>( _lc, sub_idx );

	    // Set angle and origin.
            _lc.set_viewing_angle( view_angle );
            _lc.set_origin( ori );
            LOGILN( "Viewing angle set to: ", to_degrees( view_angle ) );
            LOGILN( "Origin set to: (", ori[0], ", ", ori[1], ", ", ori[2], ")" );
         }

      protected:

         geometry_type _geom;
         real_type _box_size;
         real_type _box_z;
         int _rng_seed;
         engine_type _eng;
         bool _unique;

         simulation const* _sim;
         query<real_type> _qry;
         filter _filt;
         tao::lightcone _lc;
         box<real_type> _box;
         bool _my_be;
         backend_type* _be;
         typename backend_type::lightcone_galaxy_iterator _c_it;
         typename backend_type::box_galaxy_iterator _b_it;
         tao::batch<real_type> _bat;

         unsigned _tile_idx;
         unsigned _num_tiles;
	 unsigned _num_tbls;
         // profile::progress _prog;
      };

   }
}

#endif
