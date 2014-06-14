#include <iostream>
#include <vector>
#include <libhpc/libhpc.hh>
#include <tao/base/utils.hh>
#include "sage.hh"
#include "hdf5_types.hh"

class application
   : public hpc::application
{
public:

   application( int argc,
                char* argv[] )
      : hpc::application( argc, argv )
   {
      // Setup some options.
      options().add_options()
	 ( "sage,s", hpc::po::value<hpc::fs::path>( &_fn ), "SAGE HDF5 file" )
	 ( "ggi,g",  hpc::po::value<unsigned long long>( &_ggi ), "global galaxy index" );

      // Parse options.
      parse_options( argc, argv );
      EXCEPT( !_fn.empty(), "No SAGE filename given." );
   }

   void
   operator()()
   {
      hpc::h5::file file( _fn.native(), H5F_ACC_RDONLY );

      hpc::h5::dataset displs_dset( file, "tree_displs" );
      std::vector<unsigned long long> displs( displs_dset.extent() );
      displs_dset.read( displs );
      auto it = std::lower_bound( displs.begin(), displs.end(), _ggi );
      EXCEPT( it != displs.end(), "Failed to find tree for global galaxy index." );
      unsigned tree_idx = it - displs.begin();
      if( displs[tree_idx] != _ggi ) --tree_idx;

      unsigned tree_size = file.read<unsigned>( "tree_counts", tree_idx );
      unsigned long long tree_displ = displs[tree_idx];
      unsigned lgi = _ggi - tree_displ;
      std::vector<sage::galaxy> gals( tree_size );
      hpc::h5::datatype mem_type, file_type;
      sage::make_hdf5_types( mem_type, file_type );
      hpc::h5::dataset gals_dset( file, "galaxies" );
      gals_dset.read( gals.data(), mem_type, gals.size(), tree_displ );

      std::multimap<unsigned,unsigned> parents;
      for( unsigned ii = 0; ii < gals.size(); ++ii )
      {
	 if( gals[ii].descendant != -1 )
	    parents.emplace( gals[ii].descendant, ii );
      }

      dump_ggis( gals, parents, lgi );
   }

   void
   dump_ggis( std::vector<sage::galaxy> const& gals,
	      std::multimap<unsigned,unsigned> const& parents,
	      unsigned lgi )
   {
      std::cout << gals[lgi].global_index << "(" << gals[lgi].snapshot << ")\n";
      auto rng = parents.equal_range( lgi );
      while( rng.first != rng.second )
      {
	 dump_ggis( gals, parents, rng.first->second );
	 ++rng.first;
      }
   }

protected:

   hpc::fs::path _fn;
   unsigned long long _ggi;
};

#define HPC_APP_CLASS application
#include <libhpc/mpi/main.hh>
