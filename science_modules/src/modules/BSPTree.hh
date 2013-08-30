#ifndef tao_modules_bsptree_hh
#define tao_modules_bsptree_hh

#ifdef HAVE_POSTGRESQL
#include <soci/postgresql/soci-postgresql.h>
#endif
#include <soci/soci.h>
#include <libhpc/libhpc.hh>
#include <vector>
#include <iostream>

namespace tao
{
   using namespace hpc;

   struct BSPRectangle
   {
	   int XMin;
	   int XMax;
	   int YMin;
	   int YMax;
	   int XLocation;
	   int YLocation;
   };

   class BSP2DPoint
   {
   public:
	   int X;
	   int Y;

	   BSP2DPoint(int _X,int _Y);
   };
   ///
   class BSPtree
   {
   	   public:
			BSPtree(int StepSize,hpc::string DBName,hpc::string DBHost,hpc::string DBPort,hpc::string DBUserName,hpc::string DBPassword);
			~BSPtree();




			std::vector<string> GetTablesList(std::vector<BSP2DPoint> PolyPoints);


   	   protected:

			void GenerateRectangles();


			BSPRectangle GetBoundingRect(std::vector<BSP2DPoint> PolyPoints);
			bool IntersectTwoRect(BSPRectangle RectA,BSPRectangle RectB);
			std::vector<BSP2DPoint> GetRectIds(std::vector<BSP2DPoint> PolyPoints);


			void _db_connect();
			void _db_disconnect();

			float _ccw(BSP2DPoint A,BSP2DPoint B,BSP2DPoint C);
			bool _seg_intersect(BSP2DPoint A,BSP2DPoint B,BSP2DPoint C,BSP2DPoint D);

			bool IntersectPolyRect(std::vector<BSP2DPoint> PolyPoints,BSPRectangle BoundingRect,BSPRectangle Rect);

			std::vector<BSPRectangle> RectanglesList;
			soci::session _sql;
			bool IsConnected;
			hpc::string _dbname, _dbhost, _dbport, _dbuser, _dbpass;
			int _stepsize;



   };

}
#endif

