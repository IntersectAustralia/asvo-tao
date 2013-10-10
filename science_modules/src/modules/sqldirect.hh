#ifndef tao_modules_sqldirect_sqldirect_hh
#define tao_modules_sqldirect_sqldirect_hh

#include <boost/algorithm/string/replace.hpp>
#include "tao/base/base.hh"


namespace tao {
   namespace modules {
      using namespace hpc;
      using boost::algorithm::replace_all;

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
	    : module_type( name, base ),
              _be( 0 )
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
            if( _be )
               delete _be;
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

            // Create the backend.
            _be = new backend_type;
            _be->connect( global_dict );

	    _read_options( global_dict );
	 }

	 ///
	 /// Run the module.
	 ///
	 virtual
	 void
	 execute()
	 {
	    LOGDLN( "Execute Iteration: ", this->_it );

	    if( this->_it == 0 )
	       begin();
	    else
	       ++(*this);

	    if( done() )
	       this->_complete = true;
	    else
	    {
	       *(*this);
	    }
	 }

	 virtual
	 	  optional<boost::any>
	 	  find_attribute( const string& name )
	 	  {

	 		 if( name == "filter" )
	 			 return boost::any( &((tao::filter const&)_filt) );
	 		 else
	 			return module_type::find_attribute( name );
	 	  }


	 virtual
	 tao::batch<real_type>&
	 batch()
	 {
	    return _bat;
	 }

	 ///
	 /// Begin iterating over galaxies.
	 ///
	 void
	 begin()
	 {
	    LOGDLN( "Start Begin: ", this->_it );

	    string CurrentQuery=_sqlquery;

	    _Tables_it=_be->table_begin();

	    _prog.set_local_size( _be->num_tables() );
	    LOG_PUSH_TAG( "progress" );
	    LOGILN( runtime(), ",progress,", _prog.complete()*100.0, "%" );
	    LOG_POP_TAG( "progress" );

	    replace_all( CurrentQuery, "-table-", _Tables_it->name() );
	    LOGDLN( "Query: ", CurrentQuery );

	    PrepareGalaxyObject(CurrentQuery);
	    FetchData(CurrentQuery);


	    LOGDLN( "End Begin: ", this->_it );
	 }

	 ///
	 /// Check for completed iteration.
	 ///
	 bool
	 done()
	 {
            LOGDLN( "Done: ", (_Tables_it==_be->table_end()) );

	    if(_Tables_it==_be->table_end()  || _IsRecordLimitReached)
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
	    LOGDLN( "Operator++: ", this->_it );
	    _Tables_it++;
	    if(_Tables_it!=_be->table_end())
	    {

	       string CurrentQuery=_sqlquery;

	       replace_all( CurrentQuery, "-table-", _Tables_it->name() );
	       LOGDLN( "++Query: ", CurrentQuery );
	       FetchData(CurrentQuery);

	       _prog.set_delta( 1 );
	       _prog.update();

	       LOG_PUSH_TAG( "progress" );
	       LOGILN( runtime(), ",progress,", _prog.complete()*100.0, "%" );
	       LOG_POP_TAG( "progress" );


	    }


	    LOGDLN( "End Operator++: ", this->_it );
	 }

	 ///
	 /// Get current batch.
	 ///
	 tao::batch<real_type>&
	 operator*()
	 {
	    return _bat;
	 }

	 bool
	 RecordLimitReached()
	 {

	    if(_OutputLimit!=-1 && _RecordsCount>=_OutputLimit)
	    {
	       return true;
	    }
	    else
	       return false;
	 }

