#include "csv.hh"

using namespace hpc;

namespace tao {
   namespace modules {

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
         _fn = global_dict.get<string>( "outputdir" ) + "/" +
            _dict.get<string>( "filename" ) + "." + mpi::rank_string() + ".csv";
         _fields = _dict.get_list<string>( "fields" );

         // Open the file.
         open();

         // Reset the number of records.
         _records = 0;
      }

      ///
      ///
      ///
      void
      csv::execute()
      {
         timer_start();
         ASSERT( parents().size() == 1 );

         // Grab the batch from the parent object.
         const tao::batch<real_type>& bat = parents().front()->batch();

         // Repeat for each galaxy in the batch.
         for( unsigned ii = 0; ii < bat.size(); ++ii )
         {
            auto it = _fields.cbegin();
            if( it != _fields.cend() )
            {
               _write_field( bat, ii, *it++ );
               while( it != _fields.cend() )
               {
                  _file << ", ";
                  _write_field( bat, ii, *it++ );
               }
               _file << "\n";
            }

            // Increment number of written records.
            ++_records;
         }

         timer_stop();
      }

      void
      csv::open()
      {
         // Open the file, truncating.
         _file.open( _fn, std::fstream::trunc );

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
      csv::log_metrics()
      {
         module::log_metrics();
         LOGILN( _name, " number of records written: ", mpi::comm::world.all_reduce( _records ) );
      }

      void
      csv::_write_field( const tao::batch<real_type>& bat,
                         unsigned idx,
                         const string& field )
      {
         switch( std::get<2>( bat.field( field ) ) )
         {
            case tao::batch<real_type>::STRING:
               _file << bat.scalar<string>( field )[idx];
               break;

            case tao::batch<real_type>::DOUBLE:
               _file << bat.scalar<double>( field )[idx];
               break;

            case tao::batch<real_type>::INTEGER:
               _file << bat.scalar<int>( field )[idx];
               break;

            case tao::batch<real_type>::UNSIGNED_LONG_LONG:
               _file << bat.scalar<unsigned long long>( field )[idx];
               break;

            case tao::batch<real_type>::LONG_LONG:
               _file << bat.scalar<long long>( field )[idx];
               break;

            default:
               ASSERT( 0 );
         }
      }

   }
}
