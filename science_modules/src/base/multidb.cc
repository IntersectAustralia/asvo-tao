#include <stdio.h>
#include <soci/soci.h>
#ifdef HAVE_POSTGRESQL
#include <soci/postgresql/soci-postgresql.h>
#endif
#include <pugixml.hpp>
#include <libhpc/logging.hh>
#include <libhpc/debug/assert.hh>
#include "multidb.hh"

using namespace hpc;
using namespace pugi;
using namespace soci;
using namespace std;


namespace tao
{

	ServerInfo::ServerInfo(const string& _DBName,const string& _Host,const string& _UserName,const string& _Password,const string& _Port)
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
		CloseConnection();
	}

	void ServerInfo::OpenConnection()
	{
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

#ifdef HAVE_POSTGRESQL
				Connection.open( soci::postgresql, ConnectionString );
#endif

				_connected=true;
			}
		}
		catch(const std::exception& ex)
		{
			LOGDLN( "Error opening database connection: ", ex.what() );
			ASSERT( 0 );
		}
	}

	void ServerInfo::CloseConnection()
	{
		if( _connected )
		{
			LOGDLN( "Disconnecting from database." );
			Connection.close();
			_connected = false;
		}
	}

	void ServerInfo::RestartConnection()
	{
		if(_connected)
		{
			CloseConnection();
			OpenConnection();
		}
		else
		{
			OpenConnection();
		}
	}

	void ServerInfo::IncrementConnectionUsage()
	{
		_QueriesCount++;
	}

	bool ServerInfo::Connected()
	{
           return _connected;
	}

        multidb::multidb()
	{
		_serverscount=0;
		_tree_pre="tree_";
		_IsTableLoaded=false;
	}

	multidb::multidb(const xml_dict& dict)
	{
		_serverscount=0;
		_IsTableLoaded=false;
		_read_db_options(dict);
		ReadTableMapping();

	}
	multidb::multidb(const string& dbname,const string& tree_pre)
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

        void multidb::Connect(const xml_dict& dict)
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

	bool multidb::AddNewServer(const string& _Host,const string& _UserName,const string& _Password,const string& _Port)
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

	void multidb::_read_db_options(const xml_dict& dict)
	{
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

                bool old_state = TempDbServer->Connected();
                if( !old_state )
                   TempDbServer->OpenConnection();

                // Must destroy rowset before disconnection (added by Luke).
                {

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

                }

                if( !old_state )
                   TempDbServer->CloseConnection();

		_IsTableLoaded=true;
		LOGDLN( "Table Mapping Done");

	}

	bool multidb::TableExist(const string& TableName)
	{
		ASSERT(_IsTableLoaded);
		return (TablesMapping.count(TableName)>0);
	}

	bool multidb::ExecuteNoQuery_AllServers(const string& SQLStatement)
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

	soci::session& multidb::operator [](const string& TableName)
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


