#ifndef bolshoi_utils_hh
#define bolshoi_utils_hh

#include <libhpc/libhpc.hh>

///
/// Finish reading a line.
///
template< class Stream >
void
finish_line( Stream& strm )
{
   strm.ignore( std::numeric_limits<std::streamsize>::max(), '\n' );
   ASSERT( !strm.fail() );
}

///
/// Read past any comments.
///
template< class Stream >
void
skip_comments( Stream& strm )
{
   while( strm.peek() == '#' )
   {
      LOGDLN( "Ignoring line of comments." );
      finish_line( strm );
   }
   ASSERT( !strm.fail() );
}

///
///
///
void
load_forests_map( hpc::multimap<long long,long long>& forests );

///
///
///
void
load_locations_map( hpc::map<long long,std::pair<unsigned,size_t>>& locations,
		    hpc::map<unsigned,hpc::string>& file_map );

///
///
///
void
load_forest_sizes_map( hpc::map<long long,unsigned>& forest_sizes );

#endif
