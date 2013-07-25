#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <libhpc/libhpc.hh>
#include <vector>
#include <iostream>
#include <pugixml.hpp>

#include "tao/base/base.hh"
#include "tao/modules/modules.hh"
#include "tao/base/multidb.hh"

using namespace std;
using namespace hpc;
using namespace tao;
#define NDEBUG




class MultiDB_suite : public CxxTest::TestSuite
{
public:


	void test_MultiDB()
	{


		LOG_PUSH( new logging::file( "TestLog.log" ) );
		TS_TRACE("Starting MultiDB Test");
		string ParamXMLFile="params0.xml";
		string BasicXMLFile="basicsetting.xml";
		options::xml_dict xml;

		xml.read( ParamXMLFile, "/tao" );
		xml.read( BasicXMLFile );

		TS_TRACE("XML Read Done");

		multidb db("bolshoi_full_dist","tree_");
		db.AddNewServer("tao01.hpc.swin.edu.au","taoadmin","tao_admin_password_##","3306");
		db.AddNewServer("tao02.hpc.swin.edu.au","taoadmin","tao_admin_password_##","3306");


		db.OpenAllConnections();
		db.RestartAllConnections();
		db.CloseAllConnections();

		db["tree_1"];

		TS_TRACE("Tree Loading Test");
		soci::session* OldConnection=NULL;
		for(int j=0;j<10;j++)
		{
			soci::session*  CurrentConnection=db.GetConnectionToAnyServer();
			if(CurrentConnection!=OldConnection)
			{
				TS_TRACE("New Connection");
				OldConnection=CurrentConnection;
			}
			else
				ASSERT( 0 );
		}
		TS_TRACE("Start SQL");
		db.ExecuteNoQuery_AllServers("Create Table Test(Id int);");
		db.ExecuteNoQuery_AllServers("Drop Table Test;");



		TS_TRACE("End Setting Test");


	}

};
