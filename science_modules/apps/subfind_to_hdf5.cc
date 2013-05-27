#include <cstdlib>
#include <iostream>
#include <boost/filesystem.hpp>
#include <libhpc/libhpc.hh>
#include <libhpc/debug/except.hh>
#include "tao/base/subfind.hh"

using namespace hpc;
using namespace tao;
namespace fs = boost::filesystem;

void
count_files( const fs::path& dir,
             vector<unsigned>& file_idxs,
             const string& prefix = "trees_063.",
             const mpi::comm& comm = mpi::comm::world )
{
   // Only rank 0 needs to perform this part.
   if( comm.rank() == 0 )
   {
      ASSERT( fs::exists( dir ) );
      ASSERT( fs::is_directory( dir ) );

      LOGILN( "Search directory: ", dir );
      LOGILN( "Using file prefix: \"", prefix, "\"" );

      // Clear any existing file indices.
      file_idxs.clear();

      // Prepare the file regex.
      boost::regex prog( prefix + "(\\d+)" );

      // Iterate over all the files.
      for( fs::directory_iterator it( dir ); it != fs::directory_iterator(); ++it )
      {
         if( fs::is_regular_file( it->status() ) )
         {
            boost::cmatch match;
            if( boost::regex_match( it->path().filename().c_str(), match, prog ) )
            {
               unsigned idx = boost::lexical_cast<unsigned>( string( match[1].first, match[2].second ) );
               file_idxs.push_back( idx );
               LOGDLN( "Found file: ", it->path().filename() );
            }
         }
      }
   }

   // Share file indices.
   comm.bcasta( file_idxs );

   LOGILN( "Found ", file_idxs.size(), " files to process." );
}

void
scan_files( const fs::path& dir,
            const vector<unsigned>& file_idxs,
            map<unsigned long long,unsigned>& file_map,
            unsigned long long& num_local_trees,
            unsigned long long& tot_trees,
            unsigned long long& num_local_halos,
            unsigned long long& tot_halos,
            const string& prefix = "trees_063.",
            const mpi::comm& comm = mpi::comm::world )
{
   // Clear the incoming file map.
   file_map.clear();

   // Distribute the files.
   unsigned first = (comm.rank()*file_idxs.size())/comm.size();
   unsigned last = ((comm.rank() + 1)*file_idxs.size())/comm.size();
   LOGILN( "Operating on file range: [", first, "-", last, ")" );

   // Track the total number of trees and halos for fun.
   num_local_trees = 0;
   num_local_halos = 0;

   while( first != last )
   {
      fs::path filepath = dir/(prefix + to_string( file_idxs[first] ));
      std::ifstream file( filepath.c_str(), std::ios::binary );

      // Read the number of trees and halos.
      unsigned num_trees, num_halos;
      file.read( (char*)&num_trees, sizeof(num_trees) );
      file.read( (char*)&num_halos, sizeof(num_halos) );
      EXCEPT( file );

#ifndef NLOG
      // If there are zero trees or halos warn the user.
      if( !num_trees )
         LOGILN( "Warning: Zero trees in file: ", filepath );
      if( !num_halos )
         LOGILN( "Warning: Zero halos in file: ", filepath );
#endif

      // Insert into the local mapping.
      file_map.insert( num_halos, file_idxs[first] );

      // Update totals.
      num_local_trees += num_trees;
      num_local_halos += num_halos;

      // Move to the next file.
      ++first;
   }

   // Reduce to all ranks.
   tot_trees = comm.all_reduce( num_local_trees );
   tot_halos = comm.all_reduce( num_local_halos );
   LOGILN( "Found ", tot_trees, " trees to process." );
   LOGILN( "Found ", tot_halos, " halos to process." );
}

