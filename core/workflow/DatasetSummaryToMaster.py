import psycopg2
from psycopg2 import extras
import xml.etree.ElementTree as ET
import logging
import string

class ParseProfileData(object):

    

    def __init__(self,XMLFileName):        
        self.ParseXML(XMLFileName)
        self.InitDBConnection()
        self.InsertSummaryRecord="INSERT INTO tablessummary ("
        self.InsertSummaryRecord=self.InsertSummaryRecord+"tablename, databasename,serverip,galaxycount,treecount,mingalaxypertable,maxgalaxypertable) "        
        self.InsertSummaryRecord=self.InsertSummaryRecord+"Values (%s,%s,%s,%s,%s,%s,%s)"
        
        
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
        
        masterNode=SettingsNode[1]      
        
        self.Options[masterNode.tag+':serverip']= masterNode.findall('serverip')[0].text
        self.Options[masterNode.tag+':port']= masterNode.findall('port')[0].text
        self.Options[masterNode.tag+':user']= masterNode.findall('user')[0].text
        self.Options[masterNode.tag+':password']= masterNode.findall('password')[0].text  
        self.Options[masterNode.tag+':DBName']= masterNode.findall('DBName')[0].text 
        
        
        
        
        
    def ProcessTables(self,ServerID):
        
        GetTablesListSt="select table_name from information_schema.tables where table_schema='public' order by table_name;"
        self.ActiveCursors[ServerID].execute(GetTablesListSt)
        TablesList= self.ActiveCursors[ServerID].fetchall()           
        
        Count=0
        for Table in TablesList:
            TableName=Table[0]
            
            if string.find(TableName,self.Options['PGDB:TreeTablePrefix'])==0:
                print(str(ServerID)+":Processing Table: "+TableName+ "\t "+str(Count)+"/"+str(len(TablesList)))
                self.GetTableSummary(TableName,ServerID)                
            Count=Count+1
            
    def GetTableSummary(self,TableName,ServerIndex):
        
        GetSummarySQL="select count(*),count(Distinct treeindex) from @TABLEName;"
        GetSummarySQL= string.replace(GetSummarySQL,"@TABLEName",TableName)        
        self.ActiveCursors[ServerIndex].execute(GetSummarySQL)
        SummaryListArr= self.ActiveCursors[ServerIndex].fetchall() 
        
        
        GetSummarySQL="select treeindex,count(*) from @TABLEName group by treeindex;"
        GetSummarySQL= string.replace(GetSummarySQL,"@TABLEName",TableName)        
        self.ActiveCursors[ServerIndex].execute(GetSummarySQL)
        TreeSummaryListArr= self.ActiveCursors[ServerIndex].fetchall() 
        MaxGCount=0;
        MinGCount=9999;
        for TreeSummary in TreeSummaryListArr:
            MaxGCount=max(MaxGCount,TreeSummary[1])  
            MinGCount=min(MinGCount,TreeSummary[1])          
        
        if len(SummaryListArr)==0:
            return
        SummaryList=SummaryListArr[0]
        
        if SummaryList[0]==None:
            return
        
        GalaxyCount=SummaryList[0]
        TreeCount=SummaryList[1]
        serverip=self.Options['PGDB:serverInfo'+str(ServerIndex)+':serverip']
        dbname=self.Options['PGDB:DBName']
        Params=(TableName,dbname,serverip,GalaxyCount,TreeCount,MinGCount,MaxGCount)
        
        self.MasterCursor.execute(self.InsertSummaryRecord,Params)      
        
        
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
                     
        
        
        ConnectionStr="host="+self.Options['master:serverip']+" user="+self.Options['master:user']+" password="+self.Options['master:password']+" port="+str(self.Options['master:port'])+" dbname="+self.Options['master:DBName']     
        self.MasterDBConnection=psycopg2.connect(ConnectionStr)
        self.MasterDBConnection.autocommit=True
        self.MasterCursor=self.MasterDBConnection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        print('Connection to DB is open...')
        self.ConnectionOpened=True

if __name__ == '__main__':
     ParseProfileDataObj=ParseProfileData("summarygeneration.xml")
     for i in range(0,ParseProfileDataObj.serverscount):
         ParseProfileDataObj.ProcessTables(i)