#include "sqldirect.hh"
#include <fstream>
#include <boost/range.hpp>
#include <boost/algorithm/string/replace.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/tokenizer.hpp>
#include <soci/sqlite3/soci-sqlite3.h>



using namespace hpc;
using boost::algorithm::replace_all;


namespace tao {

	// Factory function used to create a new lightcone.
	module*	sqldirect::factory( const string& name,pugi::xml_node base )
	{
		return new sqldirect( name, base );
	}

	sqldirect::sqldirect( const string& name, pugi::xml_node base )
	: module( name, base )
	{
		_sqlquery="";
		_language="";
		_pass_through=true;
		_database="";

	}

	sqldirect::~sqldirect()
	{
	}


	void  sqldirect::initialise( const options::xml_dict& global_dict )
	{
		LOG_ENTER();

		module::initialise( global_dict );
		_read_options( global_dict );


		LOG_EXIT();
	}

	///
	/// Run the module.
	///
	void sqldirect::execute()
	{
		LOG_ENTER();
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


	   _it++;


	   LOG_EXIT();

	}

	tao::galaxy& sqldirect::galaxy()
    {
		LOG_ENTER();
		LOG_EXIT();
    }



	void sqldirect::begin()
	{
		LOG_ENTER();

		LOGDLN( "Start Begin: ", _it );

		string CurrentQuery=_sqlquery;







		_Tables_it=(*_db).TableNames.begin();


		replace_all( CurrentQuery, "-table-", *_Tables_it );
		LOGDLN( "Query: ", CurrentQuery );


		FetchData(CurrentQuery,true);


		LOGDLN( "End Begin: ", _it );
		LOG_EXIT();
	}

