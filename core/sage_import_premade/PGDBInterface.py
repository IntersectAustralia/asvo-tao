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
from io import BytesIO
import numpy
import struct
import traceback

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
    
             
    
        
    def CloseConnections(self):        
        self.DBConnection.CloseConnections()
        
                
           
            
    
  
    def GetListofUnProcessedTrees(self,CommSize,CommRank):
        return self.DBConnection.ExecuteQuerySQLStatment("SELECT * FROM TreeProcessingSummary where Processed=FALSE and mod(LoadingTreeID,"+str(CommSize)+")="+str(CommRank)+" order by LoadingTreeID;")        
    
    def SetTreeAsProcessed(self,TreeID):
        self.DBConnection.ExecuteNoQuerySQLStatment("UPDATE TreeProcessingSummary set Processed=TRUE where LoadingTreeID= "+str(TreeID))
    
        
    
        
        
    
    def CreateNewTree(self,TableID,TreeData):
        # TreeData Must be a numpy fields array with the correct format for postgresql
        
        try:
            cpyData = BytesIO()            
            TablePrefix=self.Options['PGDB:TreeTablePrefix']
            NewTableName=TablePrefix+str(TableID)            
            HostIndex=self.DBConnection.MapTableIDToServerIndex(TableID)          
            
            
            cpyData.write(struct.pack('!11sii', b'PGCOPY\n\377\r\n\0', 0, 0))
            cpyData.write(TreeData.tostring())
            cpyData.write(struct.pack('!h', -1))  # file trailer    
            logging.info("Start Copying Data....")
            cpyData.seek(0)
            self.DBConnection.ActiveCursors[HostIndex].copy_expert('COPY '+NewTableName+' FROM STDIN WITH BINARY', cpyData)       
            logging.info("Adding "+str(len(TreeData))+" Galaxies to Table"+str(TableID))
        except Exception as Exp:
            logging.info(">>>>>Error While Processing Tree")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp)  
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logging.error(''.join('!! ' + line for line in lines))          
            raw_input("PLease press enter to continue.....")
            
                
   
            
        