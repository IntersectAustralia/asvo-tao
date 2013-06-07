'''
Created on 01/10/2012
@author: Amr Hassan
'''
import pg
import getpass
import math
import string
import sys
import DBConnection
import logging

class DBInterface(object):
    '''
    This class will handle the interface with the DB
    '''
    FormatMapping={'int':'INT',
                   'float':'FLOAT',
                   'long long':'BIGINT'                   
                   }
    
    
    
    
    DebugToFile=False
    
    def __init__(self,CurrentSAGEStruct,Options,CommRank):
        '''
        Constructor
        '''
        self.Options=Options
        self.Log = open(self.Options['RunningSettings:OutputDir']+'DBCreation_sql'+str(CommRank)+'.txt', 'wt')
        
        self.CurrentSAGEStruct=CurrentSAGEStruct
        
        self.DBConnection=DBConnection.DBConnection(Options)
        
        self.CreateInsertTemplate()                       
        
        
        self.CurrentGalaxiesCounter=int(Options['RunningSettings:GalaxiesPerTable'])+1 # To Create the First Table
    
    
            
        
    
    
    def CreateInsertTemplate(self):
        self.INSERTTemplate="INSERT INTO @TABLEName ("           
        for field in self.CurrentSAGEStruct:
            if field[3]==1:                
                FieldName=field[2]
                self.INSERTTemplate=self.INSERTTemplate+ FieldName+","
        self.INSERTTemplate=self.INSERTTemplate+"GlobalTreeID," 
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyGlobalID,"
        self.INSERTTemplate=self.INSERTTemplate+"LocalGalaxyID,"
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyX,"
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyY,"
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyZ)"
    
    
    def CloseConnections(self):        
        self.DBConnection.CloseConnections()
        self.CloseDebugFile()
                
           
            
    
  
    def GetListofUnProcessedFiles(self,CommSize,CommRank):
        return self.DBConnection.ExecuteQuerySQLStatment("SELECT * FROM datafiles where Processed=FALSE and fileid%"+str(CommSize)+"="+str(CommRank)+" order by fileid;")        
    
    def SetFileAsProcessed(self,FileID):
        self.DBConnection.ExecuteNoQuerySQLStatment("UPDATE datafiles set Processed=TRUE where fileid= "+str(FileID))
    
        
                
    def StartTransaction(self):
        self.DBConnection.StartTransaction()
    def CommitTransaction(self):
        self.DBConnection.CommitTransaction()
        
    def CreateNewTree(self,TableID,TreeData):
        
        self.LocalGalaxyID=0
        
          
        if len(TreeData)>1000:
            for c in range(0,(len(TreeData)/1000)+1):
                start=c*1000
                end=min((c+1)*1000,len(TreeData))
                #sys.stdout.write("\033[0;33m"+str(start)+":"+str(end)+" from "+str(len(TreeData))+"\033[0m\r")
                #sys.stdout.flush()
                if start!=end:                    
                    self.PrepareInsertStatement(TableID,TreeData[start:end])
        else:            
            self.PrepareInsertStatement(TableID,TreeData) 
               
        
        self.CurrentGalaxiesCounter=self.CurrentGalaxiesCounter+len(TreeData)
        
        logging.info("Adding "+str(len(TreeData))+" Galaxies to Table"+str(TableID))
        
    
    def PrepareInsertStatement(self,TableID,TreeData):
        InsertStatment=""
        
        try:            
            TablePrefix=self.Options['PGDB:TreeTablePrefix']
            NewTableName=TablePrefix+str(TableID)
            InsertStatment= string.replace(self.INSERTTemplate,"@TABLEName",NewTableName)
            InsertStatment=InsertStatment+" VALUES "            
            
            
            for TreeField in TreeData:
                    
                InsertStatment=InsertStatment+"("
                for field in self.CurrentSAGEStruct:                
                    if field[3]==1:                
                        FieldName=field[0]
                        InsertStatment=InsertStatment+ str(TreeField[FieldName])+","
                
                InsertStatment=InsertStatment+str(TreeField['TreeID'])+","
                InsertStatment=InsertStatment+str(TreeField['CentralGalaxyGlobalID'])+","                
                InsertStatment=InsertStatment+str(self.LocalGalaxyID)+","
                
                InsertStatment=InsertStatment+str(TreeField['CentralGalaxyX'])+","
                InsertStatment=InsertStatment+str(TreeField['CentralGalaxyY'])+","
                InsertStatment=InsertStatment+str(TreeField['CentralGalaxyZ'])+"),"
                self.LocalGalaxyID=self.LocalGalaxyID+1
                
            InsertStatment=InsertStatment[:-1]+";"
            
            
            if self.DebugToFile==True:
                self.Log.write(InsertStatment+"\n\n")
                self.Log.flush()
            HostIndex=self.DBConnection.MapTableIDToServerIndex(TableID)    
            
            self.DBConnection.ExecuteNoQuerySQLStatment(InsertStatment,HostIndex)
            
        except Exception as Exp:
            logging.info(">>>>>Error While Processing Tree")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp)            
            logging.info("Current SQL Statement =\n"+InsertStatment)
            raw_input("PLease press enter to continue.....")
            
                
    def CloseDebugFile(self):        
        if self.DebugToFile==True and self.Log!=None:
            self.Log.close()
            
        