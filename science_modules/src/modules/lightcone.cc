#include "lightcone.hh"

using namespace hpc;

namespace tao {
   namespace modules {

      // Factory function used to create a new lightcone.
      module*
      lightcone::factory( const string& name,
                          pugi::xml_node base )
      {
         return new lightcone( name, base );
      }

      lightcone::lightcone( const string& name,
                            pugi::xml_node base )
         : module( name, base )
      {
      }

      ///
      /// Initialise the module.
      ///
      void
      lightcone::initialise( const options::xml_dict& global_dict )
      {
         LOGILN( "Initialising lightcone module.", setindent( 2 ) );

         module::initialise( global_dict );
         _read_options( global_dict );

         // We need to calculate the total number of tiles in the
         // cone that we will be querying so we can give a meaningful
         // progress indicator (I say meaningful...).
         _num_tiles = 0;
         for( auto it = _lc.tile_begin(); it != _lc.tile_end(); ++it )
            ++_num_tiles;

         LOGILN( "Done.", setindent( -2 ) );
      }

      ///
      /// Run the module.
      ///
      void
      lightcone::execute()
      {
         timer_start();

         // Is this my first time through? If so begin iterating.
         if( _it == 0 )
         {
            if( _geom == CONE )
               _c_it = _lc.galaxy_begin( _qry, _be, &_bat );
            else
               _b_it = _box.galaxy_begin( _qry, _be, &_bat );
         }
         else
         {
            if( _geom == CONE )
            {
               ++_c_it;

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
               ++_b_it;
            }
         }

         // Check for completion.
         if( _geom == CONE )
         {
            if( _c_it == _lc.galaxy_end( _qry, _be ) )
               _complete = true;
         }
         else if( _b_it == _box.galaxy_end( _qry, _be ) )
         {
            _complete = true;
         }

         timer_stop();
      }

      ///
      ///
      ///
      tao::batch<real_type>&
      lightcone::batch()
      {
         return _bat;
      }

      void
      lightcone::log_metrics()
      {
         module::log_metrics();
         LOGILN( _name, " number of tiles: ", _num_tiles );
      }

      ///
      /// Setup parameters. For performance sake, we cache all
      /// the parameters we need from the parameter dictionary.
      ///
      void
      lightcone::_read_options( const options::xml_dict& global_dict )
      {
         timer_start();

         // Cache the local dictionary.
         const options::xml_dict& dict = _dict;

         // Have the multidb backend connect through the dictionary.
         _be.connect( global_dict );

         // Simulation box size comes from backend.
         _sim.set_box_size( _be.box_size() );

         // Cosmological values.
         real_type hubble = dict.get<real_type>( "hubble", 73.0 );
         real_type omega_m = dict.get<real_type>( "omega_m", 0.25 );
         real_type omega_l = dict.get<real_type>( "omega_l", 0.75 );
         _sim.set_cosmology( hubble, omega_m, omega_l );

         // Extract the list of redshift snapshots from the backend to
         // be set on the simulation.
         {
            vector<real_type> snap_zs;
            _be.snapshot_redshifts( snap_zs );
            _sim.set_snapshot_redshifts( snap_zs );
         }

         // Now set the simulation on the backend.
         _be.set_simulation( &_sim );

         // Get box type.
         string box_type = dict.get<string>( "geometry", "light-cone" );
         to_lower( box_type );
         LOGILN( "Box type: ", box_type );
         if( box_type == "light-cone" )
         {
            _geom = CONE;

            // Get tile repetition type.
            string tile_repeat = dict.get<string>( "box-repetition", "unique" );
            to_lower( tile_repeat );
            LOGILN( "Tile repetition type: ", tile_repeat );
            _unique = (tile_repeat == "unique");

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
            _eng.seed( _rng_seed );

            // Redshift ranges.
            real_type snap_z_max = _sim.redshifts().front();
            real_type snap_z_min = _sim.redshifts().back();
            real_type max_z = std::min( dict.get<real_type>( "redshift-max", snap_z_max ), snap_z_max );
            real_type min_z = std::min( dict.get<real_type>( "redshift-min", snap_z_min ), snap_z_min );
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
         }
         else
         {
            _geom = BOX;

            // Box size.
            real_type box_size = dict.get<real_type>( "query-box-size", _sim.box_size() );

            // Snapshot.
            real_type redshift = dict.get<real_type>( "redshift", _sim.redshifts().front() );
         }

         // Output field information.
         _qry.add_base_output_fields();
         {
            list<string> _fields = dict.get_list<string>( "output-fields" );
            for( const auto& field : _fields )
               _qry.add_output_field( field );
         }
         LOGILN( "Extracting fields: ", _qry.output_fields() );

         // Filter information.
         string filt_field = global_dict.get<string>( "workflow:record-filter:filter:filter-attribute", "" );
         to_lower( filt_field );
         string filt_min = global_dict.get<string>( "workflow:record-filter:filter:filter-min", "" );
         string filt_max = global_dict.get<string>( "workflow:record-filter:filter:filter-max", "" );
         if( !filt_field.empty() && filt_field != "" )
         {
            _filt.set_field_name( filt_field );
            _filt.set_minimum( filt_min );
            _filt.set_maximum( filt_max );
            LOGILN( "Filter name: ", filt_field );
            LOGILN( "Filter range: [", filt_min, ", ", filt_max, ")" );
         }

         timer_stop();
      }

      // void
      // application::_setup_backend( const options::xml_dict& global_dict )
      // {
      //    // Read the batch size from the dictionary.
      //    unsigned batch_size = global_dict.get<unsigned>( "settings:database:batch-size", 1000 );
      //    LOGILN( "Setting batch size: ", batch_size );

      //    _db = new multidb( *_global_dict );
      //    _db->OpenAllConnections();
      // }

   }
}
