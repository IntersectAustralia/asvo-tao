import pickle, os, logging,string
import pg
import locale
import time
from datetime import date
import logging
import settingReader
class DBInterface(object): 
    
    def __init__(self,Options):        
        
        self.Options=Options          
        self.InitDBConnection(self.Options)
        self.IsOpen=False
        self.QueriesCount=0
        
    def InitDBConnection(self,Options):
        
        ####### PostgreSQL Backend Master DB ################# 
        self.serverip=Options['PGDB:serverip']
        self.username=Options['PGDB:user']
        self.password=Options['PGDB:password']
        self.port=int(Options['PGDB:port'])
        self.DBName=Options['PGDB:NewDBName']    
               
        
        self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname=self.DBName)
        print('Connection to DB is open...')    
        self.IsOpen=True
        
    def CloseConnections(self):  
        if self.IsOpen==True:      
            self.CurrentConnection.close()        
            print('Connection to DB is Closed...')
            self.IsOpen=False
                
    def ExecuteNoQuerySQLStatment(self,SQLStatment):
        try:
                      
            self.CurrentConnection.query(SQLStatment)  
            return True            
        except Exception as Exp:
            print(">>>>>Error While Executing Non-Query SQL Statement")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            return False
            
    def ExecuteQuerySQLStatment(self,SQLStatment):
        try: 
                                
            resultsList=self.CurrentConnection.query(SQLStatment).getresult()           
            return resultsList  
        except Exception as Exp:
            print(">>>>>Error While Executing Query SQL Statement")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            
    def ExecuteQuerySQLStatmentAsDict(self,SQLStatment):
        try:
            
                    
            resultsList=self.CurrentConnection.query(SQLStatment).dictresult()           
            return resultsList  
        except Exception as Exp:
            print(">>>>>Error While Executing Query SQL Statement")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)


if __name__ == '__main__':
    [Options]=settingReader.ParseParams("settings.xml")
    DBConnectionObj=DBInterface(Options)
    DBConnectionObj.CloseConnections()