int
main( int argc,
      char* argv[] )
{
   mpi::initialise( argc, argv );
   mpi::comm comm( mpi::comm::world );
   LOG_PUSH( new mpi::logger( "log." ) );

   ASSERT( argc >= 3 );
   fs::path base_dir( argv[1] );
   string prefix( argv[2] );

   // Produce a mapping from number of halos in a file to the
   // index of that file.
   unsigned long long num_local_trees, num_local_halos;
   unsigned long long tot_trees, tot_halos;
   map<unsigned long long,unsigned> file_map;
   vector<unsigned> file_idxs;
   {
      count_files( base_dir, file_idxs, prefix );
      scan_files( base_dir, file_idxs, file_map, num_local_trees, tot_trees, num_local_halos, tot_halos, prefix );
   }

   // Produce my file offsets by performing an MPI scan.
   unsigned long long tree_displ = comm.scan( num_local_trees );
   unsigned long long halo_displ = comm.scan( num_local_halos );

   // Create the HDF5 data types.
   h5::datatype mem_type, file_type;
   subfind::make_hdf5_types( mem_type, file_type );

   // Create a property list to split the halos dataset
   // across multiple files.
   h5::property_list props( H5P_DATASET_CREATE );
   {
      unsigned long long remain = tot_halos*file_type.size();
      char name[15];
      unsigned file_idx = 0;
      while( remain )
      {
         sprintf( name, "halos.%04d", file_idx++ );
         unsigned long long size = std::min<unsigned long long>( remain, (unsigned long long)1 << 31 );
         props.set_external( name, size );
         remain -= size;

         // Must create the files, HDF5 won't do it!
         std::ofstream tmp( name );
      }
      LOGILN( "Splitting across ", file_idx, " files." );
   }

   // Create the HDF5 file and a couple of groups.
   h5::file output( "output.h5", H5F_ACC_TRUNC );
   h5::dataspace tree_mem_space, tree_file_space;
   tree_mem_space.create( 1 );
   tree_file_space.create( tot_trees );
   h5::dataset tree_displ_dset( output, "tree_displs", h5::datatype::std_i64be, tree_file_space );
   h5::dataset tree_count_dset( output, "tree_counts", h5::datatype::std_i64be, tree_file_space );
   h5::dataspace halo_file_space;
   halo_file_space.create( tot_halos );
   h5::dataset halo_dset( output, "halos", file_type, halo_file_space, none, false, props );

   // Iterate over my local set of files.
   unsigned first = (comm.rank()*file_idxs.size())/comm.size();
   unsigned last = ((comm.rank() + 1)*file_idxs.size())/comm.size();
   while( first != last )
   {
      // unsigned long long num_halos = pair.first;
      // unsigned file_idx = pair.second;
      unsigned file_idx = file_idxs[first++];

      // Open the file.
      fs::path filepath = base_dir/(prefix + to_string( file_idx ));
      std::ifstream file( filepath.c_str(), std::ios::binary );

      // Read number of trees.
      unsigned num_trees;
      {
         int dummy;
         file.read( (char*)&num_trees, sizeof(num_trees) );
         file.read( (char*)&dummy, sizeof(dummy) );
         EXCEPT( file );
         LOGDLN( "Number of trees in file: ", num_trees );
      }

      // Read tree sizes.
      vector<unsigned> num_tree_halos( num_trees );
      file.read( (char*)num_tree_halos.data(), sizeof(unsigned)*num_trees );
      EXCEPT( file );

      // Iterate over trees.
      vector<subfind::halo> halos;
      for( unsigned ii = 0; ii < num_trees; ++ii )
      {
         // Load the current tree.
         LOGDLN( "Reading tree with index: ", ii, setindent( 2 ) );
         halos.resize( num_tree_halos[ii] );
         file.read( (char*)halos.data(), halos.size()*sizeof(subfind::halo) );
         EXCEPT( file );

         // Write out to HDF5.
         tree_file_space.select_one( tree_displ++ );
         tree_count_dset.write( &num_tree_halos[ii], h5::datatype::native_int, tree_mem_space, tree_file_space );
         tree_displ_dset.write( &halo_displ, h5::datatype::native_llong, tree_mem_space, tree_file_space );
         if( halos.size() )
         {
            h5::dataspace halo_mem_space;
            halo_mem_space.create( halos.size() );
            ASSERT( halo_displ + halos.size() <= tot_halos );
            halo_file_space.select_range( halo_displ, halo_displ + halos.size() );
            halo_dset.write( halos.data(), mem_type, halo_mem_space, halo_file_space );
         }

         // Accumulate displacement.
         halo_displ += num_tree_halos[ii];

         LOGD( setindent( -2 ) );
      }
   }

   mpi::finalise();
   return EXIT_SUCCESS;
}
