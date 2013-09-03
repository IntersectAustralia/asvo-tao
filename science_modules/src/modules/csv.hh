#ifndef tao_modules_csv_hh
#define tao_modules_csv_hh

#include <fstream>
#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/batch.hh"
#include "tao/base/types.hh"

namespace tao {
   namespace modules {
      using namespace hpc;

      template< class Backend >
      class csv
         : public module<Backend>
      {
      public:

         typedef Backend backend_type;
         typedef module<backend_type> module_type;

         static
         module_type*
         factory( const string& name,
                  pugi::xml_node base )
         {
            return new csv( name, base );
         }

      public:

         csv( const string& name = string(),
              pugi::xml_node base = pugi::xml_node() )
            : module_type( name, base ),
              _records( 0 )
         {
         }

         virtual
         ~csv()
         {
         }

         ///
         ///
         ///
         virtual
         void
         initialise( const options::xml_dict& global_dict )
         {
            // Don't initialise if we're already doing so.
            if( this->_init )
               return;
            module_type::initialise( global_dict );

            auto timer = this->timer_start();
            LOGILN( "Initialising CSV module.", setindent( 2 ) );

            // Cache dictionary.
            const options::xml_dict& dict = this->_dict;

            _fn = global_dict.get<string>( "outputdir" ) + "/" +
               dict.get<string>( "filename" ) + "." + mpi::rank_string() + ".csv";
            _fields = dict.get_list<string>( "fields" );

            // Open the file.
            open();

            // Reset the number of records.
            _records = 0;

            LOGILN( "Done.", setindent( -2 ) );
         }

         ///
         ///
         ///
         virtual
         void
         execute()
         {
            auto timer = this->timer_start();
            ASSERT( this->parents().size() == 1 );

            // Grab the batch from the parent object.
            const tao::batch<real_type>& bat = this->parents().front()->batch();

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
         }

         void
         open()
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

         virtual
         void
         log_metrics()
         {
            module_type::log_metrics();
            LOGILN( this->_name, " number of records written: ", mpi::comm::world.all_reduce( _records ) );
         }

      protected:

         void
         _write_field( const tao::batch<real_type>& bat,
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

      protected:

         std::ofstream _file;
         string _fn;
         list<string> _fields;
         unsigned long long _records;
      };

   }
}

#endif
