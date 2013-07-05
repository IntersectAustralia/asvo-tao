
import string
import settingReader # Read the XML settings
import PGDBInterface # Interaction with the postgreSQL DB
import time
from decimal import Decimal
import DBConnection
import logging

class DataImportSpeed:    
        
    def __init__(self,Options,PGDB):
        self.Options=Options
        self.PGDB=PGDB
        
        
    def GetCurrentProcessedGalaxiesCount(self):
        StateSt="select sum(totalnumberofgalaxies) from datafiles where processed=true;"
        return self.PGDB.ExecuteQuerySQLStatment(StateSt)[0][0]
        
    
    def GetGalaxiesCount(self):
        StateSt="select sum(totalnumberofgalaxies) from datafiles"
        return self.PGDB.ExecuteQuerySQLStatment(StateSt)[0][0]
        
        
        
if __name__ == '__main__':
    logging.basicConfig(filename='log/DataImportSpeed.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
    
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml")
    CurrentPGDB=DBConnection.DBConnection(Options)
    DataImportSpeedObj=DataImportSpeed(Options,CurrentPGDB)
    InitialValue=DataImportSpeedObj.GetCurrentProcessedGalaxiesCount()
    TotalGalaxies=DataImportSpeedObj.GetGalaxiesCount()
    
    STime=time.time() 
    
    try:
        
        while (True):
            time.sleep(10)            
            CurrentValue=DataImportSpeedObj.GetCurrentProcessedGalaxiesCount()
            CTime= time.time()
            logging.info (str(STime)+"/"+str(CTime))
            Elapsed=CTime-STime
            logging.info("Total Imported="+str(CurrentValue)+"/"+str(TotalGalaxies)+"="+str(((CurrentValue*Decimal(100.0))/TotalGalaxies))+"%")
            
            logging.info("Imported from Start="+str(CurrentValue-InitialValue)+"\tElapsed="+str(Elapsed)+" seconds")      
            logging.info("Current Speed ="+str(int((CurrentValue-InitialValue)/Decimal(Elapsed)))+" Record/Second")
            
    except Exception as Exp:
        logging.info(Exp)
        CurrentPGDB.CloseConnections()