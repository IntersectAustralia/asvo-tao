
import string
import sys # for listing directory contents
import settingReader # Read the XML settings

import DBConnection
import logging

class MasterTablesUpdate:    
        
    def __init__(self,Options,PGDB):
        self.Options=Options
        self.DBConnection=DBConnection.DBConnection(Options)
    def CreateRedshiftTable(self):
        CreatTBSt="CREATE TABLE Snap_redshift (SnapNum Int4,redshift float4);"
        self.DBConnection.ExecuteNoQuerySQLStatment(CreatTBSt)
    def CreateMetadataTable(self):
        CreatTBSt="CREATE TABLE metadata (Metakey varchar(500),MetaValue varchar(5000));"        
        self.DBConnection.ExecuteNoQuerySQLStatment(CreatTBSt)
    
    def AddMetaDataValue(self,Key,Value):
        InsertVSt="INSERT  INTO metadata values ('"+str(Key)+"','"+str(Value)+"');"        
        self.DBConnection.ExecuteNoQuerySQLStatment(InsertVSt)
        
    def FillMetadataTable(self):
        self.AddMetaDataValue("BoxSize", self.Options['RunningSettings:SimulationBoxX'])
        self.AddMetaDataValue("BSPCellSize", self.Options['RunningSettings:BSPCellSize'])
        self.AddMetaDataValue("TreeTablePrefix", self.Options['PGDB:TreeTablePrefix'])
        
        
            
    def FillRedshiftData(self):
        SnapshotFile=self.Options['RunningSettings:SnpshottoRedshiftMapping']
        f = open(SnapshotFile, 'rt')
        RedShifList=[]
        for line in f:
            RedShifList.append(round((1/float(line))-1,2))
        
        for i in range(0,len(RedShifList)):
               CurrentSnapNum=i
               logging.info(str(CurrentSnapNum)+":"+str(RedShifList[i]))
               InsertSt="INSERT INTO Snap_redshift Values ("+str(CurrentSnapNum)+","+str(RedShifList[i])+");"
               self.DBConnection.ExecuteNoQuerySQLStatment(InsertSt)
    
        
        
        
#if __name__ == '__main__':
#    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml")
#    CurrentPGDB=PGDBInterface.DBInterface(CurrentSAGEStruct,Options,0)
#    MasterTablesUpdateObj=MasterTablesUpdate(Options,CurrentPGDB)
#    MasterTablesUpdateObj.CreateMetadataTable()
#    MasterTablesUpdateObj.FillMetadataTable()
#    MasterTablesUpdateObj.CreateRedshiftTable()
#    MasterTablesUpdateObj.FillRedshiftData()