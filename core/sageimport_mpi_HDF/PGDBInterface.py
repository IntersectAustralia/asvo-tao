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
from io import StringIO


class DBInterface(object):
    '''
    This class will handle the interface with the DB
    '''
    FormatMapping={'int':'INT',
                   'float':'FLOAT',
                   'long long':'BIGINT'                   
                   }
    
    
    
    
   
    def __init__(self,CurrentSAGEStruct,Options,CommRank):
        '''
        Constructor
        '''
        self.Options=Options
        
        
        self.CurrentSAGEStruct=CurrentSAGEStruct
        
        self.DBConnection=DBConnection.DBConnection(Options)
        
        self.CreateInsertTemplate()                       
        
        
        self.CurrentGalaxiesCounter=int(Options['RunningSettings:GalaxiesPerTable'])+1 # To Create the First Table
    
    
            
        
    
    
    def CreateInsertTemplate(self):
        Values=" values ("
        self.INSERTTemplate="INSERT INTO @TABLEName ("           
        for field in self.CurrentSAGEStruct:                            
            FieldName=field[2]
            self.INSERTTemplate=self.INSERTTemplate+ FieldName+","
            Values=Values+"%s,"
        self.INSERTTemplate=self.INSERTTemplate+"GlobalTreeID," 
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyGlobalID,"
        self.INSERTTemplate=self.INSERTTemplate+"LocalGalaxyID,"
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyX,"
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyY,"
        self.INSERTTemplate=self.INSERTTemplate+"CentralGalaxyZ)"
        Values=Values+"%s,%s,%s,%s,%s,%s)"
        self.INSERTTemplate=self.INSERTTemplate+Values
    
        print self.INSERTTemplate
    def CloseConnections(self):        
        self.DBConnection.CloseConnections()
        
                
           
            
    
  
    def GetListofUnProcessedTrees(self,CommSize,CommRank):
        return self.DBConnection.ExecuteQuerySQLStatment("SELECT * FROM TreeProcessingSummary where Processed=FALSE and mod(LoadingTreeID,"+str(CommSize)+")="+str(CommRank)+" order by LoadingTreeID;")        
    
    def SetTreeAsProcessed(self,TreeID):
        self.DBConnection.ExecuteNoQuerySQLStatment("UPDATE TreeProcessingSummary set Processed=TRUE where LoadingTreeID= "+str(TreeID))
    
        
   
        
    def CreateNewTree(self,TableID,TreeData):
        
        self.LocalGalaxyID=0
        
          
        if len(TreeData)>1000:
            for c in range(0,(len(TreeData)/1000)+1):
                start=c*1000
                end=min((c+1)*1000,len(TreeData))                
                if start!=end:                    
                    self.InsertData(TableID,TreeData[start:end])
        else:            
            self.InsertData(TableID,TreeData) 
               
        
        self.CurrentGalaxiesCounter=self.CurrentGalaxiesCounter+len(TreeData)
        
        logging.info("Adding "+str(len(TreeData))+" Galaxies to Table"+str(TableID))
        
    
    def InsertData(self,TableID,TreeData):
        cpyData = StringIO()
        
        try:            
            TablePrefix=self.Options['PGDB:TreeTablePrefix']
            NewTableName=TablePrefix+str(TableID)
            InsertStatment= string.replace(self.INSERTTemplate,"@TABLEName",NewTableName)
            HostIndex=self.DBConnection.MapTableIDToServerIndex(TableID)          
            
            
            for TreeField in TreeData:
                    
                FieldData=[]
                for field in self.CurrentSAGEStruct:                
                    if field[3]==1:                
                        FieldName=field[0]
                        FieldData.append(TreeField[FieldName])
                
                FieldData.append(TreeField['TreeID'])
                FieldData.append(TreeField['CentralGalaxyGlobalID'])                
                FieldData.append(self.LocalGalaxyID)
                
                FieldData.append(TreeField['CentralGalaxyX'])
                FieldData.append(TreeField['CentralGalaxyY'])
                FieldData.append(TreeField['CentralGalaxyZ'])
                self.LocalGalaxyID=self.LocalGalaxyID+1
               
                cpyData.write('\t'.join([repr(x) for x in FieldData]) + '\n')
                
           
            
            
           
                
            
            self.DBConnection.ExecuteNoQuerySQLStatment(InsertStatment,HostIndex)
            
        except Exception as Exp:
            logging.info(">>>>>Error While Processing Tree")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp)            
            logging.info("Current SQL Statement =\n"+InsertStatment)
            raw_input("PLease press enter to continue.....")
            
                
   
            
        