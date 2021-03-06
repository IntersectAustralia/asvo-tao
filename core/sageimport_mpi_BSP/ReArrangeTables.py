import DBConnection
import getpass
import math
import string
import sys
import settingReader
import numpy
import matplotlib.pyplot as plt
import time
from mpi4py import MPI # MPI Implementation
import logging

class ReArrangeTrees(object):
    
    FormatMapping={'int':'INT','float':'FLOAT4','long long':'BIGINT'}
    
    
    def __init__(self,CommRank,CurrentSAGEStruct,Options):
        '''
        Constructor
        '''
        self.CommRank=CommRank
        self.Options=Options
        self.DBConnection=DBConnection.DBConnection(Options)
        self.CurrentSAGEStruct=CurrentSAGEStruct
        
        logging.info('Connection to DB is open...Start Creating Tables')
        self.CreateNewTableTemplate()
        
    
    
    def CloseConnections(self):        
        self.DBConnection.close()       
        logging.info('Connection to DB is Closed...')
    
             
    def GetGridLimits(self):
        TreeMappingSt="select min(gridx),min(gridy),max(gridx),max(gridy) from treemapping;"
        MappingLimits=self.DBConnection.ExecuteQuerySQLStatment(TreeMappingSt)[0]
        
        
        
        
        MinX=MappingLimits[0]
        MinY=MappingLimits[1]
        
        MaxX=MappingLimits[2]
        MaxY=MappingLimits[3]
        
        
        
        return [MinX,MinY,MaxX,MaxY]  
    def GetTreeIDMinMax(self):
        TreeIDsSt="select min(globaltreeid),max(globaltreeid) from treesummary;"
        GlobalTreeLimit=self.DBConnection.ExecuteQuerySQLStatment(TreeIDsSt)[0]
        
        
        MinTreeID=GlobalTreeLimit[0]
        MaxTreeID=GlobalTreeLimit[1]
        
        return [MinTreeID,MaxTreeID]    
    def GenerateTables(self,MinX,MinY,MaxX,MaxY):
        
        
        
        setWarningOff="set client_min_messages='warning'; "
        self.DBConnection.ExecuteNoQuerySQLStatment(setWarningOff)
        
        for i in range(MinX,MaxX+1):
            for j in range(MinY,MaxY+1):
                self.CreateNewTable(i,j)
                logging.info("Table "+str(i)+","+str(j)+" Created")
                
        return [MinTreeID,MaxTreeID]
        
        
    def GetMinTable(self,TreeMappingRows):
        TablePrefix=self.Options['PGDB:ReArrangedTreeTablePrefix']
        if len(TreeMappingRows)>1:
            TablesList=[]
            TablesCountList=[]
            for Row in TreeMappingRows:                
                NewTableName=TablePrefix+str(Row[1])+"_"+str(Row[2])
                TableCountSt="Select count(*) from "+NewTableName+";"
                TableCount=self.ExecuteQuerySQLStatment(TableCountSt)[0][0]
                
                TablesList.append(NewTableName)
                TablesCountList.append(TableCount)
                
            return TablesList[numpy.argmin(TablesCountList)]
            
        else:
            return TablePrefix+str(TreeMappingRows[0][1])+"_"+str(TreeMappingRows[0][2])   
            
    def ProcessTree(self,TreeID):
        
        TreeTablesSt="Select tablename from treesummary where globaltreeid="+str(TreeID)
        TreeTable=self.DBConnection.ExecuteQuerySQLStatment(TreeTablesSt)
        if len(TreeTable)>0:
            TableName=self.ExecuteQuerySQLStatment(TreeTablesSt)[0][0]
        
            TreeMappingSt="select * from treemapping where globaltreeid="+str(TreeID)
            Rows=self.ExecuteQuerySQLStatment(TreeMappingSt)
        
            NewTableName=self.GetMinTable(Rows)
        
        
            MoveSt="Insert into "+NewTableName+" Select * from "+TableName+" where globaltreeid="+str(TreeID)+";"
            self.DBConnection.ExecuteNoQuerySQLStatment(MoveSt)
        
        
        
        
        
        
        
    def ArrangeTrees(self,TreeIDMin,TreeIDMax):    
        for TreeID in range(TreeIDMin,TreeIDMax+1): 
            start= time.clock()      
            self.ProcessTree(TreeID)
            end= time.clock()
            logging.info(str(CommRank)+":Moving Tree "+str(TreeID-TreeIDMin)+"/"+str(TreeIDMax-TreeIDMin+1)+"="+str(int(((TreeID-TreeIDMin)/float(TreeIDMax-TreeIDMin))*100))+"%\t"+str((end-start)/1000.0)+"S")
            
            
            
    
    ## Use Statement concatenation and the  CurrentSAGEStrcuture loaded from the XML settings to create a new table template
    def CreateNewTableTemplate(self):
        self.CreateTableTemplate="CREATE TABLE @TABLEName ("
        for field in self.CurrentSAGEStruct:
            if field[3]==1:
                ## Mapping SAGE (C/C++) to DB data types
                FieldDT=self.FormatMapping[field[1]]
                FieldName=field[2]
                self.CreateTableTemplate=self.CreateTableTemplate+ FieldName +' '+FieldDT+","
        self.CreateTableTemplate=self.CreateTableTemplate+"GlobalTreeID BIGINT,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyGlobalID BIGINT,"     
        self.CreateTableTemplate=self.CreateTableTemplate+"LocalGalaxyID INT,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyX FLOAT4,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyY FLOAT4,"
        self.CreateTableTemplate=self.CreateTableTemplate+"CentralGalaxyZ FLOAT4, CONSTRAINT @TABLEName_pkey PRIMARY KEY (GlobalIndex))"
                
    ## Perform create table for a specific TableIndex            
    def CreateNewTable(self,XIndex,YIndex):        
        
               
        CreateTableStatment=""
        try:
            
            ## The Table name is defined using the TreeTablePrefix from the XML config file
            TablePrefix=self.Options['PGDB:ReArrangedTreeTablePrefix']
            NewTableName=TablePrefix+str(XIndex)+"_"+str(YIndex)
            ## If the table exists drop it 
            DropSt="DROP TABLE IF EXISTS "+NewTableName+";"
            self.DBConnection.ExecuteNoQuerySQLStatment(DropSt)
            CreateTableStatment= string.replace(self.CreateTableTemplate,"@TABLEName",NewTableName)
            
                        
            
            CreateTableStatment=string.lower(CreateTableStatment)
            
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateTableStatment)
            
            ## Create Table indices             
            
            CreateIndexStatment="Create Index SnapNum_Index_"+NewTableName+" on  "+NewTableName+" (SnapNum);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index GlobalTreeID_Index_"+NewTableName+" on  "+NewTableName+" (GlobalTreeID);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index CentralGalaxyX_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyX);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index CentralGalaxyY_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyY);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index CentralGalaxyZ_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyZ);"
            self.DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            
             
            #logging.info("Table "+NewTableName+" Created With Index ...")
            
            
        except Exception as Exp:
            ## If an error happen catch it and let the user know
            logging.info(">>>>>Error While creating New Table")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp)            
            logging.info("Current SQL Statement =\n"+CreateTableStatment)
            raw_input("PLease press enter to continue.....")       
                
                 
