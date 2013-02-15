#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <libhpc/libhpc.hh>
#include "modules/src/settingReader.hh"
#include <vector>
#include <iostream>

using namespace std;
using namespace hpc;
using namespace tao;
#define NDEBUG




class SettingReader_suite : public CxxTest::TestSuite
{
public:


	void test_SettingReader()
	{
		TS_TRACE("Starting SettingReader Test");
		hpc::string ParamXMLFile="/home/amr/tao01.xml";
		hpc::string BasicXMLFile="/home/amr/basicsetting.xml";

		SettingReader Reader(BasicXMLFile,ParamXMLFile);
		LightConeParams Params= Reader.LoadLightCone();
		//TS_ASSERT(TableList.size()>0);
		PrintLightCone(Params);

		TS_TRACE("End Setting Test");


	}
	void PrintLightCone(LightConeParams Parmas)
	{

	   cout<<Parmas.ModuleVersion<<endl;
	   cout<<Parmas.Geometry<<endl;
	   cout<<Parmas.Simultation<<endl;
	   cout<<Parmas.GalaxyModel<<endl;
	   cout<<Parmas.BoxRepetition<<endl;

	   cout<<Parmas.NumberofCones<<endl;

	   cout<<Parmas.redshiftmin<<endl;
	   cout<<Parmas.redshiftmax<<endl;


	   cout<<Parmas.ramin<<endl;
	   cout<<Parmas.ramax<<endl;
	   cout<<Parmas.decmin<<endl;
	   cout<<Parmas.decmax<<endl;


	   for(int i=0;i<Parmas.OutputFieldsList.size();i++)
	   {
		   cout<<Parmas.OutputFieldsList[i].FieldDBName<<"\t"<<Parmas.OutputFieldsList[i].FieldLabel<<endl;

	   }



	   cout<<Parmas.rngseed<<endl;



	}
};
