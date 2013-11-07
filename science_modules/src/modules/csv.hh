#ifndef tao_modules_csv_hh
#define tao_modules_csv_hh

#include <fstream>
#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/batch.hh"
#include "tao/base/types.hh"
#include "tao/base/filter.hh"

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

            if( mpi::comm::world.size() == 1 )
	       _fn = global_dict.get<string>( "outputdir" ) + "/" + dict.get<hpc::string>( "filename" ) ;
	    else
	       _fn = global_dict.get<string>( "outputdir" ) + "/" + dict.get<hpc::string>( "filename" ) + "." + mpi::rank_string();
            LOGILN( "File Name: ", _fn );
            _fields = dict.get_list<string>( "fields" );
            ReadFieldsInfo(dict );

            // Open the file.
            open();

            // Reset the number of records.
            _records = 0;

            // Get the filter from the lightcone module.
            _filt = this->template attribute<tao::filter const*>( "filter" );

            LOGILN( "Done.", setindent( -2 ) );
         }

         void
	 ReadFieldsInfo( const options::xml_dict& dict )
	 {
	    list<optional<hpc::string>> Templabels = dict.get_list_attributes<string>( "fields","label" );



	    auto lblit = Templabels.cbegin();

	    auto fldsit = _fields.cbegin();
	    while( lblit != Templabels.cend() )
	    {

	       if(!*lblit)
		  _labels.push_back(*fldsit);
	       else
		  _labels.push_back(**lblit);

	       // Increment all the iterators at the same time
	       lblit++;
	       fldsit++;
	    }
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

            // Repeat for each galaxy in the batch, passing through
            // the filter on the way.
	    unsigned cur_count = 0;
            for( auto bat_it = _filt->begin( bat ); bat_it != _filt->end( bat ); ++bat_it )
            {
               unsigned ii = *bat_it;

               // Process each field.
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
	       ++cur_count;
               ++_records;
            }
	    LOGDLN( "Wrote ", cur_count, " records to CSV: ", _fn );
         }



         string
	 _encode( string _toencode_string )
	 {
	    std::map<char, std::string> transformations;
	    transformations['&']  = std::string("_");
	    transformations[' ']  = std::string("_");
	    transformations['\''] = std::string("_");
	    transformations['"']  = std::string("_");
	    transformations['>']  = std::string("_");
	    transformations['<']  = std::string("_");
	    transformations['/']  = std::string("_");

	    std::string reserved_chars;
	    for (auto ti = transformations.begin(); ti != transformations.end(); ti++)
	    {
	       reserved_chars += ti->first;
	    }

	    size_t pos = 0;
	    while (std::string::npos != (pos = _toencode_string.find_first_of(reserved_chars, pos)))
	    {
	       _toencode_string.replace(pos, 1, transformations[_toencode_string[pos]]);
	       pos++;
	    }

	    return _toencode_string;
	 }

         void
         open()
         {
            // Open the file, truncating.
            _file.open( _fn, std::fstream::trunc );
            EXCEPT( _file.is_open(), "Unable to open output file: ", _fn );





	    auto lblit = _labels.cbegin();

	    string FieldName=*lblit++;
	    FieldName=_encode(FieldName);
	    _file<<FieldName;

	    while( lblit != _labels.cend() )
	    {
	       string FieldName=*lblit++;
	       FieldName=_encode(FieldName);
	       _file<<","<<FieldName;
	    }
	    _file<<std::endl;








            // Dump out a list of field names first.
            /*auto it = _fields.cbegin();
	      if( it != _fields.cend() )
	      {
	      _file << *it++;
	      while( it != _fields.cend() )
	      _file << ", " << *it++;
	      _file << "\n";
	      }*/
         }

         virtual
         void
         log_metrics()
         {
            module_type::log_metrics();
            LOGILN( this->_name, " number of records written: ", _records );
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
         list<hpc::string> _labels;
         unsigned long long _records;
         tao::filter const* _filt;
      };

   }
}

#endif
