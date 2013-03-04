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
   csv::setup_options( options::dictionary& dict,
                       optional<const string&> prefix )
   {
      dict.add_option( new options::string( "filename" ), prefix );
      dict.add_option( new options::list<options::string>( "fields" ), prefix );
   }

   ///
   ///
   ///
   void
   csv::initialise( const options::dictionary& dict,
                    optional<const string&> prefix )
   {
      LOG_ENTER();

      // Get the sub dictionary, if it exists.
      const options::dictionary& sub = prefix ? dict.sub( *prefix ) : dict;

      _fn = sub.get<string>( "filename" );
      _fields = sub.get_list<string>( "fields" );

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

      _timer.stop();
   }

   void
   csv::log_metrics()
   {
      module::log_metrics();
      LOGILN( _name, " number of records written: ", _records );
   }

   void
   csv::_write_field( const tao::galaxy& galaxy,
		      const string& field )
   {
      auto val = galaxy.field( field );
      switch( val.second )
      {
	 case tao::galaxy::STRING:
	    _file << galaxy.value<string>( field );
	    break;

	 case tao::galaxy::DOUBLE:
	    _file << galaxy.value<double>( field );
	    break;

	 case tao::galaxy::INTEGER:
	    _file << galaxy.value<int>( field );
	    break;

	 case tao::galaxy::UNSIGNED_LONG_LONG:
	    _file << galaxy.value<unsigned long long>( field );
	    break;

	 case tao::galaxy::LONG_LONG:
	    _file << galaxy.value<long long>( field );
	    break;

	 default:
	    ASSERT( 0 );
      }
   }
}
