#include "sqldirect.hh"
#include <fstream>
#include <boost/range.hpp>
#include <boost/algorithm/string/replace.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/tokenizer.hpp>
#include <soci/sqlite3/soci-sqlite3.h>



using namespace hpc;

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
		_server="";
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
	}

	tao::galaxy& sqldirect::galaxy()
    {
    }

	void  sqldirect::_read_options( const options::xml_dict& global_dict )
    {
		_timer.start();
		LOG_ENTER();

		// Cache the local dictionary.
		const options::xml_dict& dict = _dict;

		_sqlquery=dict.get<string>( "query", "sql" );
		_language=dict.get<string>( "language", "sql" );


		LOGDLN( "sqlQuery: ", _sqlquery );
		LOGDLN( "query Language: ", _language );


		_pass_through=(dict.get<string>( "pass-through", "sql" )=="True");

		if(_pass_through==true)
		{
			_database=dict.get<string>( "database", "sql" );
			_server=dict.get<string>( "server", "sql" );
		}
		else
		{
			_database="";
			_server="";
		}

		LOGDLN( "database: ", _database );
		LOGDLN( "server: ", _server );




		LOG_EXIT();
		_timer.stop();

    }
}
