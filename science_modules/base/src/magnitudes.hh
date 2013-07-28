#ifndef tao_base_magnitudes_hh
#define tao_base_magnitudes_hh

#include "types.hh"
#include "sed.hh"
#include "bandpass.hh"

namespace tao {

   real_type
   calc_area( real_type redshift );

   real_type
   calc_abs_area();

   real_type
   apparent_magnitude( const tao::sed& sed,
                       const bandpass& bp,
                       real_type area );

   real_type
   apparent_magnitude( real_type spec_int,
                       real_type bp_int,
                       real_type area );

   real_type
   absolute_magnitude( const tao::sed& sed,
                       const bandpass& bp );

}

#endif
