'''
Created on 28/09/2012

@author: Amr Hassan
'''
import os
import sys
import struct
import MySQlDBInterface.MySQlDBInterface

class SAGEDataReader:
    '''
    The Module handles the data reading from SAGE output to a memory data structure.
    '''
    CurrentFolderPath=""
    CurrentGlobalTreeID=0
    FormatMapping={'int':'i',
                   'float':'f',
                   'long long':'q',
                   'float3':'3f'
                   }
    CurrentSAGEStruct=[
                      ['Type' ,'int'],
                      ['GalaxyIndex' ,'long long'],                      
                      ['HaloIndex' ,'int'],
                      ['FOFHaloIndex','int'],
                      ['TreeIndex','int'],
                      ['Descendant','int'],
                      ['SnapNum','int'],
                      ['CentralGal','int'],
                      ['CentralMvir','float'],
                      ['PosX','float'],
                      ['PosY','float'],
                      ['PosZ','float'],
                      ['VelX','float'],
                      ['VelY','float'],
                      ['VelZ','float'],
                      ['SpinX','float'],
                      ['SpinY','float'],
                      ['SpinZ','float'],
                      ['Len','int'],
                      ['Mvir','float'],
                      ['Rvir','float'],
                      ['Vvir','float'],
                      ['Vmax','float'],
                      ['VelDisp','float'],
                      ['ColdGas','float'],
                      ['StellarMass','float'],
                      ['BulgeMass','float'],
                      ['HotGas','float'],
                      ['EjectedMass','float'],
                      ['BlackHoleMass','float'],
                      ['ICS','float'],
                      ['MetalsColdGas','float'],
                      ['MetalsStellarMass','float'],
                      ['MetalsBulgeMass','float'],
                      ['MetalsHotGas','float'],
                      ['MetalsEjectedMass','float'],
                      ['MetalsICS','float'],
                      ['Sfr','float'],
                      ['SfrBulge','float'],
                      ['SfrICS','float'],
                      ['DiskScaleRadius','float'],
                      ['Cooling','float'],
                      ['Heating','float'],
                      ['Dummy' ,'int'] 
                      ]
    def __init__(self,FolderPath):
        '''
        Initialize the Class to handle a specific file path
        '''
        self.CurrentFolderPath=FolderPath
        
        # Just in case the folder path contain additional '/' Remove it
        if self.CurrentFolderPath.endswith("/"):
            self.CurrentFolderPath=self.CurrentFolderPath[:-1] 
            
        # Get a list of Non-Empty Files
        self.NonEmptyFiles=self.GetNonEmptyFilesList()
  
    def GetStructSizeAndFormat(self):
        '''
        Use the struct definition and the data mapping schema defined to return the expected field size
        in Bytes
        '''
        FormatStr=''
        for field in self.CurrentSAGEStruct:
            FormatStr=FormatStr+self.FormatMapping[field[1]]
        TotalSizeInBytes=struct.calcsize(FormatStr)
        return [FormatStr, TotalSizeInBytes]    
        
            
    def GetNonEmptyFilesList(self):
        '''
        Get List of Files where the file size is greater than zero
        '''
        
        dirList=os.listdir(self.CurrentFolderPath)
        fullPathArray=[]
        for fname in dirList:
            statinfo = os.stat(self.CurrentFolderPath+'/'+fname)                
            #print(fname+'\t'+str(statinfo.st_size/1024)+' KB')
            if(statinfo.st_size>0):
                fullPathArray.append([self.CurrentFolderPath+'/'+fname,statinfo.st_size])
        return fullPathArray
    
    def ReadTreeField(self,CurrentFile,FieldSize,FieldFormat,CurrentFileGalaxyID,TreeID):
        '''
        Read a single Galaxy information based on the pre-defined struct
        '''
        GalaxiesField= struct.unpack(FieldFormat, CurrentFile.read(FieldSize))
        FieldData={}
        FieldsIndex=0;
        for Field in self.CurrentSAGEStruct:            
            FieldData[Field[0]]=GalaxiesField[FieldsIndex]
            FieldsIndex=FieldsIndex+1
        FieldData['FileGalaxyID']=CurrentFileGalaxyID
        FieldData['TreeID']=TreeID
        
        return FieldData
        
    
    def ProcessFile(self,FilePath,FormatStr,FieldSize):
        CurrentFile=open(FilePath,"rb")
        CurrentFileGalaxyID=0
        Log = open('/home/amr/TempOutput/'+str(self.CurrentGlobalTreeID)+'.csv', 'wt')
        try:
            NumberofTrees= struct.unpack('i', CurrentFile.read(4))[0]
            TotalNumberOfGalaxies= struct.unpack('i', CurrentFile.read(4))[0]
            Log.write('\t Trees Count= '+str(NumberofTrees)+'\n')
            Log.write('\t Total Number of Galaxies = '+str(TotalNumberOfGalaxies)+'\n')
            
            
            # Read the number of Galaxies per each tree
            SumOfAllGalaxies=0                
            TreeLengthList=[]                
            for i in range(0,NumberofTrees):
                GalaxiesperTree= struct.unpack('i', CurrentFile.read(4))[0]
                TreeLengthList.append(GalaxiesperTree)     
                SumOfAllGalaxies=SumOfAllGalaxies+ GalaxiesperTree    
                
            
            # Verify the total number of galaxies 
            if not SumOfAllGalaxies==TotalNumberOfGalaxies: raise AssertionError
            #TypeZeroCount=0
            for i in range(0,NumberofTrees):
                NumberofGalaxiesInTree=TreeLengthList[i]
                print NumberofGalaxiesInTree
                TreeFields=[]
                
                Log.write('SnapNum,FOFHaloIndex,Type,CentralMvir,Mvir,StellarMass,GalaxyIndex,TreeIndexss,Descendant,FileGalaxyID,TreeID\n')    
                for j in range(0,NumberofGalaxiesInTree):
                    #read the fields of this tree
                    FieldData=self.ReadTreeField(CurrentFile, FieldSize, FormatStr,CurrentFileGalaxyID,self.CurrentGlobalTreeID)
                    TreeFields.append(FieldData)
                    CurrentFileGalaxyID=CurrentFileGalaxyID+1
                    Log.write(str(FieldData['SnapNum'])+','
                          +str(FieldData['FOFHaloIndex'])+','    
                          +str(FieldData['Type'])+','
                          +str(FieldData['CentralMvir'])+','
                          +str(FieldData['Mvir'])+','
                          +str(FieldData['StellarMass'])+','
                          +str(FieldData['GalaxyIndex'])
                          +','+str(FieldData['TreeIndex'])                          
                          +','+str(FieldData['Descendant'])
                          +','+str(FieldData['FileGalaxyID'])
                          +','+str(FieldData['TreeID'])+'\n')
                    #print FieldData
                    #if FieldData['Type']==0:
                    #    TypeZeroCount=TypeZeroCount+1
                        
                raw_input("Press Any Key to Continue")
                self.CurrentGlobalTreeID=self.CurrentGlobalTreeID+1
             
            #print TypeZeroCount
        except:
            print('\t Error happen while processing file')
            print('\t File Name: '+FilePath)
            print('\t Error:'+  str(sys.exc_info()))   
                        
            
        finally:
            CurrentFile.close()
            Log.close()
            
    def ProcessAllFiles(self):
        '''
        Process All the Non-Empty Files
        '''
        [FormatStr,FieldSize]=self.GetStructSizeAndFormat()
        
        
        for fobject in self.NonEmptyFiles:
            # Updating the user with what is going on
            print('Processing File:'+fobject[0])
            print('\t File Size:'+str(fobject[1]/1024)+' KB')
            
            self.ProcessFile(fobject[0],FormatStr,FieldSize)
            
            raw_input("Press Any Key to Continue")
            
                
        
        