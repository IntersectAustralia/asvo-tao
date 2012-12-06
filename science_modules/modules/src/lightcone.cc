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
      : module(),
        _z_min( 0.0 ),
        _z_max( 0.0 ),
        _use_random( false ),
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
      dict.add_option( new options::string( "database-type", "postgresql" ), prefix );
      dict.add_option( new options::string( "database-name", "millennium_full_mpi" ), prefix );
      dict.add_option( new options::string( "database-host", "tao02.hpc.swin.edu.au" ), prefix );
      dict.add_option( new options::string( "database-port", "3306" ), prefix );
      dict.add_option( new options::string( "database-user", string() ), prefix );
      dict.add_option( new options::string( "database-pass", string() ), prefix );
      dict.add_option( new options::string( "query-type", "light-cone" ), prefix );
      dict.add_option( new options::real( "redshift-max" ), prefix );
      dict.add_option( new options::real( "redshift-min" ), prefix );
      dict.add_option( new options::real( "z_snap" ), prefix );
      dict.add_option( new options::real( "box_size" ), prefix );
      dict.add_option( new options::real( "ra-min", 0.0 ), prefix );
      dict.add_option( new options::real( "ra-max", 90.0 ), prefix );
      dict.add_option( new options::real( "dec-min", 0.0 ), prefix );
      dict.add_option( new options::real( "dec-max", 90.0 ), prefix );
      dict.add_option( new options::real( "H0", 100.0 ), prefix );
   }

   ///
   ///
   ///
   void
   lightcone::setup_options( options::dictionary& dict,
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

      _read_options( dict, prefix );
      _setup_query_template();

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::initialise( const options::dictionary& dict,
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
      LOG_EXIT();
   }

   ///
   /// Begin iterating over galaxies.
   ///
   void
   lightcone::begin()
   {
      LOG_ENTER();

      if( _box_type != "box" )
      {
	 // The outer loop is over the boxes.
	 _get_boxes( _boxes );
	 LOGDLN( "Boxes: ", _boxes );
	 _cur_box = _boxes.begin();
	 _settle_box();
      }
      else
      {
         // auto it = std::find( _snap_redshifts.begin(), _snap_redshifts.end(), _z_snap );
         // ASSERT( it != _snap_redshifts.end() );
         // mpi::lindex idx = it - _snap_redshifts.begin();
         // // TODO: Setup ranges.
         // _build_pixels( _x0, _y0, _z0 );

         // // Set the current snapshot to the end to be sure we will
         // // terminate as expected.
         // _cur_snap = _snap_idxs.size();
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

      // We are done when we are out of tables.
      bool result = (_cur_table == _table_names.size());

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
         LOGDLN( "Finished iterating over current rowset." );
         if( _box_type != "box" )
         {
	    if( ++_cur_table == _table_names.size() ||
		(_settle_table(), _cur_table == _table_names.size()) )
            {
               LOGDLN( "Finished iterating over current boxes." );
               if( ++_cur_box != _boxes.end() )
                  _settle_box();
            }
         }
      }

      LOG_EXIT();
   }

   ///
   /// Get current galaxy.
   ///
   const galaxy
   lightcone::operator*() const
   {
#ifndef NDEBUG
      {
	 // Check that the row actually belongs in this range.
         galaxy gal( *_cur_row, *_cur_box );
         real_type dist = sqrt( pow( gal.x(), 2.0 ) + pow( gal.y(), 2.0 ) + pow( gal.z(), 2.0 ) );
         ASSERT( dist >= _dist_range.start() && dist < _dist_range.finish() );
      }
#endif
      return galaxy( *_cur_row, *_cur_box );
   }

   ///
   /// Get current redshift.
   ///
   lightcone::real_type
   lightcone::redshift() const
   {
      ASSERT( _cur_row != _rows->end() );
      return _snap_redshifts[_cur_row->get<int>( "snapnum" )];
   }

   ///
   /// Get a list of tree table names to search.
   ///
   void
   lightcone::_query_table_names( vector<string>& table_names )
   {
      LOG_ENTER();

      // Get the number of tables.
      unsigned num_tables;
      string query;
      if( _dbtype == "sqlite" )
      {
	 query = "SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND SUBSTR(name,1,5)='tree_'";
      }
      else
      {
	 query = "SELECT COUNT(table_name) FROM information_schema.tables"
	    " WHERE table_schema='public' AND SUBSTR(table_name,1,5)='tree_'";
      }
      LOGDLN( "Query for number of table names: ", query );
      _sql << query, soci::into( num_tables );
      LOGDLN( "Number of tables: ", num_tables );

      // Retrieve all the table names.
      table_names.reallocate( num_tables );
      if( _dbtype == "sqlite" )
      {
	 query = "SELECT name FROM sqlite_master WHERE type='table' AND SUBSTR(name,1,5)='tree_'";
      }
      else
      {
	 query = "SELECT table_name FROM information_schema.tables"
	    " WHERE table_schema='public' AND SUBSTR(table_name,1,5)='tree_'";
      }
      LOGDLN( "Query for table names: ", query );
      _sql << query, soci::into( (std::vector<std::string>&)table_names );
      LOGDLN( "Table names: ", table_names );

      LOG_EXIT();
   }

   void
   lightcone::_settle_table()
   {
      LOG_ENTER();

      // Keep moving over tables until we find one that
      // returns boxes or we run out of tables.
      do
      {
         LOGDLN( "Current table index: ", _cur_table );
	 LOGDLN( "Current table name: ", _table_names[_cur_table] );
	 LOGILN( "Table ", _cur_table, " of ", _table_names.size() );

	 const array<real_type,3>& box = *_cur_box;
         _build_pixels( _x0 + box[0], _y0 + box[1], _z0 + box[2] );
	 LOGDLN( "Any objects in this box/table: ", ((_cur_row != _rows->end()) ? "true" : "false") );
      }
      while( _cur_row == _rows->end() && ++_cur_table != _table_names.size() );

      LOG_EXIT();
   }

   void
   lightcone::_settle_box()
   {
      LOG_ENTER();

      do
      {
         LOGDLN( "Using box ", *_cur_box );
         LOGDLN( "Iterating over ", _table_names.size(), " tables." );
         _cur_table = 0;
         if( _cur_table < _table_names.size() )
	 {
	    // Calculate the minimum and maximum snapshots
	    // that can fall within this box.
	    const array<real_type,3>& box = *_cur_box;

	    // Calculate the minimum and maximum length in this box.
	    real_type min_len = sqrt( box[0]*box[0] + box[1]*box[1] + box[2]*box[2] );
	    real_type max_len = sqrt( (box[0] + _domain_size)*(box[0] + _domain_size) + 
				      (box[1] + _domain_size)*(box[1] + _domain_size) + 
				      (box[2] + _domain_size)*(box[2] + _domain_size) );
	    LOGDLN( "Length range is from ", min_len, " to ", max_len );

	    // Find the first redshift that is greater than my minimum.
	    for( unsigned ii = 0; ii < _snap_redshifts.size(); ++ii )
	    {
	       if( _redshift_to_distance( _snap_redshifts[ii] ) < max_len )
	       {
		  if( ii > 0 )
		     _min_snap = ii - 1;
		  else
		     _min_snap = 0;
		  LOGDLN( "Minimum snapshot is ", _min_snap, " with length of ",
			  _redshift_to_distance( _snap_redshifts[_min_snap] ) );
		  break;
	       }
	    }

	    // Find the first redshift greater than my maximum.
	    unsigned ii;
	    for( ii = _min_snap + 1; ii < _snap_redshifts.size(); ++ii )
	    {
	       if( _redshift_to_distance( _snap_redshifts[ii] ) < min_len )
	       {
		  _max_snap = ii;
		  break;
	       }
	    }
	    if( ii == _snap_redshifts.size() )
	       _max_snap = _snap_redshifts.size() - 1;
	    LOGDLN( "Maximum snapshot is ", _max_snap, " with length of ",
		    _redshift_to_distance( _snap_redshifts[_max_snap] ) );

	    // Now prepare tables.
            _settle_table();
	 }
      }
      while( _cur_table == _table_names.size() && ++_cur_box != _boxes.end() );

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
      string query;
      _build_query( offs_x, offs_y, offs_z, query );

      // Execute the query and retrieve the rows.
      _rows = new soci::rowset<soci::row>( (_sql.prepare << query) );
      _cur_row = _rows->begin();

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_build_query( real_type offs_x,
                            real_type offs_y,
                            real_type offs_z,
                            string& query )
   {
      LOG_ENTER();

      real_type ra_min = to_radians( _ra_min );
      real_type ra_max = to_radians( _ra_max );
      real_type dec_min = to_radians( _dec_min );
      real_type dec_max = to_radians( _dec_max );

      vector<string> ops;
      _random_rotation_and_shifting( ops );
      string& pos1 = ops[0];
      string& pos2 = ops[4];
      string& pos3 = ops[8];
      string& halo_pos1 = ops[1];
      string& halo_pos2 = ops[5];
      string& halo_pos3 = ops[9];
      string& vel1 = ops[2];
      string& vel2 = ops[6];
      string& vel3 = ops[10];
      string& spin1 = ops[3];
      string& spin2 = ops[7];
      string& spin3 = ops[11];

      pos1 = str( format( "(%1% + %2% - %3%)" ) % offs_x % pos1 % _x0 );
      pos2 = str( format( "(%1% + %2% - %3%)" ) % offs_y % pos2 % _y0 );
      pos3 = str( format( "(%1% + %2% - %3%)" ) % offs_z % pos3 % _z0 );
      halo_pos1 = str( format( "(%1% + %2% - %3%)" ) % offs_x % halo_pos1 % _x0 );
      halo_pos2 = str( format( "(%1% + %2% - %3%)" ) % offs_y % halo_pos2 % _y0 );
      halo_pos3 = str( format( "(%1% + %2% - %3%)" ) % offs_z % halo_pos3 % _z0 );

      // Cache some values.
      real_type z_min = _z_min;
      real_type z_max = _z_max;
      real_type max_dist = _dist_range.finish();
      real_type min_dist = _dist_range.start();

      real_type halo_pos1_max = max_dist*cos( ra_min )*cos( dec_min );
      real_type halo_pos2_max = max_dist*sin( ra_max )*cos( dec_min );
      real_type halo_pos3_max = max_dist*sin( dec_max );
      real_type halo_pos1_min = min_dist*cos( ra_max )*cos( dec_max );
      real_type halo_pos2_min = min_dist*sin( ra_min )*cos( dec_max );
      real_type halo_pos3_min = min_dist*sin( dec_min );
      LOGD( "Halo position range: (", halo_pos1_min, ", ", halo_pos2_min, ", ", halo_pos3_min, ")" );
      LOGDLN( " - (", halo_pos1_max, ", ", halo_pos2_max, ", ", halo_pos3_max, ")" );

      // Apply all my current values to the query template to build up
      // the final SQL query string.
      query = _query_template;
      replace_all( query, "-table-", _table_names[_cur_table] );
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
      replace_all( query, "-vel1-", to_string( vel1 ) );
      replace_all( query, "-vel2-", to_string( vel2 ) );
      replace_all( query, "-vel3-", to_string( vel3 ) );
      replace_all( query, "-max_dist-", to_string( max_dist ) );
      replace_all( query, "-last_dist-", to_string( min_dist ) );
      replace_all( query, "-min_snap-", to_string( _min_snap ) );
      replace_all( query, "-max_snap-", to_string( _max_snap ) );

      // Replace references to the Posx coordinates.
      replace_all( query, "Pos1", _crd_strs[0] );
      replace_all( query, "Pos2", _crd_strs[1] );
      replace_all( query, "Pos3", _crd_strs[2] );

      LOGDLN( "Query: ", query );
      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_random_rotation_and_shifting( vector<string>& ops )
   {
      LOG_ENTER();

      // Cache the current box size.
      real_type domain_size = _domain_size;

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
            ASSERT( domain_size > 0.0 );

            offs1 = generate_uniform( 0.0, domain_size*1000.0 )/1000.0;
            offs2 = generate_uniform( 0.0, domain_size*1000.0 )/1000.0;
            offs3 = generate_uniform( 0.0, domain_size*1000.0 )/1000.0;
            rnd = generate_uniform<int>( 1, 6 );
         }

         // Rotation 1.
         if( _dbtype == "sqlite" )
         {
            ops[0] = str( format( "(case sign(%1%+Pos1-%2%) when 1 then %3%+Pos1 else Pos1+%4%-%5% end)" ) % offs1 % domain_size % offs1 % offs1 % domain_size );
            ops[1] = str( format( "(case sign(%1%+halo_pos1-%2%) when 1 then %3%+halo_pos1 else halo_pos1+%4%-%5% end)" ) % offs1 % domain_size % offs1 % offs1 % domain_size );
         }
         else
         {
            ops[0] = str( format( "IF(%1% + Pos1 < %2%,%3%+Pos1,Pos1+%4%-%5%)" ) % offs1 % domain_size % offs1 % offs1 % domain_size );
            ops[1] = str( format( "IF(%1% + halo_pos1 < %2%,%3%+halo_pos1,halo_pos1+%4%-%5%)" ) % offs1 % domain_size % offs1 % offs1 % domain_size );
         }
         ops[2] = "Vel1";
         ops[3] = "Spin1";

         // Rotation 2.
         if( _dbtype == "sqlite" )
         {
            ops[4] = str( format( "(case sign(%1%+Pos2-%2%) when 1 then %3%+Pos2 else Pos2+%4%-%5% end)" ) % offs2 % domain_size % offs2 % offs2 % domain_size );
            ops[5] = str( format( "(case sign(%1%+halo_pos2-%2%) when 1 then %3%+halo_pos2 else halo_pos2+%4%-%5% end)" ) % offs2 % domain_size % offs2 % offs2 % domain_size );
         }
         else
         {
            ops[4] = str( format( "if(%1%+Pos2<%2%,%3%+Pos2,Pos2+%4%-%5%)" ) % offs2 % domain_size % offs2 % offs2 % domain_size );
            ops[5] = str( format( "if(%1%+halo_pos2<%2%,%3%+halo_pos2,halo_pos2+%4%-%5%)" ) % offs2 % domain_size % offs2 % offs2 % domain_size );
         }
         ops[6] = "Vel2";
         ops[7] = "Spin2";

         // Rotation 3.
         if( _dbtype == "sqlite" )
         {
            ops[8] = str( format( "(case sign(%1%+Pos3-%2%) when 1 then %3%+Pos3 else Pos3+%4%-%5% end)" ) % offs3 % domain_size % offs3 % offs3 % domain_size );
            ops[9] = str( format( "(case sign(%1%+halo_pos3-%2%) when 1 then %3%+halo_pos3 else halo_pos3+%4%-%5% end)" ) % offs3 % domain_size % offs3 % offs3 % domain_size );
         }
         else
         {
            ops[8] = str( format( "if(%1%+Pos3<%2%,%3%+Pos3,Pos3+%4%-%5%)" ) % offs3 % domain_size % offs3 % offs3 % domain_size );
            ops[9] = str( format( "if(%1%+halo_pos3<%2%,%3%+halo_pos3,halo_pos3+%4%-%5%)" ) % offs3 % domain_size % offs3 % offs3 % domain_size );
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

      // Cache the current box size.
      real_type domain_size = _domain_size;

      // Start fresh.
      boxes.clear();

      // Only run the loop if the distance is greater than the box side length.
      if( _dist_range.finish() > domain_size )
      {
         LOGDLN( "Maximum distanceof ", _dist_range.finish(), " greater than box side of ", domain_size, ", calculating boxes." );

         // TODO: Removed the " + domain_size" from each conditional, it seems
         // to me that keeping it in just adds one extra useless iteration
         // per loop.
         for( real_type ii = 0.0; ii <= _dist_range.finish(); ii += domain_size )
         {
            for( real_type jj = 0.0; jj <= _dist_range.finish(); jj += domain_size )
            {
               for( real_type kk = 0.0; kk <= _dist_range.finish(); kk += domain_size )
               {
                  if( (sqrt( pow( ii + domain_size + _unique_offs_x, 2.0 ) + 
                             pow( jj + domain_size + _unique_offs_y, 2.0 ) + 
                             pow( kk + domain_size + _unique_offs_z, 2.0 ) ) > (_dist_range.start() - domain_size)) &&
                      (((ii + domain_size + _unique_offs_x)/sqrt( pow( ii + domain_size + _unique_offs_x, 2.0) + 
								  pow( jj, 2.0 ) )) > cos( to_radians( _ra_max ) )) &&
                      (ii/sqrt( pow( ii, 2.0 ) + pow( jj + domain_size + _unique_offs_y, 2.0 ) ) < cos( to_radians( _ra_min ) )) &&
                      ((sqrt( pow( ii + domain_size + _unique_offs_x, 2.0 ) + pow( jj + domain_size + _unique_offs_y, 2.0 )))/sqrt( pow( ii + domain_size + _unique_offs_x, 2.0 ) + pow( jj + domain_size + _unique_offs_y, 2.0 ) + pow( kk, 2.0 ) ) > cos( to_radians( _dec_max ) )) &&
                      ((sqrt( pow( ii, 2.0 ) + pow( jj, 2.0 )))/sqrt( pow( ii, 2.0 ) + pow( jj, 2.0 ) + pow( kk + domain_size + _unique_offs_z, 2.0 ) ) < cos( to_radians( _dec_min ) )) )
                  {
                     boxes.push_back( array<real_type,3>( ii, jj, kk ) );
                  }
               }
            }
         }
      }
      else
      {
         LOGDLN( "Maximum distance of ", _dist_range.finish(), " less than box side of ", domain_size, ", using single box." );
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
   lightcone::_read_options( const options::dictionary& dict,
                             optional<const string&> prefix )
   {
      LOG_ENTER();

      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      // Extract database details.
      _dbtype = sub.get<string>( "database-type" );
      _dbname = sub.get<string>( "database-name" );
      _dbhost = sub.get<string>( "database-host" );
      _dbport = sub.get<string>( "database-port" );
      _dbuser = sub.get<string>( "database-user" );
      _dbpass = sub.get<string>( "database-pass" );

      // Connect to the database.
      _db_connect( _sql );

      // Get box type.
      _box_type = sub.get<string>( "box_type" );
      LOGDLN( "Box type '", _box_type );

      // Get the domain size.
      {
	 double size;
	 // _sql << "SELECT domain_size FROM summary", soci::into( size );
	 size = 500;
	 _domain_size = size;
	 LOGDLN( "Simulation domain size: ", _domain_size );
      }

      // Extract and parse the snapshot redshifts.
      _read_snapshots();

      // Setup the redshifts table if we are building a cone.
      if( _box_type != "box" )
	 _setup_redshift_ranges();

      // Query the table names we'll be using.
      _query_table_names( _table_names );

      // Redshift ranges.
      real_type snap_z_max = _snap_redshifts.front(), snap_z_min = _snap_redshifts.back();
      _z_max = sub.get<real_type>( "z_max", snap_z_max );
      _z_max = std::min( _z_max, snap_z_max );
      _z_min = sub.get<real_type>( "z_min", snap_z_min );
      LOGDLN( "Redshift range: (", _z_min, ", ", _z_max, ")" );

      // Create distance range.
      _dist_range.set( _redshift_to_distance( _z_min ), _redshift_to_distance( _z_max ) );
      LOGDLN( "Distance range: (", _dist_range.start(), ", ", _dist_range.finish(), ")" );

      // Right ascension.
      _ra_min = sub.get<real_type>( "ra_min" );
      if( _ra_min < 0.0 )
         _ra_min = 0.0;
      _ra_max = sub.get<real_type>( "ra_max" ); // TODO divide by 60.0?
      if( _ra_max >= 89.9999999 )
         _ra_max = 89.9999999;
      if( _ra_min > _ra_max )
         _ra_min = _ra_max;
      real_type width = _ra_max - _ra_min;
      _ra_max = _ra_min + (width*(mpi::comm::world.rank() + 1))/mpi::comm::world.size();
      _ra_min += (width*mpi::comm::world.rank())/mpi::comm::world.size();
      LOGDLN( "Have right ascension range ", _ra_min, " - ", _ra_max );

      // Declination.
      _dec_min = sub.get<real_type>( "dec_min" );
      if( _dec_min < 0.0 )
         _dec_min = 0.0;
      _dec_max = sub.get<real_type>( "dec_max" ); // TODO divide by 60.0?
      if( _dec_max >= 89.9999999 )
         _dec_max = 89.9999999;
      if( _dec_min > _dec_max )
         _dec_min = _dec_max;
      LOGDLN( "Have declination range ", _dec_min, " - ", _dec_max );

      // For the box type.
      if( _box_type == "box" )
      {
         _z_snap = sub.get<real_type>( "z_snap" );
         _box_size = sub.get<real_type>( "box_size" );
      }

      // Astronomical values.
      _H0 = sub.get<real_type>( "H0" );
      LOGDLN( "Using H0 = ", _H0 );

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_setup_query_template()
   {
      LOG_ENTER();

      // Set the coordinate strings we want to use.
      _crd_strs[0] = "posx";
      _crd_strs[1] = "posy";
      _crd_strs[2] = "posz";

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
         _query_template = "posx, posy, posz, redshift";

      _query_template = "SELECT " + _query_template + " FROM -table-";
      _query_template += " INNER JOIN redshift_ranges ON (-table-.snapnum = redshift_ranges.snapnum)";
      _query_template += " WHERE";

      if( _box_type != "box" )
      {
	 _query_template += " -table-.snapnum >= -min_snap- AND -table-.snapnum <= -max_snap-";
	 _query_template += " AND (POW(-pos1-,2) + POW(-pos2-,2) + POW(-pos3-,2)) >= "
	    "redshift_ranges.min";
	 _query_template += " AND (POW(-pos1-,2) + POW(-pos2-,2) + POW(-pos3-,2)) < "
	    "redshift_ranges.max";
	 _query_template += " AND -pos1-/(SQRT(POW(-pos1-,2) + POW(-pos2-,2))) > "
	    + to_string( cos( to_radians( _ra_max ) ) );
	 _query_template += " AND -pos1-/(SQRT(POW(-pos1-,2) + POW(-pos2-,2))) < "
	    + to_string( cos( to_radians( _ra_min ) ) );
	 _query_template += " AND SQRT(POW(-pos1-,2) + POW(-pos2-,2))/(SQRT(POW(-pos1-,2) + "
	    "POW(-pos2-,2) + POW(-pos3-,2))) > " + to_string( cos( to_radians( _dec_max ) ) );
	 _query_template += " AND SQRT(POW(-pos1-,2) + POW(-pos2-,2))/(SQRT(POW(-pos1-,2) + "
	    "POW(-pos2-,2) + POW(-pos3-,2))) < " + to_string( cos( to_radians( _dec_min ) ) );
      }
      else
      {
	 // if( _box_side > 0.0 )
	 // {
	 _query_template += str( format( " -pos1- < %1%  AND -pos2- < %2% AND -pos3- < %3% " ) % _box_size % _box_size % _box_size );
	 // }
	 // else
	 // {
	 //    _query_template += str( format( " redshift_real > %1% AND redshift_real < %2%" ) % _z_min % _z_max );
	 // }
      }

      if( _filter != "" )
      {
         if( _filter_min != "" )
         {
            _query_template += str( format( " AND %1% >= %2%" ) % _output_fields.get( _filter ) % _filter_min );
         }
         if( _filter_max != "" )
         {
            _query_template += str( format( " AND %1% <= %2%" ) % _output_fields.get( _filter ) % _filter_max );
         }
      }

      LOGDLN( "Query template: ", _query_template );
      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_read_snapshots()
   {
      LOG_ENTER();

      // Find number of snapshots and resize the containers.
      unsigned num_snaps;
      _sql << "SELECT COUNT(*) FROM snap_redshift", soci::into( num_snaps );
      LOGDLN( num_snaps, " snapshots." );
      _snap_redshifts.reallocate( num_snaps );

      // Read meta data.
      _sql << "SELECT redshift FROM snap_redshift ORDER BY snapnum",
         soci::into( (std::vector<real_type>&)_snap_redshifts );
      LOGDLN( "Redshifts: ", _snap_redshifts );

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   lightcone::_setup_redshift_ranges()
   {
      LOG_ENTER();

      ASSERT( _snap_redshifts.size() >= 2, "Must be at least two snapshots." );

      // Create a temporary table to hold values.
      _sql << "CREATE TEMPORARY TABLE redshift_ranges (snapnum INTEGER, "
      	 "redshift DOUBLE PRECISION, min DOUBLE PRECISION, max DOUBLE PRECISION)";

      // Insert the first redshift range.
      real_type low = _redshift_to_distance( _snap_redshifts[0] ),
	 upp = _redshift_to_distance( _snap_redshifts[1] ),
	 mid = upp + 0.5*(low - upp);
      _sql << "INSERT INTO redshift_ranges VALUES(0, :z, :min, :max)",
	 soci::use( _snap_redshifts[0] ), soci::use( mid*mid ), soci::use( low*low );
      LOGDLN( "Redshift range for snapshot 0: ", mid, " - ", low );

      // Walk over snapshots creating distances.
      for( unsigned ii = 1; ii < _snap_redshifts.size() - 1; ++ii )
      {
	 low = upp;
	 upp = _redshift_to_distance( _snap_redshifts[ii + 1] );
	 real_type new_mid = upp + 0.5*(low - upp);
	 _sql << "INSERT INTO redshift_ranges VALUES(:snapnum, :z, :min, :max)",
	    soci::use( ii ), soci::use( _snap_redshifts[ii] ),
	    soci::use( new_mid*new_mid ), soci::use( mid*mid );
	 LOGDLN( "Redshift range for snapshot ", ii, ": ", new_mid, " - ", mid );
	 mid = new_mid;
      }

      // Insert the last redshift range.
      _sql << "INSERT INTO redshift_ranges VALUES(:snapnum, :z, :min, :max)",
	 soci::use( _snap_redshifts.size() - 1 ), soci::use( _snap_redshifts.back() ),
	 soci::use( upp*upp ), soci::use( mid*mid );
      LOGDLN( "Redshift range for snapshot ", _snap_redshifts.size() - 1, ": ", upp, " - ", mid );

      LOG_EXIT();
   }
}
