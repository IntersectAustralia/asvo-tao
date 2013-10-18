import psycopg2
from psycopg2 import extras
import math
import string
import sys
import settingReader # Read the XML settings
import logging

class DBConnection(object):
       
    
    def __init__(self,Options,ConnectToDefaultDB=False):
        self.ConnectionOpened=False
        self.QueriesCount=0
        self.Options=Options       
        self.PrepareDatabaseInfo()
        
    def PrepareDatabaseInfo(self):
        self.serverscount=int(self.Options['PGDB:ServersCount'])
        
        self.DBservers=[]
        self.CurrentConnections=[]
        self.ActiveCursors=[]
        for i in range(0,self.serverscount): 
            serverinfo={}                   
            serverinfo['serverip']=self.Options['PGDB:serverInfo'+str(i)+':serverip']
            serverinfo['username']=self.Options['PGDB:serverInfo'+str(i)+':user']
            serverinfo['password']=self.Options['PGDB:serverInfo'+str(i)+':password']
            serverinfo['port']=int(self.Options['PGDB:serverInfo'+str(i)+':port'])
            self.DBservers.append(serverinfo)  
            
    
    def ConnectDB(self,Current_DBName, ServerID):  
        serverinfo=self.DBservers[ServerID]   
        ConnectionStr="host="+serverinfo['serverip']+" user="+serverinfo['username']+" password="+serverinfo['password']+" port="+str(serverinfo['port'])+" dbname="+Current_DBName
        CurrentConnection=psycopg2.connect(ConnectionStr)
        CurrentConnection.autocommit=True
        self.CurrentConnections=CurrentConnection
        self.ActiveCursors=CurrentConnection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('Connection to DB is open...')
        self.ConnectionOpened=True
    
    def ChangeConnection(self,Current_DBName,ServerID):
        self.CloseConnections()
        self.ConnectDB(Current_DBName,ServerID)
                 
    
        
    def CloseConnections(self): 
        if self.ConnectionOpened==True: 
            self.ActiveCursors.close()
            self.CurrentConnections.close()              
            self.ConnectionOpened=False       
            
    def ExecuteNoQuerySQLStatment(self,SQLStatment,SQLParamsDict=None):
        try:
            print(SQLStatment) 
    
            #SQLStatment=string.lower(SQLStatment)  
            if SQLParamsDict==None:
                self.ActiveCursors.execute(SQLStatment)
            else:
                self.ActiveCursors.execute(SQLStatment,SQLParamsDict)              
        except Exception as Exp:            
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
            
    def ExecuteQuerySQLStatment(self,SQLStatment,SQLParamsDict={}):
        
        try:
            print(SQLStatment)
            print(SQLParamsDict)
      
           
            self.ActiveCursors.execute(SQLStatment,SQLParamsDict)
            resultsList= self.ActiveCursors.fetchall()           
            return resultsList
        except Exception as Exp:
            
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....") 
            
             
if __name__ == '__main__':
    
    if len(sys.argv)<2:
        print("Error Not Enough Arguments")
        exit()
    SettingFile=sys.argv[1]
    
    
    [CurrentSAGEStruct,Options]=settingReader.ParseParams(SettingFile)
    DBConnectionObj=DBConnection(Options)
    
    for i in range(0,DBConnectionObj.serverscount):
        DBConnectionObj.ChangeConnection('postgres',i)
        Results=DBConnectionObj.ExecuteQuerySQLStatment("select datname from pg_database where datistemplate=false;", i)
        print Results
        for DBName in Results:
            print DBName[0]
            if DBName[0]!='postgres':
                try:
                    DBConnectionObj.ChangeConnection(str(DBName[0]),i)
                    print "Connection To"+str(DBName[0])+" .... Done"
                    DBConnectionObj.ExecuteNoQuerySQLStatment("GRANT CONNECT ON DATABASE "+DBName[0]+" to tao_sciencemodules_user;")
                    DBConnectionObj.ExecuteNoQuerySQLStatment("REVOKE ALL ON ALL TABLES IN SCHEMA public From tao_sciencemodules_user;")
                    DBConnectionObj.ExecuteNoQuerySQLStatment("GRANT SELECT ON ALL TABLES IN SCHEMA public to tao_sciencemodules_user;")
                    
                except Exception as Exp:
                    print Exp
                
    