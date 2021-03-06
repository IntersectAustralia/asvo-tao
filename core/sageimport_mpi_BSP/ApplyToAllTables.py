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
        self.DBConnection.close()       
        logging.info('Connection to DB is Closed...')
    
        
    
   
  
    
  
            
    def ApplyQueryToTable(self,TableName):
        logging.info(TableName)
        ALTERSQL=" ALTER TABLE @TABLENAME ALTER COLUMN centralmvir TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN posx TYPE FLOAT4"
        ALTERSQL=ALTERSQL+" , ALTER COLUMN posy TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN posz TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN velx TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN vely TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN velz TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN spinx TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN spiny TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN spinz TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN mvir TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN rvir TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN vvir TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN vmax TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN veldisp TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN coldgas TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , logging.infoALTER COLUMN stellarmass TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN bulgemass TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN hotgas TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN ejectedmass TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN blackholemass TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN ics TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN metalscoldgas TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN metalsstellarmass TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN metalsbulgemass TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN metalshotgas TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN metalsejectedmass TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN metalsics TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN sfr TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN sfrbulge TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN sfrics TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN diskscaleradius TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN cooling TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN heating TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN centralgalaxyx TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN centralgalaxyy TYPE FLOAT4 "
        ALTERSQL=ALTERSQL+" , ALTER COLUMN centralgalaxyz TYPE FLOAT4; "
        ALTERSQL= string.replace(ALTERSQL,"@TABLENAME",TableName)
        
        self.DBConnection.ExecuteNoQuerySQLStatment(ALTERSQL)
    
        
        
    def GetTablesList(self):
        
        GetTablesListSt="select table_name from information_schema.tables where table_schema='public';"
        TablesList=self.DBConnection.ExecuteQuerySQLStatment(GetTablesListSt)
        StartIndex=int(raw_input("From Which Index Should I start?"))
        for Table in TablesList[StartIndex:]:
            TableName=Table[0]
            if string.find(TableName,self.Options['PGDB:TreeTablePrefix'])==0:
                self.ApplyQueryToTable(TableName)
                
                 
if __name__ == '__main__':
    logging.basicConfig(filename='log/ApplytoAllTables.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
    logging.info('Starting DB processing')
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml") 
    ProcessTablesObj=ProcessTables(Options)
    ProcessTablesObj.GetTablesList()
    
                  
        
        
        
        
         