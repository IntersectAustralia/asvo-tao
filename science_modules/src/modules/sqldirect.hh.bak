#ifndef tao_modules_sqldirect_sqldirect_hh
#define tao_modules_sqldirect_sqldirect_hh

#include "tao/base/base.hh"
#include "tao/base/types.hh"

namespace tao {
   namespace modules {
      using namespace hpc;

      template< class Backend >
      class sqldirect
	 : public module< Backend >
      {
      public:

	 typedef Backend backend_type;
	 typedef module<backend_type> module_type;

	 static
	 module_type*
	 factory( const string& name,
		  pugi::xml_node base )
	 {
	    return new sqldirect( name, base );
	 }

      public:

	 sqldirect( const string& name = string(),
		    pugi::xml_node base = pugi::xml_node() )
	    : module( name, base )
	 {
	    _sqlquery="";
	    _language="";
	    _pass_through=true;
	    _database="";
	    _RecordsCount=0;
	    _IsRecordLimitReached=false;
	 }

	 virtual
	 ~sqldirect()
	 {
	 }

	 virtual
	 void
	 initialise( const options::xml_dict& global_dict )
	 {
            // Don't initialise if we're already doing so.
            if( this->_init )
               return;
            module_type::initialise( global_dict );

            auto timer = this->timer_start();
            LOGILN( "Initialising sqldirect module.", setindent( 2 ) );

	    _read_options( global_dict );
	 }

	 ///
	 /// Run the module.
	 ///
	 virtual
	 void
	 execute()
	 {
	    LOGDLN( "Execute Iteration: ", _it );

	    if( _it == 0 )
	       begin();
	    else
	       ++(*this);

	    if( done() )
	       _complete = true;
	    else
	    {
	       *(*this);
	    }
	 }

	 virtual
	 tao::batch<real_type>&
	 batch()
	 {
	    return _gal;
	 }

	 ///
	 /// Begin iterating over galaxies.
	 ///
	 void
	 begin()
	 {
	    LOGDLN( "Start Begin: ", _it );

	    string CurrentQuery=_sqlquery;

	    _Tables_it=(*_db).TableNames.begin();

	    _prog.set_local_size( (*_db).TableNames.size() );
	    LOG_PUSH_TAG( "progress" );
	    LOGILN( runtime(), ",progress,", _prog.complete()*100.0, "%" );
	    LOG_POP_TAG( "progress" );

	    replace_all( CurrentQuery, "-table-", *_Tables_it );
	    LOGDLN( "Query: ", CurrentQuery );

	    PrepareGalaxyObject(CurrentQuery);
	    FetchData(CurrentQuery);


	    LOGDLN( "End Begin: ", _it );
	 }

	 ///
	 /// Check for completed iteration.
	 ///
	 bool
	 done()
	 {
	    LOGDLN( "Done: ", (_Tables_it==(*_db).TableNames.end()) );

	    if(_Tables_it==(*_db).TableNames.end()  || _IsRecordLimitReached)
	       return true;
	    else
	       return false;
	 }

	 ///
	 /// Advance to next galaxy.
	 ///
	 void
	 operator++()
	 {
	    LOGDLN( "Operator++: ", _it );
	    _Tables_it++;
	    if(_Tables_it!=(*_db).TableNames.end())
	    {

	       string CurrentQuery=_sqlquery;

	       replace_all( CurrentQuery, "-table-", *_Tables_it );
	       LOGDLN( "++Query: ", CurrentQuery );
	       FetchData(CurrentQuery);

	       _prog.set_delta( 1 );
	       _prog.update();

	       LOG_PUSH_TAG( "progress" );
	       LOGILN( runtime(), ",progress,", _prog.complete()*100.0, "%" );
	       LOG_POP_TAG( "progress" );


	    }


	    LOGDLN( "End Operator++: ", _it );
	 }

	 ///
	 /// Get current batch.
	 ///
	 tao::batch<real_type>&
	 operator*()
	 {
	    return _gal;
	 }

	 bool
	 sqldirect::RecordLimitReached()
	 {

	    if(_OutputLimit!=-1 && _RecordsCount>=_OutputLimit)
	    {
	       return true;
	    }
	    else
	       return false;
	 }

	 void
	 sqldirect::PrepareGalaxyObject(string query)
	 {
	    std::size_t pos=query.find("where");
	    string modquery=query;
	    if(pos!=std::string::npos)
	       modquery=query.substr(0,pos);

	    soci::rowset<soci::row> rs= (*_db)[(*_Tables_it)].prepare << modquery;
	    if (rs.begin()==rs.end())
	       LOGDLN( "Fetch Data: No Data. Query : ",modquery);
	    if(rs.begin()!=rs.end() )
	    {
	       LOGDLN( "Fetch Data: Query : ",modquery);
	       soci::row const& firstrow = *(rs.begin());
	       _field_stor.reallocate( firstrow.size() );
	       _field_types.reallocate( firstrow.size() );
	       _field_names.reallocate( firstrow.size() );
	       for(std::size_t i = 0; i != firstrow.size(); ++i)
	       {
		  const soci::column_properties & props = firstrow.get_properties(i);



		  switch(props.get_data_type())
		  {
		     case soci::dt_string:
			LOGDLN( "Field Name: ", props.get_name(), " String" );
			_field_types[i] = galaxy::STRING;
			_field_stor[i] = new vector<string>();
			_field_names[i]=props.get_name();
			break;
		     case soci::dt_double:
			LOGDLN( "Field Name: ", props.get_name(), " Double" );
			_field_types[i] = galaxy::DOUBLE;
			_field_stor[i] = new vector<double>();
			_field_names[i]=props.get_name();
			break;
		     case soci::dt_integer:
			LOGDLN( "Field Name: ", props.get_name(), " Integer" );
			_field_types[i] = galaxy::INTEGER;
			_field_stor[i] = new vector<int>();
			_field_names[i]=props.get_name();
			break;
		     case soci::dt_unsigned_long_long:
			LOGDLN( "Field Name: ", props.get_name(), " unsigned Long Long" );
			_field_types[i] = galaxy::UNSIGNED_LONG_LONG;
			_field_stor[i] = new vector<unsigned long long>();
			_field_names[i]=props.get_name();
			break;
		     case soci::dt_long_long:
			LOGDLN( "Field Name: ", props.get_name(), " Long Long" );
			_field_types[i] = galaxy::LONG_LONG;
			_field_stor[i] = new vector<long long>();
			_field_names[i]=props.get_name();
			break;
		     default:
			ASSERT( 0 );
		  }

	       }

	    }
	 }

	 void sqldirect::FetchData(string query)
	 {




	    for(int i = 0; i < _field_types.size(); i++)
	    {
	       switch( _field_types[i] )
	       {
		  case galaxy::STRING:

		     ((vector<string>*)_field_stor[i])->clear();
		     break;
		  case galaxy::DOUBLE:
		     ((vector<double>*)_field_stor[i])->clear();
		     break;
		  case galaxy::INTEGER:
		     ((vector<int>*)_field_stor[i])->clear();
		     break;
		  case galaxy::UNSIGNED_LONG_LONG:
		     ((vector<unsigned long long>*)_field_stor[i])->clear();
		  case galaxy::LONG_LONG:
		     ((vector<long long>*)_field_stor[i])->clear();
		     break;
		  default:
		     ASSERT( 0 );
	       }
	    }


	    _gal.clear();
	    _gal.set_table( *_Tables_it );



	    if(RecordLimitReached())
	    {
	       LOGDLN( "Record Limit Reached = ", _RecordsCount," Terminating" );
	       _IsRecordLimitReached=true;
	       return;
	    }

	    soci::rowset<soci::row> rs= (*_db)[(*_Tables_it)].prepare << query;
	    int rowscount=0;


	    for (soci::rowset<soci::row>::const_iterator it = rs.begin(); it != rs.end(); ++it)
	    {

	       if(RecordLimitReached())
	       {
		  LOGDLN( "Record Limit Reached = ", _RecordsCount," Terminating" );

		  break;
	       }

	       LOGDLN( "Record Count= ", _RecordsCount );
	       _RecordsCount++;
	       soci::row const& currentrow = *it;


	       for(std::size_t i = 0; i != currentrow.size(); ++i)
	       {

		  const soci::column_properties & props = currentrow.get_properties(i);

		  switch(props.get_data_type())
		  {
		     case soci::dt_string:
			((vector<string>*)_field_stor[i])->push_back(currentrow.get<string>(i));
			//LOGD(currentrow.get<string>(i));
			break;
		     case soci::dt_double:
			((vector<double>*)_field_stor[i])->push_back(currentrow.get<double>(i));
			//LOGD(currentrow.get<double>(i));
			break;
		     case soci::dt_integer:
			((vector<int>*)_field_stor[i])->push_back(currentrow.get<int>(i));
			//LOGD(currentrow.get<int>(i));
			break;
		     case soci::dt_unsigned_long_long:
			((vector<unsigned long long>*)_field_stor[i])->push_back(currentrow.get<unsigned long long>(i));
			//LOGD(currentrow.get<unsigned long long>(i));
			break;
		     case soci::dt_long_long:
			((vector<long long>*)_field_stor[i])->push_back(currentrow.get<long long>(i));
			//LOGD(currentrow.get<long long>(i));
			break;
		     default:
			ASSERT( 0 );
		  }
		  //LOGD(" , ");

	       }
	       //LOGD("\n");
	       rowscount++;
	       if (rowscount%10000==0)
		  LOGDLN( "New Row: ", rowscount);
	    }




	    for(int i = 0; i < _field_types.size(); i++)
	    {
	       switch( _field_types[i] )
	       {
		  case galaxy::STRING:
		     LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy ... Size=",((vector<string>*)_field_stor[i])->size() );
		     _gal.set_batch_size( ((vector<string>*)_field_stor[i])->size() );
		     _gal.set_field<string>( _field_names[i], *(vector<string>*)_field_stor[i] );
		     break;
		  case galaxy::DOUBLE:
		     LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy ... Size=",((vector<double>*)_field_stor[i])->size()  );
		     _gal.set_batch_size( ((vector<double>*)_field_stor[i])->size() );
		     _gal.set_field<double>( _field_names[i], *(vector<double>*)_field_stor[i] );
		     break;
		  case galaxy::INTEGER:
		     LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy ... Size=",((vector<int>*)_field_stor[i])->size()  );
		     _gal.set_batch_size( ((vector<int>*)_field_stor[i])->size() );
		     _gal.set_field<int>( _field_names[i], *(vector<int>*)_field_stor[i] );
		     break;
		  case galaxy::UNSIGNED_LONG_LONG:
		     LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy ... Size=",((vector<unsigned long long>*)_field_stor[i])->size()  );
		     _gal.set_batch_size( ((vector<unsigned long long>*)_field_stor[i])->size() );
		     _gal.set_field<unsigned long long>( _field_names[i], *(vector<unsigned long long>*)_field_stor[i] );
		     break;
		  case galaxy::LONG_LONG:
		     LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy ... Size=",((vector<long long>*)_field_stor[i])->size()  );
		     _gal.set_batch_size( ((vector<long long>*)_field_stor[i])->size() );
		     _gal.set_field<long long>( _field_names[i], *(vector<long long>*)_field_stor[i] );
		     break;
		  default:
		     ASSERT( 0 );
	       }
	    }

	    /*for (auto& x: _gal._fields)
	      {
	      LOGDLN(x.first);
	      }*/





	 }

      protected:

	 void
	 _read_options( const options::xml_dict& global_dict )
	 {
	    _sqlquery=this->_dict.get<string>( "query" );
	    _OutputLimit=this->_dict.get<long>( "limit", -1 );
	    LOGDLN( "sqlQuery: ", _sqlquery );
	    LOGDLN( "outputRecord Limit: ", _OutputLimit );
	 }

      protected:

	 string _sqlquery;
	 string _language;

	 bool _pass_through;

	 tao::galaxy _gal;
	 profile::progress _prog;

	 string _database;
	 std::list<string>::iterator _Tables_it;



	 vector<void*> _field_stor;
	 vector<galaxy::field_value_type> _field_types;
	 vector<string> _field_names;
	 long _OutputLimit;
	 long _RecordsCount;
	 bool _IsRecordLimitReached;
	 bool RecordLimitReached();
	 void FetchData(string query);
	 void PrepareGalaxyObject(string query);
      };

   }
}


#endif
