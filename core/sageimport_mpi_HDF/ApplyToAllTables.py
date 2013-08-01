import pg
import getpass
import math
import string
import sys
import settingReader
import numpy
import matplotlib.pyplot as plt
import DBConnection
import logging

class ProcessTables(object):
    
    def __init__(self,Options):
        '''
        Constructor
        '''
        self.Options=Options
        self.DBConnection=DBConnection.DBConnection(Options)        
        logging.info('Connection to DB is open...')     
        
    
    
    def CloseConnections(self):        
        self.DBConnection.CloseConnections()       
        logging.info('Connection to DB is Closed...')
    
  
            
    def ApplyQueryToTable(self,TableName,ServerIndex):
        logging.info(TableName)
        SQLStat="INSERT INTO GalaxyMapping SELECT globalindex,'@TABLENAME' from @TABLENAME;"        
        SQLStat= string.replace(SQLStat,"@TABLENAME",TableName)        
        self.DBConnection.ExecuteNoQuerySQLStatment(SQLStat,ServerIndex)
    
        
        
    def ExecuteQueries(self,ServerIndex):
        
        CreateSQLSt="DROP TABLE IF EXISTS GalaxyMapping; CREATE Table GalaxyMapping (globalindex bigint,tablename varchar(500));"
        self.DBConnection.ExecuteNoQuerySQLStatment(CreateSQLSt,ServerIndex)
        
        
        GetTablesListSt="select table_name from information_schema.tables where table_schema='public';"
        TablesList=self.DBConnection.ExecuteQuerySQLStatment(GetTablesListSt,ServerIndex)                
        for Table in TablesList:
            TableName=Table[0]
            if string.find(TableName,self.Options['PGDB:TreeTablePrefix'])==0:
                self.ApplyQueryToTable(TableName,ServerIndex)
                
        CreateSQLSt="ALTER TABLE GalaxyMapping ADD PRIMARY KEY (globalindex); "
        self.DBConnection.ExecuteNoQuerySQLStatment(CreateSQLSt,ServerIndex)       
                 
if __name__ == '__main__':
    logging.basicConfig(filename='ApplytoAllTables.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
    logging.info('Starting DB processing')
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml") 
    ProcessTablesObj=ProcessTables(Options)    
    for i in range(0,int(Options['PGDB:ServersCount'])):        
        ProcessTablesObj.ExecuteQueries(i)
    
                  
        
        
        
        
         