#include "BSPTree.hh"
#include <iostream>
using namespace std;

namespace tao
{


	BSP2DPoint::BSP2DPoint(int _X,int _Y)
	{
		X=_X;
		Y=_Y;
	}

	BSPtree::BSPtree(int StepSize,hpc::string DBName,hpc::string DBHost,hpc::string DBPort,hpc::string DBUserName,hpc::string DBPassword)
	{
		_stepsize=StepSize;
		_dbname=DBName;
		_dbhost=DBHost;
		_dbport=DBPort;
		_dbuser=DBUserName;
		_dbpass=DBPassword;
		IsConnected=false;
		_db_connect();
	}

	BSPtree::~BSPtree()
	{
		_db_disconnect();
	}


	void BSPtree::_db_connect()
	{

		try
		{

			string connect = "dbname=" + _dbname;
			connect += " host=" + _dbhost;
			connect += " port=" + _dbport;
			connect += " user=" + _dbuser;
			connect += " password='" + _dbpass + "'";
			//cout<<"Connection String:"<<connect<<endl;
#ifdef HAVE_POSTGRESQL
			_sql.open( soci::postgresql, connect );
#endif
			//cout<<"Connection Open"<<endl;

		}
		catch( const std::exception& ex )
		{
			// TODO: Handle database errors.
			cout<<"Error - Connecting to DB "<<ex.what()<<endl;
			ASSERT( 0 );
		}

		// Flag as connected.
		IsConnected = true;

	}
	void BSPtree::_db_disconnect()
	{
		if(IsConnected==true)
		{
			_sql.close();
			IsConnected = false;
		}

	}

	void BSPtree::GenerateRectangles()
	{
		double MinX,MinY,MinZ;
		double MaxX,MaxY,MaxZ;

		string query;

		/// Get Database Dimensions - Maximum Cube Size
		query="select min(MinX),min(MinY),min(MinZ),max(MaxX),max(MaxY),max(MaxZ) from TreeSummary;";
		_sql << query, soci::into(MinX),soci::into(MinY),soci::into(MinZ),soci::into(MaxX),soci::into(MaxY),soci::into(MaxZ);

		///////////////////////////////////////////////////////////////////////////////////////////////
		int XLocation=-1;
		int YLocation=-1;

		for(int x=MinX;x<MaxX;x+=_stepsize)
		{
			XLocation++;
			YLocation=-1;
			for(int y=MinY;y<MaxY;y+=_stepsize)
			{
				YLocation++;
				BSPRectangle Rect;
				Rect.XMin=x;
				Rect.XMax=x+_stepsize;
				Rect.YMin=y;
				Rect.YMax=y+_stepsize;
				Rect.XLocation=XLocation;
				Rect.YLocation=YLocation;
				RectanglesList.push_back(Rect);
			}
		}
	}

	BSPRectangle BSPtree::GetBoundingRect(std::vector<BSP2DPoint> PolyPoints)
	{
		int PolyXMin,PolyXMax;

		int PolyYMin,PolyYMax;

		PolyXMin=PolyXMax=PolyPoints[0].X;
		PolyYMin=PolyYMax=PolyPoints[0].Y;


		for(int i=0;i<PolyPoints.size();i++)
		{
			if(PolyPoints[i].X<PolyXMin)
				PolyXMin=PolyPoints[i].X;
			if(PolyPoints[i].X>PolyXMax)
				PolyXMax=PolyPoints[i].X;

			if(PolyPoints[i].Y<PolyYMin)
				PolyYMin=PolyPoints[i].Y;
			if(PolyPoints[i].Y>PolyYMax)
				PolyYMax=PolyPoints[i].Y;
		}

		BSPRectangle Rect;
		Rect.XMin=PolyXMin;
		Rect.XMax=PolyXMax;
		Rect.YMin=PolyYMin;
		Rect.YMax=PolyYMax;

		return Rect;
	}

	bool BSPtree::IntersectTwoRect(BSPRectangle RectA,BSPRectangle RectB)
	{
		if(RectA.XMin < RectB.XMax && RectA.XMax > RectB.XMin && RectA.YMin < RectB.YMax && RectA.YMax > RectB.YMin)
		{
			return true;
		}
		else
			return false;
	}

