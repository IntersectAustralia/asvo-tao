#include <cstdlib>
#include <iostream>
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>
#include <soci/soci.h>
// #include <soci/sqlite3/soci-sqlite3.h>
// #include <soci/mysql/soci-mysql.h>
#include <soci/postgresql/soci-postgresql.h>
#include <libhpc/libhpc.hh>

using namespace hpc;

void
walk_tree( int idx,
           int tree_idx,
	   map<int,int>& tree_idxs,
           multimap<int,int>& parents )
{
   // Mark each galaxy with a tree index. If this galaxy already has
   // a tree index then we have a problem. This tests for the
   // independance of each tree.
   ASSERT( tree_idxs.get( idx ) == -1,
           "Overlapping trees." );
   tree_idxs.insert( idx, tree_idx );

   // Process each parent.
   auto rng = parents.equal_range( idx );
   while( rng.first != rng.second )
   {
      walk_tree( (*rng.first).second, tree_idx, tree_idxs, parents );
      ++rng.first;
   }
}

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );

   // Create any timers we need.
   profile::timer sql_timer;

   // ASSERT( argc > 1 );
   LOG_PUSH( new logging::stdout() );

   // Open database session.
   #include "tao/base/credentials.hh"
   string connect = "dbname=millennium_full_mpi host=tao02.hpc.swin.edu.au port=3306 user=" + username + " password='" + password + "'";
   soci::session sql( soci::postgresql, connect );

   // Get a complete list of tables.
   sql_timer.start();
   string query = "SELECT table_name FROM information_schema.tables"
     " WHERE table_schema='public' AND SUBSTR(table_name,1,5)='tree_'";
   soci::rowset<std::string> tables = (sql.prepare << query);
   sql_timer.stop();

   // Loop over all the tables in the database.
   for( auto table_it = tables.begin(); table_it != tables.end(); ++table_it )
   {
      sql_timer.start();
      const auto& table = *table_it;
      sql_timer.stop_tally();

      LOGILN( "Looking at table \"", table, "\".", setindent( 2 ) );

      // How many trees are in this table?
      query = "SELECT DISTINCT globaltreeid FROM " + table + " ORDER BY globaltreeid";
      sql_timer.start();
      soci::rowset<long long> tree_ids = (sql.prepare << query);
      sql_timer.stop();

      // Loop over each tree.
      for( auto tree_id_it = tree_ids.begin(); tree_id_it != tree_ids.end(); ++tree_id_it )
      {
	 sql_timer.start();
	 const auto& tree_id = *tree_id_it;
	 sql_timer.stop_tally();

	 LOGILN( "Looking at tree ", tree_id, ".", setindent( 2 ) );

         // Prepare a row iterator for the galaxies in this tree.
         query = "SELECT * FROM " + table + " WHERE globaltreeid=" + to_string( tree_id );
	 LOGDLN( "Query: ", query );
	 sql_timer.start();
         soci::rowset<soci::row> galaxies = (sql.prepare << query);
	 sql_timer.stop_tally();

         // Need to represent the parents of each galaxy, and also
         // the bases of each tree. We also need to store the FOF
         // groups to check galaxy types.
         multimap<int,int> parents;
         list<int> bases;
         multimap<int,int> fof_groups;
         map<int,int> tree_idxs;

         // Loop over all the galaxies.
         for( auto gal_it = galaxies.begin(); gal_it != galaxies.end(); ++gal_it )
         {
	    sql_timer.start();
	    const auto& gal = *gal_it;
	    sql_timer.stop_tally();

            // Cache some information from the galaxy row.
            long long id = gal.get<long long>( "globalindex" );
            int type = gal.get<int>( "objecttype" );
            int fof_idx = gal.get<int>( "fofhaloindex" );
            long long desc = gal.get<long long>( "globaldescendant" );
            int snap = gal.get<int>( "snapnum" );
	    LOGDLN( "Looking at galaxy with ID ", id, "." );

            // All descendants must be local to the tree. They can also
            // be -1, indicating no descendant.
	    if( desc != -1 )
	    {
	       query = "SELECT COUNT(*) FROM " + table + " WHERE globaltreeid=" + to_string( tree_id );
	       query += " AND globalindex=" + to_string( desc );
	       LOGDLN( "Query: ", query );
	       int num_matches;
	       sql_timer.start();
	       sql << query, soci::into( num_matches );
	       sql_timer.stop_tally();
	       ASSERT( num_matches != 0,
		       "Unable to find descendant in the same tree as progenitor." );
	       ASSERT( num_matches == 1,
		       "More than one match for a global ID and tree ID." );
	    }

            // All types must be 0, 1 or 2.
            ASSERT( type >= 0 && type <= 2,
                    "Bad galaxy type." );

            // All snapshot numbers must be <= 63.
            ASSERT( snap <= 63,
                    "Bad snapshot number." );

            // Add parent information.
            if( desc != -1 )
               parents.insert( desc, id );
            else
               bases.push_back( id );

            // Clear the tree index to a dummy value. Note that there cannot
            // be more than one insertion.
            ASSERT( !tree_idxs.has( id ),
                    "Found duplicate global IDs." );
            tree_idxs.insert( id, -1 );

            // Insert the FOF group details.
            fof_groups.insert( fof_idx, id );
         }

         // Starting from the bases, walk up the tree to compute some
         // values and checks.
         int tree_idx = 0;
         for( auto idx : bases )
         {
            LOGDLN( "Walking tree with base at ", idx, "." );
            walk_tree( idx, tree_idx, tree_idxs, parents );
            ++tree_idx;
         }

         // // Process each FOF group and check that the galaxy types are okay.
         // for( unsigned jj = 0; jj < halos.size(); ++jj )
         // {
         //    bool have_primary = false;
         //    auto rng = fof_groups.equal_range( jj );
         //    while( rng.first != rng.second )
         //    {
         //       unsigned idx = (*rng.first).second;
         //       if( halos[idx].type == 0 )
         //       {
         //          ASSERT( !have_primary, "Multiple primary galaxies in FOF group." );
         //          have_primary = true;
         //       }
         //       ++rng.first;
         //    }
         // }

	 LOGILN( "Mean query time per row: ", sql_timer.mean() );
	 LOGI( setindent( -2 ) );
      }

      LOGI( setindent( -2 ) );
   }

   mpi::finalise();
   return EXIT_SUCCESS;
}
