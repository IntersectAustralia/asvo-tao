#ifndef tao_base_query_hh
#define tao_base_query_hh

#include <string>
#include <set>
#include <vector>
#include <libhpc/system/string.hh>
#include <libhpc/system/view.hh>

namespace tao {

   template< class T >
   class query
   {
   public:

      typedef T real_type;

   public:

      query()
      {
         add_base_output_fields();
      }

      void
      clear()
      {
         _of_set.clear();
         _out_fields.clear();
      }

      void
      add_base_output_fields()
      {
         add_output_field( "posx" );
         add_output_field( "posy" );
         add_output_field( "posz" );
         add_output_field( "velx" );
         add_output_field( "vely" );
         add_output_field( "velz" );
         add_output_field( "snapnum" );
         add_output_field( "globaltreeid" );
         add_output_field( "localgalaxyid" );
	 add_output_field( "globalindex" );
	 add_output_field( "sfrdisk" );
	 add_output_field( "sfrbulge" );
	 add_output_field( "sfrdiskz" );
	 add_output_field( "sfrbulgez" );
	 add_output_field( "coldgas" );
	 add_output_field( "metalscoldgas" );
	 add_output_field( "diskscaleradius" );
      }

      void
      add_output_field( const std::string& field )
      {
         _out_fields.clear();
         _of_set.insert( hpc::to_lower_copy( field ) );
      }

      const hpc::view<std::vector<std::string>>
      output_fields()
      {
         if( _out_fields.empty() )
         {
            _out_fields.resize( _of_set.size() );
            std::copy( _of_set.begin(), _of_set.end(), _out_fields.begin() );
         }
         return _out_fields;
      }

   protected:

      std::set<std::string> _of_set;
      std::vector<std::string> _out_fields;
   };

}

#endif