	float BSPtree::_ccw(BSP2DPoint A,BSP2DPoint B,BSP2DPoint C)
	{
		return (C.Y-A.Y)*(B.X-A.X) > (B.Y-A.Y) * (C.X-A.X);
	}

	bool BSPtree::_seg_intersect(BSP2DPoint A,BSP2DPoint B,BSP2DPoint C,BSP2DPoint D)
	{
		return _ccw(A,C,D) != _ccw(B,C,D) && _ccw(A,B,C)!= _ccw(A,B,D);
	}

	bool BSPtree::IntersectPolyRect(std::vector<BSP2DPoint> PolyPoints,BSPRectangle BoundingRect,BSPRectangle Rect)
	{
		PolyPoints.push_back(PolyPoints[0]);
		if (IntersectTwoRect(Rect,BoundingRect)==true)
		{
			bool IntersectionResults=false;
			for(int i=0;i<PolyPoints.size()-1;i++)
			{
				IntersectionResults = IntersectionResults || _seg_intersect(PolyPoints[i],PolyPoints[i+1],BSP2DPoint(Rect.XMin,Rect.YMin),BSP2DPoint(Rect.XMin,Rect.YMax));
				IntersectionResults = IntersectionResults || _seg_intersect(PolyPoints[i],PolyPoints[i+1],BSP2DPoint(Rect.XMin,Rect.YMax),BSP2DPoint(Rect.XMax,Rect.YMax));
				IntersectionResults = IntersectionResults || _seg_intersect(PolyPoints[i],PolyPoints[i+1],BSP2DPoint(Rect.XMax,Rect.YMax),BSP2DPoint(Rect.XMax,Rect.YMin));
				IntersectionResults = IntersectionResults || _seg_intersect(PolyPoints[i],PolyPoints[i+1],BSP2DPoint(Rect.XMax,Rect.YMin),BSP2DPoint(Rect.XMin,Rect.YMin));

			}
			return IntersectionResults;
		}
		else
			return false;
	}

	std::vector<BSP2DPoint> BSPtree::GetRectIds(std::vector<BSP2DPoint> PolyPoints)
	{
		BSPRectangle BoundingRect=GetBoundingRect(PolyPoints);
		std::vector<BSP2DPoint> RectIds;
		for(int i=0;i<RectanglesList.size();i++)
		{
			BSPRectangle Rect=RectanglesList[i];
			if(IntersectPolyRect(PolyPoints,BoundingRect,Rect))
			{
				RectIds.push_back(BSP2DPoint(Rect.XLocation,Rect.YLocation));
			}
		}

		return RectIds;
	}

	std::vector<string> BSPtree::GetTablesList(std::vector<BSP2DPoint> PolyPoints)
	{
		if(RectanglesList.size()==0)
			GenerateRectangles();

		//cout<<"Generated Rectangles List ... Done"<<endl;
		std::vector<BSP2DPoint> ListOfPositions=GetRectIds(PolyPoints);

		//cout<<"Generated RectIDs List ... Done"<<endl;

		string GridXLocation="";
		string GridYLocation="";



		for(int i=0;i<ListOfPositions.size();i++)
		{
			ostringstream GridXLocationstream;
			ostringstream GridYLocationstream;

			GridXLocationstream<<ListOfPositions[i].X<<",";
			GridYLocationstream<<ListOfPositions[i].Y<<",";

			if(GridXLocation.find(GridXLocationstream.str())==-1)
				GridXLocation=GridXLocation+GridXLocationstream.str();
			if(GridYLocation.find(GridYLocationstream.str())==-1)
				GridYLocation=GridYLocation+GridYLocationstream.str();

		}

		GridXLocation=GridXLocation.substr(0,GridXLocation.size()-1);
		GridYLocation=GridYLocation.substr(0,GridYLocation.size()-1);

		string Query="select distinct tablename from TreeSummary  where globaltreeid in (Select globaltreeid from TreeMapping where gridx in ("+GridXLocation+") and gridy in ("+GridYLocation+"));";
		//cout<<"Query:"<<endl<<Query<<endl;

		std::vector<string> TablesList(4000);
		_sql<<Query, soci::into((std::vector<string>&)TablesList );


		return TablesList;



	}

}
