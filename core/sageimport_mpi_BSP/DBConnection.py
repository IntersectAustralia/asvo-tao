import pg
import math
import string
import sys
import settingReader # Read the XML settings
import logging

class DBConnection(object):
       
    
    def __init__(self,Options,ConnectToDefaultDB=False):
        self.ConnectionOpened=False
        self.InTransactions=False
        self.QueriesCount=0
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
        logging.info('Connection to DB is open...')
        self.ConnectionOpened=True
    
    def AutoRestartDBConnections(self):
        self.IncrementQueriesCount()
        if self.QueriesCount>=50:
           self.RestartConnection()
           self.QueriesCount=0
            
    def IncrementQueriesCount(self):
        if self.DBName!="postgres":
            self.QueriesCount=self.QueriesCount+1
    def RestartConnection(self):
        if self.DBName!="postgres" and self.ConnectionOpened==True and self.InTransactions==False:
            logging.info("Restarting DB Connections")
            self.CloseConnections()
            self.InitDBConnection(False)
        
    def CloseConnections(self): 
        if self.ConnectionOpened==True: 
            for i in range(0,self.serverscount):
                self.CurrentConnections[i].close()              
            self.ConnectionOpened=False   
    
    def StartTransaction(self):
        
        self.ExecuteNoQuerySQLStatment_On_AllServers("BEGIN;")
        self.InTransactions=True
        logging.info("Start Transaction")
        
    def CommitTransaction(self):
        
        self.ExecuteNoQuerySQLStatment_On_AllServers("COMMIT;")        
        self.InTransactions=False
        logging.info("End Transaction")
        
    def ExecuteNoQuerySQLStatment_On_AllServers(self,SQLStatment):
        for i in range(0,self.serverscount):
            self.ExecuteNoQuerySQLStatment(SQLStatment, i)
    
    def MapTableIDToServerIndex(self,TableID):
        return TableID%self.serverscount
    
    def ExecuteNoQuerySQLStatment(self,SQLStatment,DatabaseIndex=0):
        try:            
            self.AutoRestartDBConnections()
            SQLStatment=string.lower(SQLStatment)  
            self.CurrentConnections[DatabaseIndex].query(SQLStatment)              
        except Exception as Exp:
            logging.info(">>>>>Error While Executing NoQuery Statement On Server ("+str(DatabaseIndex)+")")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp)            
            logging.info("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
            
    def ExecuteQuerySQLStatment(self,SQLStatment,DatabaseIndex=0):
        
        try:
            self.AutoRestartDBConnections()           
            resultsList=self.CurrentConnections[DatabaseIndex].query(SQLStatment).getresult()            
            return resultsList
        except Exception as Exp:
            logging.info(">>>>>Error While Executing Query Statement On Server ("+str(DatabaseIndex)+")")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp)            
            logging.info("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")                            
        
        

            
        
    
    