#ifndef tao_base_galaxy_hh
#define tao_base_galaxy_hh

#include <soci/soci.h>
#include <libhpc/libhpc.hh>

namespace tao {

   class galaxy
   {
   public:

      typedef double real_type;

   public:

      galaxy( const soci::row& row,
              const hpc::array<real_type,3>& box,
	      const hpc::string& table );

      const soci::row&
      row() const;

      const hpc::string&
      table() const;

      long long
      id() const;

      int
      local_id() const;

      long long
      tree_id() const;

      real_type
      x() const;

      real_type
      y() const;

      real_type
      z() const;

      real_type
      redshift() const;

      real_type
      disk_metallicity() const;

      real_type
      bulge_metallicity() const;

      unsigned
      flat_file() const;

      unsigned
      flat_offset() const;

      unsigned
      flat_length() const;

      friend std::ostream&
      operator<<( std::ostream& strm,
                  const galaxy& obj );

   public:

      const soci::row& _row;
      const hpc::array<real_type,3>& _box;
      const hpc::string& _table;
   };
}

#endif