	 void
	 PrepareGalaxyObject(string query)
	 {
	    std::size_t pos=query.find("where");
	    string modquery=query;
	    if(pos!=std::string::npos)
	       modquery=query.substr(0,pos);

	    soci::rowset<soci::row> rs= _be->session( _Tables_it->name() ).prepare << modquery;
	    if (rs.begin()==rs.end())
	       LOGDLN( "Fetch Data: No Data. Query : ",modquery);
	    if(rs.begin()!=rs.end() )
	    {
	       LOGDLN( "Fetch Data: Query : ",modquery);
	       soci::row const& firstrow = *(rs.begin());
	       _field_types.resize( firstrow.size() );
	       _field_names.resize( firstrow.size() );
	       for(std::size_t i = 0; i != firstrow.size(); ++i)
	       {
		  const soci::column_properties & props = firstrow.get_properties(i);



		  switch(props.get_data_type())
		  {
		     case soci::dt_string:
			LOGDLN( "Field Name: ", props.get_name(), " String" );
			_field_types[i] = tao::batch<real_type>::STRING;
			_field_names[i]=props.get_name();
			_bat.set_scalar<string>( props.get_name() );
			break;
		     case soci::dt_double:
			LOGDLN( "Field Name: ", props.get_name(), " Double" );
			_field_types[i] = tao::batch<real_type>::DOUBLE;
			_field_names[i]=props.get_name();
			_bat.set_scalar<double>( props.get_name() );
			break;
		     case soci::dt_integer:
			LOGDLN( "Field Name: ", props.get_name(), " Integer" );
			_field_types[i] = tao::batch<real_type>::INTEGER;
			_field_names[i]=props.get_name();
			_bat.set_scalar<int>( props.get_name() );
			break;
		     case soci::dt_unsigned_long_long:
			LOGDLN( "Field Name: ", props.get_name(), " unsigned Long Long" );
			_field_types[i] = tao::batch<real_type>::UNSIGNED_LONG_LONG;
			_field_names[i]=props.get_name();
			_bat.set_scalar<unsigned long long>( props.get_name() );
			break;
		     case soci::dt_long_long:
			LOGDLN( "Field Name: ", props.get_name(), " Long Long" );
			_field_types[i] = tao::batch<real_type>::LONG_LONG;
			_field_names[i]=props.get_name();
			_bat.set_scalar<long long>( props.get_name() );
			break;
		     default:
			ASSERT( 0 );
		  }

	       }

	    }
	 }

