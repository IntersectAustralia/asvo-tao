
import string
import sys # for listing directory contents
import settingReader # Read the XML settings

import DBConnection
import logging
import h5py 

class MasterTablesUpdate:    
        
    def __init__(self,Options,PGDB):
        self.Options=Options
        self.DBConnection=DBConnection.DBConnection(Options)
        self.CurrentH5InputFile=Options['RunningSettings:InputFile']
        self.InputFile=h5py.File(self.CurrentH5InputFile,'r')
    def CreateRedshiftTable(self):
        CreatTBSt="CREATE TABLE Snap_redshift (SnapNum Int4,redshift float4);"
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(CreatTBSt)
    def CreateMetadataTable(self):
        CreatTBSt="CREATE TABLE metadata (Metakey varchar(500),MetaValue varchar(5000));"        
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(CreatTBSt)
    
    def AddMetaDataValue(self,Key,Value):
        InsertVSt="INSERT  INTO metadata values ('"+str(Key)+"','"+str(Value)+"');"        
        self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(InsertVSt)
        
    def FillMetadataTable(self):
        self.AddMetaDataValue("BoxSize", self.Options['RunningSettings:SimulationBoxX'])
        self.AddMetaDataValue("BSPCellSize", self.Options['RunningSettings:BSPCellSize'])
        self.AddMetaDataValue("TreeTablePrefix", self.Options['PGDB:TreeTablePrefix'])
        for item in self.InputFile['cosmology']:            
            self.AddMetaDataValue(str(item), str(self.InputFile['cosmology'][item][0]))
        
            
    def FillRedshiftData(self):        
        
        RedShifList=self.InputFile['snapshot_redshifts']        
        for i in range(0,len(RedShifList)):
               CurrentSnapNum=i
               logging.info(str(CurrentSnapNum)+":"+str(RedShifList[i]))
               InsertSt="INSERT INTO Snap_redshift Values ("+str(CurrentSnapNum)+","+str(RedShifList[i])+");"
               
               self.DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(InsertSt)
    
        
        
        
#if __name__ == '__main__':
#    [CurrentSAGEStruct,Options]=settingReader.ParseParams("importsetting/mill_mini_2servers_setting.xml")
    #CurrentPGDB=PGDBInterface.DBInterface(CurrentSAGEStruct,Options,0)
#    MasterTablesUpdateObj=MasterTablesUpdate(Options,[])
#    MasterTablesUpdateObj.CreateMetadataTable()
#    MasterTablesUpdateObj.FillMetadataTable()
#    MasterTablesUpdateObj.CreateRedshiftTable()
#    MasterTablesUpdateObj.FillRedshiftData()