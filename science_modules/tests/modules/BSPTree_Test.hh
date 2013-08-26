#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>
#include <cxxtest/TestSuite.h>
#include <libhpc/libhpc.hh>
#include "modules/src/BSPTree.hh"
#include <vector>
#include <iostream>

using namespace std;
using namespace hpc;
using namespace tao;





class BSP_suite : public CxxTest::TestSuite
{
public:


	void test_BSP()
	{
		TS_TRACE("Starting BSP Test");
		int StepSize=20;
		hpc::string DBName="millennium_full";
		hpc::string DBHost="tao02.hpc.swin.edu.au";
		hpc::string DBPort="3306";
		hpc::string DBUserName="taoadmin";
		hpc::string DBPassword="tao_admin_password_##";

		BSPtree B(StepSize,DBName,DBHost,DBPort,DBUserName,DBPassword);


		std::vector<BSP2DPoint> PolyPoints;
		PolyPoints.push_back(BSP2DPoint(0,0));
		PolyPoints.push_back(BSP2DPoint(500,0));
		PolyPoints.push_back(BSP2DPoint(500,50));

		std::vector<string> TableList=B.GetTablesList(PolyPoints);

		TS_ASSERT(TableList.size()>0);

		for(int i=0;i<TableList.size();i++)
		{
			cout<<TableList[i]<<endl;
		}

		TS_TRACE("End BSP Test");


	}
};
