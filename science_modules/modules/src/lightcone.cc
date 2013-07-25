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
               _c_it = _lc.galaxy_begin( _be );
            else
               _b_it = _box.galaxy_begin( _be );
         }
         else
         {
            if( _geom == CONE )
               ++_c_it;
            else
               ++_b_it;
         }

         // Check for completion.
         if( _geom == CONE )
         {
            if( _c_it == _lc.galaxy_end( _be ) )
               _complete = true;
         }
         else if( _b_it == _box.galaxy_end( _be ) )
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
         if( _type == CONE )
            return *_c_it;
         else
            return *_b_it;
      }

      unsigned
      lightcone::num_boxes() const
      {
         return _boxes.size();
      }

      void
      lightcone::log_metrics()
      {
         module::log_metrics();
         LOGILN( _name, " number of boxes: ", num_boxes() );
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
            _real_rng.set_range( 0, _sim.box_size() );
            _int_rng.set_range( 1, 6 );
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
            _real_rng.set_seed( _rng_seed );
            _int_rng.reset();

            // Redshift ranges.
            real_type snap_z_max = _sim.redshifts().front();
            real_type snap_z_min = _sim.redshifts().back();
            real_type max_z = std::min( dict.get<real_type>( "redshift-max", snap_z_max ), snap_z_max );
            real_type min_z = std::min( dict.get<real_type>( "redshift-min", snap_z_min ), snap_z_min );
            LOGILN( "Redshift range: [", _z_min, ", ", _z_max, ")" );

            // Right ascension.
            real_type min_ra = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "ra-min", 0.0 ), 0.0 ), 90.0 );
            real_type max_ra = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "ra-max", 10.0 ), 0.0 ), 90.0 );
            min_ra = std::min<real_type>( min_ra, max_ra );
            LOGILN( "Have right ascension range: [", min_ra, ", ", max_ra, ")" );

            // Declination.
            real_type min_dec = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "dec-min", 0.0 ), 0.0 ), 90.0 );
            real_type max_dec = std::min<real_type>( std::max<real_type>( dict.get<real_type>( "dec-max", 10.0 ), 0.0 ), 90.0 );
            min_dec = std::min<real_type>( min_dec, max_dec );
            LOGILN( "Have declination range: [", min_dec, ", ", max_dec, ")" );
         }
         else
         {
            _geom = BOX;

            // Box size.
            real_type box_size = dict.get<string>( "query-box-size", );

            // Snapshot.
            real_type redshift = dict.get<real_type>( "redshift" );
         }

         // Output field information.
         _qry.add_base_output_fields();
         {
            list<string> _fields = dict.get_list<string>( "output-fields" );
            for( const auto& field : _fields )
               _qry.add_output_field( field );
         }
         LOGDLN( "Extracting fields: ", _qry.output_fields() );

         // // Filter information.
         // _filter = global_dict.get<string>( "workflow:record-filter:filter:filter-attribute","" );
         // std::transform( _filter.begin(), _filter.end(), _filter.begin(), ::tolower );
         // _filter_min = global_dict.get<string>( "workflow:record-filter:filter:filter-min","" );
         // _filter_max = global_dict.get<string>( "workflow:record-filter:filter:filter-max","" );
         // LOGDLN( "Read filter name of: ", _filter );
         // LOGDLN( "Read filter range of: ", _filter_min, " to ", _filter_max );
         // if( !_output_fields.has( _filter ) )
         // {
         //    LOGDLN( "Record-filter: Couldn't locate record-filter name in lightcone output fields." );
         //    _filter.clear();
         // }

         // // Setup the distance to redshift tables.
         // _build_dist_to_z_tbl( 1000, _z_min, _z_max );

         // // Have the galaxy prepare its options.
         // _gal.read_record_filter( global_dict );

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
