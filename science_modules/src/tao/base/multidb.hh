#ifndef tao_base_multidb_hh
#define tao_base_multidb_hh

#include <string>
#include <soci/soci.h>
#include "xml_dict.hh"

namespace tao {
   using namespace std;

   class ServerInfo
   {
   	   public:
		   string ServerHost;
		   string UserName;
		   string Password;
		   string Port;

		   string DBName;
		   soci::session Connection;


		   ServerInfo(const string& _DBName,const string& _Host,const string& _UserName,const string& _Password,const string& _Port);
		   virtual ~ServerInfo();
		   void OpenConnection();
		   void CloseConnection();
		   void RestartConnection();
		   void IncrementConnectionUsage();
                   bool Connected();
   	   private:
		   bool _connected;
		   bool _QueriesCount;
   };

   class multidb
   {


	   public:
                   multidb();
	   	   multidb(const xml_dict& dict);
	   	   multidb(const string& dbname,const string& tree_pre);
           virtual ~multidb();
           void Connect(const xml_dict& dict);
           void CloseAllConnections();
           void RestartAllConnections();
           void OpenAllConnections();
           soci::session& operator [](const string& TableName);
           bool TableExist(const string& TableName);
           bool ExecuteNoQuery_AllServers(const string& SQLStatement);
           bool AddNewServer(string Dbname, string _Host,string _UserName,string _Password,string _Port);
           bool AddNewServer(const string& _Host,const string& _UserName,const string& _Password,const string& _Port);
           soci::session* GetConnectionToAnyServer();
           list<string> TableNames;
           map<string,ServerInfo*> CurrentServers;
           map<string,ServerInfo*> TablesMapping;
           void ReadTableMapping();
	   protected:
           int _serverscount;
           bool _IsTableLoaded;
           std::map<string,ServerInfo*>::iterator DefaultServerIterator;

           string _dbtype, _dbname;
           string _tree_pre;

           void  _read_db_options( const xml_dict& dict );


   };
}


#endif
