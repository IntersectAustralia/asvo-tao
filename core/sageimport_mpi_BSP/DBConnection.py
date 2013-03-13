import pg
import math
import string
import sys
import settingReader # Read the XML settings

class DBConnection(object):
       
    
    def __init__(self,Options,ConnectToDefaultDB=False):
        
        self.Options=Options       
        
        self.InitDBConnection(ConnectToDefaultDB)
        
    
    def InitDBConnection(self,ConnectToDefaultDB):
        
        ####### PostgreSQL Simulation DB ################# 
        self.serverscount=int(self.Options['PGDB:ServersCount'])
        if ConnectToDefaultDB==True:
            self.DBName="postgres"
        else:
            self.DBName=self.Options['PGDB:NewDBName']
        self.DBservers=[]
        self.CurrentConnections=[]
        for i in range(0,self.serverscount): 
            serverinfo={}
                   
            serverinfo['serverip']=self.Options['PGDB:serverInfo'+str(i)+':serverip']
            serverinfo['username']=self.Options['PGDB:serverInfo'+str(i)+':user']
            serverinfo['password']=self.Options['PGDB:serverInfo'+str(i)+':password']
            serverinfo['port']=int(self.Options['PGDB:serverInfo'+str(i)+':port'])
            self.DBservers.append(serverinfo)      
            CurrentConnection=pg.connect(host=serverinfo['serverip'],user=serverinfo['username'],passwd=serverinfo['password'],port=serverinfo['port'],dbname=self.DBName)
            self.CurrentConnections.append(CurrentConnection)
        print('Connection to DB is open...')
    
    def CloseConnections(self):  
        for i in range(0,self.serverscount):
            self.CurrentConnections[i].close()              
           
            
    
    def ExecuteNoQuerySQLStatment_On_AllServers(self,SQLStatment):
        for i in range(0,self.serverscount):
            self.ExecuteNoQuerySQLStatment(SQLStatment, i)
    
    def ExecuteNoQuerySQLStatment(self,SQLStatment,DatabaseIndex=0):
        try:            
            SQLStatment=string.lower(SQLStatment)  
            self.CurrentConnections[DatabaseIndex].query(SQLStatment)              
        except Exception as Exp:
            print(">>>>>Error While Executing XML NoQuery Statement")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
            
    def ExecuteQuerySQLStatment(self,SQLStatment,DatabaseIndex=0):
        try:           
            resultsList=self.CurrentConnections[DatabaseIndex].query(SQLStatment).getresult()            
            return resultsList
        except Exception as Exp:
            print(">>>>>Error While Executing XML Query Statement")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")                            
        
        

            
        
    
    