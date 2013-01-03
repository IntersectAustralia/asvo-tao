import math
import settingReader
import os
import sys
import struct
import string
import pg

class PreprocessFiles(object):
    ## Mapping between SAGE (C/C++) data types to Database data types 
    FormatMapping={'int':'INT','float':'FLOAT4','long long':'BIGINT'}
    
    
    ## Init the class with XML Options 
    def __init__(self,CurrentSAGEStruct,Options):       
        
        self.CurrentFolderPath=Options['RunningSettings:InputDir']
        self.CurrentSAGEStruct=CurrentSAGEStruct
        self.Options=Options
          
        if self.CurrentFolderPath.endswith("/"):
            self.CurrentFolderPath=self.CurrentFolderPath[:-1] 
            
        
        
        
        
   
    def InitDBConnection(self,ToMasterDB):
        
        ####### PostgreSQL Simulation DB ################# 
        self.serverip=self.Options['PGDB:serverip']
        self.username=self.Options['PGDB:user']
        self.password=self.Options['PGDB:password']
        self.port=int(self.Options['PGDB:port'])
        self.DBName=self.Options['PGDB:NewDBName']
        
        if self.password==None:
            print('Password for user:'+username+' is not defined')
            self.password=getpass.getpass('Please enter password:')
        
        
        # Take care that the connection will be opened to standard DB 'master'
        # This is temp. until the actual database is created
        if ToMasterDB==True:
            self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname='postgres')
        else:
            self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname=self.DBName)
        print('Connection to DB is open...')
    
    def DropDatabase(self):
        ## Check if the database already exists
        
        ResultsList=self.ExecuteQuerySQLStatment("SELECT datname FROM pg_database where datistemplate=false and datname=\'"+self.DBName+"\'")
          
        ## If the database already exists - give the user the option to drop it
        if len(ResultsList)>0:
            Response=raw_input("Database "+self.DBName+" with the same name already exists!\nIf you Choose to Continue it will be dropped. Do you want to Drop it?(y/n)")
            if Response=='y':
                ## Drop the database
                self.ExecuteNoQuerySQLStatment("Drop database "+self.DBName+";")                
                print("Database "+self.DBName+" Dropped")
    
                
    
    def CreateDB(self):
       ## Check if the database already exist and give the user the option to Drop it 
       self.DropDatabase()        
       
       ## Create New DB 
       self.ExecuteNoQuerySQLStatment("create database "+self.DBName+";") 
       print("Database "+self.DBName+" Created")
       ### Close the current Connection (To a Default DB) and open a new one on the new DB
       self.CurrentConnection.close()
       self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname=self.DBName)      
       
       
       print("Connection to Database "+self.DBName+" is opened and ready")
   
   
    # Execute SQL Statement with no return (DDL Statements and some DML statements )
    def ExecuteNoQuerySQLStatment(self,SQLStatment):
        try:    
            ### All Names will be converted to lower case
            ### If the execution fails the catch part will work - But the program will not abort 
            SQLStatment=string.lower(SQLStatment)  
            self.CurrentConnection.query(SQLStatment)
              
        except Exception as Exp:
            ## Display the error Information and the SQL statement that caused it
            print(">>>>>Error While Executing NonQuery Statement")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            ## Pause the execution until the user acknowledge the error
            raw_input("PLease press enter to continue.....")
    
    ## Execute SQL statement with return data
    ## The results is returned as an array of tuples
    def ExecuteQuerySQLStatment(self,SQLStatment):
        try:
            ### All Names will be converted to lower case
            ### If the execution fails the catch part will work - But the program will not abort
                     
            SQLStatment=string.lower(SQLStatment)
            resultsList=self.CurrentConnection.query(SQLStatment).getresult()            
            return resultsList  
        
        except Exception as Exp:
            ## Display the error Information and the SQL statement that caused it
            print(">>>>>Error While executing Query SQL ")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            ## Pause the execution until the user acknowledge the error
            raw_input("PLease press enter to continue.....")
    
    
    ## Generate All the tables required for the data importing process
    def GenerateAllTables(self): 
        ## Create Table template statement 
        self.CreateNewTableTemplate()
        
        print("WARNING ALL DATA TABLES WILL BE RECREATED .....")
        
        ## Ensure that there is no Files marked as processed..
        ## This may happen if the user drop the table and forget to update the datafiles table
        ## This execution is just a pre-caution
        self.ExecuteNoQuerySQLStatment("UPDATE datafiles set Processed=FALSE;")
        
        ## Get List of all tables expected from "datafiles" table
        TableIDs=self.ExecuteQuerySQLStatment("select distinct tableid from datafiles order by tableid;")
        ## for each tableID create New Table 
        for TableID in TableIDs:
            print("Creating Table ("+str(TableID[0])+")")
            self.CreateNewTable(TableID[0])
    
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
        try:
            
            ## The Table name is defined using the TreeTablePrefix from the XML config file
            TablePrefix=self.Options['PGDB:TreeTablePrefix']
            NewTableName=TablePrefix+str(TableIndex)
            ## If the table exists drop it 
            DropSt="DROP TABLE IF EXISTS "+NewTableName+";"
            self.ExecuteNoQuerySQLStatment(DropSt)
            CreateTableStatment= string.replace(self.CreateTableTemplate,"@TABLEName",NewTableName)
            
                        
            
            CreateTableStatment=string.lower(CreateTableStatment)
            self.ExecuteNoQuerySQLStatment(CreateTableStatment)
            
            ## Create Table indices             
            
            CreateIndexStatment="Create Index SnapNum_Index_"+NewTableName+" on  "+NewTableName+" (SnapNum);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index GlobalTreeID_Index_"+NewTableName+" on  "+NewTableName+" (GlobalTreeID);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index CentralGalaxyX_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyX);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index CentralGalaxyY_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyY);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index CentralGalaxyZ_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyZ);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            
             
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
        
        #Process All the Non-Empty Files 
        ## The table "DataFiles" will work as a record keeper for which files has been processed and which has not been processed 
        ## It will be use to support continue in case of error
        CreateTableSt="CREATE TABLE DataFiles "
        CreateTableSt=CreateTableSt+"(FileID INT, FileName varchar(500),FileSize BIGINT, "
        CreateTableSt=CreateTableSt+" NumberofTrees INT, TotalNumberOfGalaxies BIGINT, TreeIDFrom INT,TreeIDTo INT,TableID INT, Processed boolean);"
        
        self.ExecuteNoQuerySQLStatment(CreateTableSt)
        
        ## Generate insert template for the Datafiles table
        InsertTemplate="INSERT INTO DataFiles (FileID,FileName,FileSize,NumberofTrees,TotalNumberOfGalaxies, TreeIDFrom,TreeIDTo,TableID,Processed) VALUES "
        
        
        StartFrom=1
        TableID=1
        CurrentGalaxiesCounter=0
        TotalGalaxiesCount=0
        
        ## Used for reporting only (X out of Y)
        FileID=0
        TotalFilesCount=len(self.NonEmptyFiles)
        
        for fobject in self.NonEmptyFiles:
            
            
            CurrentInsertSt=InsertTemplate+"("
            print('Processing File ('+str(FileID)+"/"+str(TotalFilesCount)+"):"+fobject[0])                       
            
            
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
            CurrentInsertSt=CurrentInsertSt+str(TableID)+", FALSE)"
            self.ExecuteNoQuerySQLStatment(CurrentInsertSt)
            ##############################################################################
            
            FileID=FileID+1
            CurrentGalaxiesCounter=CurrentGalaxiesCounter+TotalNumberOfGalaxies
            if(CurrentGalaxiesCounter>=int(self.Options['RunningSettings:GalaxiesPerTable'])):
                TableID=TableID+1                
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
       
        
   
                 
    
        
        
        
        
         