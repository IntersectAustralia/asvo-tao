#include <soci/soci.h>
#include "csv.hh"

using namespace hpc;

namespace tao {

   module*
   csv::factory( const string& name,
		 pugi::xml_node base )
   {
      return new csv( name, base );
   }

   csv::csv( const string& name,
	     pugi::xml_node base )
      : module( name, base ),
        _records( 0 )
   {
   }

   csv::~csv()
   {
   }

   ///
   ///
   ///
   void
   csv::initialise( const options::xml_dict& global_dict )
   {
      LOG_ENTER();

      if(mpi::comm::world.size()==1)
    	  _fn = global_dict.get<string>( "outputdir" ) + "/" + _dict.get<hpc::string>( "filename" ) ;
      else
    	  _fn = global_dict.get<string>( "outputdir" ) + "/" + _dict.get<hpc::string>( "filename" ) + "." + mpi::rank_string();

      _fields = _dict.get_list<string>( "fields" );

      // Open the file.
      open();

      // Reset the number of records.
      _records = 0;

      LOG_EXIT();
   }

   ///
   ///
   ///
   void
   csv::execute()
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
   csv::open()
   {
      _file.open( _fn, std::fstream::out | std::fstream::trunc );

      // Dump out a list of field names first.
      auto it = _fields.cbegin();
      if( it != _fields.cend() )
      {
	 _file << *it++;
	 while( it != _fields.cend() )
	    _file << ", " << *it++;
         _file << "\n";
      }
   }

   void
   csv::process_galaxy( tao::galaxy& galaxy )
   {
      _timer.start();

      // Repeat for each galaxy in the batch.
      LOGDLN( "Beginning CSV dump of galaxies." );
      for( galaxy.begin(); !galaxy.done(); galaxy.next() )
      {
         auto it = _fields.cbegin();
         if( it != _fields.cend() )
         {
	    _write_field( galaxy, *it++ );
            while( it != _fields.cend() )
            {
               _file << ", ";
               _write_field( galaxy, *it++ );
            }
            _file << "\n";
         }

         // Increment number of written records.
         ++_records;
      }
      LOGDLN( "Ending CSV dump of galaxies." );

      _timer.stop();
   }

   void
   csv::log_metrics()
   {
      module::log_metrics();
      LOGILN( _name, " number of records written: ", mpi::comm::world.all_reduce( _records ) );
   }

   void
   csv::_write_field( const tao::galaxy& galaxy,
                      const string& field )
   {
      LOGDLN( "CSV: Writing field: ", field );
      // TODO: Can make this faster by not repeating the
      //       value lookup for each index.
      auto val = galaxy.field( field );
      switch( val.second )
      {
	 case tao::galaxy::STRING:
	    _file << galaxy.current_value<string>( field );
	    break;

	 case tao::galaxy::DOUBLE:
	    _file << galaxy.current_value<double>( field );
	    break;

	 case tao::galaxy::INTEGER:
	    _file << galaxy.current_value<int>( field );
	    break;

	 case tao::galaxy::UNSIGNED_LONG_LONG:
	    _file << galaxy.current_value<unsigned long long>( field );
	    break;

	 case tao::galaxy::LONG_LONG:
	    _file << galaxy.current_value<long long>( field );
	    break;

	 default:
	    ASSERT( 0 );
      }
   }

}
