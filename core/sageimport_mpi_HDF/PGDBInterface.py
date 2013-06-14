'''
Created on 01/10/2012
@author: Amr Hassan
'''
import psycopg2
from psycopg2 import extras
import math
import string
import sys
import DBConnection
import logging
from cStringIO import StringIO


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
        
        self.PrepareFieldsList()                       
        
        
        self.CurrentGalaxiesCounter=int(Options['RunningSettings:GalaxiesPerTable'])+1 # To Create the First Table
    
    
            
        
    
    
    def PrepareFieldsList(self):
        self.FieldsName=[]
        
                   
        for field in self.CurrentSAGEStruct:                            
            self.FieldsName.append(field[2])            
            
        self.FieldsName.append("GlobalTreeID")
        self.FieldsName.append("CentralGalaxyGlobalID")
        self.FieldsName.append("LocalGalaxyID")
             
    
        
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
        
        
        try:
            cpyData = StringIO()            
            TablePrefix=self.Options['PGDB:TreeTablePrefix']
            NewTableName=TablePrefix+str(TableID)            
            HostIndex=self.DBConnection.MapTableIDToServerIndex(TableID)          
            
            
            for TreeField in TreeData:
                    
                FieldData=[]
                
                for field in self.CurrentSAGEStruct:                                    
                        FieldName=field[0]                        
                        FieldData.append(TreeField[FieldName])
                
                FieldData.append(TreeField['TreeID'])
                FieldData.append(TreeField['CentralGalaxyGlobalID'])                
                FieldData.append(self.LocalGalaxyID)
                
                
                self.LocalGalaxyID=self.LocalGalaxyID+1
                 
                DataStr=';'.join([str(x) for x in FieldData]) + '\n'                   
                cpyData.write(DataStr)
            
            cpyData.seek(0)
            self.DBConnection.ActiveCursors[HostIndex].copy_from(cpyData, NewTableName, sep=';', columns=self.FieldsName)
            
        except Exception as Exp:
            logging.info(">>>>>Error While Processing Tree")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp)            
            raw_input("PLease press enter to continue.....")
            
                
   
            
        