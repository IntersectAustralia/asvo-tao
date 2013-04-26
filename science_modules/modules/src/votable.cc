#include <soci/soci.h>
#include "votable.hh"

using namespace hpc;

namespace tao {

   module*
   votable::factory( const string& name )
   {
      return new votable( name );
   }

   votable::votable( const string& name ): module( name ),_records( 0 )
   {
	   _istableopened=false;
	   _isfirstgalaxy=true;
   }

   votable::~votable()
   {
   }



   ///
   ///
   ///
   void  votable::initialise( const options::xml_dict& dict, optional<const string&> prefix )
   {
      LOG_ENTER();




      _fn = dict.get<hpc::string>( prefix.get()+":filename" );
      _fields = dict.get_list<hpc::string>( prefix.get()+":fields" );

      // Open the file.
      open();

      // Reset the number of records.
      _records = 0;

      LOG_EXIT();
   }

   void votable::_write_table_header(const tao::galaxy& galaxy)
   {
	   	 auto it = _fields.cbegin();
	   	 while( it != _fields.cend() )
		 {
	   		   _file<<"<FIELD name=\""+(*it)<<"\" ID=\"Col_"<<(*it)<<"\" ";
			   auto val = galaxy.field( *it );
			   switch( val.second )
			   {
				 case tao::galaxy::STRING:
					_file<<"datatype=\"char\" arraysize=\"*\"/>";
					break;

				 case tao::galaxy::DOUBLE:
					 _file<<"datatype=\"double\"/>";
					break;

				 case tao::galaxy::INTEGER:
					 _file<<"datatype=\"int\"/>";
					break;

				 case tao::galaxy::UNSIGNED_LONG_LONG:
					 _file<<"datatype=\"long\"/>";
					break;

				 case tao::galaxy::LONG_LONG:
					 _file<<"datatype=\"long\"/>";
					break;

				 default:
					ASSERT( 0 );
			   }
			 it++;
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
            _file<<"<TR>"<<std::endl;

            while( it != _fields.cend() )
            {
               _write_field( galaxy, ii, *it++ );
            }
            _file<<"</TR>"<<std::endl;
         }

         // Increment number of written records.
         ++_records;
      }

      _timer.stop();
   }

   void votable::log_metrics()
   {
      module::log_metrics();
      LOGILN( _name, " number of records written: ", _records );
   }

   void votable::_write_field( const tao::galaxy& galaxy, unsigned idx, const string& field )
   {
	   _file<<"<TD>"<<std::endl;
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
