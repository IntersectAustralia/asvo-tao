#include <cstdlib>
#include <iostream>
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>
#include <libhpc/libhpc.hh>

using namespace hpc;

// void
// walk_tree( int idx,
//            int tree_idx,
//            vector<galaxy_type>& halos,
//            multimap<int,int>& parents )
// {
//    // Mark each galaxy with a tree index. If this galaxy already has
//    // a tree index then we have a problem. This tests for the
//    // independance of each tree.
//    ASSERT( halos[idx].tree_idx == -1,
//            "Overlapping trees." );
//    halos[idx].tree_idx = tree_idx;

//    // Process each parent.
//    auto rng = parents.equal_range( idx );
//    while( rng.first != rng.second )
//    {
//       walk_tree( (*rng.first).second, tree_idx, halos, parents );
//       ++rng.first;
//    }
// }

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );

   // ASSERT( argc > 1 );
   LOG_CONSOLE();

   // Open database session.
   soci::session sql( soci::mysql, "db=random host=tao01.hpc.swin.edu.au port=3307 user=root pass='la di da'" );

   // Get a complete list of tables.
   soci::rowset<std::string> tables = (sql.prepare << "SHOW TABLES FROM Millennium_Full");

   // Loop over all the tables in the database.
   for( auto& table : tables )
   {
      // How many trees are in this table?
      query = "SELECT DISTINCT GlobalTreeID FROM " + table;
      soci::rowset<long long> tree_ids = (sql.prepare << query);

      // Loop over each tree.
      for( auto tree_id : tree_ids )
      {
         // Prepare a row iterator for the galaxies in this tree.
         query = "SELECT * FROM " + table + " WHERE GlobalTreeID=" + to_string( tree_id );
         soci::rowset<soci::row> galaxies = (sql.prepare << query);

         // Need to represent the parents of each galaxy, and also
         // the bases of each tree. We also need to store the FOF
         // groups to check galaxy types.
         multimap<int,int> parents;
         list<int> bases;
         multimap<int,int> fof_groups;
         map<int,int> tree_idxs;

         // Loop over all the galaxies.
         for( auto& gal : galaxies )
         {
            // Cache some information from the galaxy row.
            long long id = gal.get<long long>( "GlobalIndex" );
            int type = gal.get<int>( "ObjectType" );
            int fof_idx = gal.get<int>( "FOFIndex" );
            long long desc = gal.get<long long>( "DescendantGlobalID" );
            int snap = gal.get<int>( "SnapNum" );

            // All descendants must be local to the tree. They can also
            // be -1, indicating no descendant.
            query = "SELECT COUNT(*) FROM " + table + " WHERE GlobalTreeID=" + to_string( tree_id );
            query += " AND GlobalIndex=" + to_string( desc );
            int num_matches;
            sql << query, soci::into( num_matches );
            ASSERT( num_matches != 0,
                    "Unable to find descendant in the same tree as progenitor." );
            ASSERT( num_matches == 1,
                    "More than one match for a global ID and tree ID." );

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

         // // Starting from the bases, walk up the tree to compute some
         // // values and checks.
         // int tree_idx = 0;
         // for( auto idx : bases )
         // {
         //    LOGDLN( "Walking tree with base at ", idx, "." );
         //    walk_tree( idx, tree_idx, halos, parents );
         //    ++tree_idx;
         // }

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
      }
   }

   mpi::finalise();
   return EXIT_SUCCESS;
}
