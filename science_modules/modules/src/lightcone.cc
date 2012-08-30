#include <fstream>
#include <boost/range.hpp>
#include <boost/algorithm/string/replace.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/tokenizer.hpp>
#include <soci/sqlite3/soci-sqlite3.h>
#include "lightcone.hh"

using namespace hpc;
using boost::format;
using boost::str;
using boost::algorithm::replace_all;

namespace tao {

   lightcone::lightcone()
      : _connected( false ),
        _box_side( 1.0 ),
        _z_min( 0.0 ),
        _z_max( 0.0 ),
        _use_random( true ),
        _unique( false ),
        _unique_offs_x( 0.0 ),
        _unique_offs_y( 0.0 ),
        _unique_offs_z( 0.0 ),
        _H0( 100.0 ),
        _x0( 0.0 ),
        _y0( 0.0 ),
        _z0( 0.0 )
   {
   }

   lightcone::~lightcone()
   {
   }

   ///
   ///
   ///
   void
   lightcone::setup_options( options::dictionary& dict,
                             optional<const string&> prefix )
   {
      dict.add_option( new options::string( "database_type" ), prefix );
      dict.add_option( new options::string( "database_name" ), prefix );
      dict.add_option( new options::string( "database_host", string() ), prefix );
      dict.add_option( new options::string( "database_user", string() ), prefix );
      dict.add_option( new options::string( "database_pass", string() ), prefix );
      dict.add_option( new options::string( "table_name_template", "snapshot_" ), prefix );
      dict.add_option( new options::string( "box_type" ), prefix );
      dict.add_option( new options::real( "box_side" ), prefix );
      dict.add_option( new options::string( "snapshots" ), prefix );
      dict.add_option( new options::real( "z_max" ), prefix );
      dict.add_option( new options::real( "z_min" ), prefix );
      dict.add_option( new options::real( "z_snap" ), prefix );
      dict.add_option( new options::real( "box_size" ), prefix );
      dict.add_option( new options::real( "rasc_min", 0.0 ), prefix );
      dict.add_option( new options::real( "rasc_max", 90.0 ), prefix );
      dict.add_option( new options::real( "decl_min", 0.0 ), prefix );
      dict.add_option( new options::real( "decl_max", 90.0 ), prefix );
      dict.add_option( new options::real( "H0", 100.0 ), prefix );
   }

   ///
   ///
   ///
   void
   lightcone::setup_options( hpc::options::dictionary& dict,
                             const char* prefix )
   {
      setup_options( dict, string( prefix ) );
   }

