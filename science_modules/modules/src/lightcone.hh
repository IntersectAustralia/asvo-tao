#ifndef tao_lightcone_lightcone_hh
#define tao_lightcone_lightcone_hh

#include "tao/base/base.hh"

// Forward declaration of test suites to allow direct
// access to the lightcone module.
class lightcone_suite;
class sed_suite;
class filter_suite;

namespace tao {
   using namespace hpc;

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

      static
      module*
      factory( const string& name,
	       pugi::xml_node base );

   public:

      lightcone( const string& name = string(),
		 pugi::xml_node base = pugi::xml_node() );

      ~lightcone();

      ///
      ///
      ///
      virtual
      void
      initialise( const options::xml_dict& global_dict );

      ///
      /// Run the module.
      ///
      virtual
      void
      execute();

      ///
      ///
      ///
      virtual
      tao::galaxy&
      galaxy();

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
      tao::galaxy&
      operator*();

      const set<string>&
      output_fields() const;

      unsigned
      num_boxes() const;

      virtual
      void
      log_metrics();

   protected:

      ///
      /// Get a list of tree table names to search.
      ///
      void
      _query_table_names( vector<string>& table_names );

      void
      _settle_table();

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
                    string& query );

      void
      _random_rotation_and_shifting( vector<string>& ops );

      void
      _get_boxes( list<array<real_type,3>>& boxes );

      real_type
      _redshift_to_distance( real_type redshift ) const;

      real_type
      _distance_to_redshift( real_type dist ) const;

      void
      _read_options( const options::xml_dict& global_dict );

      void
      _setup_query_template();

      void
      _read_snapshots();

      void
      _build_dist_to_z_tbl( unsigned num_points,
			    real_type min_z,
			    real_type max_z );

      unsigned
      _box_snapshot( real_type redshift );

      ///
      ///
      ///
      void
      _setup_redshift_ranges();

      void
      _setup_batching();

      void
      _fetch();

   protected:

      string _box_type;
      string _box_repeat;
      vector<string> _table_names;
      vector<real_type> _snap_redshifts;
      real_type _domain_size;
      real_type _x0, _y0, _z0;
      real_type _z_min, _z_max;
      real_type _ra_min, _ra_max;
      real_type _dec_min, _dec_max;
      real_type _z_snap, _box_size;
      unsigned _min_snap, _max_snap, _z_snap_idx;
      bool _unique;
      real_type _unique_offs_x, _unique_offs_y, _unique_offs_z;
      range<real_type> _dist_range;
      set<string> _output_fields;
      string _filter;
      string _filter_min, _filter_max;
      real_type _h0;

      string _query_template;
      string _basic_query;
      vector<string> _ops;
      array<real_type,3> _rrs_offs;
      array<int,3> _rrs_axis;
      uniform_generator<real_type> _real_rng;
      uniform_generator<int> _int_rng;
      int _rng_seed;

      vector<real_type> _dist_to_z_tbl_dist;
      vector<real_type> _dist_to_z_tbl_z;

      string _bin_filename;
      std::ofstream _bin_file;

      size_t _cur_table;
      list<array<real_type,3>> _boxes;
      list<array<real_type,3>>::const_iterator _cur_box;
      // scoped_ptr<soci::rowset<soci::row>> _rows; // TODO: Latest SOCI doesn't like being destructed!
      // soci::rowset<soci::row>* _rows;
      // soci::rowset<soci::row>::const_iterator _cur_row;
      soci::statement* _st;
      bool _rows_exist;
      vector<void*> _field_stor;
      vector<galaxy::field_value_type> _field_types;
      vector<real_type> _gal_z;
      tao::galaxy _gal;

      string _accel_method;
      string _decomp_method;
      int _bsp_step;
      string _snap_red_table;
      map<string,string> _field_map;

      profile::progress _prog;
      profile::timer _per_box;
   };
}

#endif
