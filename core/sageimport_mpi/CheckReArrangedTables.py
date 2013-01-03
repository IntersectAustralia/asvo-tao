import pg
import getpass
import math
import string
import sys
import settingReader
import numpy
import matplotlib.pyplot as plt
import time


class CheckReArrangedTrees(object):
    
    
    
    def __init__(self,CurrentSAGEStruct,Options):
        '''
        Constructor
        '''
        
        self.Options=Options
        self.serverip=self.Options['PGDB:serverip']
        self.username=self.Options['PGDB:user']
        self.password=self.Options['PGDB:password']
        self.port=int(self.Options['PGDB:port'])
        self.DBName=self.Options['PGDB:NewDBName']
        self.CurrentSAGEStruct=CurrentSAGEStruct
        if self.password==None:
            print('Password for user:'+self.username+' is not defined')
            self.password=getpass.getpass('Please enter password:')
        
        # Take care that the connection will be opened to standard DB 'master'
        # This is temp. until the actual database is created
        self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname=self.DBName)
        print('Connection to DB is open...Start Creating Tables')
        
        
    
    
    def CloseConnections(self):        
        self.CurrentConnection.close()       
        print('Connection to DB is Closed...')
    
    def ExecuteNoQuerySQLStatment(self,SQLStatment):
        try:           
            SQLStatment=string.lower(SQLStatment)  
            self.CurrentConnection.query(SQLStatment)              
        except Exception as Exp:
            print(">>>>>Error While creating New Table")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
    def ExecuteQuerySQLStatment(self,SQLStatment):
        try:            
            SQLStatment=string.lower(SQLStatment)
            resultsList=self.CurrentConnection.query(SQLStatment).getresult()            
            return resultsList  
        except Exception as Exp:
            print(">>>>>Error While creating New Table")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
    def GetTableRecordsCount(self,TableName):
        GetSummarySQL="select count(*)from @TABLEName;"
        GetSummarySQL= string.replace(GetSummarySQL,"@TABLEName",TableName)
        SummaryListArr=self.ExecuteQuerySQLStatment(GetSummarySQL)
        if len(SummaryListArr)==0:
            return
        FieldsCount=SummaryListArr[0][0]
        
        return int(FieldsCount)
    
    def CountGalaxies(self):
        GetTablesListSt="select table_name from information_schema.tables where table_schema='public' order by table_name;"
        TablesList=self.ExecuteQuerySQLStatment(GetTablesListSt)
        OriginalTablesCount=0
        ReArrangedTablesCount=0
        Count=0
        for Table in TablesList:
            TableName=Table[0]
            
            if string.find(TableName,self.Options['PGDB:TreeTablePrefix'])==0:                
                OriginalTablesCount=OriginalTablesCount+self.GetTableRecordsCount(TableName)                
            if string.find(TableName,self.Options['PGDB:ReArrangedTreeTablePrefix'])==0:                
                ReArrangedTablesCount=ReArrangedTablesCount+self.GetTableRecordsCount(TableName)
            
            print("Processing Table: "+TableName+ "\t "+str(Count)+"/"+str(len(TablesList))+"\t"+str(ReArrangedTablesCount)+"/"+str(OriginalTablesCount))    
                
            Count=Count+1    
                    
            
if __name__ == '__main__':
    
    
    
    
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml") 
    CheckReArrangedTreesObj=CheckReArrangedTrees(CurrentSAGEStruct,Options)
    
    CheckReArrangedTreesObj.CountGalaxies()
        
     
    CheckReArrangedTreesObj.CloseConnections()
        