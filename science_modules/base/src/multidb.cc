#include <soci/sqlite3/soci-sqlite3.h>
#include <soci/postgresql/soci-postgresql.h>
#include <pugixml.hpp>
#include "multidb.hh"


using namespace hpc;
using namespace pugi;

namespace tao
{

	ServerInfo::ServerInfo(string _DBName,pugi::xml_node node)
	{

		ServerHost=node.select_single_node("serverip").node().first_child().value();
	    UserName=node.select_single_node("user").node().first_child().value();
	    Password=node.select_single_node("password").node().first_child().value();
	    Port=node.select_single_node("port").node().first_child().value();
	    DBType="postgresql";
	    DBName=_DBName;


	    _connected=false;
	    _QueriesCount=0;




	}

	ServerInfo::~ServerInfo()
	{
		LOG_ENTER();
		CloseConnection();
		LOG_EXIT();

	}

	void ServerInfo::OpenConnection()
	{
		LOG_ENTER();
		try
		{


			string ConnectionString = "dbname=" + DBName;

			ConnectionString += " host=" + ServerHost;

			ConnectionString += " port=" + Port;

			ConnectionString += " user=" + UserName;

			ConnectionString += " password='" + Password + "'";

			LOGDLN( "Connect string: ", ConnectionString );

			Connection.open( soci::postgresql, ConnectionString );
			_connected=true;
		}
		catch(const std::exception& ex)
		{
			LOGDLN( "Error opening database connection: ", ex.what() );
			ASSERT( 0 );
		}

		LOG_EXIT();

	}

	void ServerInfo::CloseConnection()
	{
		LOG_ENTER();
		if( _connected )
		{
			LOGDLN( "Disconnecting from database." );
			Connection.close();
			_connected = false;
		}
		LOG_EXIT();

	}

	void ServerInfo::RestartConnection()
	{
		LOG_ENTER();
		if(_connected)
		{
			CloseConnection();
			OpenConnection();
		}
		else
		{
			OpenConnection();
		}
		LOG_EXIT();

	}

	void ServerInfo::IncrementConnectionUsage()
	{
		LOG_ENTER();
		_QueriesCount++;
		LOG_EXIT();

	}


	multidb::multidb(const options::xml_dict& dict)
	{
		_read_db_options(dict);
	}

	multidb::~multidb()
	{

	}


	void  multidb::CloseAllConnections()
	{
		for (std::list<ServerInfo*>::iterator it=_CurrentServers.begin(); it != _CurrentServers.end(); ++it)
		    (*it)->CloseConnection();

	}

	void multidb::RestartAllConnections()
	{
		for (std::list<ServerInfo*>::iterator it=_CurrentServers.begin(); it != _CurrentServers.end(); ++it)
			(*it)->RestartConnection();

	}

	void multidb::OpenAllConnections()
	{
		for (std::list<ServerInfo*>::iterator it=_CurrentServers.begin(); it != _CurrentServers.end(); ++it)
				(*it)->OpenConnection();
	}

	void multidb::_read_db_options(const  options::xml_dict& dict )
	{
	      LOG_ENTER();


	      // Extract database details.
	      _dbtype = dict.get<string>( "settings:database:type","postgresql" );
	      _dbname = dict.get<string>( "database" );
	      _tree_pre = dict.get<string>( "settings:database:treetableprefix", "tree_" );
	      _serverscount = dict.get<int>( "settings:database:serverscount", 1 );
	      if( _dbtype != "sqlite" )
	      {
	    	  xpath_node_set ServersSet= dict.get_nodes("settings/database/serverinfo");

	    	  for(xpath_node_set::const_iterator  it = ServersSet.begin(); it != ServersSet.end(); ++it )
	    	  {
	    		  pugi::xpath_node node = *it;
	    		  ServerInfo NewServer(_dbname,node.node());
	    		  _CurrentServers.push_back(&NewServer);

	    	  }


	      }


	      LOG_EXIT();
	}



}


