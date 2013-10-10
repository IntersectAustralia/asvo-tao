#ifndef tao_modules_votable_hh
#define tao_modules_votable_hh

#include <fstream>
#include <boost/algorithm/string/replace.hpp>
#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/batch.hh"
#include "tao/base/filter.hh"

namespace tao {
   namespace modules {
      using namespace hpc;
      using boost::algorithm::replace_all;

      template< class Backend >
      class votable
         : public module<Backend>
      {
      public:

         typedef Backend backend_type;
         typedef module<backend_type> module_type;

         static module_type*
         factory( const string& name,
                  pugi::xml_node base )
         {
            return new votable( name, base );
         }

      public:

         votable( const string& name = string(),
                  pugi::xml_node base = pugi::xml_node() )
            : module_type( name, base )
         {
            _istableopened=false;
            _isfirstgalaxy=true;
         }

         virtual
         ~votable()
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
            LOGILN( "Initialising votable module.", setindent( 2 ) );

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
            open();

            // Reset the number of records.
            _records = 0;

            // Get the filter from the lightcone module.
            _filt = this->template attribute<tao::filter const*>( "filter" );

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

            // Is this the first galaxy? if so, please write the fields information
            if(_isfirstgalaxy)
            {
               _write_table_header(bat);
               _start_table();
               _isfirstgalaxy=false;
            }

            //Process the galaxy as any other galaxy
            process_galaxy( bat );
         }

         virtual
         void
         finalise()
         {
            _end_table();
            _write_footer();
         }

         void
         open()
         {
            _file.open( _fn, std::fstream::out | std::fstream::trunc );

            //Put File Header First
            _write_file_header("TempResourceName","TempTableName");
         }

         void
         process_galaxy( const tao::batch<real_type>& bat )
         {
            for( auto bat_it = _filt->begin( bat ); bat_it != _filt->end( bat ); ++bat_it )
            {
               unsigned ii = *bat_it;

               auto it = _fields.cbegin();
               if( it != _fields.cend() )
               {
                  _file<<"\t<TR>"<<std::endl;

                  while( it != _fields.cend() )
                  {
                     _write_field( bat, *it++,ii );
                  }
                  _file<<"\t</TR>"<<std::endl;
               }

               // Increment number of written records.
               ++_records;
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

         string
         _xml_encode( string _toencode_string )
         {
            std::map<char, std::string> transformations;
            transformations['&']  = std::string("&amp;");
            transformations['\''] = std::string("&apos;");
            transformations['"']  = std::string("&quot;");
            transformations['>']  = std::string("&gt;");
            transformations['<']  = std::string("&lt;");

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
         _write_field( const tao::batch<real_type>& bat,
                       const string& field,
                       unsigned idx )
         {
            _file<<"\t\t<TD>";
            auto val = bat.field( field );
            switch( std::get<2>( val ) )
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
            _file<<"</TD>"<<std::endl;
         }

         void
         _write_file_header( const string& ResourceName,
                             const string& TableName )
         {
            if(_file.is_open())
            {
               _file<<"<?xml version=\"1.0\"?>"<<std::endl;
               _file<<"<VOTABLE version=\"1.3\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns=\"http://www.ivoa.net/xml/VOTable/v1.3\"";
               _file<<" xmlns:stc=\"http://www.ivoa.net/xml/STC/v1.30\" >"<<std::endl;
               _file<<"<RESOURCE name=\""<<ResourceName<<"\">"<<std::endl;
               _file<<"<TABLE name=\""<<TableName<<"\">"<<std::endl;
            }
         }

         void
         _write_footer()
         {
            if(_file.is_open())
            {
               _file<<"</TABLE>"<<std::endl;
               _file<<"</RESOURCE>"<<std::endl;
               _file<<"</VOTABLE>"<<std::endl;
            }
         }

         void
         _write_table_header( const tao::batch<real_type>& bat )
         {
            auto it = _fields.cbegin();
            auto unitit = _units.cbegin();

            auto lblit = _labels.cbegin();
            while( it != _fields.cend() )
            {
               string FieldName=*lblit;
               replace_all(FieldName," ","_");
               FieldName=_xml_encode(FieldName);
               _file<<"<FIELD name=\""+FieldName<<"\" ID=\"Col_"<<_xml_encode(*it)<<"\" ";
               auto val = bat.field( *it );
               switch( std::get<2>( val ) )
               {
                  case tao::batch<real_type>::STRING:
                     _file<<"datatype=\"char\" arraysize=\"*\" unit=\""+_xml_encode(*unitit)+"\"";
                     break;

                  case tao::batch<real_type>::DOUBLE:
                     _file<<"datatype=\"double\" unit=\""+_xml_encode(*unitit)+"\"";
                     break;

                  case tao::batch<real_type>::INTEGER:
                     _file<<"datatype=\"int\" unit=\""+_xml_encode(*unitit)+"\"";
                     break;

                  case tao::batch<real_type>::UNSIGNED_LONG_LONG:
                     _file<<"datatype=\"long\" unit=\""+_xml_encode(*unitit)+"\"";
                     break;

                  case tao::batch<real_type>::LONG_LONG:
                     _file<<"datatype=\"long\" unit=\""+_xml_encode(*unitit)+"\"";
                     break;

                  default:
                     ASSERT( 0 );
               }

               it++;
               lblit++;
               unitit++;

               _file<<"/>"<<std::endl;
            }
         }

         void
         _start_table()
         {
            _istableopened=true;
            _file<<"<DATA>"<<std::endl;
            _file<<"<TABLEDATA>"<<std::endl;
         }

         void
         _end_table()
         {
            if(_istableopened)
            {
               _file<<"</TABLEDATA>"<<std::endl;
               _file<<"</DATA>"<<std::endl;
               _istableopened=false;
            }
         }

         void
         ReadFieldsInfo( const options::xml_dict& dict )
         {
            list<optional<hpc::string>> Templabels = dict.get_list_attributes<string>( "fields","label" );
            list<optional<hpc::string>> Tempunits = dict.get_list_attributes<string>( "fields","units" );
            list<optional<hpc::string>> Tempdescription = dict.get_list_attributes<string>( "fields","description" );


            auto lblit = Templabels.cbegin();
            auto unitit = Tempunits.cbegin();
            auto descit = Tempdescription.cbegin();
            auto fldsit = _fields.cbegin();
            while( lblit != Templabels.cend() )
            {

               if(!*lblit)
                  _labels.push_back(*fldsit);
               else
                  _labels.push_back(**lblit);

               if(!*unitit)
                  _units.push_back("unitless");
               else
                  _units.push_back(**unitit);


               if(!*descit)
                  _desc.push_back("");
               else
                  _desc.push_back(**descit);



               // Increment all the iterators at the same time
               lblit++;
               fldsit++;
               unitit++;
               descit++;
            }
         }

      protected:

         bool _isfirstgalaxy;
         bool _istableopened;
         std::ofstream _file;
         string _fn;
         list<hpc::string> _fields;
         list<hpc::string> _labels;
         list<hpc::string> _units;
         list<hpc::string> _desc;
         unsigned long long _records;
         tao::filter const* _filt;
      };

   }
}

#endif
