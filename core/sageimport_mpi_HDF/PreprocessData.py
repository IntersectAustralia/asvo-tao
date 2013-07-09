import math
import settingReader
import os
import sys
import struct
import string
import DBConnection
import logging
import h5py
from io import BytesIO
import numpy

class PreprocessData(object):

    ## Mapping between SAGE (C/C++) data types to Database data types 
    FormatMapping={'int':'INT','float':'FLOAT4','long long':'BIGINT'}
    
    
    ## Init the class with XML Options 
    def __init__(self,CurrentSAGEStruct,Options):       
        
        self.CurrentH5InputFile=Options['RunningSettings:InputFile']
        self.DBName=Options['PGDB:NewDBName']
        self.CurrentSAGEStruct=CurrentSAGEStruct
        self.Options=Options
          
       
            
       
   
    def InitDBConnection(self,ToMasterDB):
        
        ####### PostgreSQL Simulation DB ################# 
        self.DBConnection=DBConnection.DBConnection(self.Options,ToMasterDB)
        
        logging.info('Connection to DB is open...')
    
    def DropDatabase(self):
        ## Check if the database already exists
        
        ResultsList=self.DBConnection.ExecuteQuerySQLStatment("SELECT datname FROM pg_database where datistemplate=false and datname=%(dbname)s;",0,{'dbname':self.DBName})
          
        ## If the database already exists - give the user the option to drop it
        if len(ResultsList)>0:

            Response=self.Options["RunningSettings:OverWriteDB"]
            if Response=='yes':
                ## Drop the database
                self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers("Drop database "+self.DBName+";")                
                logging.info("Database "+self.DBName+" Dropped")
    
                
    
    def CreateDB(self):
       ## Check if the database already exist and give the user the option to Drop it 
       self.DropDatabase()        
       
       ## Create New DB 
       self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers("create database "+self.DBName+";") 
       logging.info("Database "+self.DBName+" Created")
       ### Close the current Connection (To a Default DB) and open a new one on the new DB
       self.DBConnection.CloseConnections()
       self.DBConnection=DBConnection.DBConnection(self.Options)      
       
       
       logging.info("Connection to Database "+self.DBName+" is opened and ready")
       self.CreateTreeMappingTable()
       
       
       #Process All the Non-Empty Files 
       ## The table "DataFiles" will work as a record keeper for which files has been processed and which has not been processed 
       ## It will be use to support continue in case of error
       CreateTableSt="SET client_min_messages TO WARNING; DROP TABLE IF EXISTS TreeProcessingSummary; CREATE TABLE TreeProcessingSummary "
       CreateTableSt=CreateTableSt+"(LoadingTreeID BIGINT, GalaxiesCount BIGINT, StartIndex BIGINT, Processed boolean);"        
       self.DBConnection.ExecuteNoQuerySQLStatment(CreateTableSt)
   
   
    def CreateTreeMappingTable(self):
        
        DropTable="SET client_min_messages TO WARNING; DROP TABLE IF EXISTS TreeMapping;"
        self.DBConnection.ExecuteNoQuerySQLStatment(DropTable)
        
        CreateTable="SET client_min_messages TO WARNING; CREATE TABLE TreeMapping ("
        CreateTable=CreateTable+"GlobalTreeID BIGINT,"       
        CreateTable=CreateTable+"GridX INT,"
        CreateTable=CreateTable+"GridY INT)"                
        
        
        self.DBConnection.ExecuteNoQuerySQLStatment(CreateTable)
    
    
    
    
    def GenerateTablesIndex(self,CommSize,CommRank):
        
        SimulationBoxX=float(self.Options['RunningSettings:SimulationBoxX'])
        SimulationBoxY=float(self.Options['RunningSettings:SimulationBoxX'])
        BSPCellSize=float(self.Options['RunningSettings:BSPCellSize'])       
        
        
        CellsInX=int(math.ceil(SimulationBoxX/BSPCellSize))
        CellsInY=int(math.ceil(SimulationBoxY/BSPCellSize))
        
        logging.info("Cells In X="+str(CellsInX))
        logging.info("Cells In Y="+str(CellsInY))
        
        
        NumberofTables=CellsInX*CellsInY
        TableIDs=range(0,NumberofTables+1)
        
        for TableID in TableIDs:
            
            self.CreateTableIndex(TableID,CommSize,CommRank)
    
    ## Generate All the tables required for the data importing process
    def GenerateAllTables(self): 
        
        
        SimulationBoxX=float(self.Options['RunningSettings:SimulationBoxX'])
        SimulationBoxY=float(self.Options['RunningSettings:SimulationBoxX'])
        BSPCellSize=float(self.Options['RunningSettings:BSPCellSize'])
        
        logging.info("Processing BOX ("+str(SimulationBoxX)+"x"+str(SimulationBoxY)+") With Cell Size="+str(BSPCellSize))
        
        CellsInX=int(math.ceil(SimulationBoxX/BSPCellSize))
        CellsInY=int(math.ceil(SimulationBoxY/BSPCellSize))
        
        logging.info("Cells In X="+str(CellsInX))
        logging.info("Cells In Y="+str(CellsInY))
        
        
        NumberofTables=CellsInX*CellsInY
        
        
        
        ## Create Table template statement 
        self.CreateNewTableTemplate()
        
        logging.info("WARNING ALL DATA TABLES WILL BE RECREATED .....")
        
        ## Ensure that there is no Files marked as processed..
        ## This may happen if the user drop the table and forget to update the datafiles table
        ## This execution is just a pre-caution
        self.DBConnection.ExecuteNoQuerySQLStatment("UPDATE TreeProcessingSummary set Processed=FALSE;")
        
        setWarningOff="set client_min_messages='warning'; "
        self.DBConnection.ExecuteNoQuerySQLStatment(setWarningOff)
        
        ## Get List of all tables expected from "datafiles" table
        #TableIDs=self.ExecuteQuerySQLStatment("select distinct tableid from datafiles order by tableid;")
        TableIDs=range(0,NumberofTables)
        self.CreateTable_DB_Mapping()
        ## for each tableID create New Table 
        for TableID in TableIDs:
            logging.info("Creating Table ("+str(TableID)+")")
            self.CreateNewTable(TableID)
        
        self.CreateNewTable(NumberofTables)
    def CreateTable_DB_Mapping(self):
        DropTable="SET client_min_messages TO WARNING; DROP TABLE IF EXISTS Table_DB_Mapping;"
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(DropTable)
        
        CreateTableMapping="SET client_min_messages TO WARNING; Create TABLE Table_DB_Mapping (TableName varchar(500),NodeName varchar(5000),IsActive boolean DEFAULT (True), PRIMARY KEY(TableName, NodeName));"
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(CreateTableMapping)
        
        
    ## Use Statement concatenation and the  CurrentSAGEStrcuture loaded from the XML settings to create a new table template
    def CreateNewTableTemplate(self):
        self.CreateTableTemplate="CREATE TABLE @TABLEName ("
        for field in self.CurrentSAGEStruct:            
            FieldDT=self.FormatMapping[field[1]]
            FieldName=field[2]
            self.CreateTableTemplate=self.CreateTableTemplate+ FieldName +' '+FieldDT+","
        self.CreateTableTemplate=self.CreateTableTemplate+"GlobalTreeID BIGINT,"
