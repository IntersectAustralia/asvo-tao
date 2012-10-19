'''
Created on 01/10/2012
sudo apt-get install python-mysqldb

@author: Amr Hassan
'''
import pg
import getpass
import math
import string
import sys
import subprocess

class DBInterface(object):
    '''
    This class will handle the interface with the DB
    '''
    FormatMapping={'int':'INT',
                   'float':'FLOAT',
                   'long long':'BIGINT'                   
                   }
    
    CurrentTableID=0
    CurrentTreesCounter=0
    
    DebugToFile=False
    
    def __init__(self,CurrentSAGEStruct,Options):
        '''
        Constructor
        '''
        self.Options=Options
        self.Log = open(self.Options['RunningSettings:OutputDir']+'DBCreation_sql.txt', 'wt')
        
        self.CurrentSAGEStruct=CurrentSAGEStruct
        
        self.InitDBConnection()
        self.CreateNewTableTemplate()
        self.CreateInsertTemplate()
        self.CreatePartitionFunction()
        #self.SetSystemPgPoolConfig(1,5)        
        self.CreateDB()
        
        self.CurrentGalaxiesCounter=int(Options['RunningSettings:GalaxiesPerTable'])+1 # To Create the First Table
    
    def CreateNewTableTemplate(self):
        self.CreateTableTemplate="CREATE TABLE @TABLEName ("
        for field in self.CurrentSAGEStruct:
            if field[3]==1:
                FieldDT=self.FormatMapping[field[1]]
                FieldName=field[2]
                self.CreateTableTemplate=self.CreateTableTemplate+ FieldName +' '+FieldDT+","
        self.CreateTableTemplate=self.CreateTableTemplate+"GlobalTreeID BIGINT,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyGlobalID BIGINT,"     
        self.CreateTableTemplate=self.CreateTableTemplate+"LocalGalaxyID INT,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyX FLOAT,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyY FLOAT,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyZ FLOAT)"
        #self.CreateTableTemplate=self.CreateTableTemplate+ "PRIMARY KEY @TABLEName_PK (GlobalIndex)) "     
        #self.CreateTableTemplate=self.CreateTableTemplate+ " TABLESPACE "+self.DBName+"_TS STORAGE DISK "
        #self.CreateTableTemplate=self.CreateTableTemplate+" ENGINE=NDBCLUSTER" #MAX_ROWS="+str(int(self.Options['RunningSettings:GalaxiesPerTable'])*5)    
        
    
    
    def CreateInsertTemplate(self):
        self.INSERTTemplate="INSERT INTO @TABLEName ("           
        for field in self.CurrentSAGEStruct:
            if field[3]==1:                
                FieldName=field[2]
                self.INSERTTemplate=self.INSERTTemplate+ FieldName+","
        self.INSERTTemplate=self.INSERTTemplate+"GlobalTreeID," 
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyGlobalID,"
        self.INSERTTemplate=self.INSERTTemplate+"LocalGalaxyID,"
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyX,"
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyY,"
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyZ)"
    def InitDBConnection(self):
        
        ####### PostgreSQL Simulation DB ################# 
        self.serverip=self.Options['PGDB:serverip']
        self.username=self.Options['PGDB:user']
        self.password=self.Options['PGDB:password']
        self.port=int(self.Options['PGDB:port'])
        self.DBName=self.Options['PGDB:NewDBName']
        
        if self.password==None:
            print('Password for user:'+username+' is not defined')
            self.password=getpass.getpass('Please enter password:')
        
        ########## PgPool System DB ##########################    
        self.Systemserverip=self.Options['PGSystemDB:serverip']
        self.Systemusername=self.Options['PGSystemDB:user']
        self.Systempassword=self.Options['PGSystemDB:password']
        self.Systemport=int(self.Options['PGSystemDB:port'])
        self.SystemDBName=self.Options['PGSystemDB:SystemDBName']
        
        if self.Systempassword==None:
            print('System Password for user:'+username+' is not defined')
            self.Systempassword=getpass.getpass('Please enter password:')    
        
        
        self.CurrentSystemConnection=pg.connect(host=self.Systemserverip,user=self.Systemusername,passwd=self.Systempassword,port=self.Systemport,dbname=self.SystemDBName)
        print('Connection to System DB is open...')
        self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname='master')
        print('Connection to DB is open...')
    
    def DeletePartitionEntry(self,DBName,TableName):
        DeleteStat="DELETE FROM pgpool_catalog.dist_def where dbname=\'"+DBName+"\' and table_name=\'"+TableName+"\';"
        DeleteStat=string.lower(DeleteStat)
        self.CurrentSystemConnection.query(DeleteStat)
    def CreatePartitionFunction(self):
        
        ##### Create pgpool partition function
        ##### Even Numbers go to TAO01 and Odd Number to TAO02
        PartitionFunction="CREATE OR REPLACE FUNCTION pgpool_catalog.dist_globaltree (val ANYELEMENT) RETURNS INTEGER AS $$"
        PartitionFunction=PartitionFunction+"SELECT CASE "
        PartitionFunction=PartitionFunction+" WHEN $1%2 = 0  THEN 0"
        PartitionFunction=PartitionFunction+" ELSE 1 END;$$ LANGUAGE sql;"

        self.CurrentSystemConnection.query(PartitionFunction) 
           
    def SetSystemPgPoolConfig(self,TableIndex):       
        
        ##### Insert Table Definition in pgpool 
        ##### 
        PartitionStat="INSERT INTO pgpool_catalog.dist_def VALUES "
        PartitionStat=PartitionStat+"(\'"+self.DBName+"\',\'public\',\'@TableName\',\'globaltreeid\',"
        PartitionStat=PartitionStat+ "ARRAY[@FIELDS], ARRAY[@FIELDSTYPE],\'pgpool_catalog.dist_globaltree\');"

        

        FieldsStr=""
        FieldsTypeStr=""
        for field in self.CurrentSAGEStruct:
            if field[3]==1:
                FieldsTypeStr=FieldsTypeStr+"\'"+self.FormatMapping[field[1]]+"\',"
                FieldsStr=FieldsStr+"\'"+field[2]+"\',"
                
        FieldsStr=FieldsStr+"\'GlobalTreeID\',"
        FieldsTypeStr=FieldsTypeStr+"\'BIGINT\',"        
        
        FieldsStr=FieldsStr+"\'CentralGalaxyGlobalID\',"
        FieldsTypeStr=FieldsTypeStr+"\'BIGINT\',"
        
        FieldsStr=FieldsStr+"\'LocalGalaxyID\',"
        FieldsTypeStr=FieldsTypeStr+"\'INT\',"
        
        FieldsStr=FieldsStr+"\'CentralGalaxyX\',"
        FieldsTypeStr=FieldsTypeStr+"\'FLOAT\',"
        
        FieldsStr=FieldsStr+"\'CentralGalaxyY\',"
        FieldsTypeStr=FieldsTypeStr+"\'FLOAT\',"
        
        FieldsStr=FieldsStr+"\'CentralGalaxyZ\'"
        FieldsTypeStr=FieldsTypeStr+"\'FLOAT\'"
        
        
        PartitionStat= string.replace(PartitionStat,"@FIELDSTYPE",FieldsTypeStr)
        PartitionStat= string.replace(PartitionStat,"@FIELDS",FieldsStr)
        
        
        
        TablePrefix=self.Options['PGDB:TreeTablePrefix']
        NewTableName=TablePrefix+str(TableIndex)
        TempPartitionStat= string.replace(PartitionStat,"@TableName",NewTableName)
        
        self.DeletePartitionEntry(self.DBName,NewTableName);   
        TempPartitionStat=string.lower(TempPartitionStat)         
        self.CurrentSystemConnection.query(TempPartitionStat)
        print("Restarting pgPool...")
        subprocess.Popen('cd /lustre/projects/p014_swin/pgpool/')
        print subprocess.Popen('which pgpool')
        print subprocess.Popen('pgpool -f  /lustre/projects/p014_swin/pgpool/pgpool.conf -F /lustre/projects/p014_swin/pgpool/pcp.conf -a /lustre/projects/p014_swin/pgpool/pool_hba.conf stop')
        print ("Server Closed .... ")
        print subprocess.Popen('pgpool -f  /lustre/projects/p014_swin/pgpool/pgpool.conf -F /lustre/projects/p014_swin/pgpool/pcp.conf -a /lustre/projects/p014_swin/pgpool/pool_hba.conf')
        
        print("Restarting pgPool... Done")    
        raw_input("Press Any Key to Cont.")
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
       ### Close the current Connection and open a new one on the new DB
       self.CurrentConnection.close()
       self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname=self.DBName)      
       
       
       print("Connection to Database "+self.DBName+" is opened and ready")
   
    def ExecuteNoQuerySQLStatment(self,SQLStatment):
        try:
            
            if self.DebugToFile==True:
                self.Log.write(SQLStatment+"\n\n")
                self.Log.flush()
            #self.cursor.execute(SQLStatment)
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
            
            if self.DebugToFile==True:
                self.Log.write(SQLStatment+"\n\n")
                self.Log.flush()
            
            resultsList=self.CurrentConnection.query(SQLStatment).getresult()
            
            return resultsList  
        except Exception as Exp:
            print(">>>>>Error While creating New Table")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
            
    def CreateNewTable(self,TableIndex):       
        CreateTableStatment=""
        try:
                
            TablePrefix=self.Options['PGDB:TreeTablePrefix']
            NewTableName=TablePrefix+str(TableIndex)
            CreateTableStatment= string.replace(self.CreateTableTemplate,"@TABLEName",NewTableName)
            if self.DebugToFile==True:
                if self.Log!=None:
                    self.Log.close()
                self.Log = open(self.Options['RunningSettings:OutputDir']+NewTableName+'_sql.txt', 'wt')
                        
            #print CreateTableStatment
            CreateTableStatment=string.lower(CreateTableStatment)
            self.ExecuteNoQuerySQLStatment(CreateTableStatment)
            
            
            CreateIndexStatment="Create Index GlobalIndex_Index_"+NewTableName+" on  "+NewTableName+" (GlobalIndex);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
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
            
            self.SetSystemPgPoolConfig(TableIndex)
            
        except Exception as Exp:
            print(">>>>>Error While creating New Table")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+CreateTableStatment)
            raw_input("PLease press enter to continue.....")
        
          
    def CreateNewTree(self,TreeData):
        print('Starting a New Tree')
        self.LocalGalaxyID=0
        if(self.CurrentGalaxiesCounter>=int(self.Options['RunningSettings:GalaxiesPerTable'])):
            print("Changing Table ID....Current Table ID "+str(self.CurrentTableID))
            self.CurrentTableID=self.CurrentTableID+1
            print("Creating New Table ...New Table ID "+str(self.CurrentTableID))            
            self.CreateNewTable(self.CurrentTableID)
            self.CurrentGalaxiesCounter=0
            
        if len(TreeData)>1000:
            for c in range(0,(len(TreeData)/1000)+1):
                start=c*1000
                end=min((c+1)*1000,len(TreeData))
                sys.stdout.write("\033[0;33m"+str(start)+":"+str(end)+" from "+str(len(TreeData))+"\033[0m\r")
                sys.stdout.flush()
                self.PrepareInsertStatement(TreeData[start:end])
        else:            
            self.PrepareInsertStatement(TreeData) 
            print("Tree Processing .. Done")   
        
        self.CurrentGalaxiesCounter=self.CurrentGalaxiesCounter+len(TreeData)
        
        self.CurrentTreesCounter=self.CurrentTreesCounter+1
        print("\n")
    def PrepareInsertStatement(self,TreeData):
        InsertStatment=""
        try:            
            TablePrefix=self.Options['PGDB:TreeTablePrefix']
            NewTableName=TablePrefix+str(self.CurrentTableID)  
            for TreeField in TreeData:
                InsertStatment= string.replace(self.INSERTTemplate,"@TABLEName",NewTableName)  
                InsertStatment=InsertStatment+" VALUES "
                Location=0
            
                #sys.stdout.write(str(Location)+"/"+str(len(TreeData))+"\r")
                #sys.stdout.flush()
                Location=Location+1
                InsertStatment=InsertStatment+"("
                for field in self.CurrentSAGEStruct:                
                    if field[3]==1:                
                        FieldName=field[0]
                        InsertStatment=InsertStatment+ str(TreeField[FieldName])+","
                InsertStatment=InsertStatment+str(self.CurrentTreesCounter)+","
                InsertStatment=InsertStatment+str(TreeField['CentralGalaxyGlobalID'])+","                
                InsertStatment=InsertStatment+str(self.LocalGalaxyID)+","
                
                InsertStatment=InsertStatment+str(TreeField['CentralGalaxyX'])+","
                InsertStatment=InsertStatment+str(TreeField['CentralGalaxyY'])+","
                InsertStatment=InsertStatment+str(TreeField['CentralGalaxyZ'])+"),"
                self.LocalGalaxyID=self.LocalGalaxyID+1
                
                InsertStatment=InsertStatment[:-1]
                if self.DebugToFile==True:
                    self.Log.write(InsertStatment+"\n\n")
                    self.Log.flush()
                
                self.ExecuteNoQuerySQLStatment(InsertStatment)
        except Exception as Exp:
            print(">>>>>Error While Processing Tree")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+InsertStatment)
            raw_input("PLease press enter to continue.....")
            
                
    def Close(self):
        self.CurrentConnection.close()
        if self.DebugToFile==True and self.Log!=None:
            self.Log.close()
            
        