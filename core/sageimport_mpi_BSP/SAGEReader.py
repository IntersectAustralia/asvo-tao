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

class SAGEDataReader:    
    #The Module handles the data reading from SAGE output to a memory data structure.
    DebugToFile=False
    CurrentFolderPath=""
    CurrentGlobalTreeID=0
    FormatMapping={'int':'i',
                   'float':'f',
                   'long long':'q'                   
                   }
    
    def __init__(self,CurrentSAGEStruct,Options,PGDB,CommSize,CommRank):
        
        
        #Initialize the Class to handle a specific file path        
        self.CurrentFolderPath=Options['RunningSettings:InputDir']
        self.CurrentSAGEStruct=CurrentSAGEStruct
        self.Options=Options
        self.PGDB=PGDB
        self.CommSize=CommSize
        self.CommRank=CommRank
        # Just in case the folder path contain additional '/' Remove it
        if self.CurrentFolderPath.endswith("/"):
            self.CurrentFolderPath=self.CurrentFolderPath[:-1] 
            
        
        
  
    def GetStructSizeAndFormat(self):
        
        #Use the struct definition and the data mapping schema defined to return the expected field size
        #in Bytes
        
        FormatStr=''
        for field in self.CurrentSAGEStruct:
            FormatStr=FormatStr+self.FormatMapping[field[1]]
        TotalSizeInBytes=struct.calcsize(FormatStr)
        return [FormatStr, TotalSizeInBytes]    
        
            
    
        
        
    
    def ProcessAllFiles(self):
        
               
        self.SimulationBoxX=float(self.Options['RunningSettings:SimulationBoxX'])
        self.SimulationBoxY=float(self.Options['RunningSettings:SimulationBoxX'])
        self.BSPCellSize=float(self.Options['RunningSettings:BSPCellSize'])
        
        
        
        self.CellsInX=int(math.ceil(self.SimulationBoxX/self.BSPCellSize))
        self.CellsInY=int(math.ceil(self.SimulationBoxY/self.BSPCellSize))
        
        
        
        
        
        #Process All the Non-Empty Files
        
        
        [self.FormatStr,self.FieldSize]=self.GetStructSizeAndFormat()
        ListOfUpProcessedFile=self.PGDB.GetListofUnProcessedFiles(self.CommSize,self.CommRank)
        TotalNumberofUnPrcoessedFiles=len(ListOfUpProcessedFile)
        FileCounter=0
        for UnProcessedFile in ListOfUpProcessedFile:
            # Updating the user with what is going on
            logging.info(str(self.CommRank)+":Processing File ("+str(FileCounter)+"/"+str(TotalNumberofUnPrcoessedFiles-1)+"):"+UnProcessedFile[1])
            logging.info('\t File Size:'+str(UnProcessedFile[2]/1024)+' KB')
            
            self.PGDB.StartTransaction()
            self.ProcessFile(UnProcessedFile)
            self.PGDB.SetFileAsProcessed(UnProcessedFile[0])            
            self.PGDB.CommintTransaction()
            FileCounter=FileCounter+1
            
        
    
    def ProcessFile(self,UnProcessedFile):
        
         
        CurrentFile=open(UnProcessedFile[1],"rb")
        CurrentFileGalaxyID=0
        
        
        TreeIDStart=UnProcessedFile[5]
        
    
        NumberofTrees= struct.unpack('i', CurrentFile.read(4))[0]
        TotalNumberOfGalaxies= struct.unpack('i', CurrentFile.read(4))[0]
        if self.DebugToFile==True:
            self.Log.write('\t Trees Count= '+str(NumberofTrees)+'\n')
            self.Log.write('\t Total Number of Galaxies = '+str(TotalNumberOfGalaxies)+'\n')
        
        
        # Read the number of Galaxies per each tree
        SumOfAllGalaxies=0                
        TreeLengthList=[]                
        for i in range(0,NumberofTrees):
            GalaxiesperTree= struct.unpack('i', CurrentFile.read(4))[0]
            
            TreeLengthList.append(GalaxiesperTree)     
            SumOfAllGalaxies=SumOfAllGalaxies+ GalaxiesperTree    
            
        
        # Verify the total number of galaxies 
        if not SumOfAllGalaxies==TotalNumberOfGalaxies:
            logging.info("Error In Header File "+str(SumOfAllGalaxies)+"/"+str(TotalNumberOfGalaxies)) 
            raise AssertionError
    
        for i in range(0,NumberofTrees):
            NumberofGalaxiesInTree=TreeLengthList[i]
            logging.info('\t '+str(self.CommRank)+': Number of Galaxies in Tree ('+str(i)+')='+str(NumberofGalaxiesInTree))
            if NumberofGalaxiesInTree>0:
                TreeData=self.ProcessTree(TreeIDStart+i,NumberofGalaxiesInTree,CurrentFile,CurrentFileGalaxyID)  
                if len(TreeData)>0: 
                    TableID=self.MapTreetoTableID(TreeData) 
                    self.PGDB.CreateNewTree(TableID,TreeData)        
            
            
         
    
        CurrentFile.close()  
                  
        if self.DebugToFile==True:
            Log.close()
    
    
        
    
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
        
        Rect1=[MinX,MaxX,MinY,MaxY]
        
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
        FinalTableID=-1
        
        if len(PossibleTables)==1:
            FinalTableID=int(PossibleTables[0])
        elif len(PossibleTables)<=10:
            FinalTableID=int(PossibleTables[randrange(len(PossibleTables))])
        else: 
                       
            FinalTableID=self.CellsInX*self.CellsInY
                        
        return FinalTableID
        
    
    def ProcessTree(self,TreeID,NumberofGalaxiesInTree,CurrentFile,CurrentFileGalaxyID):    
                
        
                
        if self.DebugToFile==True:
            self.Log.write('SnapNum,FOFHaloIndex,Type,CentralMvir,Mvir,StellarMass,GalaxyIndex,TreeIndexss,Descendant,FileGalaxyID,TreeID\n')
        
        TreeFields=[]        
        for j in range(0,NumberofGalaxiesInTree):
            #read the fields of this tree
            #logging.info(str(j)+"/"+str(NumberofGalaxiesInTree))
            FieldData=self.ReadTreeField(CurrentFile,CurrentFileGalaxyID,TreeID)
            TreeFields.append(FieldData)
            CurrentFileGalaxyID=CurrentFileGalaxyID+1
            if self.DebugToFile==True:
                self.Log.write(str(FieldData['SnapNum'])+','+
                          str(FieldData['FOFHaloIndex'])+','+
                          str(FieldData['Type'])+','+
                          str(FieldData['CentralMvir'])+','+
                          str(FieldData['Mvir'])+','+
                          str(FieldData['StellarMass'])+','+
                          str(FieldData['GalaxyIndex'])+','+
                          str(FieldData['TreeIndex'])+','+
                          str(FieldData['Descendant'])+','+
                          str(FieldData['FileGalaxyID'])+','+
                          str(FieldData['TreeID'])+'\n')
        return self.ComputeFields(TreeFields)    
    
    def ComputeFields(self,TreeData):
        for TreeField in TreeData:
            CentralGalaxyLocalID=TreeField['CentralGal']
            DescGalaxyLocalID=TreeField['Descendant']
            CentralGalaxy=TreeData[CentralGalaxyLocalID]
            TreeField['CentralGalaxyGlobalID']=CentralGalaxy['GlobalIndex']
            DescGalaxy=TreeData[DescGalaxyLocalID]
            #TreeField['DescendantGlobalID']=DescGalaxy['GalaxyIndex']
            TreeField['CentralGalaxyX']=CentralGalaxy['PosX']
            TreeField['CentralGalaxyY']=CentralGalaxy['PosY']
            TreeField['CentralGalaxyZ']=CentralGalaxy['PosZ']
            
        return TreeData
    def ReadTreeField(self,CurrentFile,CurrentFileGalaxyID,TreeID):
        
        #Read a single Galaxy information based on the pre-defined struct
        
        GalaxiesField= struct.unpack(self.FormatStr, CurrentFile.read(self.FieldSize))
        FieldData={}
        FieldsIndex=0;
        for Field in self.CurrentSAGEStruct:            
            FieldData[Field[0]]=GalaxiesField[FieldsIndex]
            FieldsIndex=FieldsIndex+1
        FieldData['FileGalaxyID']=CurrentFileGalaxyID
        FieldData['TreeID']=TreeID
        
        return FieldData        
    
            
                
        
        