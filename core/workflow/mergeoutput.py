import sys,os
import shlex, subprocess

import string
from distutils.filelist import FileList
import logging, logging.handlers
import pyfits
import h5py
import shutil
import numpy

ExtensionLocation=-2


def ValidateAllSameExtension(FilesList,SubJobIndexLocation):
    
    
    logging.info('Start Validating File List (Length and Extension)')
    if len(FilesList)==0:
        return False
    logging.info('Not an empty List')
    FirstItemExt=FilesList[0][1][ExtensionLocation]
    logging.info('First Item Ext='+FirstItemExt)
    FileExtLen=len(FilesList[0][1])
    for FileDetail in FilesList:
        
        if(FileDetail[1][ExtensionLocation]!=FirstItemExt) or (FileExtLen!= len(FileDetail[1])):
            logging.info('File List Validation Because '+FileDetail[1][ExtensionLocation]+"!="+FirstItemExt)                       
            return False
    logging.info('End Validating File List (Length and Extension)')
    return True
def HandleVOFiles(ListofFiles,OutputFileName):
    if len(ListofFiles)==0:
        return
    logging.info('Merging Output for sub-task - VOTable Files List')
    logging.info('Output File Name : '+OutputFileName)
    f=open(OutputFileName,'wt')
    Reader=open(ListofFiles[0],'rt')
    logging.info('Merging First File : '+ListofFiles[0])
    AllText=Reader.read()
    HeaderPos=AllText.find("<TR>")
    ClosingPos=AllText.find("</TABLEDATA>")
    
    Header=AllText[0:HeaderPos]
    Closing=AllText[ClosingPos:]
    
    f.write(Header)
    f.writelines(AllText[HeaderPos:ClosingPos])
    Reader.close()
    for i in range(1,len(ListofFiles)):
        logging.info('Merging File : '+ListofFiles[i])
        Reader=open(ListofFiles[i],'rt')
        AllText=Reader.read()
        HeaderPos=AllText.find("<TR>")
        ClosingPos=AllText.find("</TABLEDATA>")
        
        f.writelines(AllText[HeaderPos:ClosingPos])
        
        Reader.close()
    f.write(Closing)    
    f.close()
    logging.info('Merging Done >> '+OutputFileName)
    return True
def HandleHDF5Dataset(InputDataset,OutputDataset):
    
    StartPos= OutputDataset.shape
    OutputDataset.resize( numpy.add(InputDataset.shape,OutputDataset.shape))
    OutputDataset[StartPos[0]:]=InputDataset[:]
    
    
def HandleHDF5Files(ListofFiles,OutputFileName):
    if len(ListofFiles)==0:
        return
    logging.info('Merging Output for sub-task - HDF5 Files List')
    logging.info('Output File Name : '+OutputFileName)
        
      
    
    shutil.copy(ListofFiles[0],OutputFileName)  
    logging.info('First File Copied to  : '+OutputFileName)     
    OutputFile=h5py.File(OutputFileName,'r+')
    
    for i in range(1,len(ListofFiles)):
        logging.info('Merging File : '+ListofFiles[i])
        
        Reader = h5py.File(ListofFiles[i],'r')
        for Dset in Reader:
            
            if type(Reader[Dset])==h5py._hl.group.Group:
                for SubDataset in Reader[Dset]:                    
                    HandleHDF5Dataset(Reader[Dset+"/"+SubDataset],OutputFile[Dset+"/"+SubDataset])
            else:
                HandleHDF5Dataset(Reader[Dset],OutputFile[Dset])
        Reader.close()        
           
            
    OutputFile.close()
   
    logging.info('Merging Done >> '+OutputFileName)
    return True

def HandleFITSFiles(ListofFiles,OutputFileName):
    if len(ListofFiles)==0:
        return
    logging.info('Merging Output for sub-task - FITS Files List')
    logging.info('Output File Name : '+OutputFileName)
        
    TotalRowsCount=0;
    for i in range(0,len(ListofFiles)):
        try:
            Reader = pyfits.open(ListofFiles[i])
            logging.info("Reading FITS File Shape: "+ListofFiles[i]+" :("+ str(i)+"): "+str(Reader[1].data.shape[0]))
            TotalRowsCount=TotalRowsCount+Reader[1].data.shape[0]
        except Exception as Exp:
            logging.info('Cannot Open File:'+ListofFiles[i])
        
    
    
    Reader = pyfits.open(ListofFiles[0])       
    hdu = pyfits.new_table(Reader[1].data, nrows=TotalRowsCount)
    nrows=Reader[1].data.shape[0]
    
    for i in range(1,len(ListofFiles)):
        logging.info('Merging File : '+ListofFiles[i])
        try:
            Reader = pyfits.open(ListofFiles[i])
            for name in hdu.columns.names:            
                hdu.data.field(name)[nrows:nrows+Reader[1].data.shape[0]]=Reader[1].data.field(name)
            nrows=nrows+Reader[1].data.shape[0]
        except Exception as Exp:
            logging.info('Cannot Open File:'+ListofFiles[i])
            
    
    hdu.writeto(OutputFileName)
    logging.info('Merging Done >> '+OutputFileName)
    return True


