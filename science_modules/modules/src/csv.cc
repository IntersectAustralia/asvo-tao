#include <soci/soci.h>
#include "csv.hh"

using namespace hpc;

namespace tao {

   module*
   csv::factory( const string& name )
   {
      return new csv( name );
   }

   csv::csv( const string& name )
      : module( name ),
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
   csv::initialise( const options::xml_dict& dict,
                    optional<const string&> prefix )
   {
      LOG_ENTER();

      _fn = dict.get<hpc::string>( prefix.get()+":filename" );
      _fields = dict.get_list<hpc::string>( prefix.get()+":fields" );

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
   csv::process_galaxy( const tao::galaxy& galaxy )
   {
      _timer.start();

      // Repeat for each galaxy in the batch.
      for( unsigned ii = 0; ii < galaxy.batch_size(); ++ii )
      {
         auto it = _fields.cbegin();
         if( it != _fields.cend() )
         {
            _write_field( galaxy, *it++, ii );
            while( it != _fields.cend() )
            {
               _file << ", ";
               _write_field( galaxy, *it++, ii );
            }
            _file << "\n";
         }

         // Increment number of written records.
         ++_records;
      }

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
                      const string& field,
                      unsigned idx )
   {
      // TODO: Can make this faster by not repeating the
      //       value lookup for each index.
      auto val = galaxy.field( field );
      switch( val.second )
      {
	 case tao::galaxy::STRING:
	    _file << galaxy.values<string>( field )[idx];
	    break;

	 case tao::galaxy::DOUBLE:
	    _file << galaxy.values<double>( field )[idx];
	    break;

	 case tao::galaxy::INTEGER:
	    _file << galaxy.values<int>( field )[idx];
	    break;

	 case tao::galaxy::UNSIGNED_LONG_LONG:
	    _file << galaxy.values<unsigned long long>( field )[idx];
	    break;

	 case tao::galaxy::LONG_LONG:
	    _file << galaxy.values<long long>( field )[idx];
	    break;

	 default:
	    ASSERT( 0 );
      }
   }

}
