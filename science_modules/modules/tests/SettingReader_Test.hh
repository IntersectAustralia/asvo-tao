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




class SettingReader_suite : public CxxTest::TestSuite
{
public:


	void test_SettingReader()
	{
		LOG_PUSH( new logging::file( "TestLog.log", logging::info ) );
		TS_TRACE("Starting SettingReader Test");
		string ParamXMLFile="/home/amr/workspace/params0.xml.processed";
		string BasicXMLFile="/home/amr/workspace/basicsetting.xml";
		options::xml_dict xml;

		xml.read( ParamXMLFile, "/tao" );
		xml.read( BasicXMLFile );

		multidb db(xml);
		db.OpenAllConnections();
		//db.RestartAllConnections();
		//db.CloseAllConnections();





		TS_TRACE("End Setting Test");


	}

};
