#include <boost/range.hpp>
#include <boost/algorithm/string/replace.hpp>
#include <soci/sqlite3/soci-sqlite3.h>
#include "lightcone.hh"

using namespace hpc;
using boost::format;
using boost::str;
using boost::algorithm::replace_first;

namespace tao {

   lightcone::lightcone()
      : _box_side( 1.0 ),
        _z_min( 0.0 ),
        _z_max( 0.0 ),
        _unique( false ),
        _unique_offs_x( 0.0 ),
        _unique_offs_y( 0.0 ),
        _unique_offs_z( 0.0 ),
        _H0( 100.0 )
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
      LOG_ENTER();

      // Connect to the database.
      _db_connect( _sql );

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

      LOG_EXIT();
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
      auto query = _build_query( cur_snap_idx, next_snap_idx, offs_x, offs_y, offs_z );

      // TODO: Fetch the query and output each row.
   }

   ///
   ///
   ///
   std::string
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
      std::string& pos1 = ops[0];
      std::string& pos2 = ops[4];
      std::string& pos3 = ops[8];
      std::string& halo_pos1 = ops[1];
      std::string& halo_pos2 = ops[5];
      std::string& halo_pos3 = ops[9];
      std::string& vel1 = ops[2];
      std::string& vel2 = ops[6];
      std::string& vel3 = ops[10];
      std::string& spin1 = ops[3];
      std::string& spin2 = ops[7];
      std::string& spin3 = ops[11];

      pos1 = str( format( "(%1% + %2% - %3%)" ) % offs_x % pos1 % _x0 );
      pos2 = str( format( "(%1% + %2% - %3%)" ) % offs_y % pos2 % _y0 );
      pos3 = str( format( "(%1% + %2% - %3%)" ) % offs_z % pos3 % _z0 );
      halo_pos1 = str( format( "(%1% + %2% - %3%)" ) % offs_x % halo_pos1 % _x0 );
      halo_pos2 = str( format( "(%1% + %2% - %3%)" ) % offs_y % halo_pos2 % _y0 );
      halo_pos3 = str( format( "(%1% + %2% - %3%)" ) % offs_z % halo_pos3 % _z0 );

      auto z_max = _z_max;
      if( next_snap_idx && _box_side > 0.0 )
         z_max = std::min( z_max, _snaps[*next_snap_idx] );
      auto max_dist = _redshift_to_distance( z_max );

      real_type halo_pos1_max = max_dist*cos( ra_min )*cos( dec_min );
      real_type halo_pos2_max = max_dist*sin( ra_max )*cos( dec_min );
      real_type halo_pos3_max = max_dist*sin( dec_max );
      real_type halo_pos1_min = _last_max_dist_processed*cos( ra_max )*cos( dec_max );
      real_type halo_pos2_min = _last_max_dist_processed*sin( ra_min )*cos( dec_max );
      real_type halo_pos3_min = _last_max_dist_processed*sin( dec_min );

      // Apply all my current values to the query template to build up
      // the final SQL query string.
      std::string query = _query_template;
      replace_first( query, "-z1-", to_string( _snaps[cur_snap_idx] ) );
      replace_first( query, "-z2-", to_string( z_max ) );
      replace_first( query, "-dec_min-", to_string( _dec_min ) );
      replace_first( query, "-pos1-", pos1 );
      replace_first( query, "-pos2-", pos2 );
      replace_first( query, "-pos3-", pos3 );
      replace_first( query, "-pos1_max-", to_string( halo_pos1_max ) );
      replace_first( query, "-pos2_max-", to_string( halo_pos2_max ) );
      replace_first( query, "-pos3_max-", to_string( halo_pos3_max ) );
      replace_first( query, "-pos1_min-", to_string( halo_pos1_min ) );
      replace_first( query, "-pos2_min-", to_string( halo_pos2_min ) );
      replace_first( query, "-pos3_min-", to_string( halo_pos3_min ) );
      replace_first( query, "-halo_pos1-", halo_pos1 );
      replace_first( query, "-halo_pos2-", halo_pos2 );
      replace_first( query, "-halo_pos3-", halo_pos3 );
      replace_first( query, "-halo_pos1_max-", to_string( halo_pos1_max ) );
      replace_first( query, "-halo_pos2_max-", to_string( halo_pos2_max ) );
      replace_first( query, "-halo_pos3_max-", to_string( halo_pos3_max ) );
      replace_first( query, "-halo_pos1_min-", to_string( halo_pos1_min ) );
      replace_first( query, "-halo_pos2_min-", to_string( halo_pos2_min ) );
      replace_first( query, "-halo_pos3_min-", to_string( halo_pos3_min ) );
      replace_first( query, "-vel1-", to_string( vel1 ) );
      replace_first( query, "-vel2-", to_string( vel2 ) );
      replace_first( query, "-vel3-", to_string( vel3 ) );
      replace_first( query, "snapshot_", str( format( "snapshot_%1$03d" ) % cur_snap_idx ) );
      replace_first( query, "-max_dist-", to_string( max_dist ) );
      replace_first( query, "-last_dist-", to_string( _last_max_dist_processed ) );

#ifndef NDEBUG
      // TODO:: Dump the SQL query string to a debug file.
