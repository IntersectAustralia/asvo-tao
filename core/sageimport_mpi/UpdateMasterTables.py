
import string
import sys # for listing directory contents
import settingReader # Read the XML settings
import PGDBInterface # Interaction with the postgreSQL DB

class MasterTablesUpdate:    
        
    def __init__(self,Options,PGDB):
        self.Options=Options
        self.PGDB=PGDB
    def CreateRedshiftTable(self):
        CreatTBSt="CREATE TABLE Snap_redshift (SnapNum Int4,redshift float4);"
        self.PGDB.ExecuteNoQuerySQLStatment(CreatTBSt)
        
    def FillRedshiftData(self):
        SnapshotFile=self.Options['RunningSettings:SnpshottoRedshiftMapping']
        f = open(SnapshotFile, 'rt')
        RedShifList=[]
        for line in f:
            RedShifList.append(round((1/float(line))-1,2))
        
        for i in range(0,len(RedShifList)):
               CurrentSnapNum=i
               print(str(CurrentSnapNum)+":"+str(RedShifList[i]))
               InsertSt="INSERT INTO Snap_redshift Values ("+str(CurrentSnapNum)+","+str(RedShifList[i])+");"
               self.PGDB.ExecuteNoQuerySQLStatment(InsertSt)
    
        
        
        
if __name__ == '__main__':
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml")
    CurrentPGDB=PGDBInterface.DBInterface(CurrentSAGEStruct,Options)
    MasterTablesUpdateObj=MasterTablesUpdate(Options,CurrentPGDB)
    MasterTablesUpdateObj.CreateRedshiftTable()
    MasterTablesUpdateObj.FillRedshiftData()