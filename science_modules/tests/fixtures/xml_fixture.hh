#include <libhpc/libhpc.hh>
#include "db_fixture.hh"

struct xml_fixture
{
   static const char* lc_tmpl;
   static const char* box_tmpl;

   hpc::options::xml_dict
   make_lightcone_dict( const hpc::string& rep = "unique",
                        int seed = 0,
                        tao::real_type z_min = 0.0,
                        tao::real_type z_max = 0.06,
                        tao::real_type ra_min = 0.0,
                        tao::real_type ra_max = 10.0,
                        tao::real_type dec_min = 0.0,
                        tao::real_type dec_max = 10.0,
                        const hpc::string& filt_field = "None",
                        tao::real_type filt_min = 0.0,
                        tao::real_type filt_max = 0.0 )
   {
      boost::format fmt( lc_tmpl );
      fmt % rep % seed % z_min % z_max;
      fmt % ra_min % ra_max % dec_min % dec_max;
      fmt % filt_field % filt_min % filt_max;
      std::istringstream iss( fmt.str() );
      return hpc::options::xml_dict( iss );
   }

   hpc::options::xml_dict
   make_box_dict( int seed = 0,
                  tao::real_type box_size = 10.0,
                  tao::real_type redshift = 0.0,
                  const hpc::string& filt_field = "None",
                  tao::real_type filt_min = 0.0,
                  tao::real_type filt_max = 0.0 )
   {
      boost::format fmt( box_tmpl );
      fmt % seed % box_size % redshift;
      fmt % filt_field % filt_min % filt_max;
      std::istringstream iss( fmt.str() );
      return hpc::options::xml_dict( iss );
   }

   db_fixture db;
};
