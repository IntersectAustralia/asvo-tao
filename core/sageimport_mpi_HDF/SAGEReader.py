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

class SAGEDataReader:    
    #The Module handles the data reading from SAGE output to a memory data structure.
    
    CurrentInputFilePath=""
    CurrentGlobalTreeID=0
    FormatMapping={'int':'i',
                   'float':'f',
                   'long long':'q'                   
                   }
    
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
            
            
            
            self.ProcessTree(UnProcessedTree)
            self.PGDB.SetTreeAsProcessed(UnProcessedTree[0])            
            
            TreeCounter=TreeCounter+1
            
        
    def GenerateDictFromFields(self,TreeLoadingID,TreeData):
        TreeDict=[]
        
        for Tree in TreeData:
            
            FieldData={}            
            FieldsIndex=0
            for Field in self.CurrentSAGEStruct:            
                FieldData[Field[0]]=Tree[FieldsIndex]
                FieldsIndex=FieldsIndex+1
            
            FieldData['TreeID']=TreeLoadingID
            TreeDict.append(FieldData)
        return TreeDict    
            
    def ProcessTree(self,UnProcessedTree):
        
        
        LoadingTreeID= UnProcessedTree[0]
        StartIndex=UnProcessedTree[3]
        GalaxiesCount=UnProcessedTree[2]        
        
        
        logging.info('\t '+str(self.CommRank)+': Number of Galaxies in Tree ('+str(LoadingTreeID)+')='+str(GalaxiesCount))
        if GalaxiesCount>0:
            TreeData=self.InputFile['galaxies'][StartIndex:StartIndex+GalaxiesCount] 
                     
            TreeData=self.GenerateDictFromFields(LoadingTreeID,TreeData)
            
            self.ComputeFields(TreeData)   
            print("Compute Fields Done") 
            TableID=self.MapTreetoTableID(TreeData) 
            print("TableID="+str(TableID)) 
            self.PGDB.CreateNewTree(TableID,TreeData)        
            
            
         
    
        CurrentFile.close()  
               
       
    
    
        
    
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
            logging.info(str(TreeItem['PosX'])+","+str(TreeItem['PosY'])+","+str(TreeItem['PosZ']))
        
        Rect1=[MinX,MaxX,MinY,MaxY]
        logging.info('Tree Box'+ str(Rect1))
        XLocation=-1
        YLocation=-1
        StepSize=self.BSPCellSize
        
        PossibleTables=[]
        
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
                    logging.info("("+str(XLocation)+","+str(YLocation)+")="+str(PTableID))
                    PossibleTables=numpy.hstack([PossibleTables,PTableID])
                    logging.info("Intersect - Rect1="+str(Rect1)+"\tRect2="+str(Rect2))
                else:
                    logging.info("Fail - Rect1="+str(Rect1)+"\tRect2="+str(Rect2))
        FinalTableID=-1
        
        if len(PossibleTables)==1:
            FinalTableID=int(PossibleTables[0])
        elif len(PossibleTables)<=10:
            FinalTableID=int(PossibleTables[randrange(len(PossibleTables))])
        else:                        
            FinalTableID=self.CellsInX*self.CellsInY
        logging.info("Final Table ID="+str(FinalTableID))                
        return FinalTableID
        
    
    
    
    def ComputeFields(self,TreeData):
        for TreeField in TreeData:
            CentralGalaxyLocalID=TreeField['CentralGal']
            
            DescGalaxyLocalID=TreeField['Descendant']
            CentralGalaxy=TreeData[CentralGalaxyLocalID]
            TreeField['CentralGalaxyGlobalID']=CentralGalaxy['GlobalIndex']
            DescGalaxy=TreeData[DescGalaxyLocalID]            
            TreeField['CentralGalaxyX']=CentralGalaxy['PosX']
            TreeField['CentralGalaxyY']=CentralGalaxy['PosY']
            TreeField['CentralGalaxyZ']=CentralGalaxy['PosZ']
            
        return TreeData
    def ReadTreeField(self,CurrentFile,CurrentFileGalaxyID,TreeID):
        
        #Read a single Galaxy information based on the pre-defined struct
        #print self.FormatStr
        #print struct.calcsize(self.FormatStr)
        GalaxiesField= struct.unpack(self.FormatStr, CurrentFile.read(self.FieldSize))
        FieldData={}
        FieldsIndex=0
        for Field in self.CurrentSAGEStruct:            
            FieldData[Field[0]]=GalaxiesField[FieldsIndex]
            FieldsIndex=FieldsIndex+1
        FieldData['FileGalaxyID']=CurrentFileGalaxyID
        FieldData['TreeID']=TreeID
        
        return FieldData        
    
            
                
        
        