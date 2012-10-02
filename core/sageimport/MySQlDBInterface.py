'''
Created on 01/10/2012
sudo apt-get install python-mysqldb

@author: Amr Hassan
'''
import MySQLdb
import getpass
import math
import string

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

    def __init__(self,CurrentSAGEStruct,Options):
        '''
        Constructor
        '''
        self.Options=Options
        self.CurrentSAGEStruct=CurrentSAGEStruct
        self.CreateNewTableTemplate()
        self.CreateInsertTemplate()
        self.InitMySQLConnection()        
        self.CreateDB()
        
        
    
    def CreateNewTableTemplate(self):
        self.CreateTableTemplate="CREATE TABLE @TABLEName ("
        for field in self.CurrentSAGEStruct:
            if field[3]==1:
                FieldDT=self.FormatMapping[field[1]]
                FieldName=field[2]
                self.CreateTableTemplate=self.CreateTableTemplate+ FieldName +' '+FieldDT+","
        #self.CreateTableTemplate=self.CreateTableTemplate[:-1]
        self.CreateTableTemplate=self.CreateTableTemplate+"GlobalTreeID BIGINT"    
        self.CreateTableTemplate=self.CreateTableTemplate+ ") ENGINE=NDBCLUSTER"     
            
    
    
    def CreateInsertTemplate(self):
        self.INSERTTemplate="INSERT INTO @TABLEName ("           
        for field in self.CurrentSAGEStruct:
            if field[3]==1:                
                FieldName=field[2]
                self.INSERTTemplate=self.INSERTTemplate+ FieldName+","
        self.INSERTTemplate=self.INSERTTemplate+"GlobalTreeID)" 
        print self.INSERTTemplate        
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
        self.cursor.execute("SELECT VERSION()")
        data=self.cursor.fetchone()        
        print ("Current MYSQL DB Version : "+data[0])

    def DropDatabase(self):
        ## Check if the database already exists
        self.cursor=self.CurrentConnection.cursor()
        self.cursor.execute("Show databases Like 'Millennium_Full'")
        data=self.cursor.fetchone()  
        ## If the database already exists - give the user the option to drop it
        if data!=None:
            Response=raw_input("Database with the same name already exists!\nIf you Choose to Continue it will be dropped. Do you want to Drop it?(y/n)")
            if Response=='y':
                ## Drop the database
                self.cursor.execute("Drop database "+self.DBName+";")
                print("Database "+self.DBName+" Dropped")
                
        
    def CreateDB(self):
       ## Check if the database already exist and give the user the option to Drop it 
       self.DropDatabase() 
       ## Create New DB 
       self.cursor.execute("create database "+self.DBName+";") 
       print("Database "+self.DBName+" Created")
       ### Close the current Connection and open a new one on the new DB
       self.Close()       
       self.CurrentConnection=MySQLdb.connect(host=self.serverip,user=self.username,passwd=self.password,db=self.DBName)
       self.cursor=self.CurrentConnection.cursor()
       print("Connection to Database "+self.DBName+" is opened and ready")
   
    def CreateNewTable(self,TableIndex):
        TablePrefix=self.Options['MySQLDB:TreeTablePrefix']
        NewTableName=TablePrefix+str(TableIndex)
        CreateTableStatment= string.replace(self.CreateTableTemplate,"@TABLEName",NewTableName)        
        
        self.cursor.execute(CreateTableStatment)        
        print("Table "+NewTableName+" Created ...")
    
          
    def CreateNewTree(self,TreeData):
        print('Starting a New Tree')
        
        if(self.CurrentTreesCounter%int(self.Options['RunningSettings:TreePerTable'])==0):
            print("Changing Table ID....Current Table ID "+str(self.CurrentTableID))
            self.CurrentTableID=self.CurrentTableID+1
            print("Creating New Table ...New Table ID "+str(self.CurrentTableID))            
            self.CreateNewTable(self.CurrentTableID)
            
        
        self.PrepareInsertStatement(TreeData)
        
        self.CurrentTreesCounter=self.CurrentTreesCounter+1
        
    def PrepareInsertStatement(self,TreeData):
        TablePrefix=self.Options['MySQLDB:TreeTablePrefix']
        NewTableName=TablePrefix+str(self.CurrentTableID)  
        InsertStatment= string.replace(self.INSERTTemplate,"@TABLEName",NewTableName)  
        InsertStatment=InsertStatment+" VALUES "
        for TreeField in TreeData:
            InsertStatment=InsertStatment+"("
            for field in self.CurrentSAGEStruct:                
                if field[3]==1:                
                    FieldName=field[0]
                    InsertStatment=InsertStatment+ str(TreeField[FieldName])+","
            InsertStatment=InsertStatment+str(self.CurrentTreesCounter)+"),"
            #print InsertStatment
        InsertStatment=InsertStatment[:-1]
        
        self.cursor.execute(InsertStatment)
        self.CurrentConnection.commit()     
    def Close(self):
        self.CurrentConnection.close()
        
            
        