import sys,os

import string
from distutils.filelist import FileList
import logging, logging.handlers

def ValidateAllSameExtension(FilesList):
    logging.info('Start Validating File List (Length and Extension)')
    if len(FilesList)==0:
        return False
    
    FirstItemExt=FilesList[0][1][-2]
    FileExtLen=len(FilesList[0][1])
    for FileDetail in FilesList:
        if(FileDetail[1][-2]!=FirstItemExt) or (FileExtLen!= len(FileDetail[1])):                        
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
def PrepareLog(OutputFolder):
    LOG_FILENAME = OutputFolder+'/logfile.log'
    TAOLoger = logging.getLogger() 
    TAOLoger.setLevel(logging.DEBUG)      
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    TAOLoger.addHandler(handler)
    return TAOLoger    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit(-100);
    CurrentFolderPath=sys.argv[1]
    SubJobIndex=sys.argv[2]
    TAOLoger=PrepareLog(CurrentFolderPath) 
    logging.info('Merging Files in '+CurrentFolderPath)   
    dirList=os.listdir(CurrentFolderPath)    
    fullPathArray=[]
    map={}
    for fname in dirList:
        FileDetailsList=fname.split('.')
        if len(FileDetailsList)==5:            
            fullPathArray.append([CurrentFolderPath+'/'+fname,FileDetailsList])
            logging.info('File Added to List '+CurrentFolderPath+'/'+fname)
            if FileDetailsList[2] in map:
                map[FileDetailsList[2]].append(CurrentFolderPath+'/'+fname)
            else:
                map[FileDetailsList[2]]=[CurrentFolderPath+'/'+fname]
                
    if ValidateAllSameExtension(fullPathArray)!=True:  
        logging.info('Validating File List Failed')      
        exit(-100)
    
    
    logging.info('Merging Output for sub-task ['+str(str(SubJobIndex))+']')
    FilesList=map[str(SubJobIndex)]
    FilesList.sort()        
    OutputFileName=".".join(FilesList[0].split('.')[0:-1])
    if FilesList[0].split('.')[-2]=='csv':        
        HandleCSVFiles(FilesList,OutputFileName)
    elif FilesList[0].split('.')[-2]=='xml':
        HandleVOFiles(FilesList,OutputFileName)
        
       
    
        

    
                