<<<<<<< HEAD
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyGlobalID BIGINT,"     
        self.CreateTableTemplate=self.CreateTableTemplate+"LocalGalaxyID INT)"       
     
     
    def CreateIndexOnTreeSummaryTable(self):
        CreateIndexStatment="ALTER TABLE treesummary ADD PRIMARY KEY (globaltreeid);"
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(CreateIndexStatment)
        logging.info("Table treesummary Index Created ...") 
            
=======
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyGlobalID BIGINT)"     
        #self.CreateTableTemplate=self.CreateTableTemplate+"LocalGalaxyID INT)"       
    def CreateIndexOnTreeSummaryTable(self):
        CreateIndexStatment="ALTER TABLE treesummary  ADD PRIMARY KEY (globaltreeid);"
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(CreateIndexStatment)
        logging.info("Table treesummary Index Created ...")    
>>>>>>> be3bd6a89d13f48fc1a0eccaae7b59ed2c0856d0
                
    def CreateTableIndex(self,TableIndex,CommSize,CommRank):
        
        
        HostIndex=self.DBConnection.MapTableIDToServerIndex(TableIndex)
        
        if HostIndex==CommRank:
            logging.info("Updating Table ("+str(TableIndex)+")")
            TablePrefix=self.Options['PGDB:TreeTablePrefix']
            NewTableName=TablePrefix+str(TableIndex)
            
            
            CreateIndexStatment="ALTER TABLE  "+NewTableName+" ADD PRIMARY KEY (GlobalIndex);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            CreateIndexStatment="Create Index SnapNum_Index_"+NewTableName+" on  "+NewTableName+" (SnapNum);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            CreateIndexStatment="Create Index GlobalTreeID_Index_"+NewTableName+" on  "+NewTableName+" (GlobalTreeID);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            CreateIndexStatment="Create Index GalaxyX_Index_"+NewTableName+" on  "+NewTableName+" (posx);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            CreateIndexStatment="Create Index GalaxyY_Index_"+NewTableName+" on  "+NewTableName+" (posy);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            CreateIndexStatment="Create Index GalaxyZ_Index_"+NewTableName+" on  "+NewTableName+" (posz);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            logging.info("Table "+NewTableName+" Index Created ...")
    ## Perform create table for a specific TableIndex            
    def CreateNewTable(self,TableIndex):        
        
               
        CreateTableStatment=""
        HostIndex=self.DBConnection.MapTableIDToServerIndex(TableIndex)
        try:
            
            ## The Table name is defined using the TreeTablePrefix from the XML config file
            TablePrefix=self.Options['PGDB:TreeTablePrefix']
            NewTableName=TablePrefix+str(TableIndex)
            ## If the table exists drop it 
            DropSt="SET client_min_messages TO WARNING; DROP TABLE IF EXISTS "+NewTableName+";"
            self.DBConnection.ExecuteNoQuerySQLStatment(DropSt,HostIndex)
            CreateTableStatment= string.replace(self.CreateTableTemplate,"@TABLEName",NewTableName)
            
                        
            
            CreateTableStatment=string.lower(CreateTableStatment)
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateTableStatment,HostIndex)
            
            ## Create Table indices             
            
            
            
            NodeName=self.Options['PGDB:serverInfo'+str(HostIndex)+':serverip']
            InsertStatement="INSERT INTO Table_DB_Mapping Values('"+NewTableName+"','"+NodeName+"');" 
            self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(InsertStatement)
            logging.info("Table "+NewTableName+" Created ...")
            
            
        except Exception as Exp:
            ## If an error happen catch it and let the user know
            logging.info(">>>>>Error While creating New Table")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp)            
            logging.info("Current SQL Statement =\n"+CreateTableStatment)
            raw_input("PLease press enter to continue.....")      
    
    
    def AddTreeProcessingIndex(self):
        
        CreateIndexStatment="ALTER TABLE TreeProcessingSummary  ADD PRIMARY KEY (LoadingTreeID);"
        self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment)
         
     
    def FillTreeProcessingTable(self,CommSize,CommRank):
        
        
        ## Generate insert template for the Datafiles table        
        logging.info("Start Loading HDF5 File Done....")
        InputFile=h5py.File(self.CurrentH5InputFile,'r')
        TotalTreesCount=len(InputFile['tree_counts'])        
        logging.info("End Loading HDF5 File Done....")   
        logging.info("Trees Count="+str(TotalTreesCount))    
        ProcessShare=math.ceil(TotalTreesCount/float(CommSize)) 
        StartIndex=int(CommRank*ProcessShare)
        
        EndIndex=int(min((CommRank+1)*ProcessShare,TotalTreesCount))
        
        logging.info("Trees From "+str(StartIndex)+"===>"+str(EndIndex))         
        
        dtype = ([('treeindex', 'i8'), ('tree_counts', 'i8'), ('tree_displs', 'i8'),('processed', 'b')])
        data = numpy.empty(int(EndIndex-StartIndex), dtype)
        
        
        
        data['treeindex']=range(StartIndex,EndIndex)
        data['tree_counts']=InputFile['tree_counts'][StartIndex:EndIndex]
        data['tree_displs']=InputFile['tree_displs'][StartIndex:EndIndex]
        data['processed'].fill(False)       
        
        
        pgcopy_dtype = [('num_fields','>i2')]
        for field, dtype in data.dtype.descr:
            pgcopy_dtype += [(field + '_length', '>i4'),(field, dtype.replace('<', '>'))]
            
        pgcopy = numpy.empty(data.shape, pgcopy_dtype)
        pgcopy['num_fields'] = len(data.dtype)
        for i in range(len(data.dtype)):
            field = data.dtype.names[i]
            pgcopy[field + '_length'] = data.dtype[i].alignment
            pgcopy[field] = data[field]
            
              
        cpyData = BytesIO()       
        cpyData.write(struct.pack('!11sii', b'PGCOPY\n\377\r\n\0', 0, 0))
        cpyData.write(pgcopy.tostring())
        cpyData.write(struct.pack('!h', -1))  # file trailer    
        logging.info("Start Copying Data....")
        
        cpyData.seek(0)
        self.DBConnection.ActiveCursors[0].copy_expert('COPY treeprocessingsummary FROM STDIN WITH BINARY', cpyData)
        #self.DBConnection.ActiveCursors[0].copy_from(cpyData, 'treeprocessingsummary', sep=';', columns=('LoadingTreeID', 'GalaxiesCount', 'StartIndex', 'Processed'))
        logging.info("End Copying Data....")
        
        
    
    
    
        
   
                 
    
        
        
        
        
         