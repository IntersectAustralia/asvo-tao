#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <libhpc/libhpc.hh>
#include <vector>
#include <iostream>
#include <pugixml.hpp>


#include "tao/base/base.hh"
#include "tao/modules/modules.hh"
#include "tao/modules/sqldirect.hh"

#include <cstdlib>
#include <iostream>
#include <libhpc/options/xml_dict.hh>



using namespace std;
using namespace hpc;
using namespace tao;
using namespace pugi;
#define NDEBUG




class SQLDirect_suite : public CxxTest::TestSuite
{
public:


	void test_SQLDirect()
	{


		LOG_PUSH( new logging::file( "TestLog.log",logging::debug ) );
		TS_TRACE("Starting SQLDirect Test");
		string ParamXMLFile="params0.xml";
		string BasicXMLFile="basicsetting.xml";
		options::xml_dict xml;

		xml.read( ParamXMLFile, "/tao" );
		xml.read( BasicXMLFile );
		pugi::xml_document _doc;
		_doc.load_file(ParamXMLFile.c_str());

		xpath_node_set nodes = _doc.select_nodes( "/tao/workflow/sql[@id]" );
		xml_node cur = nodes.begin()->node();


		TS_TRACE("XML Read Done");

		sqldirect sqlobject("sql",cur);
		sqlobject.initialise(xml);

		bool complete;
		unsigned long long it = 1;

		do
	  {
		 LOGDLN( "Beginning iteration: ", it );

		 // Reset the complete flag.
		 complete = true;

		 // Loop over the modules.

		 sqlobject.process( it );
		if( !sqlobject.complete() )
		   complete = false;


		 // Advance the counter.
		 ++it;


	  }
	  while( !complete );
		/*multidb db("bolshoi_full_dist","tree_");
		db.AddNewServer("tao01.hpc.swin.edu.au","taoadmin","password","3306");
		db.AddNewServer("tao02.hpc.swin.edu.au","taoadmin","password","3306");


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
		*/


		TS_TRACE("End Setting Test");


	}

};
