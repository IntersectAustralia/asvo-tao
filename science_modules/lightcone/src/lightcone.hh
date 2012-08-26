#ifndef tao_lightcone_lightcone_hh
#define tao_lightcone_lightcone_hh

#include <soci/soci.h>
#include <libhpc/libhpc.hh>

class lightcone_suite;

namespace tao {

   ///
   /// Lightcone science module.
   ///
   class lightcone
   {
      friend class ::lightcone_suite;

   public:

      typedef double real_type;

      lightcone();

      ~lightcone();

      ///
      ///
      ///
      void
      setup_options( hpc::options::dictionary& dict );

      ///
      ///
      ///
      void
      initialise( const hpc::options::dictionary& dict );

      ///
      /// Run the module.
      ///
      void
      run();

   protected:

      void
      _build_pixels( hpc::mpi::lindex cur_snap_idx,
                     optional<hpc::mpi::lindex> next_snap_idx,
                     real_type offs_x,
                     real_type offs_y,
                     real_type offs_z );

      void
      _build_query( hpc::mpi::lindex cur_snap_idx,
                    optional<hpc::mpi::lindex> next_snap_idx,
                    real_type offs_x,
                    real_type offs_y,
                    real_type offs_z,
                    hpc::string& query );

      void
      _random_rotation_and_shifting( hpc::vector<hpc::string>& ops );

      void
      _get_boxes( real_type redshift,
                  hpc::list<hpc::array<real_type,3>>& boxes );

      real_type
      _redshift_to_distance( real_type redshift );

      void
      _setup_params( const hpc::options::dictionary& dict );

      void
      _setup_query_template();

      void
      _db_connect( soci::session& sql );

      void
      _open_bin_file();

   protected:

      soci::session _sql;
      hpc::string _dbtype, _dbname, _dbhost, _dbuser, _dbpass;

      hpc::string _box_type;
      real_type _box_side;
      hpc::vector<real_type> _snaps;
      // hpc::vector<hpc::mpi::lindex> _snap_idxs;
      real_type _x0, _y0, _z0;
      real_type _z_min, _z_max;
      real_type _ra_min, _ra_max;
      real_type _dec_min, _dec_max;
      real_type _z_snap, _box_size;
      bool _unique;
      real_type _unique_offs_x, _unique_offs_y, _unique_offs_z;
      real_type _last_max_dist_processed;
      hpc::string _table_name;
      hpc::vector<hpc::string> _include;
      hpc::map<hpc::string, hpc::string> _output_fields;
      hpc::string _filter;
      hpc::string _filter_min, _filter_max;
      hpc::string _query_template;
      real_type _H0;

      hpc::string _bin_filename;
      std::ofstream _bin_file;
   };
}

#endif
