import pg
import getpass
import math
import string
import sys
import settingReader
import numpy
import matplotlib.pyplot as plt
import time
from mpi4py import MPI # MPI Implementation

class ReArrangeTrees(object):
    
    FormatMapping={'int':'INT','float':'FLOAT4','long long':'BIGINT'}
    
    
    def __init__(self,CommRank,CurrentSAGEStruct,Options):
        '''
        Constructor
        '''
        self.CommRank=CommRank
        self.Options=Options
        self.serverip=self.Options['PGDB:serverip']
        self.username=self.Options['PGDB:user']
        self.password=self.Options['PGDB:password']
        self.port=int(self.Options['PGDB:port'])
        self.DBName=self.Options['PGDB:NewDBName']
        self.CurrentSAGEStruct=CurrentSAGEStruct
        if self.password==None:
            print('Password for user:'+self.username+' is not defined')
            self.password=getpass.getpass('Please enter password:')
        
        # Take care that the connection will be opened to standard DB 'master'
        # This is temp. until the actual database is created
        self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname=self.DBName)
        print('Connection to DB is open...Start Creating Tables')
        self.CreateNewTableTemplate()
        
    
    
    def CloseConnections(self):        
        self.CurrentConnection.close()       
        print('Connection to DB is Closed...')
    
    def ExecuteNoQuerySQLStatment(self,SQLStatment):
        try:           
            SQLStatment=string.lower(SQLStatment)  
            self.CurrentConnection.query(SQLStatment)              
        except Exception as Exp:
            print(">>>>>Error While creating New Table")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
    def ExecuteQuerySQLStatment(self,SQLStatment):
        try:            
            SQLStatment=string.lower(SQLStatment)
            resultsList=self.CurrentConnection.query(SQLStatment).getresult()            
            return resultsList  
        except Exception as Exp:
            print(">>>>>Error While creating New Table")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
         
    def GetGridLimits(self):
        TreeMappingSt="select min(gridx),min(gridy),max(gridx),max(gridy) from treemapping;"
        MappingLimits=self.ExecuteQuerySQLStatment(TreeMappingSt)[0]
        
        
        
        
        MinX=MappingLimits[0]
        MinY=MappingLimits[1]
        
        MaxX=MappingLimits[2]
        MaxY=MappingLimits[3]
        
        
        
        return [MinX,MinY,MaxX,MaxY]  
    def GetTreeIDMinMax(self):
        TreeIDsSt="select min(globaltreeid),max(globaltreeid) from treesummary;"
        GlobalTreeLimit=self.ExecuteQuerySQLStatment(TreeIDsSt)[0]
        
        
        MinTreeID=GlobalTreeLimit[0]
        MaxTreeID=GlobalTreeLimit[1]
        
        return [MinTreeID,MaxTreeID]    
    def GenerateTables(self,MinX,MinY,MaxX,MaxY):
        
        
        
        setWarningOff="set client_min_messages='warning'; "
        self.ExecuteNoQuerySQLStatment(setWarningOff)
        
        for i in range(MinX,MaxX+1):
            for j in range(MinY,MaxY+1):
                self.CreateNewTable(i,j)
                print("Table "+str(i)+","+str(j)+" Created")
                
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
        TreeTable=self.ExecuteQuerySQLStatment(TreeTablesSt)
        if len(TreeTable)>0:
            TableName=self.ExecuteQuerySQLStatment(TreeTablesSt)[0][0]
        
            TreeMappingSt="select * from treemapping where globaltreeid="+str(TreeID)
            Rows=self.ExecuteQuerySQLStatment(TreeMappingSt)
        
            NewTableName=self.GetMinTable(Rows)
        
        
            MoveSt="Insert into "+NewTableName+" Select * from "+TableName+" where globaltreeid="+str(TreeID)+";"
            self.ExecuteNoQuerySQLStatment(MoveSt)
        
        
        
        
        
        
        
    def ArrangeTrees(self,TreeIDMin,TreeIDMax):    
        for TreeID in range(TreeIDMin,TreeIDMax+1): 
            start= time.clock()      
            self.ProcessTree(TreeID)
            end= time.clock()
            print(str(CommRank)+":Moving Tree "+str(TreeID-TreeIDMin)+"/"+str(TreeIDMax-TreeIDMin+1)+"="+str(int(((TreeID-TreeIDMin)/float(TreeIDMax-TreeIDMin))*100))+"%\t"+str((end-start)/1000.0)+"S")
            
            
            
    
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
            self.ExecuteNoQuerySQLStatment(DropSt)
            CreateTableStatment= string.replace(self.CreateTableTemplate,"@TABLEName",NewTableName)
            
                        
            
            CreateTableStatment=string.lower(CreateTableStatment)
            
            self.ExecuteNoQuerySQLStatment(CreateTableStatment)
            
            ## Create Table indices             
            
            CreateIndexStatment="Create Index SnapNum_Index_"+NewTableName+" on  "+NewTableName+" (SnapNum);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index GlobalTreeID_Index_"+NewTableName+" on  "+NewTableName+" (GlobalTreeID);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index CentralGalaxyX_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyX);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index CentralGalaxyY_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyY);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            CreateIndexStatment="Create Index CentralGalaxyZ_Index_"+NewTableName+" on  "+NewTableName+" (CentralGalaxyZ);"
            self.ExecuteNoQuerySQLStatment(CreateIndexStatment)
            
             
            #print("Table "+NewTableName+" Created With Index ...")
            
            
        except Exception as Exp:
            ## If an error happen catch it and let the user know
            print(">>>>>Error While creating New Table")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+CreateTableStatment)
            raw_input("PLease press enter to continue.....")       
                
                 
if __name__ == '__main__':
    
    
    comm = MPI.COMM_WORLD
    CommRank = comm.Get_rank()
    
    CommSize= comm.Get_size()
    
    if CommRank==0:
        print('SAGE Tree Re-Arranging ( MPI version)')
    
    
    print("MPI Starting .... My Rank is: "+str(CommRank)+"/"+str(CommSize))
    
      
    
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml") 
    ReArrangeTablesObj=ReArrangeTrees(CommRank,CurrentSAGEStruct,Options)
    
    LocalMinTreeID=0
    LocalMaxTreeID=0
    
    if CommRank==0:
        [MinX,MinY,MaxX,MaxY] =ReArrangeTablesObj.GetGridLimits()
        [MinTreeID,MaxTreeID]=ReArrangeTablesObj.GetTreeIDMinMax()
        ReArrangeTablesObj.GenerateTables(MinX,MinY,MaxX,MaxY)
        print([MinTreeID,MaxTreeID])
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
        
        
    print ("Node ("+str(CommRank)+"): From ="+str(LocalMinTreeID)+"\t To="+str(LocalMaxTreeID))
    
        
    ReArrangeTablesObj.ArrangeTrees(LocalMinTreeID,LocalMaxTreeID) 
    ReArrangeTablesObj.CloseConnections()
        
        
        
        
         