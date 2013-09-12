#include <soci/soci.h>
#include "fits.hh"
#include <boost/algorithm/string/replace.hpp>
#include <boost/spirit/include/classic.hpp>

using namespace hpc;
using boost::algorithm::replace_all;

namespace tao {

   module*
   fits::factory( const string& name,
		  pugi::xml_node base )
   {
      return new fits( name, base );
   }

   fits::fits( const string& name, pugi::xml_node base ): module( name, base ),_records( 0 )
   {
      _istableopened=false;
      _isfirstgalaxy=true;
   }

   fits::~fits()
   {
   }


   void fits::ReadFieldsInfo(const options::xml_dict& dict )
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
	    _units.push_back("");
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

///
///
///
   void  fits::initialise( const options::xml_dict& global_dict )
   {
      LOG_ENTER();


      if(mpi::comm::world.size()==1)
    	  _fn = global_dict.get<string>( "outputdir" ) + "/" + _dict.get<hpc::string>( "filename" ) ;
      else
    	  _fn = global_dict.get<string>( "outputdir" ) + "/" + _dict.get<hpc::string>( "filename" ) + "." + mpi::rank_string();



      _fields = _dict.get_list<hpc::string>( "fields" );

      ReadFieldsInfo(_dict );
      // Open the file.
      open();

      // Reset the number of records.
      _records = 0;

      LOG_EXIT();
   }

   void fits::_write_table_header(const tao::galaxy& galaxy)
   {
      LOG_ENTER();


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
	 FieldName=encode_fieldName(FieldName);
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





	 auto val = galaxy.field( *it );
	 switch( val.second )
	 {
	    case tao::galaxy::STRING:
	       tform[index]=(char*)"A";
	       break;

	    case tao::galaxy::DOUBLE:
	       tform[index]=(char*)"D";
	       break;

	    case tao::galaxy::INTEGER:
	       tform[index]=(char*)"J";
	       break;

	    case tao::galaxy::UNSIGNED_LONG_LONG:
	       tform[index]=(char*)"K";
	       break;

	    case tao::galaxy::LONG_LONG:
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
      LOG_EXIT();
   }
///
///
///
   void fits::execute()
   {
      _timer.start();
      LOG_ENTER();
      ASSERT( parents().size() == 1 );



      // Grab the galaxy from the parent object.
      tao::galaxy& gal = parents().front()->galaxy();

      // Is this the first galaxy? if so, please write the fields information
      if(_isfirstgalaxy)
      {
	 _write_table_header(gal);

	 _isfirstgalaxy=false;
      }
      //Process the galaxy as any other galaxy
      process_galaxy( gal );

      LOG_EXIT();
      _timer.stop();
   }

   void fits::open()
   {
      int status=0;
      if(fits_create_file(&_file,("!"+_fn).c_str(), &status))
      {
	 LOGDLN(status);
	 ASSERT(status==0);
      }




      // Fields information need a single galaxy so I will be waiting till the first galaxy is available

   }

   void fits::finalise()
   {

      int status=0;
      if(fits_close_file(_file,&status))
	 ASSERT(status==0);

   }




   void fits::process_galaxy( tao::galaxy& galaxy )
   {
      _timer.start();

      for( galaxy.begin(); !galaxy.done(); galaxy.next() )
      {

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
	       _write_field( galaxy, *it++,ColIndex );
	       ColIndex++;
	    }

	 }

	 // Increment number of written records.
	 ++_records;
	 LOGDLN("FITS: ROW Count=",_records);
      }
      _timer.stop();
   }

   void fits::log_metrics()
   {
      module::log_metrics();
      LOGILN( _name, " number of records written: ", mpi::comm::world.all_reduce( _records ) );
   }

   string fits::encode_fieldName(string _toencode_string)
   	{
   		std::map<char, std::string> transformations;
   		transformations['&']  = std::string("_");
   		transformations['(']  = std::string("");
   		transformations[')']  = std::string("");
   		transformations['\''] = std::string("_");
   		transformations['"']  = std::string("_");
   		transformations['>']  = std::string("_");
   		transformations['<']  = std::string("_");
   		transformations['*']  = std::string("_");
   		transformations[' ']  = std::string("_");
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

   void fits::_write_field( const tao::galaxy& galaxy, const string& field,int ColIndex )
   {
      int status=0;


      auto val = galaxy.field( field );
      switch( val.second )
      {
	 case tao::galaxy::STRING:
	    fits_write_col(_file,TSTRING,ColIndex,_records+1,1,1,(void*)galaxy.current_value<string>(field).c_str(),&status);
	    LOGDLN(status);
	    ASSERT(status==0);
	    break;

	 case tao::galaxy::DOUBLE:
	 {
	    double FieldVal=galaxy.current_value<double>( field );
	    fits_write_col(_file,TDOUBLE,ColIndex,_records+1,1,1,(void*)&FieldVal,&status);
	    LOGDLN(status);
	    ASSERT(status==0);
	 }
	 break;

	 case tao::galaxy::INTEGER:
	 {
	    int FieldVal=galaxy.current_value<int>(field);
	    fits_write_col(_file,TINT,ColIndex,_records+1,1,1,(void*)&FieldVal,&status);
	    LOGDLN(status);
	    ASSERT(status==0);
	 }
	 break;

	 case tao::galaxy::UNSIGNED_LONG_LONG:
	 {
	    unsigned long long FieldVal=galaxy.current_value<unsigned long long>(field);
	    fits_write_col(_file,TLONG,ColIndex,_records+1,1,1,(void*)&FieldVal,&status);
	    LOGDLN(status);
	    ASSERT(status==0);
	 }
	 break;

	 case tao::galaxy::LONG_LONG:
	 {
	    long long FieldVal=galaxy.current_value<long long>(field);
	    fits_write_col(_file,TLONG,ColIndex,_records+1,1,1,(void*)&FieldVal,&status);
	    LOGDLN(status);
	    ASSERT(status==0);
	 }
	 break;

	 default:
	    ASSERT( 0 );
      }

   }
}
