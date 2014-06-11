class file_chunker
   : public hpc::mpi::async::event_handler
{
public:

   file_chunker( hpc::fs::path const& param_fn,
                 hpc::fs::path const& exp_fn );

   ///
   /// Worker has requested a chunk.
   ///
   virtual
   void
   event( MPI_Status const& stat );

protected:

   void
   _load_indices( hpc::fs::path const& fn );

   void
   _load_redshifts( hpc::fs::path const& fn );

   void
   _next_file();

   void
   _make_filename();

   void
   _load_tree_sizes();

   void
   _next_chunk();

protected:

   std::set<double> _redshifts;
   std::array<size_t,2> _idx_rng;
   std::set<double>::const_iterator _z_it;
   size_t _idx_it;
   hpc::fs::path _cur_path;
   hpc::fs::path _sage_path;
   std::vector<size_t> _tree_sizes;
   std::vector<size_t>::const_iterator _tree_it;
   hpc::varray<size_t,2> _chunk;
   unsigned long long _n_trees_done;
   hpc::mpi::indexer<hpc::varray<size_t,2>> _idxs;
};