	void sqldirect::FetchData(string query,bool IsFirstCall)
	{
		soci::rowset<soci::row> rs= (*_db)[(*_Tables_it)].prepare << query;
		int rowscount=0;

		_gal.clear();
		_gal.set_table( *_Tables_it );

		if(IsFirstCall==true)
		{
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
						_field_stor[i] = new vector<string>( _batch_size );
						_field_names[i]=props.get_name();
						break;
					case soci::dt_double:
						LOGDLN( "Field Name: ", props.get_name(), " Double" );
						_field_types[i] = galaxy::DOUBLE;
						_field_stor[i] = new vector<double>( _batch_size );
						_field_names[i]=props.get_name();
						break;
					case soci::dt_integer:
						LOGDLN( "Field Name: ", props.get_name(), " Integer" );
						_field_types[i] = galaxy::INTEGER;
						_field_stor[i] = new vector<int>( _batch_size );
						_field_names[i]=props.get_name();
						break;
					case soci::dt_unsigned_long_long:
						LOGDLN( "Field Name: ", props.get_name(), " unsigned Long Long" );
						_field_types[i] = galaxy::UNSIGNED_LONG_LONG;
						_field_stor[i] = new vector<unsigned long long>( _batch_size );
						_field_names[i]=props.get_name();
						break;
					case soci::dt_long_long:
						LOGDLN( "Field Name: ", props.get_name(), " Long Long" );
						_field_types[i] = galaxy::LONG_LONG;
						_field_stor[i] = new vector<long long>( _batch_size );
						_field_names[i]=props.get_name();
						break;
					default:
						ASSERT( 0 );
				}
			}
		}



		for (soci::rowset<soci::row>::const_iterator it = rs.begin(); it != rs.end(); ++it)
		{
			soci::row const& currentrow = *it;


			for(std::size_t i = 0; i != currentrow.size(); ++i)
			{
				const soci::column_properties & props = currentrow.get_properties(i);

				switch(props.get_data_type())
				{
					case soci::dt_string:
						((vector<string>*)_field_stor[i])->push_back(currentrow.get<string>(i));
						break;
					case soci::dt_double:
						((vector<double>*)_field_stor[i])->push_back(currentrow.get<double>(i));
						break;
					case soci::dt_integer:
						((vector<int>*)_field_stor[i])->push_back(currentrow.get<int>(i));
						break;
					case soci::dt_unsigned_long_long:
						((vector<unsigned long long>*)_field_stor[i])->push_back(currentrow.get<unsigned long long>(i));
						break;
					case soci::dt_long_long:
						((vector<long long>*)_field_stor[i])->push_back(currentrow.get<long long>(i));
						break;
					default:
						ASSERT( 0 );
				}

			}
			rowscount++;
			if (rowscount%10000==0)
				LOGDLN( "New Row: ", rowscount);
		}

		for(int i = 0; i < _field_types.size(); i++)
		{
			switch( _field_types[i] )
			{
				case galaxy::STRING:
					LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy" );
					_gal.set_batch_size( ((vector<string>*)_field_stor[i])->size() );
					_gal.set_field<string>( _field_names[i], *(vector<string>*)_field_stor[i] );
					break;
				case galaxy::DOUBLE:
					LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy" );
					_gal.set_batch_size( ((vector<double>*)_field_stor[i])->size() );
					_gal.set_field<double>( _field_names[i], *(vector<double>*)_field_stor[i] );
					break;
				case galaxy::INTEGER:
					LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy" );
					_gal.set_batch_size( ((vector<int>*)_field_stor[i])->size() );
					_gal.set_field<int>( _field_names[i], *(vector<int>*)_field_stor[i] );
					break;
				case galaxy::UNSIGNED_LONG_LONG:
					LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy" );
					_gal.set_batch_size( ((vector<unsigned long long>*)_field_stor[i])->size() );
					_gal.set_field<unsigned long long>( _field_names[i], *(vector<unsigned long long>*)_field_stor[i] );
					break;
				case galaxy::LONG_LONG:
					LOGDLN( "Set Field Name: ", _field_names[i], " To Galaxy" );
					_gal.set_batch_size( ((vector<long long>*)_field_stor[i])->size() );
					_gal.set_field<long long>( _field_names[i], *(vector<long long>*)_field_stor[i] );
					break;
				default:
					ASSERT( 0 );
			}
		}





	}

	bool sqldirect::done()
	{

		LOG_ENTER();
		LOGDLN( "Done: ", (_Tables_it==(*_db).TableNames.end()) );
		if(_Tables_it==(*_db).TableNames.end())
			return true;
		else
			return false;

		LOG_EXIT();

	}

	void sqldirect::operator++()
	{
		LOG_ENTER();
		LOGDLN( "Operator++: ", _it );
		_Tables_it++;
		if(_Tables_it!=(*_db).TableNames.end())
		{

			string CurrentQuery=_sqlquery;

			replace_all( CurrentQuery, "-table-", *_Tables_it );
			LOGDLN( "++Query: ", CurrentQuery );
			FetchData(CurrentQuery);
		}


		LOGDLN( "End Operator++: ", _it );

		LOG_EXIT();

	}


	tao::galaxy& sqldirect::operator*()
	{
		LOG_ENTER();
		LOG_EXIT();

	}

	const set<string>&	sqldirect::get_output_fields() const
	{
		LOG_ENTER();
		LOG_EXIT();

	}




	void  sqldirect::_read_options( const options::xml_dict& global_dict )
    {
		_timer.start();
		LOG_ENTER();



		// Cache the local dictionary.

		_sqlquery=_dict.get<string>( "query" );
		_language=_dict.get<string>( "language", "sql" );


		LOGDLN( "sqlQuery: ", _sqlquery );
		LOGDLN( "query Language: ", _language );


		_pass_through=(_dict.get<string>( "pass-through" )=="True");

		if(_pass_through==true)
		{
			_database=_dict.get<string>( "database" );
		}
		else
		{
			_database="";
		}

		LOGDLN( "database: ", _database );




		// Extract database details.
		_read_db_options( global_dict );

		// Connect to the database.
		_db_connect();


		LOG_EXIT();
		_timer.stop();

    }
}
