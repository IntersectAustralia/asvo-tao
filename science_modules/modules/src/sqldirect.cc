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

		if(IsFirstCall==true)
		{
			soci::row const& firstrow = *(rs.begin());

			for(std::size_t i = 0; i != firstrow.size(); ++i)
			{
				const soci::column_properties & props = firstrow.get_properties(i);



				switch(props.get_data_type())
				{
				case soci::dt_string:
					LOGDLN( "Field Name: ", props.get_name(), " String" );
					break;
				case soci::dt_double:
					LOGDLN( "Field Name: ", props.get_name(), " Double" );
					break;
				case soci::dt_integer:
					LOGDLN( "Field Name: ", props.get_name(), " Integer" );
					break;
				case soci::dt_unsigned_long:
					LOGDLN( "Field Name: ", props.get_name(), " Long" );
					break;
				case soci::dt_long_long:
					LOGDLN( "Field Name: ", props.get_name(), " Long Long" );
					break;
				case soci::dt_date:
					LOGDLN( "Field Name: ", props.get_name(), " Date" );

					break;
				}


			}
		}









		for (soci::rowset<soci::row>::const_iterator it = rs.begin(); it != rs.end(); ++it)
		{
			soci::row const& currentrow = *it;
			//LOGDLN( "New Row: ", rowscount++ );
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
