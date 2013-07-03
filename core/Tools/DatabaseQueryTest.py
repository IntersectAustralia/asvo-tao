from mpi4py import MPI # MPI Implementation
import psycopg2
from psycopg2 import extras
import xml.etree.ElementTree as ET
import logging
import string,sys
import time,os

class TestClass(object): 
    
    def __init__(self,XMLFileName):
        self.ParseXML(XMLFileName)
        self.InitDBConnection()
        #self.InsertSummaryRecord="INSERT INTO tablessummary ("
        #self.InsertSummaryRecord=self.InsertSummaryRecord+"tablename, databasename,serverip,galaxycount,treecount,mingalaxypertable,maxgalaxypertable) "
        #self.InsertSummaryRecord=self.InsertSummaryRecord+"Values (%s,%s,%s,%s,%s,%s,%s)"
    
    def ParseXML(self,XMLSetting):
            self.Options=dict()
            
            tree = ET.ElementTree(file=XMLSetting)
            SettingsNode = tree.getroot()
            
            
            pgNode=SettingsNode[0]
            self.Options[pgNode.tag+':TreeTablePrefix']= pgNode.findall('TreeTablePrefix')[0].text
            self.Options[pgNode.tag+':DBName']= pgNode.findall('DBName')[0].text
            self.Options[pgNode.tag+':DBAlias']= pgNode.findall('DBAlias')[0].text
            self.Options[pgNode.tag+':ServersCount']= pgNode.findall('ServersCount')[0].text
            
            serversList=pgNode.findall('serverInfo')
            ServerIndex=0
            for pgfield in serversList:
               for pgserverinfo in pgfield:
                   self.Options[pgNode.tag+':'+pgfield.tag+str(ServerIndex)+":"+pgserverinfo.tag]= pgserverinfo.text
               ServerIndex=ServerIndex+1           
            
    
    def CloseConnections(self):
            if self.ConnectionOpened==True:
                for i in range(0,self.serverscount):
                    self.ActiveCursors[i].close()
                    self.CurrentConnections[i].close()
                self.ConnectionOpened=False
                
    def InitDBConnection(self):
        
        ####### PostgreSQL Simulation DB #################
        self.serverscount=int(self.Options['PGDB:ServersCount'])
        self.DBName=self.Options['PGDB:DBName']
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
                     
        
        
        
        print('Connection to DB is open...')
        self.ConnectionOpened=True
    def RunTest(self,TableName,ServerID):
        
        logging.info('Start Test')
        start= time.clock()
        GetTablesListSt="select count(Distinct treeindex) from "+TableName+";"
        self.ActiveCursors[ServerID].execute(GetTablesListSt)
        TablesList= self.ActiveCursors[ServerID].fetchall() 
        
        end= time.clock()
        print(str(CommRank)+": Total Processing Time="+str((end-start))+" seconds")
        logging.info('End Test')









def SetupLogFile(CommRank):
    FilePath='log/logfile'+str(CommRank)+'.log'
    if os.path.exists(FilePath):
        os.remove(FilePath)
    logging.basicConfig(filename=FilePath,level=logging.DEBUG,format='%(asctime)s %(message)s')





if __name__ == '__main__':  
    
    TableName='tree_169'#sys.argv[1]  
    ServerID=1#int(sys.argv[1])
      
    
    
      
    comm = MPI.COMM_WORLD
    CommRank = comm.Get_rank()
    
    CommSize= comm.Get_size()
    
    
    SetupLogFile(CommRank)
    
    logging.info('Starting Database Testing tool')
    TestClassObj=TestClass("setting.xml")
    
    TestClassObj.RunTest(TableName,ServerID)
    
    TestClassObj.CloseConnections()  
    
    
    
    logging.info('End Database Testing tool')
    
    