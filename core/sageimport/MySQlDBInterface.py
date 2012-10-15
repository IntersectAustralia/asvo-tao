'''
Created on 01/10/2012
sudo apt-get install python-mysqldb

@author: Amr Hassan
'''
import MySQLdb
import getpass
import math
import string
import sys

class MySQlDBInterface(object):
    '''
    This class will handle the interface with the MySQLDB
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
        
        self.InitMySQLConnection()
        self.CreateNewTableTemplate()
        self.CreateInsertTemplate()
                
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
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyZ FLOAT"
        #self.CreateTableTemplate=self.CreateTableTemplate+ "PRIMARY KEY @TABLEName_PK (GlobalIndex)) "     
        self.CreateTableTemplate=self.CreateTableTemplate+ " TABLESPACE "+self.DBName+"_TS STORAGE DISK "
        self.CreateTableTemplate=self.CreateTableTemplate+" ENGINE=NDBCLUSTER MAX_ROWS="+str(int(self.Options['RunningSettings:GalaxiesPerTable'])*5)    
        
    
    
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
    def InitMySQLConnection(self):
        
        self.serverip=self.Options['MySQLDB:serverip']
        self.username=self.Options['MySQLDB:user']
        self.password=self.Options['MySQLDB:password']
        self.DBName=self.Options['MySQLDB:NewDBName']
        
        if self.password==None:
            print('Password for user:'+username+' is not defined')
            password=getpass.getpass('Please enter password:')
        
        
        self.CurrentConnection=MySQLdb.connect(host=self.serverip,user=self.username,passwd=self.password)
        print('Connection to DB is open...')
        self.cursor=self.CurrentConnection.cursor()
        self.ExecuteNoQuerySQLStatment("SELECT VERSION()")
        data=self.cursor.fetchone()        
        print ("Current MYSQL DB Version : "+data[0])

    def DropDatabase(self):
        ## Check if the database already exists
        self.cursor=self.CurrentConnection.cursor()
        self.ExecuteNoQuerySQLStatment("Show databases Like '"+self.DBName+"'")
        data=self.cursor.fetchone()  
        ## If the database already exists - give the user the option to drop it
        if data!=None:
            Response=raw_input("Database "+self.DBName+" with the same name already exists!\nIf you Choose to Continue it will be dropped. Do you want to Drop it?(y/n)")
            if Response=='y':
                ## Drop the database
                self.ExecuteNoQuerySQLStatment("Drop database "+self.DBName+";")
                #self.ExecuteNoQuerySQLStatment("Drop TABLESPACE "+self.DBName+"_LOGFILEGROUP ENGINE NDBCLUSTER;")
                #self.ExecuteNoQuerySQLStatment("Drop LOGFILE "+self.DBName+"_TS ENGINE NDBCLUSTER;")
                print("Database "+self.DBName+" Dropped")
    
                
    def CreateTableSpace(self):
        ####### Create a Log File Group ###################
        ###### Table space allow MYSQL to store Non-Index Columns into the secondary storage instead of Memory #####
        ####### See http://dev.mysql.com/doc/refman/5.1/en/mysql-cluster-disk-data.html for Details #####
        
        
        CreateLogFileStatement="CREATE LOGFILE GROUP "+self.DBName+"_LOGFILEGROUP "
        CreateLogFileStatement=CreateLogFileStatement+" ADD UNDOFILE \'"+self.DBName+"_LOGFILEGROUP_1"+".log\'"
        CreateLogFileStatement=CreateLogFileStatement+" INITIAL_SIZE 128M"
        CreateLogFileStatement=CreateLogFileStatement+" UNDO_BUFFER_SIZE 8M"
        CreateLogFileStatement=CreateLogFileStatement+" ENGINE NDBCLUSTER;"
        self.ExecuteNoQuerySQLStatment(CreateLogFileStatement);
        
        
        CreateTableSapceFileStatement="CREATE TABLESPACE "+self.DBName+"_TS ";
        CreateTableSapceFileStatement=CreateTableSapceFileStatement+" ADD DATAFILE \'"+self.DBName+"_TS_1"+".dat\'"
        CreateTableSapceFileStatement=CreateTableSapceFileStatement+" USE LOGFILE GROUP "+self.DBName+"_LOGFILEGROUP "
        CreateTableSapceFileStatement=CreateTableSapceFileStatement+" INITIAL_SIZE 128M"
        CreateTableSapceFileStatement=CreateTableSapceFileStatement+" ENGINE NDBCLUSTER;"
        self.ExecuteNoQuerySQLStatment(CreateTableSapceFileStatement);
        
        
        
    def CreateDB(self):
       ## Check if the database already exist and give the user the option to Drop it 
       self.DropDatabase()        
       #self.CreateTableSpace()
       ## Create New DB 
       self.ExecuteNoQuerySQLStatment("create database "+self.DBName+";") 
       print("Database "+self.DBName+" Created")
       ### Close the current Connection and open a new one on the new DB
       self.CurrentConnection.close()      
       self.CurrentConnection=MySQLdb.connect(host=self.serverip,user=self.username,passwd=self.password,db=self.DBName)
       self.cursor=self.CurrentConnection.cursor()
       print("Connection to Database "+self.DBName+" is opened and ready")
   
    def ExecuteNoQuerySQLStatment(self,SQLStatment):
        if self.DebugToFile==True:
            self.Log.write(SQLStatment+"\n\n")
            self.Log.flush()
        self.cursor.execute(SQLStatment)
        self.CurrentConnection.commit()  
    
    def CreateNewTable(self,TableIndex):       
        
            
        TablePrefix=self.Options['MySQLDB:TreeTablePrefix']
        NewTableName=TablePrefix+str(TableIndex)
        CreateTableStatment= string.replace(self.CreateTableTemplate,"@TABLEName",NewTableName)
        if self.DebugToFile==True:
            if self.Log!=None:
                self.Log.close()
            self.Log = open(self.Options['RunningSettings:OutputDir']+NewTableName+'_sql.txt', 'wt')
                    
        #print CreateTableStatment
        self.ExecuteNoQuerySQLStatment(CreateTableStatment)
        
        
        CreateIndexStatment="Create Index GlobalIndex_Index on  "+NewTableName+" (GlobalIndex);"
        self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
        CreateIndexStatment="Create Index SnapNum_Index on  "+NewTableName+" (SnapNum);"
        self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
        CreateIndexStatment="Create Index GlobalTreeID_Index on  "+NewTableName+" (GlobalTreeID);"
        self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
        CreateIndexStatment="Create Index CentralGalaxyX_Index on  "+NewTableName+" (CentralGalaxyX);"
        self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
        CreateIndexStatment="Create Index CentralGalaxyY_Index on  "+NewTableName+" (CentralGalaxyY);"
        self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
        CreateIndexStatment="Create Index CentralGalaxyZ_Index on  "+NewTableName+" (CentralGalaxyZ);"
        self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
        
         
        print("Table "+NewTableName+" Created With Index ...")
    
          
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
        TablePrefix=self.Options['MySQLDB:TreeTablePrefix']
        NewTableName=TablePrefix+str(self.CurrentTableID)  
        InsertStatment= string.replace(self.INSERTTemplate,"@TABLEName",NewTableName)  
        InsertStatment=InsertStatment+" VALUES "
        Location=0
        for TreeField in TreeData:
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
            #InsertStatment=InsertStatment+str(TreeField['DescendantGlobalID'])+","
            InsertStatment=InsertStatment+str(self.LocalGalaxyID)+","
            
            InsertStatment=InsertStatment+str(TreeField['CentralGalaxyX'])+","
            InsertStatment=InsertStatment+str(TreeField['CentralGalaxyY'])+","
            InsertStatment=InsertStatment+str(TreeField['CentralGalaxyZ'])+"),"
            self.LocalGalaxyID=self.LocalGalaxyID+1
            #print InsertStatment
        InsertStatment=InsertStatment[:-1]
        if self.DebugToFile==True:
            self.Log.write(InsertStatment+"\n\n")
            self.Log.flush()
        #print(InsertStatment)    
        self.ExecuteNoQuerySQLStatment(InsertStatment)
            
    def Close(self):
        self.CurrentConnection.close()
        if self.DebugToFile==True and self.Log!=None:
            self.Log.close()
            
        