def HandleCSVFiles(ListofFiles,OutputFileName):    
    if len(ListofFiles)==0:
        return
    logging.info('Merging Output for sub-task - CSV Files List')
    logging.info('Output File Name : '+OutputFileName)
    f=open(OutputFileName,'wt')
    Reader=open(ListofFiles[0],'rt')
    logging.info('Merging First File : '+ListofFiles[0])
    f.write(Reader.read())
    Reader.close()
    for i in range(1,len(ListofFiles)):
        logging.info('Merging File : '+ListofFiles[i])
        Reader=open(ListofFiles[i],'rt')
        f.writelines(Reader.readlines()[1:])
        Reader.close()
    f.close()
    logging.info('Merging Done >> '+OutputFileName)
    return True
def PrepareLog(OutputFolder,SubJobIndex):
    LOG_FILENAME = OutputFolder+'/merging_logfile.'+str(SubJobIndex)+'.log'
    TAOLoger = logging.getLogger() 
    TAOLoger.setLevel(logging.DEBUG)      
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    TAOLoger.addHandler(handler)
    return TAOLoger
def ProcessFiles(FilesList,OutputFileName):
    logging.info("## Start Process Files ...") 
    logging.info("## Merging files with extension :"+FilesList[0].split('.')[-2])
    logging.info(FilesList)
    if FilesList[0].split('.')[ExtensionLocation]=='csv':        
        return HandleCSVFiles(FilesList,OutputFileName)
    elif FilesList[0].split('.')[ExtensionLocation]=='xml':
        return HandleVOFiles(FilesList,OutputFileName)
    elif FilesList[0].split('.')[ExtensionLocation]=='fits':
        return HandleFITSFiles(FilesList,OutputFileName)
    elif FilesList[0].split('.')[ExtensionLocation]=='hdf5':
        return HandleHDF5Files(FilesList,OutputFileName)
    else:
        logging.info("This Format is not Known for me ! "+FilesList[0].split('.')[-2])
    logging.info("## End Process Files ...") 
def RemoveFiles(FilesList):
    logging.info("Removing Files:") 
    logging.info(FilesList)
    for DataFile in FilesList:
        logging.info("Delete File:"+DataFile)
        os.remove(DataFile)
def CompressFile(CurrentFolderPath,OutputFileName,JobIndex):
    InputFileName=OutputFileName.replace(CurrentFolderPath,"")
    InputFileName=InputFileName.strip('/')
    CompressedFileName=InputFileName+".tar.gz"
    os.chdir(CurrentFolderPath)    
    #stdout = subprocess.check_output(shlex.split('tar -czf \"%s\" \"%s\"'%(CompressedFileName,InputFileName)))
    stdout = subprocess.check_output(shlex.split('gzip \"%s\"'%(InputFileName)))
    #os.remove(InputFileName)    
               
if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(-100);
    CurrentFolderPath=sys.argv[1]
    CurrentLogPath=sys.argv[1].replace("/output","/log")
    SubJobIndex=sys.argv[2]
    JobIndex=sys.argv[3]
    TAOLoger=PrepareLog(CurrentLogPath,SubJobIndex) 
    logging.info('Merging Files in '+CurrentFolderPath)   
    dirList=os.listdir(CurrentFolderPath)    
    fullPathArray=[]
    
    SubJobIndexLocation=2
    
    map={}
    for fname in dirList:
        FileDetailsList=fname.split('.')
        if len(FileDetailsList)>=5 and FileDetailsList[-1]!='gz':            
            fullPathArray.append([CurrentFolderPath+'/'+fname,FileDetailsList])
            logging.info('File Added to List '+CurrentFolderPath+'/'+fname)
            if FileDetailsList[SubJobIndexLocation] in map:
                map[FileDetailsList[SubJobIndexLocation]].append(CurrentFolderPath+'/'+fname)
            else:
                map[FileDetailsList[SubJobIndexLocation]]=[CurrentFolderPath+'/'+fname]
                
    if ValidateAllSameExtension(fullPathArray,SubJobIndexLocation)!=True:  
        logging.info('Validating File List Failed')      
        exit(-100)
    
    
    logging.info('Merging Output for sub-task ['+str(str(SubJobIndex))+']')
    FilesList=map[str(SubJobIndex)]
    FilesList.sort()  
    FileNameParts=FilesList[0].replace(".output.","."+str(JobIndex)+".").split('.')[0:-1]    
    OutputFileName=".".join(FileNameParts)
    
    if (ProcessFiles(FilesList,OutputFileName)==True):        
        CompressFile(CurrentFolderPath,OutputFileName,JobIndex)
        
        RemoveFiles(FilesList)
        
       
    
        

    
                
