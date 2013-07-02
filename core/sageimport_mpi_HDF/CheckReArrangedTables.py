import pg
import getpass
import math
import string
import sys
import settingReader
import numpy
import matplotlib.pyplot as plt
import time
import DBConnection
import logging


class CheckReArrangedTrees(object):
    
    
    
    def __init__(self,CurrentSAGEStruct,Options):
        '''
        Constructor
        '''
        
        self.Options=Options
        self.DBConnection=DBConnection.DBConnection(Options)
        self.CurrentSAGEStruct=CurrentSAGEStruct        
        
        # Take care that the connection will be opened to standard DB 'master'
        # This is temp. until the actual database is created
        
        logging.info('Connection to DB is open...Start Creating Tables')
        
        
    
    
    def CloseConnections(self):        
        self.DBConnection.close()       
        logging.info('Connection to DB is Closed...')
    
   
    def GetTableRecordsCount(self,TableName):
        GetSummarySQL="select count(*)from @TABLEName;"
        GetSummarySQL= string.replace(GetSummarySQL,"@TABLEName",TableName)
        SummaryListArr=self.DBConnection.ExecuteQuerySQLStatment(GetSummarySQL)
        if len(SummaryListArr)==0:
            return
        FieldsCount=SummaryListArr[0][0]
        
        return int(FieldsCount)
    
    def CountGalaxies(self):
        GetTablesListSt="select table_name from information_schema.tables where table_schema='public' order by table_name;"
        TablesList=self.DBConnection.ExecuteQuerySQLStatment(GetTablesListSt)
        OriginalTablesCount=0
        ReArrangedTablesCount=0
        Count=0
        for Table in TablesList:
            TableName=Table[0]
            
            if string.find(TableName,self.Options['PGDB:TreeTablePrefix'])==0:                
                OriginalTablesCount=OriginalTablesCount+self.GetTableRecordsCount(TableName)                
            if string.find(TableName,self.Options['PGDB:ReArrangedTreeTablePrefix'])==0:                
                ReArrangedTablesCount=ReArrangedTablesCount+self.GetTableRecordsCount(TableName)
            
            logging.info("Processing Table: "+TableName+ "\t "+str(Count)+"/"+str(len(TablesList))+"\t"+str(ReArrangedTablesCount)+"/"+str(OriginalTablesCount))    
                
            Count=Count+1    
                    
            
if __name__ == '__main__':
    
    
    logging.basicConfig(filename='log/CheckReArrangeTableslogfile.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
    
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml") 
    CheckReArrangedTreesObj=CheckReArrangedTrees(CurrentSAGEStruct,Options)
    
    CheckReArrangedTreesObj.CountGalaxies()
        
     
    CheckReArrangedTreesObj.CloseConnections()
        