#endif

      // TODO: Submit the query using whatever C++ database library
      //       we decide upon. I think perhaps SOCI might be a
      //       good choice.

      // Return the parsed query object.
      return query;
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
            // A zero box side length causes a hang.
            ASSERT( _box_side > 0.0 );

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
      unsigned n = 1000;
      real_type dz = redshift/(real_type)n;
      real_type integral = 0.0;
	
      real_type c = 299792.458;
      real_type H0 = _H0;
      real_type h = _H0/100.0;
      real_type WM = 0.25;
      real_type WV = 1.0 - WM - 0.4165/(H0*H0);
      real_type WR = 4.165e-5/(h*h);
      real_type WK = 1.0 - WM - WR - WV;
      real_type az = 1.0/(1.0 + 1.0*redshift);
      real_type DTT = 0.0;
      real_type DCMR = 0.0;
      for( unsigned ii = 0; ii < n; ++ii )
      {
         real_type a = az + (1.0 - az)*((real_type)ii + 0.5)/(real_type)n;
         real_type adot = sqrt( WK + (WM/a) + (WR/(a*a)) + (WV*a*a));
         DTT += 1.0/adot;
         DCMR += 1.0/(a*adot);
      }
      DTT = (1.0 - az)*DTT/(real_type)n;
      DCMR = (1.0 - az)*DCMR/(real_type)n;
      real_type d = (c/H0)*DCMR;
      return d;
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

      _H0 = 100.0;
   }

   ///
   ///
   ///
   void
   lightcone::_setup_query_template()
   {
      _query_template = "";
      for( auto& field : _include )
      {
         if( _output_fields.has( field ) )
         {
            _query_template += (_query_template.empty() ? "" : ", ") + _output_fields.get( field ) + " as " + field;
         }
         // else
         // {
         //    for ($i = 0; $i < count($this->include); $i++) {
         //       if (isset($this->include[$i]) && $this->include[$i] == $field) {
         //          echo $this->include[$i] . " = $field\n";
         //          unset($this->include[$i]);
         //          break;
         //       }
         //    }
         // }
      }

      _query_template = "select " + _query_template + " from " + _table_name + " where ";
    
      if( _type != "box" && _box_side > 0.0 )
      {
         if( _output_fields.has( "halo_pos1" ) && _output_fields.has( "halo_pos2" ) && _output_fields.has( "halo_pos3" ) )
         {
            _query_template += " -halo_pos1- < -halo_pos1_max- and -halo_pos1- > -halo_pos1_min- ";
            _query_template += " and -halo_pos2- < -halo_pos2_max- and -halo_pos2- > -halo_pos2_min- ";
            _query_template += " and -halo_pos3- < -halo_pos3_max- and -halo_pos3- > -halo_pos3_min- ";
            _query_template += " and sqrt(pow(-halo_pos1-,2)+pow(-halo_pos2-,2)+pow(-halo_pos3-,2)) < -max_dist- ";
            _query_template += " and sqrt(pow(-halo_pos1-,2)+pow(-halo_pos2-,2)+pow(-halo_pos3-,2)) >= -last_dist- ";
         } else {
            _query_template += " -pos1- < -pos1_max- and -pos1- > -pos1_min- ";
            _query_template += " and -pos2- < -pos2_max- and -pos2- > -pos2_min- ";
            _query_template += " and -pos3- < -pos3_max- and -pos3- > -pos3_min- ";
            _query_template += " and sqrt(pow(-pos1-,2)+pow(-pos2-,2)+pow(-pos3-,2)) < -max_dist- ";
            _query_template += " and sqrt(pow(-pos1-,2)+pow(-pos2-,2)+pow(-pos3-,2)) >= -last_dist- ";
         }
         _query_template += " and sqrt(pow(-pos1-,2)+pow(-pos2-,2)+pow(-pos3-,2)) < " + to_string( _redshift_to_distance( _z_max ) );
         _query_template += " and -pos1-/(sqrt(pow(-pos1-,2)+pow(-pos2-,2))) > " + to_string( cos( _ra_max ) );
         _query_template += " and -pos1-/(sqrt(pow(-pos1-,2)+pow(-pos2-,2))) < " + to_string( cos( _ra_min ) );
         _query_template += " and sqrt(pow(-pos1-,2)+pow(-pos2-,2))/(sqrt(pow(-pos1-,2)+pow(-pos2-,2)+pow(-pos3-,2))) > " + to_string( cos( _dec_max ) );
         _query_template += " and sqrt(pow(-pos1-,2)+pow(-pos2-,2))/(sqrt(pow(-pos1-,2)+pow(-pos2-,2)+pow(-pos3-,2))) < " + to_string( cos( _dec_min ) );
      }
      else
      {
         if( _box_side > 0.0 )
         {
            _query_template += str( format( " -pos1- < %1%  and -pos2- < %2% and -pos3- < %3% " ) % _output_box_size % _output_box_size % _output_box_size );
         }
         else
         {
            _query_template += str( format( " redshift_real > %1% and redshift_real < %2%" ) % _z_min % _z_max );
         }
      }

      if( _filter != "" )
      {
         if( _filter_min != "" )
         {
            _query_template += str( format( " and %1% >= %2%" ) % _output_fields.get( _filter ) % _filter_min );
         }
         if( _filter_max != "" )
         {
            _query_template += str( format( " and %1% <= %2%" ) % _output_fields.get( _filter ) % _filter_max );
         }
      }
   }

   void
   lightcone::_db_connect( soci::session& sql )
   {
      try
      {
         if( !_sqlite_filename.empty() )
         {
            sql.open( soci::sqlite3, _sqlite_filename );
         }
         else
         {
            ASSERT( 0 );
            // sql.open( soci::mysql, str( format( "host=%1% db=%2% user=%3% password='%4'" ) % _dbhost % _dbname % _dbuser % _dbpass ) );
         }
      }
      catch( const std::exception& ex )
      {
         // TODO: Handle database errors.
         ASSERT( 0 );
      }
   }
}
