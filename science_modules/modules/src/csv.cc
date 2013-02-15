#include <soci/soci.h>
#include "csv.hh"

using namespace hpc;

namespace tao {

   csv::csv( const string& name )
      : module( name )
   {
   }

   ///
   ///
   ///
   void
   csv::setup_options( options::dictionary& dict,
                       optional<const string&> prefix )
   {
   }

   ///
   ///
   ///
   void
   csv::initialise( const options::dictionary& dict,
                    optional<const string&> prefix )
   {
   }

   ///
   ///
   ///
   void
   csv::execute()
   {
   }

   ///
   ///
   ///
   tao::galaxy&
   csv::galaxy()
   {
   }

   void
   csv::set_filename( const string& filename )
   {
      LOG_ENTER();

      _fn = filename + "." + to_string( mpi::comm::world.rank() );
      LOGDLN( "Set filename to: ", _fn );

      LOG_EXIT();
   }

   void
   csv::open()
   {
      _file.open( _fn, std::fstream::out | std::fstream::trunc );

      // Dump out a list of field names first.
      const auto& fields = _lc->output_fields();
      auto it = fields.cbegin();
      if( it != fields.cend() )
      {
	 _file << *it++;
	 while( it != fields.cend() )
	    _file << ", " << *it++;
	 _file << ", apparant magnitude";
      }
      else
	 _file << "apparant magnitude";
      _file << "\n";
   }

   void
   csv::process_galaxy( const tao::galaxy& galaxy,
			double app_mag )
   {
      const auto& fields = _lc->output_fields();
      auto it = fields.cbegin();
      if( it != fields.cend() )
      {
	 _write_field( galaxy, *it++ );
	 while( it != fields.cend() )
	 {
	    _file << ", ";
	    _write_field( galaxy, *it++ );
	 }
	 _file << ", " << app_mag;
      }
      else
	 _file << app_mag;
      _file << "\n";
   }

   void
   csv::_write_field( const tao::galaxy& galaxy,
		      const string& field )
   {
      const soci::row& row = galaxy.row();
      switch( row.get_properties( field ).get_data_type() )
      {
	 case soci::dt_string:
	    _file << row.get<std::string>( field );
	    break;

	 case soci::dt_double:
	    _file << row.get<double>( field );
	    break;

	 case soci::dt_integer:
	    _file << row.get<int>( field );
	    break;

	 case soci::dt_unsigned_long_long:
	    _file << row.get<unsigned long long>( field );
	    break;

	 case soci::dt_long_long:
	    _file << row.get<long long>( field );
	    break;

	 default:
	    ASSERT( 0 );
      }
   }
}