   ///
   /// Initialise the module.
   ///
   void
   lightcone::initialise( const options::dictionary& dict,
                          optional<const string&> prefix )
   {
      LOG_ENTER();

      _setup_params( dict, prefix );
      _setup_query_template();

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::initialise( hpc::options::dictionary& dict,
                          const char* prefix )
   {
      initialise( dict, string( prefix ) );
   }

   ///
   /// Run the module.
   ///
   void
   lightcone::run()
   {
      LOG_ENTER();

//       // Connect to the database.
//       _db_connect( _sql );

//       // TODO: Check that any output databases have been created,
//       //       or create them now.

//       // _open_bin_file();

//       // Prepare the last max distance processed value.
//       _last_max_dist_processed = (_z_min > 0.0) ? _redshift_to_distance( _z_min ) : 0.0;

//       if( _box_type != "box" && _box_side > 0.0 )
//       {
//          LOGLN( "Build cone, simulation box side length: ", _box_side );

//          // Iterate over the reversed snapshot indices.
//          LOGLN( "Iterating over ", _snaps.size(), " snapshots." );
//          for( mpi::lindex ii = 0; ii < _snaps.size(); ++ii )
//          {
//             LOGLN( "Snapshot ", ii, ", redshift ", _snaps[ii], setindent( 2 ) );

//             // Terminate the loop if the redshift is outside our maximum.
//             // This is why we reversed the snapshots.
//             if( _snaps[ii] > _z_max )
//             {
//                LOGLN( "Exceeded maximum redshift of ", _z_max, setindent( -2 ) );
//                break;
//             }

//             real_type z_max = _z_max;
//             mpi::lindex cur_snap_idx = ii;
//             optional<mpi::lindex> next_snap_idx;
//             if( ii != _snaps.size() - 1 )
//             {
//                next_snap_idx = ii + 1;
//                z_max = std::min( z_max, _snaps[*next_snap_idx] );
//                // auto max_dist = _redshift_to_distance( _snaps[*next_snap_idx] );
//             }
//             LOGLN( "Current snapshot index: ", cur_snap_idx );
// #ifndef NLOG
//             if( next_snap_idx )
//                LOGLN( "Next snapshot index: ", *next_snap_idx );
//             else
//                LOGLN( "No next snapshot." );
// #endif
//             LOGLN( "Max redshift: ", z_max );
//             LOGLN( "Max distance: ", _redshift_to_distance( z_max ) );
//             LOGLN( "Last max distance: ", _last_max_dist_processed );

//             list<array<real_type,3>> boxes;
//             _get_boxes( z_max, boxes );
//             LOGLN( "Boxes: ", boxes );
//             for( auto& box : boxes )
//                _build_pixels( cur_snap_idx, next_snap_idx, _x0 + box[0], _y0 + box[1], _z0 + box[2] );

//             if( next_snap_idx )
//             {
//                real_type dist = _redshift_to_distance( _snaps[*next_snap_idx] );
//                _last_max_dist_processed = _last_max_dist_processed < dist ? dist : _last_max_dist_processed;
//             }

//             LOG( setindent( -2 ) );
//          }
//       }
//       else if( _box_side > 0.0 )
//       {
//          LOGLN( "Selecting box, with side length: ", _box_side );
//          auto it = std::find( _snaps.begin(), _snaps.end(), _z_snap );
//          ASSERT( it != _snaps.end() );
//          mpi::lindex idx = it - _snaps.begin();
//          _build_pixels( idx, idx, _x0, _y0, _z0 );
//       }
//       else
//       {
//          LOGLN( "Have an empty domain." );
//          // TODO: Zero sized box, should report an error?
//          // _build_pixels( 0, 0, 0, 0, 0 );
//       }

//       // TODO: If we outputted to a database, close it off.

//       // TODO: If we outputted to a binary format, close that off too.

      LOG_EXIT();
   }

   ///
   /// Begin iterating over galaxies.
   ///
   void
   lightcone::begin()
   {
      LOG_ENTER();

      // Connect to the database.
      _db_connect( _sql );

      if( _box_type != "box" && _box_side > 0.0 )
      {
         LOGLN( "Build cone, simulation box side length: ", _box_side );

         // Iterate over the reversed snapshot indices.
         LOGLN( "Iterating over ", _snaps.size(), " snapshots." );
         _cur_snap = 0;
         if( _cur_snap < _snaps.size() )
            _settle_snap();
      }
      else if( _box_side > 0.0 )
      {
         LOGLN( "Selecting box, with side length: ", _box_side );
         auto it = std::find( _snaps.begin(), _snaps.end(), _z_snap );
         ASSERT( it != _snaps.end() );
         mpi::lindex idx = it - _snaps.begin();
         // TODO: Setup ranges.
         _build_pixels( _x0, _y0, _z0 );

         // Set the current snapshot to the end to be sure we will
         // terminate as expected.
         _cur_snap = _snaps.size();
      }
      else
      {
         LOGLN( "Have an empty domain." );
         _cur_snap = _snaps.size();
      }

      LOG_EXIT();
   }

   ///
   /// Check for completed iteration.
   ///
   bool
   lightcone::done()
   {
      LOG_ENTER();

      // We need botht the row check and the snapshot check to catch
      // the box and cone versions.
      LOGLN( "Current snapshot ", _cur_snap, "/", _snaps.size() );
      bool result = (_cur_row == _rows->end() && _cur_snap == _snaps.size());
      LOGLN( "Finished: ", result );

      // If we are done, close the database.
      if( result )
         _db_disconnect();

      LOG_EXIT();
      return result;
   }

   ///
   /// Advance to next galaxy.
   ///
   void
   lightcone::operator++()
   {
      LOG_ENTER();

      if( ++_cur_row == _rows->end() )
      {
         LOGLN( "Finished iterating over current rowset." );
         if( _box_type != "box" )
         {
            if( ++_cur_box == _boxes.end() ||
                (_settle_box(), _cur_box == _boxes.end()) )
            {
               LOGLN( "Finished iterating over current boxes." );
               if( ++_cur_snap != _snaps.size() )
                  _settle_snap();
            }
         }
      }

      LOG_EXIT();
   }

   ///
   /// Get current galaxy.
   ///
   const lightcone::row_type&
   lightcone::operator*() const
   {
      return *_cur_row;
   }

   void
   lightcone::_settle_snap()
   {
      LOG_ENTER();

      do
      {
         LOGLN( "Current snapshot index: ", _cur_snap );

         // Prepare my redshift range for this snapshot.
         if( _cur_snap == 0 )
         {
            // For the first snapshot use +1/2.
            _z_range.set( _snaps[_cur_snap], _snaps[_cur_snap + 1] );
            _z_range.set_finish( _z_range.finish() - 0.5*_z_range.length() );
         }
         else if( _cur_snap == _snaps.size() - 1 )
         {
            // For the last snapshot use -1/2.
            _z_range.set( _snaps[_cur_snap - 1], _snaps[_cur_snap] );
            _z_range.set_start( _z_range.start() + 0.5*_z_range.length() );
         }
         else
         {
            // For internal snapshots use (+/-)1/2. Assumes _z_range.finish
            // is set to the previous snapshot's finish point.
            _z_range.set_start( _z_range.finish() );
            _z_range.set_finish( _snaps[_cur_snap] + 0.5*(_snaps[_cur_snap + 1] - _snaps[_cur_snap]) );
         }
         LOGLN( "Unlimited redshift range: ", _z_range );

         // If we have moved beyond the maximum range we can finish now.
         if( _z_range.start() > _z_max )
         {
            LOGLN( "Exceeded maximum redshift of ", _z_max );
            _cur_snap = _snaps.size();
            break;
         }

         // Only proceed to use this range if it exists somewhere within
         // the cutoff points.
         if( _z_range.finish() >= _z_min )
         {
            // Limit the redshift range.
            _z_range.set_start( std::max( _z_range.start(), _z_min ) );
            _z_range.set_finish( std::min( _z_range.finish(), _z_max ) );
            LOGLN( "Final redshift range: ", _z_range );

            _dist_range.set( _redshift_to_distance( _z_range.start() ), _redshift_to_distance( _z_range.finish() ) );
            LOGLN( "Distance range: ", _dist_range );

            _get_boxes( _boxes );
            LOGLN( "Boxes: ", _boxes );
            _cur_box = _boxes.begin();
            _settle_box();
         }
      }
      while( _cur_box == _boxes.end() && ++_cur_snap < _snaps.size() );

      LOG_EXIT();
   }

   void
   lightcone::_settle_box()
   {
      LOG_ENTER();

      do
      {
         const array<real_type,3>& box = *_cur_box;
         LOGLN( "Using box ", box );
         _build_pixels( _x0 + box[0], _y0 + box[1], _z0 + box[2] );
#ifndef NLOG
         if( _cur_row == _rows->end() )
            LOGLN( "There are no objects in this box." );
#endif
      } while( _cur_row == _rows->end() && ++_cur_box != _boxes.end() );

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_build_pixels( real_type offs_x,
                             real_type offs_y,
                             real_type offs_z )
   {
      LOG_ENTER();

      // Produce the SQL query text.
      std::string query;
      _build_query( offs_x, offs_y, offs_z, query );

      // Execute the query and retrieve the rows.
      _rows = new soci::rowset<soci::row>( (_sql.prepare << query) );
      _cur_row = _rows->begin();

//       // Iterate over each returned row.
//       mpi::gindex num_galaxies = 0;
//       for( soci::rowset<soci::row>::const_iterator it = rowset.begin(); it != rowset.end(); ++it )
//       {
//          const soci::row& row = *it;
//          for( std::size_t ii = 0; ii < row.size(); ++ii )
//          {
//             // Writing each column is a bit annoying. I've not assumed that
//             // all fields will be double, which was assumed in the original
//             // lightcone module.
//             soci::data_type dt = row.get_properties( ii ).get_data_type();
//             if( dt == soci::dt_double )
//             {
//                double val = row.get<double>( ii );
//                _bin_file.write( (char*)&val, sizeof(double) );
//             }
//             else if( dt == soci::dt_integer )
//             {
//                int val = row.get<int>( ii );
//                _bin_file.write( (char*)&val, sizeof(int) );
//             }
//             else if( dt == soci::dt_unsigned_long )
//             {
//                unsigned long val = row.get<unsigned long>( ii );
//                _bin_file.write( (char*)&val, sizeof(unsigned long) );
//             }
//             else if( dt == soci::dt_long_long )
//             {
//                long long val = row.get<long long>( ii );
//                _bin_file.write( (char*)&val, sizeof(long long) );
//             }
//             else if( dt == soci::dt_string )
//             {
//                std::string val = row.get<std::string>( ii );
//                _bin_file.write( (char*)val.c_str(), sizeof(char)*val.size() );
//             }
// #ifndef NDEBUG
//             else
//                ASSERT( 0 );
// #endif
//          }
//          ++num_galaxies;
//       }

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_build_query( real_type offs_x,
                            real_type offs_y,
                            real_type offs_z,
                            std::string& query )
   {
      LOG_ENTER();

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

      // Cache some values.
      real_type z_min = _z_range.start();
      real_type z_max = _z_range.finish();
      real_type max_dist = _dist_range.finish();
      real_type min_dist = _dist_range.start();

      real_type halo_pos1_max = max_dist*cos( ra_min )*cos( dec_min );
      real_type halo_pos2_max = max_dist*sin( ra_max )*cos( dec_min );
      real_type halo_pos3_max = max_dist*sin( dec_max );
      real_type halo_pos1_min = min_dist*cos( ra_max )*cos( dec_max );
      real_type halo_pos2_min = min_dist*sin( ra_min )*cos( dec_max );
      real_type halo_pos3_min = min_dist*sin( dec_min );
      LOG( "Halo position range: (", halo_pos1_min, ", ", halo_pos2_min, ", ", halo_pos3_min, ")" );
      LOGLN( " - (", halo_pos1_max, ", ", halo_pos2_max, ", ", halo_pos3_max, ")" );

      // Apply all my current values to the query template to build up
      // the final SQL query string.
      query = _query_template;
      replace_all( query, "-z1-", to_string( z_min ) );
      replace_all( query, "-z2-", to_string( z_max ) );
      replace_all( query, "-dec_min-", to_string( dec_min ) ); // TODO: Is this okay as radians?
      replace_all( query, "-pos1-", pos1 );
      replace_all( query, "-pos2-", pos2 );
      replace_all( query, "-pos3-", pos3 );
      replace_all( query, "-pos1_max-", to_string( halo_pos1_max ) );
      replace_all( query, "-pos2_max-", to_string( halo_pos2_max ) );
      replace_all( query, "-pos3_max-", to_string( halo_pos3_max ) );
      replace_all( query, "-pos1_min-", to_string( halo_pos1_min ) );
      replace_all( query, "-pos2_min-", to_string( halo_pos2_min ) );
      replace_all( query, "-pos3_min-", to_string( halo_pos3_min ) );
      replace_all( query, "-halo_pos1-", halo_pos1 );
      replace_all( query, "-halo_pos2-", halo_pos2 );
      replace_all( query, "-halo_pos3-", halo_pos3 );
      replace_all( query, "-halo_pos1_max-", to_string( halo_pos1_max ) );
      replace_all( query, "-halo_pos2_max-", to_string( halo_pos2_max ) );
      replace_all( query, "-halo_pos3_max-", to_string( halo_pos3_max ) );
      replace_all( query, "-halo_pos1_min-", to_string( halo_pos1_min ) );
      replace_all( query, "-halo_pos2_min-", to_string( halo_pos2_min ) );
      replace_all( query, "-halo_pos3_min-", to_string( halo_pos3_min ) );
      replace_all( query, "-vel1-", to_string( vel1 ) );
      replace_all( query, "-vel2-", to_string( vel2 ) );
      replace_all( query, "-vel3-", to_string( vel3 ) );
      replace_all( query, "snapshot_", str( format( "snapshot_%1$03d" ) % _cur_snap ) );
      replace_all( query, "-max_dist-", to_string( max_dist ) );
      replace_all( query, "-last_dist-", to_string( min_dist ) );

      LOGLN( "Query: ", query );
      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_random_rotation_and_shifting( vector<std::string>& ops )
   {
      LOG_ENTER();

      // Four values (p, h, v, s) in three groups.
      ops.resize( 12 );

      // Common values.
      ops[2] = "Vel1";
      ops[3] = "Spin1";
      ops[6] = "Vel2";
      ops[7] = "Spin2";
      ops[10] = "Vel3";
      ops[11] = "Spin3";

      if( _box_type == "box" || !_use_random )
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
         if( _dbtype == "sqlite" )
         {
            ops[0] = str( format( "(case sign(%1%+Pos1-%2%) when 1 then %3%+Pos1 else Pos1+%4%-%5% end)" ) % offs1 % _box_side % offs1 % offs1 % _box_side );
            ops[1] = str( format( "(case sign(%1%+halo_pos1-%2%) when 1 then %3%+halo_pos1 else halo_pos1+%4%-%5% end)" ) % offs1 % _box_side % offs1 % offs1 % _box_side );
         }
         else
         {
            ops[0] = str( format( "if(%1%+Pos1<%2%,%3%+Pos1,Pos1+%4%-%5%)" ) % offs1 % _box_side % offs1 % offs1 % _box_side );
            ops[1] = str( format( "if(%1%+halo_pos1<%2%,%3%+halo_pos1,halo_pos1+%4%-%5%)" ) % offs1 % _box_side % offs1 % offs1 % _box_side );
         }
         ops[2] = "Vel1";
         ops[3] = "Spin1";

         // Rotation 2.
         if( _dbtype == "sqlite" )
         {
            ops[4] = str( format( "(case sign(%1%+Pos2-%2%) when 1 then %3%+Pos2 else Pos2+%4%-%5% end)" ) % offs2 % _box_side % offs2 % offs2 % _box_side );
            ops[5] = str( format( "(case sign(%1%+halo_pos2-%2%) when 1 then %3%+halo_pos2 else halo_pos2+%4%-%5% end)" ) % offs2 % _box_side % offs2 % offs2 % _box_side );
         }
         else
         {
            ops[4] = str( format( "if(%1%+Pos2<%2%,%3%+Pos2,Pos2+%4%-%5%)" ) % offs2 % _box_side % offs2 % offs2 % _box_side );
            ops[5] = str( format( "if(%1%+halo_pos2<%2%,%3%+halo_pos2,halo_pos2+%4%-%5%)" ) % offs2 % _box_side % offs2 % offs2 % _box_side );
         }
         ops[6] = "Vel2";
         ops[7] = "Spin2";

         // Rotation 3.
         if( _dbtype == "sqlite" )
         {
            ops[8] = str( format( "(case sign(%1%+Pos3-%2%) when 1 then %3%+Pos3 else Pos3+%4%-%5% end)" ) % offs3 % _box_side % offs3 % offs3 % _box_side );
            ops[9] = str( format( "(case sign(%1%+halo_pos3-%2%) when 1 then %3%+halo_pos3 else halo_pos3+%4%-%5% end)" ) % offs3 % _box_side % offs3 % offs3 % _box_side );
         }
         else
         {
            ops[8] = str( format( "if(%1%+Pos3<%2%,%3%+Pos3,Pos3+%4%-%5%)" ) % offs3 % _box_side % offs3 % offs3 % _box_side );
            ops[9] = str( format( "if(%1%+halo_pos3<%2%,%3%+halo_pos3,halo_pos3+%4%-%5%)" ) % offs3 % _box_side % offs3 % offs3 % _box_side );
         }
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

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_get_boxes( list<array<real_type,3>>& boxes )
   {
      LOG_ENTER();

      // Start fresh.
      boxes.clear();

      // Only run the loop if the distance is greater than the box side length.
      if( _dist_range.finish() > _box_side )
      {
         LOGLN( "Maximum distanceof ", _dist_range.finish(), " greater than box side of ", _box_side, ", calculating boxes." );

         // TODO: Removed the " + _box_side" from each conditional, it seems
         // to me that keeping it in just adds one extra useless iteration
         // per loop.
         for( real_type ii = 0.0; ii <= _dist_range.finish(); ii += _box_side )
         {
            for( real_type jj = 0.0; jj <= _dist_range.finish(); jj += _box_side )
            {
               for( real_type kk = 0.0; kk <= _dist_range.finish(); kk += _box_side )
               {
                  if( (sqrt( pow( ii + _box_side + _unique_offs_x, 2.0 ) + 
                             pow( jj + _box_side + _unique_offs_y, 2.0 ) + 
                             pow( kk + _box_side + _unique_offs_z, 2.0 ) ) > (_dist_range.start() - _box_side)) &&
                      (((ii + _box_side + _unique_offs_x)/sqrt( pow( ii + _box_side + _unique_offs_x, 2.0) + 
                                                                pow( jj, 2.0 ) )) > cos( to_radians( _ra_max ) )) &&
                      (ii/sqrt( pow( ii, 2.0 ) + pow( jj + _box_side + _unique_offs_y, 2.0 ) ) < cos( to_radians( _ra_min ) )) &&
                      ((sqrt( pow( ii + _box_side + _unique_offs_x, 2.0 ) + pow( jj + _box_side + _unique_offs_y, 2.0 )))/sqrt( pow( ii + _box_side + _unique_offs_x, 2.0 ) + pow( jj + _box_side + _unique_offs_y, 2.0 ) + pow( kk, 2.0 ) ) > cos( to_radians( _dec_max ) )) &&
                      ((sqrt( pow( ii, 2.0 ) + pow( jj, 2.0 )))/sqrt( pow( ii, 2.0 ) + pow( jj, 2.0 ) + pow( kk + _box_side + _unique_offs_z, 2.0 ) ) < cos( to_radians( _dec_min ) )) )
                  {
                     boxes.push_back( array<real_type,3>( ii, jj, kk ) );
                  }
               }
            }
         }
      }
      else
      {
         LOGLN( "Maximum distance of ", _dist_range.finish(), " less than box side of ", _box_side, ", using single box." );
         boxes.push_back( array<real_type,3>( 0.0, 0.0, 0.0 ) );
      }

      LOG_EXIT();
   }

   ///
   ///
   ///
   lightcone::real_type
   lightcone::_redshift_to_distance( real_type redshift )
   {
      LOG_ENTER();

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

      LOG_EXIT();
      return d;
   }

   ///
   /// Setup parameters.
   ///
   /// For performance sake, we cache all the parameters we need
   /// from the parameter dictionary.
   ///
   void
   lightcone::_setup_params( const options::dictionary& dict,
                             optional<const string&> prefix )
   {
      LOG_ENTER();

      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      // Extract database details.
      _dbtype = sub.get<string>( "database_type" );
      _dbname = sub.get<string>( "database_name" );
      _dbhost = sub.get<string>( "database_host" );
      _dbuser = sub.get<string>( "database_user" );
      _dbpass = sub.get<string>( "database_pass" );
      _table_name = sub.get<string>( "table_name_template" );

      // Get box type and side length.
      _box_type = sub.get<string>( "box_type" );
      _box_side = sub.get<real_type>( "box_side" );
      LOGLN( "Read box type '", _box_type, "' and side length ", _box_side );

      // Extract and parse the snapshot redshifts.
      _snaps.clear();
      string snaps_str = sub.get<string>( "snapshots" );
      boost::tokenizer<boost::char_separator<char> > tokens( snaps_str, boost::char_separator<char>( "," ) );
      for( const auto& redshift : tokens )
         _snaps.push_back( boost::lexical_cast<double>( boost::trim_copy( redshift ) ) );

      // Reverse the snapshots to start most recent (lowest redshift to highest).
      std::reverse( _snaps.begin(), _snaps.end() );
      LOGLN( "Snapshots: ", _snaps );

      // If not doing a simple box we need at least two snapshots.
      ASSERT( _box_type == "box" || _snaps.size() > 1 );

      // Redshift ranges.
      real_type snap_z_max = _snaps.back(), snap_z_min = _snaps.front();
      _z_max = sub.get<real_type>( "z_max", snap_z_max );
      _z_max = std::min( _z_max, snap_z_max );
      _z_min = sub.get<real_type>( "z_min", snap_z_min );
      LOGLN( "Redshift range: (", _z_min, ", ", _z_max, ")" );

      // Right ascension.
      _ra_min = sub.get<real_type>( "rasc_min" );
      if( _ra_min < 0.0 )
         _ra_min = 0.0;
      _ra_max = sub.get<real_type>( "rasc_max" ); // TODO divide by 60.0?
      if( _ra_max >= 89.9999999 )
         _ra_max = 89.9999999;
      if( _ra_min > _ra_max )
         _ra_min = _ra_max;
      LOGLN( "Have right ascension range ", _ra_min, " - ", _ra_max );

      // Declination.
      _dec_min = sub.get<real_type>( "decl_min" );
      if( _dec_min < 0.0 )
         _dec_min = 0.0;
      _dec_max = sub.get<real_type>( "decl_max" ); // TODO divide by 60.0?
      if( _dec_max >= 89.9999999 )
         _dec_max = 89.9999999;
      if( _dec_min > _dec_max )
         _dec_min = _dec_max;
      LOGLN( "Have declination range ", _dec_min, " - ", _dec_max );

      // For the box type.
      if( _box_type == "box" )
      {
         _z_snap = sub.get<real_type>( "z_snap" );
         _box_size = sub.get<real_type>( "box_size" );
      }

      // Astronomical values.
      _H0 = sub.get<real_type>( "H0" );
      LOGLN( "Using H0 = ", _H0 );

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_setup_query_template()
   {
      LOG_ENTER();

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
      if( _query_template == "" )
         _query_template = "*";

      _query_template = "select " + _query_template + " from " + _table_name + " where";
    
      if( _box_type != "box" && _box_side > 0.0 )
      {
         if( _output_fields.has( "halo_pos1" ) && _output_fields.has( "halo_pos2" ) && _output_fields.has( "halo_pos3" ) )
         {
            _query_template += " -halo_pos1- < -halo_pos1_max- and -halo_pos1- >= -halo_pos1_min-";
            _query_template += " and -halo_pos2- < -halo_pos2_max- and -halo_pos2- >= -halo_pos2_min-";
            _query_template += " and -halo_pos3- < -halo_pos3_max- and -halo_pos3- >= -halo_pos3_min-";
            _query_template += " and sqrt(pow(-halo_pos1-,2)+pow(-halo_pos2-,2)+pow(-halo_pos3-,2)) < -max_dist-";
            _query_template += " and sqrt(pow(-halo_pos1-,2)+pow(-halo_pos2-,2)+pow(-halo_pos3-,2)) >= -last_dist-";
         } else {
            _query_template += " -pos1- < -pos1_max- and -pos1- >= -pos1_min-";
            _query_template += " and -pos2- < -pos2_max- and -pos2- >= -pos2_min-";
            _query_template += " and -pos3- < -pos3_max- and -pos3- >= -pos3_min-";
            _query_template += " and sqrt(pow(-pos1-,2)+pow(-pos2-,2)+pow(-pos3-,2)) < -max_dist-";
            _query_template += " and sqrt(pow(-pos1-,2)+pow(-pos2-,2)+pow(-pos3-,2)) >= -last_dist-";
         }
         _query_template += " and sqrt(pow(-pos1-,2)+pow(-pos2-,2)+pow(-pos3-,2)) < " + to_string( _redshift_to_distance( _z_max ) );
         _query_template += " and -pos1-/(sqrt(pow(-pos1-,2)+pow(-pos2-,2))) > " + to_string( cos( to_radians( _ra_max ) ) );
         _query_template += " and -pos1-/(sqrt(pow(-pos1-,2)+pow(-pos2-,2))) < " + to_string( cos( to_radians( _ra_min ) ) );
         _query_template += " and sqrt(pow(-pos1-,2)+pow(-pos2-,2))/(sqrt(pow(-pos1-,2)+pow(-pos2-,2)+pow(-pos3-,2))) > " + to_string( cos( to_radians( _dec_max ) ) );
         _query_template += " and sqrt(pow(-pos1-,2)+pow(-pos2-,2))/(sqrt(pow(-pos1-,2)+pow(-pos2-,2)+pow(-pos3-,2))) < " + to_string( cos( to_radians( _dec_min ) ) );
      }
      else
      {
         if( _box_side > 0.0 )
         {
            _query_template += str( format( " -pos1- < %1%  and -pos2- < %2% and -pos3- < %3% " ) % _box_size % _box_size % _box_size );
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

      LOGLN( "Query template: ", _query_template );
      LOG_EXIT();
   }

   void
   lightcone::_db_connect( soci::session& sql )
         
   {
      LOG_ENTER();

      // First check if the database is already open, and close if so.
      _db_disconnect();

      LOGLN( "Connecting to ", _dbtype, " database: ", _dbname );
      try
      {
         if( _dbtype == "sqlite" )
            sql.open( soci::sqlite3, _dbname );
         else
         {
            ASSERT( 0 );
            // sql.open( soci::mysql, str( format( "host=%1% db=%2% user=%3% password='%4'" ) % _dbhost % _dbname % _dbuser % _dbpass ) );
         }
      }
      catch( const std::exception& ex )
      {
         // TODO: Handle database errors.
         LOGLN( "Error opening database connection: ", ex.what() );
         ASSERT( 0 );
      }

      // Mark connection.
      _connected = true;

      LOG_EXIT();
   }

   void
   lightcone::_db_disconnect()
   {
      if( _connected )
      {
         LOGLN( "Disconnecting from database." );
         _sql.close();
         _connected = false;
      }
   }

   void
   lightcone::_open_bin_file()
   {
      LOG_ENTER();

      if( !_bin_filename.empty() )
      {
         _bin_file.open( _bin_filename, std::ios::out | std::ios::binary );
      }

      LOG_EXIT();
   }
}
