import pg
import getpass
import math
import string
import sys
import settingReader
import numpy
import matplotlib.pyplot as plt
import matplotlib
from MySQLdb.constants.FLAG import NUM



class BSPTree(object):
    
    def __init__(self,Options):
        '''
        Constructor
        '''
        self.Options=Options
        self.serverip=self.Options['PGDB:serverip']
        self.username=self.Options['PGDB:user']
        self.password=self.Options['PGDB:password']
        self.port=int(self.Options['PGDB:port'])
        self.DBName=self.Options['PGDB:NewDBName']
        
        if self.password==None:
            print('Password for user:'+self.username+' is not defined')
            self.password=getpass.getpass('Please enter password:')
        
        # Take care that the connection will be opened to standard DB 'master'
        # This is temp. until the actual database is created
        self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname=self.DBName)
        print('Connection to DB is open...Start Creating Tables')
        

    def ExecuteNoQuerySQLStatment(self,SQLStatment):
        try:           
           
            SQLStatment=string.lower(SQLStatment)  
            self.CurrentConnection.query(SQLStatment)
              
        except Exception as Exp:
            print(">>>>>Error While creating New Table")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
            
    def ExecuteQuerySQLStatment(self,SQLStatment):
        try:
            
            SQLStatment=string.lower(SQLStatment)
            resultsList=self.CurrentConnection.query(SQLStatment).getresult()
            
            return resultsList  
        except Exception as Exp:
            print(">>>>>Error While creating New Table")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
     
    def GenerateRectangles(self):
        GetBoundryBox="select min(MinX), min(MinY), min(MinZ), max(MaxX), max(MaxY), max(MaxZ) from TreeSummary;"
        GlobalSummary=self.ExecuteQuerySQLStatment(GetBoundryBox)[0]
        
        MinX=int(math.floor(GlobalSummary[0]))
        MinY=int(math.floor(GlobalSummary[1]))
        MinZ=int(math.floor(GlobalSummary[2]))
        
        MaxX=int(math.ceil(GlobalSummary[3]))
        MaxY=int(math.ceil(GlobalSummary[4]))
        MaxZ=int(math.ceil(GlobalSummary[5]))
        
        XLocation=-1
        YLocation=-1
        StepSize=20
        
        self.RectArr=numpy.zeros((0,6))
        
        
        
        ### Intersection between two Rectangles 
        ### http://silentmatt.com/rectangle-intersection/
        for X in range(MinX,MaxX,StepSize):
            XLocation=XLocation+1
            YLocation=-1
            for Y in range(MinY,MaxY,StepSize):
                
                YLocation=YLocation+1
                BX1=X;
                BX2=X+StepSize
                BY1=Y
                BY2=Y+StepSize  
                self.RectArr=numpy.vstack([self.RectArr,[BX1,BX2,BY1,BY2,XLocation,YLocation]])
    
    def GetRectIds(self,PolyPoints):       
        
        BoundingRect=self.GetBoundingRect(PolyPoints)
        LocationsMatrix=numpy.zeros([0,2])
        
        for Rect in self.RectArr: 
            
            color='yellow'    
            #if self.InsidePolygon(Rect[0],Rect[2] , PolyPoints): 
            #    color='blue'
            #if self.InsidePolygon(Rect[1],Rect[2] , PolyPoints): 
            #    color='blue'
            #if self.InsidePolygon(Rect[0],Rect[3] , PolyPoints): 
            #    color='blue'
            #if self.InsidePolygon(Rect[1],Rect[3] , PolyPoints): 
            #    color='blue'
            if self.IntersectPolyRect(PolyPoints,BoundingRect,Rect):
                 color='blue'
                 LocationsMatrix=numpy.vstack([LocationsMatrix,Rect[4:6]])          
            plt.gca().add_patch(matplotlib.patches.Rectangle((Rect[0],Rect[2]), Rect[1]-Rect[0], Rect[3]-Rect[2],fc=color))
            
            
            
            
            
            
            
            
        #plt.gca().add_patch(matplotlib.patches.Rectangle((BoundingRect[0],BoundingRect[2]), BoundingRect[1]-BoundingRect[0], BoundingRect[3]-BoundingRect[2],fc='white'))    
        plt.gca().add_patch(matplotlib.patches.Polygon(PolyPoints,fc='red'))
        plt.gca().autoscale_view()
        plt.draw()
        plt.show()
        
        
        return LocationsMatrix
        
        
    
    def IntersectTwoRect(self,RectA,RectB):
        ## Rect=[X1,X2,Y1,Y2]
        if (RectA[0] < RectB[1] and RectA[1] > RectB[0] and RectA[2] < RectB[3] and RectA[3] > RectB[2]): 
            return True;
        else:
            return False;
    def GetBoundingRect(self,PolyPoints):
        
        PolyMinX=PolyMaxX=PolyPoints[0][0]  
        PolyMinY=PolyMaxY=PolyPoints[0][1]
        
        for P in PolyPoints:
            if P[0]<PolyMinX:
                PolyMinX=P[0]
            if P[0]>PolyMaxX:
                PolyMaxX=P[0]
            if P[1]<PolyMinY:
                PolyMinY=P[1]
            if P[1]>PolyMaxY:
                PolyMaxY=P[1]
        
        return [PolyMinX,PolyMaxX,PolyMinY,PolyMaxY]
        
        
        
    
    def IntersectPolyRect(self,PolyPoints,PolygonBoundingRect,Rect):
        
        PolyPoints= numpy.vstack([PolyPoints,PolyPoints[0]])
        
        
        if self.IntersectTwoRect(Rect, PolygonBoundingRect):
            IntersectionResults=False
            for i in range(0,len(PolyPoints)-1):
                
                IntersectionResults= IntersectionResults or self.seg_intersect(PolyPoints[i],PolyPoints[i+1],[Rect[0],Rect[2]],[Rect[0],Rect[3]])
                IntersectionResults= IntersectionResults or self.seg_intersect(PolyPoints[i],PolyPoints[i+1],[Rect[0],Rect[3]],[Rect[1],Rect[3]])
                IntersectionResults= IntersectionResults or self.seg_intersect(PolyPoints[i],PolyPoints[i+1],[Rect[1],Rect[3]],[Rect[1],Rect[2]])
                IntersectionResults= IntersectionResults or self.seg_intersect(PolyPoints[i],PolyPoints[i+1],[Rect[1],Rect[2]],[Rect[0],Rect[2]])
                
                
            return IntersectionResults  
        else:
            return False
        
        
    
    def ccw(self,A,B,C):
        return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

    def seg_intersect(self,A,B,C,D):
        return self.ccw(A,C,D) != self.ccw(B,C,D) and self.ccw(A,B,C) != self.ccw(A,B,D)
         
         
        
    

   
        
    def InsidePolygon(self,x,y,points):
        
        n = len(points)
        inside = False
        p1x, p1y = points[0]
        for i in range(1, n + 1):
            p2x, p2y = points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
 
    
        
