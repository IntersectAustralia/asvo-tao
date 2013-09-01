#include <libhpc/libhpc.hh>
#include "db_fixture.hh"

using namespace hpc;

struct xml_fixture
{
   static const char* lc_tmpl;
   static const char* box_tmpl;

   options::xml_dict
   make_lightcone_dict( const string& rep = "unique",
                        int seed = 0,
                        real_type z_min = 0.0,
                        real_type z_max = 0.06,
                        real_type ra_min = 0.0,
                        real_type ra_max = 10.0,
                        real_type dec_min = 0.0,
                        real_type dec_max = 10.0,
                        const string& filt_field = "None",
                        real_type filt_min = 0.0,
                        real_type filt_max = 0.0 )
   {
      boost::format fmt( lc_tmpl );
      fmt % rep % seed % z_min % z_max;
      fmt % ra_min % ra_max % dec_min % dec_max;
      fmt % filt_field % filt_min % filt_max;
      std::istringstream iss( fmt.str() );
      return options::xml_dict( iss );
   }

   options::xml_dict
   make_box_dict( int seed = 0,
                  real_type box_size = 10.0,
                  real_type redshift = 0.0,
                  const string& filt_field = "None",
                  real_type filt_min = 0.0,
                  real_type filt_max = 0.0 )
   {
      boost::format fmt( box_tmpl );
      fmt % seed % box_size % redshift;
      fmt % filt_field % filt_min % filt_max;
      std::istringstream iss( fmt.str() );
      return options::xml_dict( iss );
   }

   db_fixture db;
};
