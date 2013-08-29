#ifndef tao_base_multidb_hh
#define tao_base_multidb_hh

#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include <libhpc/options/xml_dict.hh>


namespace tao {
   using namespace hpc;

   class ServerInfo
   {
   	   public:
		   string ServerHost;
		   string UserName;
		   string Password;
		   string Port;

		   string DBName;
		   soci::session Connection;


		   ServerInfo(string _DBName,string _Host,string _UserName,string _Password,string _Port);
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
	   	   multidb(const options::xml_dict& dict);
	   	   multidb(string dbname,string tree_pre);
           virtual ~multidb();
           void Connect(const options::xml_dict& dict);
           void CloseAllConnections();
           void RestartAllConnections();
           void OpenAllConnections();
           soci::session& operator [](string TableName);
           bool TableExist(string TableName);
           bool ExecuteNoQuery_AllServers(string SQLStatement);
           bool AddNewServer(string Dbname, string _Host,string _UserName,string _Password,string _Port);
           bool AddNewServer(string _Host,string _UserName,string _Password,string _Port);
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

           void  _read_db_options( const options::xml_dict& dict );


   };
}


#endif
