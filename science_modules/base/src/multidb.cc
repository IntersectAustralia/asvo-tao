#include <soci/sqlite3/soci-sqlite3.h>
#include <soci/postgresql/soci-postgresql.h>
#include <pugixml.hpp>
#include "multidb.hh"
#include <stdio.h>

using namespace hpc;
using namespace pugi;
using namespace soci;
using namespace std;


namespace tao
{

	ServerInfo::ServerInfo(string _DBName,pugi::xml_node node)
	{

		ServerHost=node.select_single_node("serverip").node().first_child().value();
	    UserName=node.select_single_node("user").node().first_child().value();
	    Password=node.select_single_node("password").node().first_child().value();
	    Port=node.select_single_node("port").node().first_child().value();

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

			if(!_connected)
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
		ReadTableMapping();
		DefaultServerIterator=CurrentServers.begin();
	}

	multidb::~multidb()
	{
		for (std::map<string,ServerInfo*>::iterator it=CurrentServers.begin(); it != CurrentServers.end(); ++it)
				    delete it->second;
		CurrentServers.erase(CurrentServers.begin(),CurrentServers.end());
	}


	void  multidb::CloseAllConnections()
	{
		for (std::map<string,ServerInfo*>::iterator it=CurrentServers.begin(); it != CurrentServers.end(); ++it)
			it->second->CloseConnection();

	}

	void multidb::RestartAllConnections()
	{
		for (std::map<string,ServerInfo*>::iterator it=CurrentServers.begin(); it != CurrentServers.end(); ++it)
			it->second->RestartConnection();

	}

	void multidb::OpenAllConnections()
	{
		for (std::map<string,ServerInfo*>::iterator it=CurrentServers.begin(); it != CurrentServers.end(); ++it)
		{
			it->second->OpenConnection();
		}
	}



	void multidb::_read_db_options(const options::xml_dict& dict)
	{
		LOG_ENTER();
		// Extract database details.
		_dbtype = dict.get < string > ("settings:database:type", "postgresql");
		_dbname = dict.get < string > ("database");
		_tree_pre = dict.get < string
				> ("settings:database:treetableprefix", "tree_");
		_serverscount = dict.get<int>("settings:database:serverscount", 1);
		xpath_node_set ServersSet = dict.get_nodes("settings/database/serverinfo");
		for (xpath_node_set::const_iterator it = ServersSet.begin();it != ServersSet.end(); ++it)
		{
			pugi::xpath_node node = *it;
			ServerInfo* NewServer = new ServerInfo(_dbname, node.node());
			CurrentServers[NewServer->ServerHost] = NewServer;
		}
		LOG_EXIT();
	}

	void multidb::ReadTableMapping()
	{
		// Get Object of the first DB Server to load the data from it
		std::map<string, ServerInfo*>::iterator it = CurrentServers.begin();
		ServerInfo* TempDbServer = it->second;
		TempDbServer->OpenConnection();
		string query ="SELECT tablename, nodename  FROM table_db_mapping Where isactive=True;";
		rowset < row > TablesMappingRowset = (TempDbServer->Connection.prepare << query);
		for (rowset<row>::const_iterator it = TablesMappingRowset.begin();it != TablesMappingRowset.end(); ++it)
		{
			const row& row = *it;
			string TableName=row.get<string>(0);
			if(TablesMapping.count(TableName)==0)
				TablesMapping[TableName]=CurrentServers[row.get<string>(1)];
			TableNames.push_back(TableName);
		}

		TempDbServer->CloseConnection();

	}

	bool multidb::TableExist(string TableName)
	{
		return (TablesMapping.count(TableName)>0);
	}

	bool multidb::ExecuteNoQuery_AllServers(string SQLStatement)
	{
		for (std::map<string,ServerInfo*>::iterator it=CurrentServers.begin(); it != CurrentServers.end(); ++it)
		{
			it->second->OpenConnection();
			it->second->Connection<<SQLStatement;
		}

	}

	soci::session* multidb::GetConnectionToAnyServer()
	{

		if(DefaultServerIterator==CurrentServers.end())
		{
			DefaultServerIterator=CurrentServers.begin();
		}
		DefaultServerIterator->second->OpenConnection();
		soci::session* OpenedSession= &DefaultServerIterator->second->Connection;

		DefaultServerIterator++;
		return OpenedSession;

	}


	soci::session* multidb::operator [](string TableName)
	{
		if(TablesMapping.count(TableName)>0)
		{
			TablesMapping[TableName]->OpenConnection();
			return &TablesMapping[TableName]->Connection;

		}
		else
		{
			//Table Name Doesnot exists in the List
			assert(0);
		}
	}



}


