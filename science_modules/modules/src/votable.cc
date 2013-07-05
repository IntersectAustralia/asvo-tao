#include <soci/soci.h>
#include "votable.hh"
#include <boost/algorithm/string/replace.hpp>
#include <boost/spirit/include/classic.hpp>

using namespace hpc;
using boost::algorithm::replace_all;

namespace tao {

   module*
   votable::factory( const string& name,
		     pugi::xml_node base )
   {
      return new votable( name, base );
   }

   votable::votable( const string& name, pugi::xml_node base ): module( name, base ),_records( 0 )
   {
      _istableopened=false;
      _isfirstgalaxy=true;
   }

   votable::~votable()
   {
   }


   void votable::ReadFieldsInfo(const options::xml_dict& dict)
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

   ///
   ///
   ///
   void  votable::initialise( const options::xml_dict& global_dict )
   {
      LOG_ENTER();

      _fn = global_dict.get<string>( "outputdir" ) + "/" + _dict.get<string>( "filename" ) + "." + mpi::rank_string();
      _fields = _dict.get_list<string>( "fields" );


      ReadFieldsInfo(_dict);
      // Open the file.
      open();

      // Reset the number of records.
      _records = 0;

      LOG_EXIT();
   }
   string votable::_xml_encode(string _toencode_string)
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
   void votable::_write_table_header(const tao::galaxy& galaxy)
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
	 auto val = galaxy.field( *it );
	 switch( val.second )
	 {
	    case tao::galaxy::STRING:
	       _file<<"datatype=\"char\" arraysize=\"*\" unit=\""+_xml_encode(*unitit)+"\"";
	       break;

	    case tao::galaxy::DOUBLE:
	       _file<<"datatype=\"double\" unit=\""+_xml_encode(*unitit)+"\"";
	       break;

	    case tao::galaxy::INTEGER:
	       _file<<"datatype=\"int\" unit=\""+_xml_encode(*unitit)+"\"";
	       break;

	    case tao::galaxy::UNSIGNED_LONG_LONG:
	       _file<<"datatype=\"long\" unit=\""+_xml_encode(*unitit)+"\"";
	       break;

	    case tao::galaxy::LONG_LONG:
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
///
///
///
   void votable::execute()
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

   void votable::open()
   {
      _file.open( _fn, std::fstream::out | std::fstream::trunc );

      //Put File Header First
      _write_file_header("TempResourceName","TempTableName");
      // Fields information need a single galaxy so I will be waiting till the first galaxy is available

   }

   void votable::finalise()
   {
      _end_table();
      _write_footer();

   }

   void votable::_write_file_header(const string& ResourceName,const string& TableName)
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
   void votable::_write_footer()
   {
      if(_file.is_open())
      {
	 _file<<"</TABLE>"<<std::endl;
	 _file<<"</RESOURCE>"<<std::endl;
	 _file<<"</VOTABLE>"<<std::endl;
      }

   }
   void votable::_start_table()
   {
      _istableopened=true;
      _file<<"<DATA>"<<std::endl;
      _file<<"<TABLEDATA>"<<std::endl;
   }
   void votable::_end_table()
   {

      if(_istableopened)
      {
	 _file<<"</TABLEDATA>"<<std::endl;
	 _file<<"</DATA>"<<std::endl;
	 _istableopened=false;
      }

   }
   void votable::process_galaxy( const tao::galaxy& galaxy )
   {
      _timer.start();

      for( unsigned ii = 0; ii < galaxy.batch_size(); ++ii )
      {
	 auto it = _fields.cbegin();
	 if( it != _fields.cend() )
	 {
	    _file<<"\t<TR>"<<std::endl;

	    while( it != _fields.cend() )
	    {
	       _write_field( galaxy, *it++,ii );
	    }
	    _file<<"\t</TR>"<<std::endl;
	 }

	 // Increment number of written records.
	 ++_records;
      }

      _timer.stop();
   }

   void votable::log_metrics()
   {
      module::log_metrics();
      LOGILN( _name, " number of records written: ", mpi::comm::world.all_reduce( _records ) );
   }

   void votable::_write_field( const tao::galaxy& galaxy, const string& field,unsigned idx )
   {
      _file<<"\t\t<TD>";
      auto val = galaxy.field( field );
      switch( val.second )
      {
	 case tao::galaxy::STRING:
	    _file << galaxy.values<string>( field )[idx];
	    break;

	 case tao::galaxy::DOUBLE:
	    _file << galaxy.values<double>( field )[idx];
	    break;

	 case tao::galaxy::INTEGER:
	    _file << galaxy.values<int>( field )[idx];
	    break;

	 case tao::galaxy::UNSIGNED_LONG_LONG:
	    _file << galaxy.values<unsigned long long>( field )[idx];
	    break;

	 case tao::galaxy::LONG_LONG:
	    _file << galaxy.values<long long>( field )[idx];
	    break;

	 default:
	    ASSERT( 0 );
      }
      _file<<"</TD>"<<std::endl;
   }
}
