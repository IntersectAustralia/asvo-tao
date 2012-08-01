#ifndef tao_lightcone_lightcone_hh
#define tao_lightcone_lightcone_hh

#include <string>
#include <soci/soci.h>
#include <libhpc/containers/vector.hh>
#include <libhpc/hpcmpi/mpi.hh>

class lightcone_suite;

namespace tao {

   ///
   /// Lightcone science module.
   ///
   class lightcone
   {
   public:

      typedef double real_type;

      lightcone();

      ~lightcone();

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

      std::string
      _build_query( hpc::mpi::lindex cur_snap_idx,
                    optional<hpc::mpi::lindex> next_snap_idx,
                    real_type offs_x,
                    real_type offs_y,
                    real_type offs_z );

      void
      _random_rotation_and_shifting( hpc::vector<std::string>& ops );

      real_type
      _redshift_to_distance( real_type redshift );

      void
      _setup_params();

      void
      _setup_query_template();

      void
      _db_connect( soci::session& sql );

   protected:

      soci::session _sql;
      std::string _dbhost, _dbname, _dbuser, _dbpass;
      std::string _sqlite_filename;

      std::string _type;
      real_type _box_side;
      hpc::vector<real_type> _snaps;
      hpc::vector<hpc::mpi::lindex> _snap_idxs;
      real_type _x0, _y0, _z0;
      real_type _z_min, _z_max;
      real_type _ra_min, _ra_max;
      real_type _dec_min, _dec_max;
      bool _unique;
      real_type _unique_offs_x, _unique_offs_y, _unique_offs_z;
      real_type _last_max_dist_processed;
      real_type _output_box_size;
      std::string _table_name;
      hpc::vector<std::string> _include;
      hpc::map<std::string, std::string> _output_fields;
      std::string _filter;
      std::string _filter_min, _filter_max;
      std::string _query_template;
      real_type _H0;

      friend class ::lightcone_suite;
   };
}

#endif
