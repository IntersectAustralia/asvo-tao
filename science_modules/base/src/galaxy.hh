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
              const hpc::array<real_type,3>& box );

      int
      id() const;

      real_type
      x() const;

      real_type
      y() const;

      real_type
      z() const;

      unsigned
      flat_file() const;

      unsigned
      flat_offset() const;

      unsigned
      flat_length() const;

   protected:

      const soci::row& _row;
      const hpc::array<real_type,3>& _box;
   };
}

#endif
