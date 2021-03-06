import pg
import getpass
import math
import string
import sys,os
import settingReader
import numpy
import DBConnection
import logging
#import matplotlib.pyplot as plt


class ProcessTables(object):
    
    def __init__(self,Options):
        '''
        Constructor
        '''
        self.Options=Options
        self.DBConnection=DBConnection.DBConnection(Options)
        logging.info('Connection to DB is open...Start Creating Tables')
        
        
        logging.info('Summary Table Created ...')
    
    def CreateMainTables(self):
        self.CreateSummaryTable()
        self.CreateTreeSummaryTable()
    def CloseConnections(self):        
        self.DBConnection.CloseConnections()       
        logging.info('Connection to DB is Closed...') 
    
    
    def CreateSummaryTable(self):
        
        DropTable="DROP TABLE IF EXISTS Summary;"
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(DropTable)
        
        CreateTable="CREATE TABLE Summary ("
        CreateTable=CreateTable+"TableName varchar(100),"        
        CreateTable=CreateTable+"MinX FLOAT4,"
        CreateTable=CreateTable+"MinY FLOAT4,"
        CreateTable=CreateTable+"MinZ FLOAT4,"
        CreateTable=CreateTable+"MaxX FLOAT4,"
        CreateTable=CreateTable+"MaxY FLOAT4,"
        CreateTable=CreateTable+"MaxZ FLOAT4,"        
        CreateTable=CreateTable+"MinSnap INT4,"
        CreateTable=CreateTable+"MaxSnap INT4,"
        CreateTable=CreateTable+"GalaxyCount BIGINT)"
        
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(CreateTable)
    def CreateTreeSummaryTable(self):
        
        DropTable="DROP TABLE IF EXISTS TreeSummary;"
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(DropTable)
        
        CreateTable="CREATE TABLE TreeSummary ("        
        CreateTable=CreateTable+"GlobalTreeID BIGINT,"       
        CreateTable=CreateTable+"MinX FLOAT4,"
        CreateTable=CreateTable+"MinY FLOAT4,"
        CreateTable=CreateTable+"MinZ FLOAT4,"
        CreateTable=CreateTable+"MaxX FLOAT4,"
        CreateTable=CreateTable+"MaxY FLOAT4,"
        CreateTable=CreateTable+"MaxZ FLOAT4,"        
        CreateTable=CreateTable+"GalaxyCount BIGINT,"
        CreateTable=CreateTable+"TABLENAME VARCHAR(200))"
        
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(CreateTable)
    
    
            
    def GetTableSummary(self,TableName,ServerIndex):
        
        GetSummarySQL="select min(PosX),max(PosX),min(PosY),max(PosY),min(PosZ),max(PosZ),min(snapnum),max(snapnum),count(*) from @TABLEName;"
        GetSummarySQL= string.replace(GetSummarySQL,"@TABLEName",TableName)
        
        SummaryListArr=self.DBConnection.ExecuteQuerySQLStatment(GetSummarySQL,ServerIndex)
        if len(SummaryListArr)==0:
            return
        SummaryList=SummaryListArr[0]
        
        if SummaryList[0]==None:
            return
        MinPosX= SummaryList[0]
        MaxPosX= SummaryList[1]
        MinPosY= SummaryList[2]
        MaxPosY= SummaryList[3]
        MinPosZ= SummaryList[4]
        MaxPosZ= SummaryList[5]        
        MinSnap= SummaryList[6]
        MaxSnap= SummaryList[7]
        GalaxyCount=SummaryList[8]
        
        
        InsertSummaryRecord="INSERT INTO Summary ("
        InsertSummaryRecord=InsertSummaryRecord+"TableName, GalaxyCount, "
        InsertSummaryRecord=InsertSummaryRecord+"MinX, MinY, MinZ, "
        InsertSummaryRecord=InsertSummaryRecord+"MaxX, MaxY, MaxZ,MinSnap,MaxSnap) Values ("
        InsertSummaryRecord=InsertSummaryRecord+"\'"+TableName+"\',"+str(GalaxyCount)+","
        InsertSummaryRecord=InsertSummaryRecord+str(MinPosX)+","+str(MinPosY)+","+str(MinPosZ)+","
        InsertSummaryRecord=InsertSummaryRecord+str(MaxPosX)+","+str(MaxPosY)+","+str(MaxPosZ)+","+str(MinSnap)+","+str(MaxSnap)
        InsertSummaryRecord=InsertSummaryRecord+")"
        InsertSummaryRecord= string.replace(InsertSummaryRecord,"none","0")
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(InsertSummaryRecord)
        
        
        
    def GetTreeSummary(self,TableName,ServerIndex):
        logging.info("GetTreeSummary ..... Processing Table: "+TableName)
        #GetSummarySQL="INSERT INTO TreeSummary select GlobalTreeID,min(PosX),min(PosY),min(PosZ),max(PosX),max(PosY),max(PosZ),count(*),'"+TableName+"' from @TABLEName group by GlobalTreeID order by GlobalTreeID;"
        GetSummarySQL="select GlobalTreeID,min(PosX),min(PosY),min(PosZ),max(PosX),max(PosY),max(PosZ),count(*),'"+TableName+"' from @TABLEName group by GlobalTreeID order by GlobalTreeID;"
        GetSummarySQL= string.replace(GetSummarySQL,"@TABLEName",TableName)
        
                
        Resultsset=self.DBConnection.ExecuteQuerySQLStatment(GetSummarySQL,ServerIndex)
        RecordsCount=0
        InserSummarySQL="Insert into TreeSummary Values"
        for Row in Resultsset:
            
            RecordsCount=RecordsCount+1
            
            
            globaltreeid=Row[0]
            minx=Row[1]
            miny=Row[2]
            minz=Row[3]
            maxx=Row[4]
            maxy=Row[5]
            maxz=Row[6]
            count=Row[7]
            InserSummarySQL=InserSummarySQL+"("+str(globaltreeid)+","+str(minx)+","+str(miny)+","+str(minz)+","+str(maxx)+","+str(maxy)+","+str(maxz)+","+str(count)+",'"+TableName+"'),"
            
            if RecordsCount%100==0:                
                InserSummarySQL=InserSummarySQL[:-1]+";"            
                self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(InserSummarySQL)
                InserSummarySQL="Insert into TreeSummary Values"
        if RecordsCount%100>0: 
            InserSummarySQL=InserSummarySQL[:-1]+";"            
            self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(InserSummarySQL)
                
        logging.info("End Processing Table: "+TableName)
            
    
    
                
           
        
    def SummarizeLocationInfo(self):
        self.DBConnection.ExecuteNoQuerySQLStatment("DROP Table if Exists TreeLocationsCount;")
        self.DBConnection.ExecuteNoQuerySQLStatment("Create Table TreeLocationsCount (GlobalTreeID Bigint,LocationsCount int);")
        self.DBConnection.ExecuteNoQuerySQLStatment("Insert into TreeLocationsCount select globaltreeid,count(*) from TreeMapping group by globaltreeid order by count(*) desc ;")
        
        #########################################################################################
        
        GridData=self.DBConnection.ExecuteQuerySQLStatment("select gridx,gridy,count(*) from TreeMapping  group by  gridx,gridy;")
        #Arr=numpy.zeros((25,25))
        #for GridPoint in GridData:
        #   Arr[GridPoint[0],GridPoint[1]]=GridPoint[2] 
        #print Arr
        #plt.contourf(Arr)
        #plt.colorbar()
        #plt.show()
        
    def ValidateImportProcess(self):
        
        
        DataFileSummarySt="select sum(totalnumberofgalaxies),max(treeidto) from datafiles;"
        DataFilesSummary=self.DBConnection.ExecuteQuerySQLStatment(DataFileSummarySt)[0]
        ETotalNumberofExpectedGalaxies=DataFilesSummary[0]
        EMaxTreeID=DataFilesSummary[1]
        
        
        TreeSummarySt="select sum(galaxycount),max(globaltreeid) from treesummary;"
        TreeSummaryInfo=self.DBConnection.ExecuteQuerySQLStatment(TreeSummarySt)[0]
        CTotalNumberofExpectedGalaxies=TreeSummaryInfo[0]
        CMaxTreeID=TreeSummaryInfo[1]
        
        logging.info("----------------------------------------------------------------")
        logging.info("Validate Importing Process")
        logging.info("Total Number of Galaxies = "+str(CTotalNumberofExpectedGalaxies)+"\nExpected Number of Galaxies (Header Info)="+str(ETotalNumberofExpectedGalaxies))
        logging.info("Total Number of Trees = "+str(CMaxTreeID)+"\nExpected Number of Trees (Header Info)="+str(EMaxTreeID))
        
        if CMaxTreeID==EMaxTreeID and CTotalNumberofExpectedGalaxies==ETotalNumberofExpectedGalaxies:
            logging.info("Data Validation Completed")
        else:
            logging.info("Error in the Import Process. Please revise the imported data!")
        
        
        
        
        
    def SummarizeTables(self,ServerID):
        
        GetTablesListSt="select table_name from information_schema.tables where table_schema='public' order by table_name;"
        TablesList=self.DBConnection.ExecuteQuerySQLStatment(GetTablesListSt,ServerID)
        Count=0
        for Table in TablesList:
            TableName=Table[0]
            
            if string.find(TableName,self.Options['PGDB:TreeTablePrefix'])==0:
                logging.info(str(ServerID)+":Processing Table: "+TableName+ "\t "+str(Count)+"/"+str(len(TablesList)))
                self.GetTableSummary(TableName,ServerID)
                self.GetTreeSummary(TableName,ServerID)
            Count=Count+1
                
                 
#if __name__ == '__main__':
#    print('Starting DB processing')
#    FilePath='log/logfile_AnalyzeTable.log'
#    if os.path.exists(FilePath):
#        os.remove(FilePath)
#    logging.basicConfig(filename=FilePath,level=logging.DEBUG,format='%(asctime)s %(message)s')
    
#    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml") 
#    ProcessTablesObj=ProcessTables(Options)
#    for i in range(0,ProcessTablesObj.DBConnection.serverscount):
#        ProcessTablesObj.GetTablesList(i)
   
#    ProcessTablesObj.SummarizeLocationInfo()  
#    ProcessTablesObj.ValidateImportProcess()            
#    ProcessTablesObj.CloseConnections()      
        
        
        
         