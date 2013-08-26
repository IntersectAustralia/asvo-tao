#include <soci/soci.h>
#include "hdf5.hh"

using namespace hpc;

namespace tao {

   module*
   hdf5::factory( const string& name,
		  pugi::xml_node base )
   {
      return new hdf5( name, base );
   }

   hdf5::hdf5( const string& name,
	       pugi::xml_node base )
      : module( name, base ),
	_chunk_size( 100 ),
	_ready( false ),
	_records( 0 )
   {
   }

   hdf5::~hdf5()
   {
   }

   ///
   ///
   ///
   void
   hdf5::initialise( const options::xml_dict& global_dict )
   {
      LOG_ENTER();

      // Get our information.
      _fn = global_dict.get<string>( "outputdir" ) + "/" + _dict.get<string>( "filename" ) + "." + mpi::rank_string();
      _fields = _dict.get_list<string>( "fields" );

      // Open the file.
      open();

      // Reset the number of records.
      _records = 0;

      // Make sure we create the fields.
      _ready = false;

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   hdf5::execute()
   {
      _timer.start();
      LOG_ENTER();
      ASSERT( parents().size() == 1 );

      // Grab the galaxy from the parent object.
      tao::galaxy& gal = parents().front()->galaxy();

      process_galaxy( gal );

      LOG_EXIT();
      _timer.stop();
   }

   void
   hdf5::open()
   {
      // Create the file.
      _file.open( _fn, H5F_ACC_TRUNC );
   }

   void
   hdf5::process_galaxy( tao::galaxy& galaxy )
   {
      _timer.start();

      // Create datasets for the field names. Note that I can only
      // do this when I have a galaxy object, hence doing it once
      // here.
      if( !_ready )
      {
	 for( const auto& field : _fields )
	 {
	    h5::datatype dtype = _field_type( galaxy, field );
	    h5::dataspace dspace;
	    dspace.create( galaxy.batch_size(), true );
	    h5::property_list props( H5P_DATASET_CREATE );
	    props.set_chunk_size( _chunk_size );
	    props.set_deflate();
	    h5::dataset* dset = new h5::dataset( _file, field, dtype, dspace, none, false, props );
	    _dsets.push_back( dset );

	    // Dump first chunk.
	    unsigned ii = 0;
	    for( galaxy.begin(); !galaxy.done(); galaxy.next(), ++ii )
	    {
	       dspace.select_one( ii );
	       _write_field( galaxy, field, *dset, dspace );
	    }
	 }

	 // Flag as complete.
	 _ready = true;
      }
      else
      {
	 // Process each element.
	 for( galaxy.begin(); !galaxy.done(); galaxy.next() )
	 {
	    // Write the fields.
	    auto dset_it = _dsets.begin();
	    for( const auto& field : _fields )
	    {
	       h5::dataset* dset = (*dset_it++).get();
	       hsize_t old_size;
	       {
		  h5::dataspace dspace( *dset );
		  old_size = dspace.size();
		  dset->extend( old_size + 1 );
	       }
	       h5::dataspace dspace( *dset );
	       dspace.select_one( old_size );
	       _write_field( galaxy, field, *dset, dspace );
	    }
	 }
      }

      // Increment number of written records.
      _records += galaxy.batch_size();

      _timer.stop();
   }

   void
   hdf5::log_metrics()
   {
      module::log_metrics();
      LOGILN( _name, " number of records written: ", mpi::comm::world.all_reduce( _records ) );
   }

   h5::datatype
   hdf5::_field_type( const tao::galaxy& galaxy,
		      const string& field )
   {
      auto val = galaxy.field( field );
      switch( val.second )
      {
	 case tao::galaxy::STRING:
	    return h5::datatype::string;
	    break;

	 case tao::galaxy::DOUBLE:
	    return h5::datatype::native_double;
	    break;

	 case tao::galaxy::INTEGER:
	    return h5::datatype::native_int;
	    break;

	 case tao::galaxy::UNSIGNED_LONG_LONG:
	    return h5::datatype::native_llong;
	    break;

	 case tao::galaxy::LONG_LONG:
	    return h5::datatype::native_llong;
	    break;

	 default:
	    ASSERT( 0 );
      }
   }

   void
   hdf5::_write_field( const tao::galaxy& galaxy,
		       const string& field,
		       h5::dataset& dset,
		       h5::dataspace& dspace )
   {
      auto val = galaxy.field( field );
      h5::dataspace mem_space;
      mem_space.create( 1 );
      mem_space.select_all();
      switch( val.second )
      {
	 case tao::galaxy::STRING:
	 {
	    string data = galaxy.current_value<string>( field );
	    dset.write( data.c_str(), h5::datatype::string, mem_space, dspace );
	    break;
	 }

	 case tao::galaxy::DOUBLE:
	 {
	    double data = galaxy.current_value<double>( field );
	    dset.write( &data, h5::datatype::native_double, mem_space, dspace );
	    break;
	 }

	 case tao::galaxy::INTEGER:
	 {
	    double data = galaxy.current_value<int>( field );
	    dset.write( &data, h5::datatype::native_int, mem_space, dspace );
	    break;
	 }

	 case tao::galaxy::UNSIGNED_LONG_LONG:
	 {
	    double data = galaxy.current_value<unsigned long long>( field );
	    dset.write( &data, h5::datatype::native_llong, mem_space, dspace );
	    break;
	 }

	 case tao::galaxy::LONG_LONG:
	 {
	    double data = galaxy.current_value<long long>( field );
	    dset.write( &data, h5::datatype::native_llong, mem_space, dspace );
	    break;
	 }

	 default:
	    ASSERT( 0 );
      }
   }
}
