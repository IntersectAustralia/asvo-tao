#include <stdlib.h>
#include <boost/lexical_cast.hpp>
#include "galaxy.hh"

using namespace hpc;

namespace tao {

   galaxy::galaxy()
      : _table( NULL )
   {
   }

   galaxy::galaxy( const string& table )
      : _table( &table )
   {
   }

   void
   galaxy::clear()
   {
      _batch_size = 0;
      _fields.clear();
   }

   void
   galaxy::set_table( const string& table )
   {
      _table = &table;
   }

   void
   galaxy::set_batch_size( unsigned size )
   {
      _batch_size = size;
   }

   void
   galaxy::read_record_filter( const options::xml_dict& global_dict )
   {
      _filter = global_dict.get<string>( "workflow:record-filter:filter:filter-attribute","" );
      // std::transform( _filter.begin(), _filter.end(), _filter.begin(), ::tolower );
      string min = global_dict.get<string>( "workflow:record-filter:filter:filter-min","" );
      string max = global_dict.get<string>( "workflow:record-filter:filter:filter-max","" );

      // Convert to doubles.
      if( min != "None" && min != "none" && !min.empty() )
	 _filter_min = boost::lexical_cast<double>( min );
      else
	 _filter_min = -std::numeric_limits<double>::max();
      if( max != "None" && max != "none" && !max.empty() )
	 _filter_max = boost::lexical_cast<double>( max );
      else
	 _filter_max = std::numeric_limits<double>::max();

      LOGDLN( "Read filter name of: ", _filter );
      LOGDLN( "Read filter range of: ", _filter_min, " to ", _filter_max );
   }

   void
   galaxy::begin()
   {
      LOGDLN( "Beginning galaxy record iteration." );
      _it = 0;
      settle();
   }

   bool
   galaxy::done() const
   {
      return _it == _batch_size;
   }

   void
   galaxy::next()
   {
      ++_it;
      settle();
   }

   void
   galaxy::settle()
   {
      // In order to filter we need a filter name and that name must be
      // defined on the galaxy.
      if( !_filter.empty() && _fields.find( _filter ) != _fields.end() )
      {
	 LOGDLN( "Checking for filtered value." );
	 while( _it != _batch_size )
	 {
	    // Do we have a value for the filter? If there are no values
	    // for the field in question then return it.
	    // TODO: Generalise to other types.
	    // TODO: Generalise to vector fields.
	    auto vals = values<double>( _filter );
	    if( vals.size() == 0 )
	    {
	       LOGDLN( "Filter field has no values yet." );
	       break;
	    }
	    if( vals[_it] > _filter_min && vals[_it] < _filter_max )
	    {
	       LOGDLN( "Value of ", vals[_it], " within range." );
	       break;
	    }
	    LOGDLN( "Value of ", vals[_it], " outside range." );
	    ++_it;
	 }
      }
      else
      {
	 LOGDLN( "No filter specified, iterating." );
      }
   }

   // void
   // galaxy::update( const soci::row& row,
   //                 const string& table )
   // {

   // }

   // void
   // galaxy::update( const galaxy& gal )
   // {
   //    _table = gal._table;
   //    _z = _row->get<real_type>( "redshift" );
   //    _fields.clear();
   // }

   // void
   // galaxy::set_redshift( real_type redshift )
   // {
   //    _z = redshift;
   //    set_field<double>( "redshift", _z );
   // }

   const string&
   galaxy::table() const
   {
      ASSERT( _table );
      return *_table;
   }

   unsigned
   galaxy::batch_size() const
   {
      return _batch_size;
   }

   // const vector<long long>&
   // galaxy::ids() const
   // {
   //    ASSERT( _row );
   //    return _row->get<long long>( "globalindex" );
   // }

   // int
   // galaxy::local_id() const
   // {
   //    ASSERT( _row );
   //    return _row->get<int>( "localgalaxyid" );
   // }

   // long long
   // galaxy::tree_id() const
   // {
   //    ASSERT( _row );
   //    return _row->get<long long>( "globaltreeid" );
   // }

//    const vector<galaxy::real_type>&
//    galaxy::x() const
//    {
//       // This is ridiculous, but it seems sqlite represents
//       // modified aliases, (0 + posx + 0) AS pos_x, as strings.
//       // "Surely not!?" you say, but indeed it is so. This
//       // means sqlite databases won't have the correct rotated/
//       // translated values used as pos_x, pos_y, pos_z.
// #ifndef NDEBUG
//       if( _row->get_properties( "pos_x" ).get_data_type() == soci::dt_string )
// 	 return atof( _row->get<std::string>( "pos_x" ).c_str() );
//       else
// 	 return _row->get<real_type>( "pos_x" );
// #else
//       return _row->get<real_type>( "pos_x" );
// #endif
//    }

//    galaxy::real_type
//    galaxy::y() const
//    {
//       ASSERT( _row );

//       // This is ridiculous, but it seems sqlite represents
//       // modified aliases, (0 + posx + 0) AS pos_x, as strings.
//       // "Surely not!?" you say, but indeed it is so. This
//       // means sqlite databases won't have the correct rotated/
//       // translated values used as pos_x, pos_y, pos_z.
// #ifndef NDEBUG
//       if( _row->get_properties( "pos_y" ).get_data_type() == soci::dt_string )
// 	 return atof( _row->get<std::string>( "pos_y" ).c_str() );
//       else
// 	 return _row->get<real_type>( "pos_y" );
// #else
//       return _row->get<real_type>( "pos_y" );
// #endif
//    }

//    galaxy::real_type
//    galaxy::z() const
//    {
//       ASSERT( _row );

//       // This is ridiculous, but it seems sqlite represents
//       // modified aliases, (0 + posx + 0) AS pos_x, as strings.
//       // "Surely not!?" you say, but indeed it is so. This
//       // means sqlite databases won't have the correct rotated/
//       // translated values used as pos_x, pos_y, pos_z.
// #ifndef NDEBUG
//       if( _row->get_properties( "pos_z" ).get_data_type() == soci::dt_string )
// 	 return atof( _row->get<std::string>( "pos_z" ).c_str() );
//       else
// 	 return _row->get<real_type>( "pos_z" );
// #else
//       return _row->get<real_type>( "pos_z" );
// #endif
//    }

//    galaxy::real_type
//    galaxy::redshift() const
//    {
//       return _z;
//    }

//    galaxy::real_type
//    galaxy::disk_metallicity() const
//    {
//       ASSERT( _row );
//       return _row->get<real_type>( "disk_metal" );
//    }

//    galaxy::real_type
//    galaxy::bulge_metallicity() const
//    {
//       ASSERT( _row );
//       return _row->get<real_type>( "bulge_metal" );
//    }

   galaxy::field_type
   galaxy::field( const string& name ) const
   {
      auto it = _fields.find( name );
      ASSERT( it != _fields.end() );
      return it->second;
   }

   std::ostream&
   operator<<( std::ostream& strm,
               const galaxy& obj )
   {
      return strm;
   }
}
