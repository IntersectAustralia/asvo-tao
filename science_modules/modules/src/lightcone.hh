#ifndef tao_lightcone_lightcone_hh
#define tao_lightcone_lightcone_hh

#include "tao/base/module.hh"

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

      lightcone();

      ~lightcone();

      ///
      ///
      ///
      void
      setup_options( options::dictionary& dict,
                     optional<const string&> prefix=optional<const string&>() );

      ///
      ///
      ///
      void
      setup_options( options::dictionary& dict,
                     const char* prefix );

      ///
      ///
      ///
      void
      initialise( const options::dictionary& dict,
                  optional<const string&> prefix=optional<const string&>() );

      ///
      ///
      ///
      void
      initialise( const options::dictionary& dict,
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
      _redshift_to_distance( real_type redshift );

      void
      _read_options( const options::dictionary& dict,
                     optional<const string&> prefix=optional<const string&>() );

      void
      _setup_query_template();

      void
      _read_snapshots();

      ///
      ///
      ///
      void
      _setup_redshift_ranges();

   protected:

      string _box_type;
      vector<string> _table_names;
      vector<real_type> _snap_redshifts;
      real_type _domain_size;
      real_type _x0, _y0, _z0;
      real_type _z_min, _z_max;
      real_type _ra_min, _ra_max;
      real_type _dec_min, _dec_max;
      real_type _z_snap, _box_size;
      unsigned _min_snap, _max_snap, _z_snap_idx;
      bool _use_random;
      bool _unique;
      real_type _unique_offs_x, _unique_offs_y, _unique_offs_z;
      range<real_type> _dist_range;
      set<string> _output_fields;
      string _filter;
      real_type _filter_min, _filter_max;
      real_type _h0;

      string _query_template;
      string _crd_strs[3];
      vector<string> _ops;

      string _bin_filename;
      std::ofstream _bin_file;

      size_t _cur_table;
      list<array<real_type,3>> _boxes;
      list<array<real_type,3>>::const_iterator _cur_box;
      scoped_ptr<soci::rowset<soci::row>> _rows;
      soci::rowset<soci::row>::const_iterator _cur_row;

      bool _use_bsp;
   };
}

#endif
