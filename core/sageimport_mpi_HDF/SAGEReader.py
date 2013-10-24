'''
Created on 28/09/2012

@author: Amr Hassan
'''
import os
import sys
import struct
import string
import math
import numpy
from random import randrange
import logging
import PGDBInterface
import h5py
import numpy
import time

class SAGEDataReader:    
    #The Module handles the data reading from SAGE output to a memory data structure.
    
    CurrentInputFilePath=""
    CurrentGlobalTreeID=0
    FormatMapping={'int':'i','float':'f','long long':'q'}
    
    
    
    def __init__(self,CurrentSAGEStruct,Options,PGDB,CommSize,CommRank):
        
        
        #Initialize the Class to handle a specific file path        
        self.CurrentInputFilePath=Options['RunningSettings:InputFile']
        self.CurrentSAGEStruct=CurrentSAGEStruct
        self.Options=Options
        self.PGDB=PGDB
        self.CommSize=CommSize
        self.CommRank=CommRank
        
            
        
        
  
    
            
    
        
        
    
    def ProcessAllTrees(self):
        
               
        self.SimulationBoxX=float(self.Options['RunningSettings:SimulationBoxX'])
        self.SimulationBoxY=float(self.Options['RunningSettings:SimulationBoxX'])
        self.BSPCellSize=float(self.Options['RunningSettings:BSPCellSize'])
        
        
        
        self.CellsInX=int(math.ceil(self.SimulationBoxX/self.BSPCellSize))
        self.CellsInY=int(math.ceil(self.SimulationBoxY/self.BSPCellSize))
        
        self.InputFile=h5py.File(self.CurrentInputFilePath,'r')
        
        
        
        #Process All the Non-Empty Files
             
        ListOfUpProcessedTrees=self.PGDB.GetListofUnProcessedTrees(self.CommSize,self.CommRank)
        
        TotalNumberofUnPrcoessedTrees=len(ListOfUpProcessedTrees)
        
        TreeCounter=0
        for UnProcessedTree in ListOfUpProcessedTrees:
            # Updating the user with what is going on
            logging.info(str(self.CommRank)+":Processing Tree ("+str(TreeCounter)+"/"+str(TotalNumberofUnPrcoessedTrees-1)+"):"+str(UnProcessedTree[0]))
            
            
            start_time = time.time()
            self.ProcessTree(UnProcessedTree)
            logging.info(">>>> Importing Tree Execution time="+str( time.time() - start_time)+ " seconds")
            start_time = time.time()
            self.PGDB.SetTreeAsProcessed(UnProcessedTree[0])                   
            logging.info(">>>> Set Tree as Processed time="+str( time.time() - start_time)+ " seconds")
            TreeCounter=TreeCounter+1
            
        
    def GenerateDictFromFields(self,TreeLoadingID,TreeData):
        TreeDict=[]
        
        pgcopy_dtype = [('num_fields','>i2')]
        FieldsList=[]
        FieldsIndex=0
        for field, dtype in TreeData.dtype.descr:
            FieldsList+=[self.CurrentSAGEStruct[FieldsIndex][0]]
            FieldName=self.CurrentSAGEStruct[FieldsIndex][0]
            pgcopy_dtype += [(FieldName + '_length', '>i4'),(FieldName, dtype.replace('<', '>'))]
            FieldsIndex=FieldsIndex+1
        
        FieldName='TreeID'        
        pgcopy_dtype += [(FieldName + '_length', '>i4'),(FieldName, '>i8')]
        FieldName='CentralGalaxyGlobalID'        
        pgcopy_dtype += [(FieldName + '_length', '>i4'),(FieldName, '>i8')]
        
        
        FieldsList+=['treeid']
        FieldsList+=['centralgalaxyglobalid']
        if(FieldsList.count('LocalGalaxyID')>0):
            logging.info("### LocalGalaxyID already Exists. No Data Will be generated")
        else:
            logging.info("### LocalGalaxyID  is Missing. Regenerate Local GalaxyID")
        
        if(FieldsList.count('LocalGalaxyID')==0):        
            FieldName='LocalGalaxyID'
            pgcopy_dtype += [(FieldName + '_length', '>i4'),(FieldName, '>i4')]
        
        
        pgcopy = numpy.empty(TreeData.shape, pgcopy_dtype)
        if(FieldsList.count('LocalGalaxyID')==0): 
            pgcopy['num_fields'] = len(TreeData.dtype)+3
        else:
            pgcopy['num_fields'] = len(TreeData.dtype)+2
            
        for i in range(0,len(TreeData.dtype)):
            field = self.CurrentSAGEStruct[i][0]                            
            pgcopy[field + '_length'] = TreeData.dtype[i].alignment
            pgcopy[field] = TreeData[TreeData.dtype.names[i]]
        
             
        pgcopy['TreeID_length'] = pgcopy.dtype[-5].alignment
        
        pgcopy['TreeID'].fill(TreeLoadingID) 
        if(FieldsList.count('LocalGalaxyID')==0):                       
            pgcopy['LocalGalaxyID']=range(0,len(TreeData))
            
        pgcopy['CentralGalaxyGlobalID_length'] = pgcopy.dtype[-3].alignment
        
        if(FieldsList.count('LocalGalaxyID')==0):
            pgcopy['LocalGalaxyID_length'] = pgcopy.dtype[-1].alignment 
        
            
            
        return pgcopy  
    
    def ComputeFields(self,TreeData):
        
        #print TreeData
        if "CentralGal" in TreeData.dtype.fields:
            for TreeField in TreeData:
                CentralGalaxyLocalID=TreeField['CentralGal']  
                         
                CentralGalaxy=TreeData[CentralGalaxyLocalID]
                TreeField['CentralGalaxyGlobalID']=CentralGalaxy['GlobalIndex']    
        else:
            logging.info('#### Central Galaxy Field Does not exist. Skipping Compute Fields #####')                
        return TreeData
      
            
    def ProcessTree(self,UnProcessedTree):
        
        
        LoadingTreeID= UnProcessedTree[0]
        StartIndex=UnProcessedTree[2]
        GalaxiesCount=UnProcessedTree[1]        
        
        
        logging.info('\t '+str(self.CommRank)+': Number of Galaxies in Tree ('+str(LoadingTreeID)+')='+str(GalaxiesCount))
        if GalaxiesCount>0:
            start_time = time.time()
            TreeData=self.InputFile['galaxies'][StartIndex:StartIndex+GalaxiesCount] 
            logging.info("Reading Data="+str( time.time() - start_time)+ " seconds")   
            start_time = time.time()      
            TreeData=self.GenerateDictFromFields(LoadingTreeID,TreeData)
            logging.info("Convert to Dict="+str( time.time() - start_time)+ " seconds") 
            start_time = time.time()   
            self.ComputeFields(TreeData) 
            logging.info("Compute Fields="+str( time.time() - start_time)+ " seconds")  
            start_time = time.time()            
            TableID=self.MapTreetoTableID(TreeData)  
            logging.info("Get TableID="+str( time.time() - start_time)+ " seconds")  
            start_time = time.time()         
            self.PGDB.CreateNewTree(TableID,TreeData)        
            logging.info("Insert to Database="+str( time.time() - start_time)+ " seconds")
            
         
    
        
               
       
    
    
        
    
    def IntersectTwoRect(self,RectA,RectB):
        ## Rect=[X1,X2,Y1,Y2]
        if (RectA[0] < RectB[1] and RectA[1] > RectB[0] and RectA[2] < RectB[3] and RectA[3] > RectB[2]): 
            return True;
        else:
            
            return False;
        
    def MapTreetoTableID(self,TreeData):
        
        
        #self.SimulationBoxX=float(self.Options['RunningSettings:SimulationBoxX'])
        #self.SimulationBoxY=float(self.Options['RunningSettings:SimulationBoxX'])
        #self.BSPCellSize=float(self.Options['RunningSettings:BSPCellSize'])              
        #self.CellsInX=int(math.ceil(self.SimulationBoxX/self.BSPCellSize))
        #self.CellsInY=int(math.ceil(self.SimulationBoxY/self.BSPCellSize))
        logging.info('Calculating Tree Bounding Box for '+ str(len(TreeData))+' Galaxy!')
        ## Get Tree Bounding Rectangle
        MinX=TreeData[0]['PosX']
        MaxX=TreeData[0]['PosX']
        
        MinY=TreeData[0]['PosY']
        MaxY=TreeData[0]['PosY']
        
        for TreeItem in TreeData:
            MinX=min(MinX,TreeItem['PosX'])
            MaxX=max(MaxX,TreeItem['PosX'])
            MinY=min(MinY,TreeItem['PosY'])
            MaxY=max(MaxY,TreeItem['PosY'])
            #logging.info(str(TreeItem['PosX'])+","+str(TreeItem['PosY'])+","+str(TreeItem['PosZ']))
        
        Rect1=[MinX,MaxX,MinY,MaxY]
        logging.info('Tree Box'+ str(Rect1))
        XLocation=-1
        YLocation=-1
        StepSize=self.BSPCellSize
        
        PossibleTables=[]
        if MaxX>self.SimulationBoxX or MaxY>self.SimulationBoxY:
            raise Exception("Error In Coordinate Values or in the simulation Box Size:("+str(MaxX)+","+str(MaxY)+") > ("+str(self.SimulationBoxX)+","+str(self.SimulationBoxY))
        ### Intersection between two Rectangles 
        ### http://silentmatt.com/rectangle-intersection/
        for X in numpy.arange(0,self.SimulationBoxX,StepSize):
            XLocation=XLocation+1
            YLocation=-1
            for Y in numpy.arange(0,self.SimulationBoxY,StepSize):
                
                YLocation=YLocation+1
                BX1=X;
                BX2=X+StepSize
                BY1=Y
                BY2=Y+StepSize
                
                Rect2=[BX1,BX2,BY1,BY2]
                
                
                if self.IntersectTwoRect(Rect1, Rect2)==True:
                    GetIntersectionWithCurrentBoundingRect="INSERT INTO TreeMapping VALUES("+str(TreeData[0]['TreeID'])+","+str(XLocation)+","+str(YLocation)+"); "                
                
                    self.PGDB.DBConnection.ExecuteNoQuerySQLStatment(GetIntersectionWithCurrentBoundingRect)
                    PTableID=int((XLocation*self.CellsInX)+YLocation)
                    PossibleTables=numpy.hstack([PossibleTables,PTableID])
        FinalTableID=-1
        
        if len(PossibleTables)==1:
            FinalTableID=int(PossibleTables[0])
        elif len(PossibleTables)<=10 and len(PossibleTables)>0:
            FinalTableID=int(PossibleTables[randrange(len(PossibleTables))])
        else:                        
            FinalTableID=self.CellsInX*self.CellsInY
        logging.info("Final Table ID="+str(FinalTableID))                
        return FinalTableID
        
    
    
    
    
            
                
        
        