	 void
         FetchData(string query)
	 {
	    for(int i = 0; i < _field_types.size(); i++)
	    {
	       switch( _field_types[i] )
	       {
	          case tao::batch<real_type>::STRING:
                     boost::any_cast<vector<string>*>( std::get<0>( _bat.field( _field_names[i] ) ) )->clear();
	             // ((vector<string>*)_field_stor[i])->clear();
	             break;
	          case tao::batch<real_type>::DOUBLE:
                     boost::any_cast<vector<double>*>( std::get<0>( _bat.field( _field_names[i] ) ) )->clear();
	             // ((vector<double>*)_field_stor[i])->clear();
	             break;
	          case tao::batch<real_type>::INTEGER:
                     boost::any_cast<vector<int>*>( std::get<0>( _bat.field( _field_names[i] ) ) )->clear();
	             // ((vector<int>*)_field_stor[i])->clear();
	             break;
	          case tao::batch<real_type>::UNSIGNED_LONG_LONG:
                     boost::any_cast<vector<unsigned long long>*>( std::get<0>( _bat.field( _field_names[i] ) ) )->clear();
	             // ((vector<unsigned long long>*)_field_stor[i])->clear();
	          case tao::batch<real_type>::LONG_LONG:
                     boost::any_cast<vector<long long>*>( std::get<0>( _bat.field( _field_names[i] ) ) )->clear();
	             // ((vector<long long>*)_field_stor[i])->clear();
	             break;
	          default:
	             ASSERT( 0 );
	       }
	    }


	    // _bat.clear();
            _bat.set_size( 0 );
            _bat.set_attribute( "table", _Tables_it->name() );
	    // _bat.set_table( *_Tables_it );



	    if(RecordLimitReached())
	    {
	       LOGDLN( "Record Limit Reached = ", _RecordsCount," Terminating" );
	       _IsRecordLimitReached=true;
	       return;
	    }

	    soci::rowset<soci::row> rs= _be->session( _Tables_it->name() ).prepare << query;
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
                        boost::any_cast<vector<string>*>( std::get<0>( _bat.field( _field_names[i] ) ) )->push_back( currentrow.get<string>(i) );
			// ((vector<string>*)_field_stor[i])->push_back(currentrow.get<string>(i));
			//LOGD(currentrow.get<string>(i));
			break;
		     case soci::dt_double:
                        boost::any_cast<vector<double>*>( std::get<0>( _bat.field( _field_names[i] ) ) )->push_back( currentrow.get<double>(i) );
			// ((vector<double>*)_field_stor[i])->push_back(currentrow.get<double>(i));
			//LOGD(currentrow.get<double>(i));
			break;
		     case soci::dt_integer:
                        boost::any_cast<vector<int>*>( std::get<0>( _bat.field( _field_names[i] ) ) )->push_back( currentrow.get<int>(i) );
			// ((vector<int>*)_field_stor[i])->push_back(currentrow.get<int>(i));
			//LOGD(currentrow.get<int>(i));
			break;
		     case soci::dt_unsigned_long_long:
                        boost::any_cast<vector<unsigned long long>*>( std::get<0>( _bat.field( _field_names[i] ) ) )->push_back( currentrow.get<unsigned long long>(i) );
			// ((vector<unsigned long long>*)_field_stor[i])->push_back(currentrow.get<unsigned long long>(i));
			//LOGD(currentrow.get<unsigned long long>(i));
			break;
		     case soci::dt_long_long:
                        boost::any_cast<vector<long long>*>( std::get<0>( _bat.field( _field_names[i] ) ) )->push_back( currentrow.get<long long>(i) );
			// ((vector<long long>*)_field_stor[i])->push_back(currentrow.get<long long>(i));
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



            _bat.update_size();

	    // for(int i = 0; i < _field_types.size(); i++)
	    // {
	    //    switch( _field_types[i] )
	    //    {
	    //       case batch<real_type>::STRING:
	    //          LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy ... Size=",((vector<string>*)_field_stor[i])->size() );
	    //          _bat.set_batch_size( ((vector<string>*)_field_stor[i])->size() );
	    //          _bat.set_field<string>( _field_names[i], *(vector<string>*)_field_stor[i] );
	    //          break;
	    //       case batch<real_type>::DOUBLE:
	    //          LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy ... Size=",((vector<double>*)_field_stor[i])->size()  );
	    //          _bat.set_batch_size( ((vector<double>*)_field_stor[i])->size() );
	    //          _bat.set_field<double>( _field_names[i], *(vector<double>*)_field_stor[i] );
	    //          break;
	    //       case batch<real_type>::INTEGER:
	    //          LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy ... Size=",((vector<int>*)_field_stor[i])->size()  );
	    //          _bat.set_batch_size( ((vector<int>*)_field_stor[i])->size() );
	    //          _bat.set_field<int>( _field_names[i], *(vector<int>*)_field_stor[i] );
	    //          break;
	    //       case batch<real_type>::UNSIGNED_LONG_LONG:
	    //          LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy ... Size=",((vector<unsigned long long>*)_field_stor[i])->size()  );
	    //          _bat.set_batch_size( ((vector<unsigned long long>*)_field_stor[i])->size() );
	    //          _bat.set_field<unsigned long long>( _field_names[i], *(vector<unsigned long long>*)_field_stor[i] );
	    //          break;
	    //       case batch<real_type>::LONG_LONG:
	    //          LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy ... Size=",((vector<long long>*)_field_stor[i])->size()  );
	    //          _bat.set_batch_size( ((vector<long long>*)_field_stor[i])->size() );
	    //          _bat.set_field<long long>( _field_names[i], *(vector<long long>*)_field_stor[i] );
	    //          break;
	    //       default:
	    //          ASSERT( 0 );
	    //    }
	    // }
	 }

      protected:

	 void
	 _read_options( const options::xml_dict& global_dict )
	 {
	    _sqlquery=this->_dict.template get<string>( "query" );
	    _OutputLimit=this->_dict.template get<long>( "limit", -1 );
	    LOGDLN( "sqlQuery: ", _sqlquery );
	    LOGDLN( "outputRecord Limit: ", _OutputLimit );
	 }

      protected:

         backend_type* _be;

	 string _sqlquery;
	 string _language;

	 bool _pass_through;

	 tao::batch<real_type> _bat;
	 profile::progress _prog;

	 string _database;
         typename backend_type::table_iterator _Tables_it;



	 vector<typename tao::batch<real_type>::field_value_type> _field_types;
	 vector<string> _field_names;
	 long _OutputLimit;
	 long _RecordsCount;
	 bool _IsRecordLimitReached;
	 tao::filter _filt;
      };

   }
}


#endif
