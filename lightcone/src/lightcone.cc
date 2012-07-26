#include <boost/range.hpp>
#include "lightcone.hh"

using namespace hpc;
using boost::format;
using boost::str;

namespace tao {

   lightcone::lightcone()
   {
   }

   lightcone::~lightcone()
   {
   }

   ///
   /// Run the module.
   ///
   void
   lightcone::run()
   {
      MPI_LOG_ENTER();

      // TODO: Check that any output databases have been created,
      //       or create them now.

      // TODO: Same as above, but for binary output file. Probably
      //       will be HDF5.

      // TODO: Figure what alternatives there are to a "box".
      if( _type != "box" && _box_side > 0.0 )
      {
         // Iterate over the reversed snapshot indices.
         for( mpi::lindex ii = 0; ii < _snap_idxs.size(); ++ii )
         {
            // Terminate the loop if the redshift is outside our maximum.
            // This is why we reversed the snapshots.
            if( _snaps[_snap_idxs[ii]] > _z_max )
               break;

            auto z_max = _z_max;
            mpi::lindex cur_snap_idx = _snap_idxs[ii];
            if( ii != _snap_idxs.size() - 1 )
            {
               auto next_snap_idx = _snap_idxs[ii + 1];
               z_max = std::min( z_max, _snaps[next_snap_idx] );
               auto max_dist = _redshift_to_distance( _snaps[next_snap_idx] );
            }

            // auto cur_boxes = _get_boxes( z_max );
            // for( auto& box : cur_boxes )
            //    _build_pixels( cur_snap_idx, next_snap_idx, _x0 + box.x, _y0 + box.y, _z0 + box.z );
         }
      }
      else if( _box_side > 0.0 )
      {
         // _build_pixels( ?, ?, _x0, _y0, _z0 );
      }
      else
      {
         // TODO: Zero sized box, should report an error?
         // _build_pixels( 0, 0, 0, 0, 0 );
      }

      // TODO: If we outputted to a database, close it off.

      // TODO: If we outputted to a binary format, close that off too.

      MPI_LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_build_pixels( mpi::lindex cur_snap_idx,
                             optional<mpi::lindex> next_snap_idx,
                             real_type offs_x,
                             real_type offs_y,
                             real_type offs_z )
   {
      // auto query = _build_query( cur_snap_idx, next_snap_idx, offs_x, offs_y, offs_z );

      // TODO: Fetch the query and output each row.
   }

   ///
   ///
   ///
   void
   lightcone::_build_query( mpi::lindex cur_snap_idx,
                            optional<mpi::lindex> next_snap_idx,
                            real_type offs_x,
                            real_type offs_y,
                            real_type offs_z )
   {
      real_type ra_min = to_radians( _ra_min );
      real_type ra_max = to_radians( _ra_max );
      real_type dec_min = to_radians( _dec_min );
      real_type dec_max = to_radians( _dec_max );

      vector<std::string> ops;
      _random_rotation_and_shifting( ops );
//       real_type pos1 = rotation_array[0]['p'];
//       real_type pos2 = rotation_array[1]['p'];
//       real_type pos3 = rotation_array[2]['p'];
//       real_type halo_pos1 = rotation_array[0]['h'];
//       real_type halo_pos2 = rotation_array[1]['h'];
//       real_type halo_pos3 = rotation_array[2]['h'];
//       real_type vel1 = rotation_array[0]['v'];
//       real_type vel2 = rotation_array[1]['v'];
//       real_type vel3 = rotation_array[2]['v'];
//       real_type spin1 = rotation_array[0]['s'];
//       real_type spin2 = rotation_array[1]['s'];
//       real_type spin3 = rotation_array[2]['s'];

//       std::string pos1 = str( format( "(%1% + %2% - %3%)" ) % offs_x % pos1 % _x0 );
//       std::string pos2 = str( format( "(%1% + %2% - %3%)" ) % offs_y % pos2 % _y0 );
//       std::string pos3 = str( format( "(%1% + %2% - %3%)" ) % offs_z % pos3 % _z0 );
//       std::string halo_pos1 = str( format( "(%1% + %2% - %3%)" ) % offs_x % halo_pos1 % _x0 );
//       std::string halo_pos2 = str( format( "(%1% + %2% - %3%)" ) % offs_y % halo_pos2 % _y0 );
//       std::string halo_pos3 = str( format( "(%1% + %2% - %3%)" ) % offs_z % halo_pos3 % _z0 );

//       auto z_max = _z_max;
//       if( next_snap_idx && _box_side > 0.0 )
//          z_max = std::min( z_max, _snaps[*next_snap_idx] );
//       auto max_dist = _redshift_to_distance( z_max );

//       real_type halo_pos1_max = max_dist*cos( ra_min )*cos( dec_min );
//       real_type halo_pos2_max = max_dist*sin( ra_max )*cos( dec_min );
//       real_type halo_pos3_max = max_dist*sin( dec_max );
//       real_type halo_pos1_min = _last_max_dist_processed*cos( ra_max )*cos( dec_max );
//       real_type halo_pos2_min = _last_max_dist_processed*sin( ra_min )*cos( dec_max );
//       real_type halo_pos3_min = _last_max_dist_processed*sin( dec_min );

//       // Apply all my current values to the query template to build up
//       // the final SQL query string.
//       std::string query = _query_template;
//       replace_first( query, "-z1-", lexical_cast<std::string>( _snaps[cur_snap_idx] ) );
//       replace_first( query, "-z2-", lexical_cast<std::string>( z_max ) );
//       replace_first( query, "-dec_min-", lexical_cast<std::string>( _dec_min ) );
//       replace_first( query, "-pos1-", pos1 );
//       replace_first( query, "-pos2-", pos2 );
//       replace_first( query, "-pos3-", pos3 );
//       replace_first( query, "-pos1_max-", lexical_cast<std::string>( halo_pos1_max ) );
//       replace_first( query, "-pos2_max-", lexical_cast<std::string>( halo_pos2_max ) );
//       replace_first( query, "-pos3_max-", lexical_cast<std::string>( halo_pos3_max ) );
//       replace_first( query, "-pos1_min-", lexical_cast<std::string>( halo_pos1_min ) );
//       replace_first( query, "-pos2_min-", lexical_cast<std::string>( halo_pos2_min ) );
//       replace_first( query, "-pos3_min-", lexical_cast<std::string>( halo_pos3_min ) );
//       replace_first( query, "-halo_pos1-", halo_pos1 );
//       replace_first( query, "-halo_pos2-", halo_pos2 );
//       replace_first( query, "-halo_pos3-", halo_pos3 );
//       replace_first( query, "-halo_pos1_max-", lexical_cast<std::string>( halo_pos1_max ) );
//       replace_first( query, "-halo_pos2_max-", lexical_cast<std::string>( halo_pos2_max ) );
//       replace_first( query, "-halo_pos3_max-", lexical_cast<std::string>( halo_pos3_max ) );
//       replace_first( query, "-halo_pos1_min-", lexical_cast<std::string>( halo_pos1_min ) );
//       replace_first( query, "-halo_pos2_min-", lexical_cast<std::string>( halo_pos2_min ) );
//       replace_first( query, "-halo_pos3_min-", lexical_cast<std::string>( halo_pos3_min ) );
//       replace_first( query, "-vel1-", lexical_cast<std::string>( vel1 ) );
//       replace_first( query, "-vel2-", lexical_cast<std::string>( vel2 ) );
//       replace_first( query, "-vel3-", lexical_cast<std::string>( vel3 ) );
//       replace_first( query, "snapshot_", str( format( "snapshot_%1$03d" ) % cur_snap_idx ) );
//       replace_first( query, "-max_dist-", lexical_cast<std::string>( max_dist ) );
//       replace_first( query, "-last_dist-", lexical_cast<std::string>( _last_max_dist_processed ) );

// #ifndef NDEBUG
//       // TODO:: Dump the SQL query string to a debug file.
// #endif

//       // TODO: Submit the query using whatever C++ database library
//       //       we decide upon. I think perhaps SOCI might be a
//       //       good choice.

//       // Return the parsed query object.
//       return result;
   }

   ///
   ///
   ///
   void
   lightcone::_random_rotation_and_shifting( vector<std::string>& ops )
   {
      // Four values (p, h, v, s) in three groups.
      ops.resize( 12 );

      // Common values.
      ops[2] = "Vel1";
      ops[3] = "Spin1";
      ops[6] = "Vel2";
      ops[7] = "Spin2";
      ops[10] = "Vel3";
      ops[11] = "Spin3";

      if( _type == "box" )
      {
         ops[0] = "Pos1";
         ops[1] = "halo_pos1";
         ops[4] = "Pos2";
         ops[5] = "halo_pos2";
         ops[8] = "Pos3";
         ops[9] = "halo_pos3";
      }
      else
      {
         real_type offs1, offs2, offs3;
         int rnd;

         if( _unique )
         {
            offs1 = _unique_offs_x;
            offs2 = _unique_offs_y;
            offs3 = _unique_offs_z;
            rnd = 1;
         }
         else
         {
            offs1 = generate_uniform( 0.0, _box_side*1000.0 )/1000.0;
            offs2 = generate_uniform( 0.0, _box_side*1000.0 )/1000.0;
            offs3 = generate_uniform( 0.0, _box_side*1000.0 )/1000.0;
            rnd = generate_uniform<int>( 1, 6 );
         }

         // Rotation 1.
         ops[0] = str( format( "if(%1%+Pos1<%2%,%3%+Pos1,Pos1+%4%-%5%)" ) % offs1 % _box_side % offs1 % offs1 % _box_side );
         ops[1] = str( format( "if(%1%+halo_pos1<%2%,%3%+halo_pos1,halo_pos1+%4%-%5%)" ) % offs1 % _box_side % offs1 % offs1 % _box_side );
         ops[2] = "Vel1";
         ops[3] = "Spin1";

         // Rotation 2.
         ops[4] = str( format( "if(%1%+Pos2<%2%,%3%+Pos2,Pos2+%4%-%5%)" ) % offs2 % _box_side % offs2 % offs2 % _box_side );
         ops[5] = str( format( "if(%1%+halo_pos2<%2%,%3%+halo_pos2,halo_pos2+%4%-%5%)" ) % offs2 % _box_side % offs2 % offs2 % _box_side );
         ops[6] = "Vel2";
         ops[7] = "Spin2";

         // Rotation 3.
         ops[8] = str( format( "if(%1%+Pos3<%2%,%3%+Pos3,Pos3+%4%-%5%)" ) % offs3 % _box_side % offs3 % offs3 % _box_side );
         ops[9] = str( format( "if(%1%+halo_pos3<%2%,%3%+halo_pos3,halo_pos3+%4%-%5%)" ) % offs3 % _box_side % offs3 % offs3 % _box_side );
         ops[10] = "Vel3";
         ops[11] = "Spin3";

         switch( rnd )
         {
            case 1:
               break;
            case 2:
               for( int ii = 0; ii < 4; ++ii )
               {
                  ops[ii].swap( ops[ii + 4] ); // 1->2, 2->1
                  ops[ii].swap( ops[ii + 8] ); // 2->1->3, 3->1
               }
               break;
            case 3:
               for( int ii = 0; ii < 4; ++ii )
               {
                  ops[ii].swap( ops[ii + 8] ); // 1->3, 3->1
                  ops[ii].swap( ops[ii + 4] ); // 3->1->2, 2->1
               }
               break;
            case 4:
               for( int ii = 0; ii < 4; ++ii )
                  ops[ii + 4].swap( ops[ii + 8] );
               break;
            case 5:
               for( int ii = 0; ii < 4; ++ii )
                  ops[ii].swap( ops[ii + 4] );
               break;
            case 6:
               for( int ii = 0; ii < 4; ++ii )
                  ops[ii].swap( ops[ii + 8] );
               break;
         }
      }
   }

   ///
   ///
   ///
   // void
   // _get_boxes()
   // {
   // }

   ///
   ///
   ///
   lightcone::real_type
   lightcone::_redshift_to_distance( real_type redshift )
   {
      // TODO
      return 0.0;
   }

   ///
   /// Setup parameters.
   ///
   /// For performance sake, we cache all the parameters we need
   /// from the parameter dictionary.
   ///
   void
   lightcone::_setup_params()
   {
      // // Get the parameter dictionary.
      // parameters& param = _parameters();

      // // Box type and size.
      // _type = param.get( "box" );
      // _box_side = 62.5; // for mini-mi TODO: Fix this hard-coding.

      // // Snapshots. Also store the reversed set of keys.
      // param.get( std::inserter( _snaps, _snaps.begin() ) );
      // boost::reverse_copy( _snaps | boost::adaptors::map_keys, std::inserter( _snap_idxs, _snap_idxs.begin() ) );

      // // Redshift ranges.
      // _z_max = std::min( param.get( "z_max" ), _snaps.get( _snap_idxs[_snap_idxs.size() - 1] ) );
   }
}
