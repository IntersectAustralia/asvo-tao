#ifndef tao_modules_hdf5_hh
#define tao_modules_hdf5_hh

#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/batch.hh"
#include "tao/base/filter.hh"

namespace tao {
   namespace modules {
      using namespace hpc;

      template< class Backend >
      class hdf5
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
            return new hdf5( name, base );
         }

      public:

         hdf5( const string& name = string(),
               pugi::xml_node base = pugi::xml_node() )
            : module_type( name, base ),
              _chunk_size( 100 ),
              _ready( false ),
              _records( 0 )
         {
         }

         virtual
         ~hdf5()
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
            LOGILN( "Initialising HDF5 module.", setindent( 2 ) );

            // Cache dictionary.
            const options::xml_dict& dict = this->_dict;

            // Get our information.
            if(mpi::comm::world.size()==1)
                      _fn = global_dict.get<string>( "outputdir" ) + "/" + dict.get<hpc::string>( "filename" ) ;
                  else
                      _fn = global_dict.get<string>( "outputdir" ) + "/" + dict.get<hpc::string>( "filename" ) + "." + mpi::rank_string();

            _fields = dict.get_list<string>( "fields" );
            ReadFieldsInfo(dict );

            // Open the file.
            _file.open( _fn, H5F_ACC_TRUNC );

            // Reset the number of records.
            _records = 0;

            // Make sure we create the fields.
            _ready = false;

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

            // Create datasets for the field names. Note that I can only
            // do this when I have a galaxy object, hence doing it once
            // here.
            if( !_ready )
            {
            	auto lblit = _labels.cbegin();

               for( const auto& field : _fields )
               {
            	  string FieldName=_encode(*lblit);
                  h5::datatype dtype = _field_type( bat, field );
                  h5::dataspace dspace;
                  dspace.create( 1, true );
                  h5::property_list props( H5P_DATASET_CREATE );
                  props.set_chunk_size( _chunk_size );
                  props.set_deflate();
                  //h5::dataset* dset = new h5::dataset( _file, field, dtype, dspace, none, false, props );
                  h5::dataset* dset = new h5::dataset( _file, FieldName, dtype, dspace, none, false, props );
                  _dsets.push_back( dset );

                  // Dump first chunk.
                  unsigned ii = 0;
                  for( auto it = _filt->begin( bat ); it != _filt->end( bat ); ++it, ++ii )
                  {
                     dset->set_extent( ii + 1 );
                     dset->space( dspace );
                     dspace.select_one( ii );
                     _write_field( bat, *it, field, *dset, dspace );
                  }
                  lblit++;

		  // Set number written for first batch.
		  _records = ii;
               }

               // Flag as complete.
               _ready = true;
            }
            else
            {
               // Process each element.
               for( auto it = _filt->begin( bat ); it != _filt->end( bat ); ++it )
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
                        dset->set_extent( old_size + 1 );
                     }
                     h5::dataspace dspace( *dset );
                     dspace.select_one( old_size );
                     _write_field( bat, *it, field, *dset, dspace );
                  }

		  // Increment records.
		  ++_records;
               }
            }
         }

         virtual
         void
         log_metrics()
         {
            module_type::log_metrics();
            LOGILN( this->_name, " number of records written: ", _records );
         }

      protected:

         h5::datatype
         _field_type( const tao::batch<real_type>& bat,
                      const string& field )
         {
            auto val = bat.field( field );
            switch( std::get<2>( val ) )
            {
               case tao::batch<real_type>::STRING:
                  return h5::datatype::string;
                  break;

               case tao::batch<real_type>::DOUBLE:
                  return h5::datatype::native_double;
                  break;

               case tao::batch<real_type>::INTEGER:
                  return h5::datatype::native_int;
                  break;

               case tao::batch<real_type>::UNSIGNED_LONG_LONG:
                  return h5::datatype::native_llong;
                  break;

               case tao::batch<real_type>::LONG_LONG:
                  return h5::datatype::native_llong;
                  break;

               default:
                  ASSERT( 0 );
            }
         }

         void
         _write_field( const tao::batch<real_type>& bat,
                       unsigned idx,
                       const string& field,
                       h5::dataset& dset,
                       h5::dataspace& dspace )
         {
            auto val = bat.field( field );
            h5::dataspace mem_space;
            mem_space.create( 1 );
            mem_space.select_all();
            switch( std::get<2>( val ) )
            {
               case tao::batch<real_type>::STRING:
               {
                  string data = bat.scalar<string>( field )[idx];
                  dset.write( data.c_str(), h5::datatype::string, mem_space, dspace );
                  break;
               }

               case tao::batch<real_type>::DOUBLE:
               {
                  double data = bat.scalar<double>( field )[idx];
                  dset.write( &data, h5::datatype::native_double, mem_space, dspace );
                  break;
               }

               case tao::batch<real_type>::INTEGER:
               {
                  double data = bat.scalar<int>( field )[idx];
                  dset.write( &data, h5::datatype::native_int, mem_space, dspace );
                  break;
               }

               case tao::batch<real_type>::UNSIGNED_LONG_LONG:
               {
                  double data = bat.scalar<unsigned long long>( field )[idx];
                  dset.write( &data, h5::datatype::native_llong, mem_space, dspace );
                  break;
               }

               case tao::batch<real_type>::LONG_LONG:
               {
                  double data = bat.scalar<long long>( field )[idx];
                  dset.write( &data, h5::datatype::native_llong, mem_space, dspace );
                  break;
               }

               default:
                  ASSERT( 0 );
            }
         }

      protected:

         h5::file _file;
         string _fn;
         list<string> _fields;
         unsigned long long _records;
         list<hpc::string> _labels;
         list<scoped_ptr<h5::dataset>> _dsets;
         hsize_t _chunk_size;
         bool _ready;
         tao::filter const* _filt;
      };

   }
}

#endif
