import math
import settingReader
import os
import sys
import struct
import string
import DBConnection

class PreprocessFiles(object):
    ## Mapping between SAGE (C/C++) data types to Database data types 
    FormatMapping={'int':'INT','float':'FLOAT4','long long':'BIGINT'}
    
    
    ## Init the class with XML Options 
    def __init__(self,CurrentSAGEStruct,Options):       
        
        self.CurrentFolderPath=Options['RunningSettings:InputDir']
        self.DBName=Options['PGDB:NewDBName']
        self.CurrentSAGEStruct=CurrentSAGEStruct
        self.Options=Options
          
        if self.CurrentFolderPath.endswith("/"):
            self.CurrentFolderPath=self.CurrentFolderPath[:-1] 
            
        
        
        
        
   
    def InitDBConnection(self,ToMasterDB):
        
        ####### PostgreSQL Simulation DB ################# 
        self.DBConnection=DBConnection.DBConnection(self.Options,ToMasterDB)
        
        print('Connection to DB is open...')
    
    def DropDatabase(self):
        ## Check if the database already exists
        
        ResultsList=self.DBConnection.ExecuteQuerySQLStatment("SELECT datname FROM pg_database where datistemplate=false and datname=\'"+self.DBName+"\'")
          
        ## If the database already exists - give the user the option to drop it
        if len(ResultsList)>0:
            sys.stdout.write("\033[0;33m"+"Database "+self.DBName+" with the same name already exists!\nIf you Choose to Continue it will be dropped. Do you want to Drop it?(y/n)\033[0m\n")
            sys.stdout.flush()
            Response=raw_input("")
            if Response=='y':
                ## Drop the database
                self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers("Drop database "+self.DBName+";")                
                print("Database "+self.DBName+" Dropped")
    
                
    
    def CreateDB(self):
       ## Check if the database already exist and give the user the option to Drop it 
       self.DropDatabase()        
       
       ## Create New DB 
       self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers("create database "+self.DBName+";") 
       print("Database "+self.DBName+" Created")
       ### Close the current Connection (To a Default DB) and open a new one on the new DB
       self.DBConnection.CloseConnections()
       self.DBConnection=DBConnection.DBConnection(self.Options)      
       
       
       print("Connection to Database "+self.DBName+" is opened and ready")
   
   
   
    
    def CreateTreeMappingTable(self):
        
        DropTable="DROP TABLE IF EXISTS TreeMapping;"
        self.DBConnection.ExecuteNoQuerySQLStatment(DropTable)
        
        CreateTable="CREATE TABLE TreeMapping ("        
        CreateTable=CreateTable+"GlobalTreeID BIGINT,"       
        CreateTable=CreateTable+"GridX INT,"
        CreateTable=CreateTable+"GridY INT)"                
        
        
        self.DBConnection.ExecuteNoQuerySQLStatment(CreateTable)
    
    ## Generate All the tables required for the data importing process
    def GenerateAllTables(self): 
        
        
        SimulationBoxX=float(self.Options['RunningSettings:SimulationBoxX'])
        SimulationBoxY=float(self.Options['RunningSettings:SimulationBoxX'])
        BSPCellSize=float(self.Options['RunningSettings:BSPCellSize'])
        
        print("Processing BOX ("+str(SimulationBoxX)+"x"+str(SimulationBoxY)+") With Cell Size="+str(BSPCellSize))
        
        CellsInX=int(math.ceil(SimulationBoxX/BSPCellSize))
        CellsInY=int(math.ceil(SimulationBoxY/BSPCellSize))
        
        print("Cells In X="+str(CellsInX))
        print("Cells In Y="+str(CellsInY))
        
        
        NumberofTables=CellsInX*CellsInY
        
        
        
        ## Create Table template statement 
        self.CreateNewTableTemplate()
        
        print("WARNING ALL DATA TABLES WILL BE RECREATED .....")
        
        ## Ensure that there is no Files marked as processed..
        ## This may happen if the user drop the table and forget to update the datafiles table
        ## This execution is just a pre-caution
        self.DBConnection.ExecuteNoQuerySQLStatment("UPDATE datafiles set Processed=FALSE;")
        
        setWarningOff="set client_min_messages='warning'; "
        self.DBConnection.ExecuteNoQuerySQLStatment(setWarningOff)
        
        ## Get List of all tables expected from "datafiles" table
        #TableIDs=self.ExecuteQuerySQLStatment("select distinct tableid from datafiles order by tableid;")
        TableIDs=range(0,NumberofTables)
        ## for each tableID create New Table 
        for TableID in TableIDs:
            print("Creating Table ("+str(TableID)+")")
            self.CreateNewTable(TableID)
        
        self.CreateNewTable(NumberofTables)
    
    ## Use Statement concatenation and the  CurrentSAGEStrcuture loaded from the XML settings to create a new table template
    def CreateNewTableTemplate(self):
        self.CreateTableTemplate="CREATE TABLE @TABLEName ("
        for field in self.CurrentSAGEStruct:
            if field[3]==1:
                ## Mapping SAGE (C/C++) to DB data types
                FieldDT=self.FormatMapping[field[1]]
                FieldName=field[2]
                self.CreateTableTemplate=self.CreateTableTemplate+ FieldName +' '+FieldDT+","
        self.CreateTableTemplate=self.CreateTableTemplate+"GlobalTreeID BIGINT,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyGlobalID BIGINT,"     
        self.CreateTableTemplate=self.CreateTableTemplate+"LocalGalaxyID INT,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyX FLOAT4,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyY FLOAT4,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyZ FLOAT4, PRIMARY KEY (GlobalIndex))"
                
    ## Perform create table for a specific TableIndex            
    def CreateNewTable(self,TableIndex):        
        
               
        CreateTableStatment=""
        HostIndex=TableIndex%self.DBConnection.serverscount
        try:
            
            ## The Table name is defined using the TreeTablePrefix from the XML config file
            TablePrefix=self.Options['PGDB:TreeTablePrefix']
            NewTableName=TablePrefix+str(TableIndex)
            ## If the table exists drop it 
            DropSt="DROP TABLE IF EXISTS "+NewTableName+";"
            self.DBConnection.ExecuteNoQuerySQLStatment(DropSt,HostIndex)
            CreateTableStatment= string.replace(self.CreateTableTemplate,"@TABLEName",NewTableName)
            
                        
            
            CreateTableStatment=string.lower(CreateTableStatment)
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateTableStatment,HostIndex)
            
            ## Create Table indices             
            
            CreateIndexStatment="Create Index SnapNum_Index_"+NewTableName+" on  "+NewTableName+" (SnapNum);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            CreateIndexStatment="Create Index GlobalTreeID_Index_"+NewTableName+" on  "+NewTableName+" (GlobalTreeID);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            CreateIndexStatment="Create Index CentralGalaxyX_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyX);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            CreateIndexStatment="Create Index CentralGalaxyY_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyY);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            CreateIndexStatment="Create Index CentralGalaxyZ_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyZ);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,HostIndex)
            
             
            print("Table "+NewTableName+" Created With Index ...")
            
            
        except Exception as Exp:
            ## If an error happen catch it and let the user know
            print(">>>>>Error While creating New Table")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+CreateTableStatment)
            raw_input("PLease press enter to continue.....")       
    
    def GetNonEmptyFilesList(self):
        
        #Get List of Files where the file size is greater than zero        
        print("Get list of files to be processed ....")
        dirList=os.listdir(self.CurrentFolderPath)
        print("Current Files Count="+str(len(dirList)))
        fullPathArray=[]
        for fname in dirList:
            ## Get file information (for getting the file size)  
            ## Some files are zero length and might cause a problem in loading so the code will exclude them before processing
            statinfo = os.stat(self.CurrentFolderPath+'/'+fname)                
            
            
            if(statinfo.st_size>0 and string.find(fname,'model_')==0):
                fullPathArray.append([self.CurrentFolderPath+'/'+fname,statinfo.st_size])
            elif(statinfo.st_size>0):
                print("File Not Included:"+fname)
        self.NonEmptyFiles=fullPathArray
     
     
    def ProcessAllFiles(self):
        
        
        self.CreateTreeMappingTable()
        
              
        #Process All the Non-Empty Files 
        ## The table "DataFiles" will work as a record keeper for which files has been processed and which has not been processed 
        ## It will be use to support continue in case of error
        CreateTableSt="CREATE TABLE DataFiles "
        CreateTableSt=CreateTableSt+"(FileID INT, FileName varchar(500),FileSize BIGINT, "
        CreateTableSt=CreateTableSt+" NumberofTrees INT, TotalNumberOfGalaxies BIGINT, TreeIDFrom INT,TreeIDTo INT,Processed boolean);"
        
        self.DBConnection.ExecuteNoQuerySQLStatment(CreateTableSt)
        
        ## Generate insert template for the Datafiles table
        InsertTemplate="INSERT INTO DataFiles (FileID,FileName,FileSize,NumberofTrees,TotalNumberOfGalaxies, TreeIDFrom,TreeIDTo,Processed) VALUES "
        
        
        StartFrom=1        
        CurrentGalaxiesCounter=0
        TotalGalaxiesCount=0
        
        ## Used for reporting only (X out of Y)
        FileID=0
        TotalFilesCount=len(self.NonEmptyFiles)
        
        for fobject in self.NonEmptyFiles:
            
            
            CurrentInsertSt=InsertTemplate+"("
            print('Processing File ('+str(FileID)+"/"+str(TotalFilesCount-1)+"):"+fobject[0])                       
            
            
            ########## Get File data from the header #########################            
            [NumberofTrees,TotalNumberOfGalaxies]=self.ProcessFile(fobject[0])
            
            TotalGalaxiesCount=TotalGalaxiesCount+TotalNumberOfGalaxies
            ##############################################################################
            ########### XML Output #######################################################
            
            CurrentInsertSt=CurrentInsertSt+str(FileID)+","
            CurrentInsertSt=CurrentInsertSt+"'"+fobject[0]+"',"
            CurrentInsertSt=CurrentInsertSt+str(fobject[1])+","
            CurrentInsertSt=CurrentInsertSt+str(NumberofTrees)+","
            CurrentInsertSt=CurrentInsertSt+str(TotalNumberOfGalaxies)+","
            CurrentInsertSt=CurrentInsertSt+str(StartFrom)+","
            CurrentInsertSt=CurrentInsertSt+str(StartFrom+NumberofTrees-1)+","
            CurrentInsertSt=CurrentInsertSt+"FALSE)"
            self.DBConnection.ExecuteNoQuerySQLStatment(CurrentInsertSt)
            ##############################################################################
            
            FileID=FileID+1
            CurrentGalaxiesCounter=CurrentGalaxiesCounter+TotalNumberOfGalaxies
            if(CurrentGalaxiesCounter>=int(self.Options['RunningSettings:GalaxiesPerTable'])):                                
                CurrentGalaxiesCounter=0
            
            StartFrom=StartFrom+NumberofTrees
        
        #SettingFile.close()
        print ("Total Number of Galaxies="+str(TotalGalaxiesCount))
    
    ## Read file header and get the information associated        
    def ProcessFile(self,FilePath):
        
        ## Open the file for reading
        CurrentFile=open(FilePath,"rb")
        CurrentFileGalaxyID=0        
        ## Read the Number of trees and galaxies 
        NumberofTrees= struct.unpack('i', CurrentFile.read(4))[0]
        TotalNumberOfGalaxies= struct.unpack('i', CurrentFile.read(4))[0]
        ## Close the file        
        CurrentFile.close()
        return [NumberofTrees,TotalNumberOfGalaxies]
    ## Close DB connection        
    def CloseConnections(self):        
        self.CurrentConnection.close()
       
        
   
                 
    
        
        
        
        
         