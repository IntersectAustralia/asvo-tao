class manager
   : public hpc::mpi::async::event_handler
{
public:

   manager( hpc::fs::path const& param_fn,
            hpc::fs::path const& exp_fn )
      : hpc::mpi::async::event_handler( 1 ),
        _idxs( 2 )
   {
      _load_indices( param_fn );
      _load_redshifts( exp_fn );
      _make_filename();
      _load_tree_sizes();
   }

   virtual
   void
   initialise( hpc::mpi::async& async )
   {
      // Add the indexer to the event manager.
      async.add_event_handler( &_idxs );

      // Prepare first chunk.
      _next_file();
   }

   ///
   /// Worker has requested a chunk.
   ///
   virtual
   void
   event( MPI_Status const& stat )
   {
      // Worker needs a filename and a chunk.
      _comm->send( _cur_path.native(), stat.MPI_SOURCE );
      _comm->send( _cur_chunk, stat.MPI_SOURCE );

      // Progress to the next chunk.
   }

   virtual
   bool
   done() const
   {
      // We're not done until the indexer registers the last
      // chunk has been processed.
      return _n_trees_done == _idxr.base()[0];
   }

protected:

   void
   _load_indices( hpc::fs::path const& fn )
   {
      std::ifstream file( fn );
      EXCEPT( file.good(), "Failed to find parameter file: ", fn );

      boost::regex first_prog( "\\s*FirstFile\\s+(\\d+)" );
      boost::regex last_prog( "\\s*LastFile\\s+(\\d+)" );
      boost::cmatch match;

      std::string line;
      int both = 0;
      while( file.good() )
      {
         std::getline( file, line );
         if( boost::regex_match( line, match, first_prog ) )
         {
            _idx_rng[0] = boost::lexical_cast<size_t>(
               match[1].first, match[1].second - match[1].first
               );
            ++both;
         }
         if( boost::regex_match( line, match, last_prog ) )
         {
            _idx_rng[1] = boost::lexical_cast<size_t>(
               match[1].first, match[1].second - match[1].first
               ) + 1;
            ++both;
         }
      }

      EXCEPT( both == 2, "Failed to find FirstFile and LastFile in parameters." );
      EXCEPT( _idx_rng[1] > _idx_rng[0], "Invalid index range." );

      LOGDLN( "Have index range: ", _idx_rng );
   }

   void
   _load_redshifts( hpc::fs::path const& fn )
   {
      std::ifstream file( fn );
      EXCEPT( file.good(), "Failed to open expansion file: ", fn );

      double exp;
      while( file.good() )
      {
         file >> exp;
         _redshifts.insert( tao::expansion_to_redshift( exp ) );
      }

      LOGDLN( "Have redshifts: ", _redshifts );
   }

   void
   _next_file()
   {
      if( ++_idx_it == _idx_rng[1] )
      {
         _idx_it = _idx_rng[0];
         if( ++_z_it == _redshifts.end() )
         {
            _cur_fn.clear();
            return;
         }
      }
      _make_filename();
      _load_tree_sizes();
   }

   void
   _make_filename()
   {
      std::stringstream ss;
      ss << "model_z" << *_z_it << "." << _idx_it;
      _cur_path = _sage_path/ss.str();
   }

   void
   _load_tree_sizes()
   {
      std::ifstream file( _cur_path.native() );
      EXCEPT( file.good(), "Failed to open SAGE file: ", _cur_path );

      unsigned n_trees, n_gals;
      file >> n_trees >> n_gals;
      _tree_sizes.reallocate( n_trees );
      for( unsigned ii = 0; ii < n_trees; ++ii )
         file >> _tree_sizes[ii];

      _chunk[0] = 0;
      _chunk[1] = 0;
      _next_chunk();
   }

   void
   _next_chunk()
   {
      _chunk[0] = _chunk[1];
      while( _tree_it != _tree_sizes.end() &&
             (_chunk[1] - _chunk[0]) + *_tree_it < _max_chunk_size )
      {
         ++_chunk[1];
         ++_tree_it;
      }
   }

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
