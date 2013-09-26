#ifndef tao_modules_fits_hh
#define tao_modules_fits_hh

#include <fstream>
#include <boost/algorithm/string/replace.hpp>
#include <libhpc/libhpc.hh>
#include "tao/base/module.hh"
#include "tao/base/batch.hh"
#include "tao/base/filter.hh"
#include "fitsio.h"

namespace tao {
   namespace modules {
      using namespace hpc;
      using boost::algorithm::replace_all;

      template< class Backend >
      class fits
         : public module<Backend>
      {
      public:

         typedef Backend backend_type;
         typedef module<backend_type> module_type;

         static module_type*
         factory( const string& name,
                  pugi::xml_node base )
         {
            return new fits( name, base );
         }

      public:

         fits( const string& name = string(),
               pugi::xml_node base = pugi::xml_node() )
            : module_type( name, base )
         {
            _istableopened=false;
            _isfirstgalaxy=true;
         }

         virtual
         ~fits()
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
            LOGILN( "Initialising fits module.", setindent( 2 ) );

            // Cache dictionary.
            const options::xml_dict& dict = this->_dict;

            // Get our information.
            _fn = global_dict.get<string>( "outputdir" ) + "/" +
               dict.get<string>( "filename" ) + "." + mpi::rank_string() + ".fits";
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

               _isfirstgalaxy=false;
            }
            //Process the galaxy as any other galaxy
            process_galaxy( bat );
         }

         virtual
         void
         finalise()
         {
            int status=0;
            if(fits_close_file(_file,&status))
               ASSERT(status==0);
         }

         void
         open()
         {
            int status=0;
            if(fits_create_file(&_file,("!"+_fn).c_str(), &status))
            {
               LOGDLN(status);
               ASSERT(status==0);
            }
         }

         void
         process_galaxy( const tao::batch<real_type>& bat )
         {
            for( auto bat_it = _filt->begin( bat ); bat_it != _filt->end( bat ); ++bat_it )
            {
               unsigned ii = *bat_it;

               int ColIndex=1;

               int status=0;

               if(fits_insert_rows(_file,_records,1,&status))
               {
                  LOGDLN(status);
                  ASSERT(status==0);
               }
               auto it = _fields.cbegin();
               if( it != _fields.cend() )
               {
                  while( it != _fields.cend() )
                  {
                     _write_field( bat, *it++,ii,ColIndex );
                     ColIndex++;
                  }
               }

               // Increment number of written records.
               ++_records;
               LOGDLN("FITS: ROW Count=",_records);
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
                       const string& field,
                       unsigned idx,
                       int ColIndex )
         {
            int status=0;

            auto val = bat.field( field );
            switch( std::get<2>( val ) )
            {
               case tao::batch<real_type>::STRING:
                  fits_write_col(_file,TSTRING,ColIndex,_records+1,1,1,(void*)bat.scalar<string>(field)[idx].c_str(),&status);
                  LOGDLN(status);
                  ASSERT(status==0);
                  break;

               case tao::batch<real_type>::DOUBLE:
               {
                  double FieldVal=bat.scalar<double>( field )[idx];
                  fits_write_col(_file,TDOUBLE,ColIndex,_records+1,1,1,(void*)&FieldVal,&status);
                  LOGDLN(status);
                  ASSERT(status==0);
               }
               break;

               case tao::batch<real_type>::INTEGER:
               {
                  int FieldVal=bat.scalar<int>(field)[idx];
                  fits_write_col(_file,TINT,ColIndex,_records+1,1,1,(void*)&FieldVal,&status);
                  LOGDLN(status);
                  ASSERT(status==0);
               }
               break;

               case tao::batch<real_type>::UNSIGNED_LONG_LONG:
               {
                  unsigned long long FieldVal=bat.scalar<unsigned long long>(field)[idx];
                  fits_write_col(_file,TLONG,ColIndex,_records+1,1,1,(void*)&FieldVal,&status);
                  LOGDLN(status);
                  ASSERT(status==0);
               }
               break;

               case tao::batch<real_type>::LONG_LONG:
               {
                  long long FieldVal=bat.scalar<long long>(field)[idx];
                  fits_write_col(_file,TLONG,ColIndex,_records+1,1,1,(void*)&FieldVal,&status);
                  LOGDLN(status);
                  ASSERT(status==0);
               }
               break;

               default:
                  ASSERT( 0 );
            }
         }

         void
         _write_table_header( const tao::batch<real_type>& bat )
         {
            int tfields=_fields.size();
            int status=0;

            char** ttype=new char*[tfields];
            char** tform=new char*[tfields];
            char** tunit=new char*[tfields];

            int index=0;
            auto it = _fields.cbegin();
            auto unitit = _units.cbegin();
            auto lblit = _labels.cbegin();
            while( it != _fields.cend() )
            {
               string FieldName=*lblit;

               replace_all(FieldName," ","_");

               ttype[index]=new char[80];
               tunit[index]=new char[80];


               memcpy(ttype[index],FieldName.c_str(),(int)FieldName.length());
               memcpy(tunit[index],(*unitit).c_str(),(int)(*unitit).length());

               ttype[index][(int)FieldName.length()]='\0';
               tunit[index][(int)(*unitit).length()]='\0';

               tform[index]=new char[3];


               string Displayttype;
               Displayttype=ttype[index];
               string Displayttunit;
               Displayttunit=tunit[index];

               auto val = bat.field( *it );
               switch( std::get<2>( val ) )
               {
                  case tao::batch<real_type>::STRING:
                     tform[index]=(char*)"A";
                     break;

                  case tao::batch<real_type>::DOUBLE:
                     tform[index]=(char*)"D";
                     break;

                  case tao::batch<real_type>::INTEGER:
                     tform[index]=(char*)"J";
                     break;

                  case tao::batch<real_type>::UNSIGNED_LONG_LONG:
                     tform[index]=(char*)"K";
                     break;

                  case tao::batch<real_type>::LONG_LONG:
                     tform[index]=(char*)"K";
                     break;

                  default:
                     ASSERT( 0 );
               }

               it++;
               lblit++;
               unitit++;
               index++;
            }

            string TableName="New Table";
            if(fits_create_tbl(_file,BINARY_TBL,0,tfields,ttype,tform,tunit,TableName.c_str(),&status))
            {
               LOGDLN(status);
               ASSERT(status==0);
            }
         }

         void
         ReadFieldsInfo( const options::xml_dict& dict )
         {
            list<optional<hpc::string>> Templabels = dict.get_list_attributes<hpc::string>( "fields","label" );
            list<optional<hpc::string>> Tempunits = dict.get_list_attributes<hpc::string>( "fields","units" );
            list<optional<hpc::string>> Tempdescription = dict.get_list_attributes<hpc::string>( "fields","description" );

            auto lblit = Templabels.cbegin();
            auto unitit = Tempunits.cbegin();
            auto descit = Tempdescription.cbegin();
            auto fldsit = _fields.cbegin();
            while( lblit != Templabels.cend() )
            {
               if(!*lblit)
                  _labels.push_back(*fldsit);
               else
               {
                  _labels.push_back(**lblit);

               }

               if(!*unitit)
                  _units.push_back("unitless");
               else
               {
                  _units.push_back(**unitit);

               }

               if(!*descit)
                  _desc.push_back("");
               else
               {
                  _desc.push_back(**descit);

               }

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
         fitsfile* _file;
         string _fn;
         list<string> _fields;
         list<string> _labels;
         list<string> _units;
         list<string> _desc;
         unsigned long long _records;
         tao::filter const* _filt;
      };

   }
}

#endif
