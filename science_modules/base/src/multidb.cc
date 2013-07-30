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

	ServerInfo::ServerInfo(string _DBName,string _Host,string _UserName,string _Password,string _Port)
	{
		ServerHost=_Host;
		UserName=_UserName;
		Password=_Password;
		Port=_Port;
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

        multidb::multidb()
	{
		_serverscount=0;
		_tree_pre="tree_";
		_IsTableLoaded=false;
	}

	multidb::multidb(const options::xml_dict& dict)
	{
		LOG_ENTER();
		_serverscount=0;
		_IsTableLoaded=false;
		_read_db_options(dict);
		ReadTableMapping();
		LOG_EXIT();

	}
	multidb::multidb(string dbname,string tree_pre)
	{
		_serverscount=0;
		_dbname=dbname;
		_tree_pre=tree_pre;
		_IsTableLoaded=false;
	}

	multidb::~multidb()
	{
		for (std::map<string,ServerInfo*>::iterator it=CurrentServers.begin(); it != CurrentServers.end(); ++it)
				    delete it->second;
		CurrentServers.erase(CurrentServers.begin(),CurrentServers.end());
	}

        void multidb::Connect(const options::xml_dict& dict)
	{
		_serverscount=0;
		_IsTableLoaded=false;
		_read_db_options(dict);
		ReadTableMapping();
                OpenAllConnections();
	}
	void  multidb::CloseAllConnections()
	{
		ASSERT(!CurrentServers.empty());
		for (std::map<string,ServerInfo*>::iterator it=CurrentServers.begin(); it != CurrentServers.end(); ++it)
			it->second->CloseConnection();

	}

	void multidb::RestartAllConnections()
	{
		ASSERT(!CurrentServers.empty());
		for (std::map<string,ServerInfo*>::iterator it=CurrentServers.begin(); it != CurrentServers.end(); ++it)
			it->second->RestartConnection();

	}

	void multidb::OpenAllConnections()
	{
		ASSERT(!CurrentServers.empty());
		for (std::map<string,ServerInfo*>::iterator it=CurrentServers.begin(); it != CurrentServers.end(); ++it)
		{
			it->second->OpenConnection();
		}
	}

        bool multidb::AddNewServer(string Dbname, string _Host,string _UserName,string _Password,string _Port)
	{
		ServerInfo* NewServer = new ServerInfo(Dbname, _Host,_UserName,_Password,_Port);
		CurrentServers[NewServer->ServerHost] = NewServer;
		if(_serverscount==0)
		{
			LOGDLN( "Setting Default Server Iterator!");
			DefaultServerIterator=CurrentServers.begin();
		}
		LOGDLN( "ServerCount ", _serverscount );
		_serverscount++;
	}

	bool multidb::AddNewServer(string _Host,string _UserName,string _Password,string _Port)
	{
		ServerInfo* NewServer = new ServerInfo(_dbname, _Host,_UserName,_Password,_Port);
		CurrentServers[NewServer->ServerHost] = NewServer;
		if(_serverscount==0)
		{
			LOGDLN( "Setting Default Server Iterator!");
			DefaultServerIterator=CurrentServers.begin();
		}
		LOGDLN( "ServerCount ", _serverscount );
		_serverscount++;
	}

	void multidb::_read_db_options(const options::xml_dict& dict)
	{
		LOG_ENTER();
		// Extract database details.
		_dbtype = dict.get < string > ("settings:database:type", "postgresql");
		_dbname = dict.get < string > ("database");
		_tree_pre = dict.get < string> ("settings:database:treetableprefix", "tree_");
		// _serverscount = dict.get<int>("settings:database:serverscount", 1);
		xpath_node_set ServersSet = dict.get_nodes("settings/database/serverinfo");

		// If there is no servers at all, Raise exception
		ASSERT(!ServersSet.empty());
		// If the number of servers claimed in settings:database:serverscount is no equal to number of serverinfo nodes
		// also, raise exception
		//_serverscount = ServersSet.size();
		// ASSERT(_serverscount==ServersSet.size());

		for (xpath_node_set::const_iterator it = ServersSet.begin();it != ServersSet.end(); ++it)
		{
			pugi::xpath_node node = *it;
			pugi::xml_node CurrentNode=node.node();
			string ServerHost=CurrentNode.select_single_node("serverip").node().first_child().value();
			string UserName=CurrentNode.select_single_node("user").node().first_child().value();
			string Password=CurrentNode.select_single_node("password").node().first_child().value();
			string Port=CurrentNode.select_single_node("port").node().first_child().value();
			AddNewServer(ServerHost,UserName,Password,Port);

		}
		LOG_EXIT();
	}

	void multidb::ReadTableMapping()
	{
		LOGDLN( "Reading Table Mapping");
		ASSERT(!CurrentServers.empty());
		// Get Object of the first DB Server to load the data from it
		std::map<string, ServerInfo*>::iterator it = CurrentServers.begin();

		ServerInfo* TempDbServer = it->second;


		// I can get at least one server
		ASSERT(TempDbServer!=NULL);

		TempDbServer->OpenConnection();
		string query ="SELECT tablename, nodename  FROM table_db_mapping Where isactive=True;";
		rowset < row > TablesMappingRowset = (TempDbServer->Connection.prepare << query);
		TablesMapping.clear();
		TableNames.clear();

		for (rowset<row>::const_iterator it = TablesMappingRowset.begin();it != TablesMappingRowset.end(); ++it)
		{
			const row& row = *it;
			string TableName=row.get<string>(0);
			if(TablesMapping.count(TableName)==0)
				TablesMapping[TableName]=CurrentServers[row.get<string>(1)];
			TableNames.push_back(TableName);
		}

		TempDbServer->CloseConnection();
		_IsTableLoaded=true;
		LOGDLN( "Table Mapping Done");

	}

	bool multidb::TableExist(string TableName)
	{
		ASSERT(_IsTableLoaded);
		return (TablesMapping.count(TableName)>0);
	}

	bool multidb::ExecuteNoQuery_AllServers(string SQLStatement)
	{
		ASSERT(!CurrentServers.empty());
		ASSERT(_IsTableLoaded);

		for (std::map<string,ServerInfo*>::iterator it=CurrentServers.begin(); it != CurrentServers.end(); ++it)
		{
			it->second->OpenConnection();
			it->second->Connection<<SQLStatement;
		}
		return true;

	}

	soci::session* multidb::GetConnectionToAnyServer()
	{
		ASSERT(!CurrentServers.empty());
		ASSERT(_IsTableLoaded);

		if(DefaultServerIterator==CurrentServers.end())
		{
			DefaultServerIterator=CurrentServers.begin();
		}

		DefaultServerIterator->second->OpenConnection();
		soci::session* OpenedSession= &DefaultServerIterator->second->Connection;

		DefaultServerIterator++;
		return OpenedSession;

	}

	soci::session& multidb::operator [](string TableName)
	{
		ASSERT(!CurrentServers.empty());
		if(_IsTableLoaded==false)
		{
			ReadTableMapping();
		}

		if(TablesMapping.count(TableName)>0)
		{
			TablesMapping[TableName]->OpenConnection();
			return TablesMapping[TableName]->Connection;

		}
		else
		{
			//Table Name Doesnot exists in the List
			assert(0);
		}
	}
}


