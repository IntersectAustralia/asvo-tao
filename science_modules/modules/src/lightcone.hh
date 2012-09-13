#ifndef tao_lightcone_lightcone_hh
#define tao_lightcone_lightcone_hh

#include "tao/base/module.hh"

class lightcone_suite;
class sed_suite;
class filter_suite;

namespace tao {

   ///
   /// Lightcone science module.
   ///
   class lightcone
      : public module
   {
      friend class ::lightcone_suite;
      friend class ::sed_suite;
      friend class ::filter_suite;

   public:

      typedef double real_type;

   public:

      lightcone();

      ~lightcone();

      ///
      ///
      ///
      void
      setup_options( hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      ///
      ///
      ///
      void
      setup_options( hpc::options::dictionary& dict,
                     const char* prefix );

      ///
      ///
      ///
      void
      initialise( const hpc::options::dictionary& dict,
                  hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      ///
      ///
      ///
      void
      initialise( const hpc::options::dictionary& dict,
                  const char* prefix );

      ///
      /// Run the module.
      ///
      void
      run();

      ///
      /// Begin iterating over galaxies.
      ///
      void
      begin();

      ///
      /// Check for completed iteration.
      ///
      bool
      done();

      ///
      /// Advance to next galaxy.
      ///
      void
      operator++();

      ///
      /// Get current galaxy.
      ///
      const galaxy
      operator*() const;

      ///
      /// Get current redshift.
      ///
      real_type
      redshift() const;

   protected:

      void
      _settle_snap();

      void
      _settle_box();

      void
      _build_pixels( real_type offs_x,
                     real_type offs_y,
                     real_type offs_z );

      void
      _build_query( real_type offs_x,
                    real_type offs_y,
                    real_type offs_z,
                    hpc::string& query );

      void
      _random_rotation_and_shifting( hpc::vector<hpc::string>& ops );

      void
      _get_boxes( hpc::list<hpc::array<real_type,3>>& boxes );

      real_type
      _redshift_to_distance( real_type redshift );

      void
      _read_options( const hpc::options::dictionary& dict,
                     hpc::optional<const hpc::string&> prefix=hpc::optional<const hpc::string&>() );

      void
      _setup_query_template();

      void
      _read_snapshots();

   protected:

      hpc::string _box_type;
      hpc::vector<unsigned> _snap_idxs;
      hpc::vector<real_type> _snap_redshifts;
      hpc::vector<real_type> _snap_box_sizes;
      real_type _x0, _y0, _z0;
      real_type _z_min, _z_max;
      real_type _ra_min, _ra_max;
      real_type _dec_min, _dec_max;
      real_type _z_snap, _box_size;
      bool _use_random;
      bool _unique;
      real_type _unique_offs_x, _unique_offs_y, _unique_offs_z;
      hpc::range<real_type> _z_range, _dist_range;
      hpc::string _table_name;
      hpc::vector<hpc::string> _include;
      hpc::map<hpc::string, hpc::string> _output_fields;
      hpc::string _filter;
      hpc::string _filter_min, _filter_max;
      real_type _H0;

      hpc::string _query_template;
      hpc::string _crd_strs[3];

      hpc::string _bin_filename;
      std::ofstream _bin_file;

      hpc::mpi::lindex _cur_snap;
      hpc::list<hpc::array<real_type,3>> _boxes;
      hpc::list<hpc::array<real_type,3>>::const_iterator _cur_box;
      hpc::scoped_ptr<soci::rowset<soci::row>> _rows;
      soci::rowset<soci::row>::const_iterator _cur_row;
   };
}

#endif
