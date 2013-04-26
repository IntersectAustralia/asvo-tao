#include <soci/soci.h>
#include "fits.hh"
#include <boost/algorithm/string/replace.hpp>


using namespace hpc;
using boost::algorithm::replace_all;

namespace tao {

module*
fits::factory( const string& name )
{
	return new fits( name );
}

fits::fits( const string& name ): module( name ),_records( 0 )
{
	_istableopened=false;
	_isfirstgalaxy=true;
}

fits::~fits()
{
}


void fits::ReadFieldsInfo(const options::xml_dict& dict, optional<const string&> prefix)
{
	list<optional<hpc::string>> Templabels = dict.get_list_attributes<hpc::string>( prefix.get()+":fields","label" );
	list<optional<hpc::string>> Tempunits = dict.get_list_attributes<hpc::string>( prefix.get()+":fields","units" );
	list<optional<hpc::string>> Tempdescription = dict.get_list_attributes<hpc::string>( prefix.get()+":fields","description" );


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

///
///
///
void  fits::initialise( const options::xml_dict& dict, optional<const string&> prefix )
{
	LOG_ENTER();




	_fn = dict.get<hpc::string>( prefix.get()+":filename" );
	_fields = dict.get_list<hpc::string>( prefix.get()+":fields" );

	ReadFieldsInfo(dict,prefix);
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
		ttype[index]=new char[FieldName.length()];
		tunit[index]=new char[(*unitit).length()];
		memcpy(ttype[index],FieldName.c_str(),(int)FieldName.length());
		memcpy(tunit[index],(*unitit).c_str(),(int)(*unitit).length());
		tform[index]=new char[3];





		auto val = galaxy.field( *it );
		switch( val.second )
		{
		case tao::galaxy::STRING:
			tform[index]="A";
			break;

		case tao::galaxy::DOUBLE:
			tform[index]="D";
			break;

		case tao::galaxy::INTEGER:
			tform[index]="J";
			break;

		case tao::galaxy::UNSIGNED_LONG_LONG:
			tform[index]="K";
			break;

		case tao::galaxy::LONG_LONG:
			tform[index]="K";
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
	if(fits_create_tbl(_file,BINARY_TBL,0,tfields,ttype,tform,ttype,TableName.c_str(),&status))
	{
		LOGILN(status);
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
		_start_table();
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
			LOGILN(status);
			ASSERT(status==0);
	}


	//Put File Header First
	_write_file_header("TempResourceName","TempTableName");
	// Fields information need a single galaxy so I will be waiting till the first galaxy is available

}

void fits::finalise()
{
	_end_table();
	_write_footer();

}

void fits::_write_file_header(const string& ResourceName,const string& TableName)
{
	/*if(_file.is_open())
	   {
		   _file<<"<?xml version=\"1.0\"?>"<<std::endl;
		   _file<<"<VOTABLE version=\"1.3\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns=\"http://www.ivoa.net/xml/VOTable/v1.3\"";
		   _file<<" xmlns:stc=\"http://www.ivoa.net/xml/STC/v1.30\" >"<<std::endl;
		   _file<<"<RESOURCE name=\""<<ResourceName<<"\">"<<std::endl;
		   _file<<"<TABLE name=\""<<TableName<<"\">"<<std::endl;
	   }*/

}
void fits::_write_footer()
{
	/*if(_file.is_open())
	   {
		   _file<<"</TABLE>"<<std::endl;
		   _file<<"</RESOURCE>"<<std::endl;
		   _file<<"</VOTABLE>"<<std::endl;
	   }*/

}
void fits::_start_table()
{
	/*_istableopened=true;
	   _file<<"<DATA>"<<std::endl;
	   _file<<"<TABLEDATA>"<<std::endl;*/
}
void fits::_end_table()
{

	/*if(_istableopened)
	   {
		   _file<<"</TABLEDATA>"<<std::endl;
		   _file<<"</DATA>"<<std::endl;
		   _istableopened=false;
	   }*/

}
void fits::process_galaxy( const tao::galaxy& galaxy )
{
	_timer.start();

	auto it = _fields.cbegin();
	if( it != _fields.cend() )
	{
		//_file<<"<TR>"<<std::endl;

		while( it != _fields.cend() )
		{
			_write_field( galaxy, *it++ );
		}
		//_file<<"</TR>"<<std::endl;
	}

	// Increment number of written records.
	++_records;

	_timer.stop();
}

void fits::log_metrics()
{
	module::log_metrics();
	LOGILN( _name, " number of records written: ", _records );
}

void fits::_write_field( const tao::galaxy& galaxy, const string& field )
{
	// _file<<"<TD>"<<std::endl;
	auto val = galaxy.field( field );
	switch( val.second )
	{
	case tao::galaxy::STRING:
		//_file << galaxy.value<string>( field );
		break;

	case tao::galaxy::DOUBLE:
		//_file << galaxy.value<double>( field );
		break;

	case tao::galaxy::INTEGER:
		//_file << galaxy.value<int>( field );
		break;

	case tao::galaxy::UNSIGNED_LONG_LONG:
		//_file << galaxy.value<unsigned long long>( field );
		break;

	case tao::galaxy::LONG_LONG:
		//_file << galaxy.value<long long>( field );
		break;

	default:
		ASSERT( 0 );
	}
	//_file<<"</TD>"<<std::endl;
}
}
