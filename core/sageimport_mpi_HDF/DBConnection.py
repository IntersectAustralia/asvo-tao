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
        self.ActiveCursors=[]
        for i in range(0,self.serverscount): 
            serverinfo={}
                   
            serverinfo['serverip']=self.Options['PGDB:serverInfo'+str(i)+':serverip']
            serverinfo['username']=self.Options['PGDB:serverInfo'+str(i)+':user']
            serverinfo['password']=self.Options['PGDB:serverInfo'+str(i)+':password']
            serverinfo['port']=int(self.Options['PGDB:serverInfo'+str(i)+':port'])
            self.DBservers.append(serverinfo)  
            ConnectionStr="host="+serverinfo['serverip']+" user="+serverinfo['username']+" password="+serverinfo['password']+" port="+str(serverinfo['port'])+" dbname="+self.DBName    
            CurrentConnection=psycopg2.connect(ConnectionStr)
            CurrentConnection.autocommit=True
            self.CurrentConnections.append(CurrentConnection)
            self.ActiveCursors.append(CurrentConnection.cursor(cursor_factory=psycopg2.extras.DictCursor))
        logging.info('Connection to DB is open...')
        self.ConnectionOpened=True
    
    def AutoRestartDBConnections(self):
        self.IncrementQueriesCount()
        if self.QueriesCount>=500:
           self.RestartConnection()
           self.QueriesCount=0
            
    def IncrementQueriesCount(self):
        if self.DBName!="postgres":
            self.QueriesCount=self.QueriesCount+1
    
    def RestartConnection(self):
        if self.DBName!="postgres" and self.ConnectionOpened==True:
            logging.info("Restarting DB Connections")
            self.CloseConnections()
            self.InitDBConnection(False)
        
    def CloseConnections(self): 
        if self.ConnectionOpened==True: 
            for i in range(0,self.serverscount):
                self.ActiveCursors[i].close()
                self.CurrentConnections[i].close()              
            self.ConnectionOpened=False       
   
    
    def GetServerID(self,TableName):
        SelectStm='select nodename from table_db_mapping where isactive=True and tablename=\''+TableName+'\';'
        Results=self.ExecuteQuerySQLStatment(SelectStm);
        if len(Results)>0:
            ServerIP=Results[0][0]
            for i in range(0,self.serverscount):
                if self.DBservers[i]['serverip']==ServerIP:
                    return i
            return -1
        else:
            return -1    
    
    def ExecuteNoQuerySQLStatment_On_AllServers(self,SQLStatment,SQLParamsDict={}):
        for i in range(0,self.serverscount):
            self.ExecuteNoQuerySQLStatment(SQLStatment,i,SQLParamsDict)
    
    def MapTableIDToServerIndex(self,TableID):
        return TableID%self.serverscount
    
    def ExecuteNoQuerySQLStatment(self,SQLStatment,DatabaseIndex=0,SQLParamsDict=None):
        try:
            #logging.info(SQLStatment)            
            self.AutoRestartDBConnections()
            SQLStatment=string.lower(SQLStatment)  
            if SQLParamsDict==None:
                self.ActiveCursors[DatabaseIndex].execute(SQLStatment)
            else:
                self.ActiveCursors[DatabaseIndex].execute(SQLStatment,SQLParamsDict)              
        except Exception as Exp:
            logging.info(SQLStatment)  
            logging.info(">>>>>Error While Executing NoQuery Statement On Server ("+str(DatabaseIndex)+")")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp)            
            logging.info("Current SQL Statement =\n"+SQLStatment)
            
            
    def ExecuteQuerySQLStatment(self,SQLStatment,DatabaseIndex=0,SQLParamsDict={}):
        
        try:
            #logging.info(SQLStatment)
            #logging.info(SQLParamsDict)
            
            self.AutoRestartDBConnections()           
            self.ActiveCursors[DatabaseIndex].execute(SQLStatment,SQLParamsDict)
            resultsList= self.ActiveCursors[DatabaseIndex].fetchall()           
            return resultsList
        except Exception as Exp:
            logging.info(SQLStatment)
            logging.info(SQLParamsDict)
            logging.info(">>>>>Error While Executing Query Statement On Server ("+str(DatabaseIndex)+")")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp)            
            logging.info("Current SQL Statement =\n"+SQLStatment)
                                    
        
        

            
        
    
    