if __name__ == '__main__':
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml") 
    BSPTreeObj=BSPTree(Options)
    BSPTreeObj.GenerateRectangles()
    #PolyPoints=[(250,90),(400,300),(250,400),(150,250)]
    PolyPoints=[(0,0),(500,0),(500,50)]
    LocationsMatrix=BSPTreeObj.GetRectIds(PolyPoints)
    
    GridXLocationsstr=''
    GridYLocationsstr=''
    GridXLocations=numpy.unique(LocationsMatrix[:,0])
    GridYLocations=numpy.unique(LocationsMatrix[:,1])
    
    for r in GridXLocations:
        GridXLocationsstr=GridXLocationsstr+','+str(int(r))
    for r in GridYLocations:
        GridYLocationsstr=GridYLocationsstr+','+str(int(r))
        
    GridXLocationsstr=GridXLocationsstr[1:]    
    GridYLocationsstr=GridYLocationsstr[1:]
    
    Query='select distinct tablename from TreeSummary  where globaltreeid in (Select globaltreeid from TreeMapping where gridx in ('+GridXLocationsstr+') and gridy in ('+GridYLocationsstr+'));'
    print Query
    TablesList=BSPTreeObj.ExecuteQuerySQLStatment(Query)
    
    for table in TablesList:
        print(table)
    #GridData=BSPTreeObj.ExecuteQuerySQLStatment("select gridx,gridy,count(*) from TreeMapping  group by  gridx,gridy;")
    #Arr=numpy.zeros((25,25))
    #for GridPoint in GridData:
    #   Arr[GridPoint[0],GridPoint[1]]=GridPoint[2] 
    #print Arr
    #plt.contourf(Arr)
    #plt.colorbar()
    #plt.show()
    