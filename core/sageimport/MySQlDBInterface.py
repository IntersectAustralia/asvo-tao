'''
Created on 01/10/2012
sudo apt-get install python-mysqldb

@author: Amr Hassan
'''
import MySQLdb
import getpass

class MySQlDBInterface(object):
    '''
    This class will handle the interface with the MySQLDB
    '''
    


    def __init__(self,Options):
        '''
        Constructor
        '''
        self.Options=Options
        print Options
        self.InitMySQLConnection()        
        self.CreateDB()
        
        self.Close()
    
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
            Response=raw_input("Database with the same name already exists! If you Choose to Continue it will be dropped. Do you want to Drop it?(y/n)")
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
   
    def CreateNewTable(self,TableIndex):
        TablePrefix=self.Options['MySQLDB:TreeTablePrefix']
        NewTableName=TablePrefix+str(TableIndex)
           
    def CreateNewTree(self):
        print('Starting a New Tree')
    def InsertNewGalaxy(self):
        printf('New Galaxy')    
    def Close(self):
        self.CurrentConnection.close()
        
            
        