import pg
import getpass
import math
import string
import sys
import settingReader
import numpy
import matplotlib.pyplot as plt


class ProcessTables(object):
    
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
        print('Connection to DB is open...')
        self.CreateSummaryTable()
        self.CreateTreeSummaryTable()
        self.CreateTreeMappingTable()
        print('Summary Table Created ...')
    
    
    def CloseConnections(self):        
        self.CurrentConnection.close()       
        print('Connection to DB is Closed...')
    
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
    
    
    def CreateSummaryTable(self):
        
        DropTable="DROP TABLE IF EXISTS Summary;"
        self.ExecuteNoQuerySQLStatment(DropTable)
        
        CreateTable="CREATE TABLE Summary ("
        CreateTable=CreateTable+"TableName varchar(100),"
        CreateTable=CreateTable+"MinTreeID BIGINT,"     
        CreateTable=CreateTable+"MaxTreeID BIGINT,"
        CreateTable=CreateTable+"MinX FLOAT4,"
        CreateTable=CreateTable+"MinY FLOAT4,"
        CreateTable=CreateTable+"MinZ FLOAT4,"
        CreateTable=CreateTable+"MaxX FLOAT4,"
        CreateTable=CreateTable+"MaxY FLOAT4,"
        CreateTable=CreateTable+"MaxZ FLOAT4,"        
        CreateTable=CreateTable+"MinSnap INT4,"
        CreateTable=CreateTable+"MaxSnap INT4,"
        CreateTable=CreateTable+"GalaxyCount BIGINT)"
        
        self.ExecuteNoQuerySQLStatment(CreateTable)
    def CreateTreeSummaryTable(self):
        
        DropTable="DROP TABLE IF EXISTS TreeSummary;"
        self.ExecuteNoQuerySQLStatment(DropTable)
        
        CreateTable="CREATE TABLE TreeSummary ("        
        CreateTable=CreateTable+"GlobalTreeID BIGINT,"       
        CreateTable=CreateTable+"MinX FLOAT4,"
        CreateTable=CreateTable+"MinY FLOAT4,"
        CreateTable=CreateTable+"MinZ FLOAT4,"
        CreateTable=CreateTable+"MaxX FLOAT4,"
        CreateTable=CreateTable+"MaxY FLOAT4,"
        CreateTable=CreateTable+"MaxZ FLOAT4,"        
        CreateTable=CreateTable+"GalaxyCount BIGINT)"
        
        self.ExecuteNoQuerySQLStatment(CreateTable)
    
    def CreateTreeMappingTable(self):
        
        DropTable="DROP TABLE IF EXISTS TreeMapping;"
        self.ExecuteNoQuerySQLStatment(DropTable)
        
        CreateTable="CREATE TABLE TreeMapping ("        
        CreateTable=CreateTable+"GlobalTreeID BIGINT,"       
        CreateTable=CreateTable+"GridX INT,"
        CreateTable=CreateTable+"GridY INT)"                
        
        
        self.ExecuteNoQuerySQLStatment(CreateTable)
            
    def GetTableSummary(self,TableName):
        print("Processing Table: "+TableName)
        GetSummarySQL="select min(PosX),max(PosX),min(PosY),max(PosY),min(PosZ),max(PosZ),min(GlobalTreeID),max(GlobalTreeID),min(snapnum),max(snapnum),count(*) from @TABLEName;"
        GetSummarySQL= string.replace(GetSummarySQL,"@TABLEName",TableName)
        SummaryListArr=self.ExecuteQuerySQLStatment(GetSummarySQL)
        if len(SummaryListArr)==0:
            return
        SummaryList=SummaryListArr[0]
        
        MinPosX= SummaryList[0]
        MaxPosX= SummaryList[1]
        MinPosY= SummaryList[2]
        MaxPosY= SummaryList[3]
        MinPosZ= SummaryList[4]
        MaxPosZ= SummaryList[5]
        MinTreeID= SummaryList[6]
        MaxTreeID= SummaryList[7]
        MinSnap= SummaryList[8]
        MaxSnap= SummaryList[9]
        GalaxyCount=SummaryList[10]
        
        
        InsertSummaryRecord="INSERT INTO Summary ("
        InsertSummaryRecord=InsertSummaryRecord+"TableName, MinTreeID, MaxTreeID, GalaxyCount, "
        InsertSummaryRecord=InsertSummaryRecord+"MinX, MinY, MinZ, "
        InsertSummaryRecord=InsertSummaryRecord+"MaxX, MaxY, MaxZ,MinSnap,MaxSnap) Values ("
        InsertSummaryRecord=InsertSummaryRecord+"\'"+TableName+"\',"+str(MinTreeID)+","+str(MaxTreeID)+","+str(GalaxyCount)+","
        InsertSummaryRecord=InsertSummaryRecord+str(MinPosX)+","+str(MinPosY)+","+str(MinPosZ)+","
        InsertSummaryRecord=InsertSummaryRecord+str(MaxPosX)+","+str(MaxPosY)+","+str(MaxPosZ)+","+str(MinSnap)+","+str(MaxSnap)
        InsertSummaryRecord=InsertSummaryRecord+")"
        InsertSummaryRecord= string.replace(InsertSummaryRecord,"none","0")
        self.ExecuteNoQuerySQLStatment(InsertSummaryRecord)
        
        print("End Processing Table: "+TableName)
        print("********************************************************************************")
    def GetTreeSummary(self,TableName):
        print("Processing Table: "+TableName)
        GetSummarySQL="INSERT INTO TreeSummary select GlobalTreeID,min(PosX),min(PosY),min(PosZ),max(PosX),max(PosY),max(PosZ),count(*) from @TABLEName group by GlobalTreeID order by GlobalTreeID;"
        GetSummarySQL= string.replace(GetSummarySQL,"@TABLEName",TableName)        
        self.ExecuteNoQuerySQLStatment(GetSummarySQL)
        
        print("End Processing Table: "+TableName)
        print("********************************************************************************")    
    
    def BuildTreeMapping(self):
        
        self.ExecuteNoQuerySQLStatment("DELETE FROM TreeMapping;")
        
        
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
                
                GetIntersectionWithCurrentBoundingRect="INSERT INTO TreeMapping select GlobalTreeID,"+str(XLocation)+","+str(YLocation)+" from TreeSummary Where MinX<"+str(BX2)+" and MaxX>"+str(BX1)+" and MinY<"+str(BY2)+" and MaxY>"+str(BY1)+";"
                
                
                self.ExecuteNoQuerySQLStatment(GetIntersectionWithCurrentBoundingRect)
                print("("+str(XLocation)+","+str(YLocation)+")")
                
           
        
    def SummarizeLocationInfo(self):
        self.ExecuteNoQuerySQLStatment("DROP Table if Exists TreeLocationsCount;")
        self.ExecuteNoQuerySQLStatment("Create Table TreeLocationsCount (GlobalTreeID Bigint,LocationsCount int);")
        self.ExecuteNoQuerySQLStatment("Insert into TreeLocationsCount select globaltreeid,count(*) from TreeMapping group by globaltreeid order by count(*) desc ;")
        
        #########################################################################################
        
        GridData=self.ExecuteQuerySQLStatment("select gridx,gridy,count(*) from TreeMapping  group by  gridx,gridy;")
        #Arr=numpy.zeros((25,25))
        #for GridPoint in GridData:
        #   Arr[GridPoint[0],GridPoint[1]]=GridPoint[2] 
        #print Arr
        #plt.contourf(Arr)
        #plt.colorbar()
        #plt.show()
        
        
    def GetTablesList(self):
        
        GetTablesListSt="select table_name from information_schema.tables where table_schema='public';"
        TablesList=self.ExecuteQuerySQLStatment(GetTablesListSt)
        for Table in TablesList:
            TableName=Table[0]
            if string.find(TableName,self.Options['PGDB:TreeTablePrefix'])==0:
                self.GetTableSummary(TableName)
                self.GetTreeSummary(TableName)
                 
if __name__ == '__main__':
    print('Starting DB processing')
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml") 
    ProcessTablesObj=ProcessTables(Options)
    ProcessTablesObj.GetTablesList()
    ProcessTablesObj.BuildTreeMapping()
    ProcessTablesObj.SummarizeLocationInfo()              
        
        
        
        
         