if __name__ == '__main__':
    
    
    comm = MPI.COMM_WORLD
    CommRank = comm.Get_rank()
    
    CommSize= comm.Get_size()
    
    if CommRank==0:
        logging.info('SAGE Tree Re-Arranging ( MPI version)')
    
    
    logging.info("MPI Starting .... My Rank is: "+str(CommRank)+"/"+str(CommSize))
    
      
    
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml") 
    ReArrangeTablesObj=ReArrangeTrees(CommRank,CurrentSAGEStruct,Options)
    
    LocalMinTreeID=0
    LocalMaxTreeID=0
    
    if CommRank==0:
        [MinX,MinY,MaxX,MaxY] =ReArrangeTablesObj.GetGridLimits()
        [MinTreeID,MaxTreeID]=ReArrangeTablesObj.GetTreeIDMinMax()
        ReArrangeTablesObj.GenerateTables(MinX,MinY,MaxX,MaxY)
        logging.info([MinTreeID,MaxTreeID])
        Current_LocalMinTreeID=int(MinTreeID+((MaxTreeID-MinTreeID)*(1.0/CommSize)))+1
        
        for i in range(1,CommSize):
            Associated_LocalMinTreeID=Current_LocalMinTreeID           
            
            Associated_LocalMaxTreeID=int(MinTreeID+((MaxTreeID-MinTreeID)*(float(i+1)/CommSize)))
            
            
            Mesg={"MinTreeID":Associated_LocalMinTreeID,"MaxTreeID":Associated_LocalMaxTreeID}
            
            comm.send(Mesg,dest=i) 
            Current_LocalMinTreeID= Associated_LocalMaxTreeID+1
        LocalMinTreeID=0
        LocalMaxTreeID=int(MinTreeID+((MaxTreeID-MinTreeID)*(1.0/CommSize)))
    else:
        Mesg=comm.recv(source=0)
        LocalMinTreeID=Mesg["MinTreeID"]
        LocalMaxTreeID=Mesg["MaxTreeID"]
        
        
    logging.info ("Node ("+str(CommRank)+"): From ="+str(LocalMinTreeID)+"\t To="+str(LocalMaxTreeID))
    
        
    ReArrangeTablesObj.ArrangeTrees(LocalMinTreeID,LocalMaxTreeID) 
    ReArrangeTablesObj.CloseConnections()
        
        
        
        
         