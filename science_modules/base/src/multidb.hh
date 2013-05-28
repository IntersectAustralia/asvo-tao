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

		   ServerInfo(string _DBName,pugi::xml_node node);
		   virtual ~ServerInfo();
		   void OpenConnection();
		   void CloseConnection();
		   void RestartConnection();
		   void IncrementConnectionUsage();
   	   private:
		   bool _connected;
		   bool _QueriesCount;
   };

   class multidb
   {


	   public:
	   	   multidb(const options::xml_dict& dict);
           virtual ~multidb();
           void CloseAllConnections();
           void RestartAllConnections();
           void OpenAllConnections();
           soci::session& operator [](string TableName);
           bool TableExist(string TableName);
           bool ExecuteNoQuery_AllServers(string SQLStatement);
           soci::session* GetConnectionToAnyServer();
           list<string> TableNames;
           map<string,ServerInfo*> CurrentServers;
           map<string,ServerInfo*> TablesMapping;
	   protected:
           int _serverscount;
           std::map<string,ServerInfo*>::iterator DefaultServerIterator;

           string _dbtype, _dbname;
           string _tree_pre;
           void ReadTableMapping();
           void  _read_db_options( const options::xml_dict& dict );


   };
}


#endif
