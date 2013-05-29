import string
import sys,os # for listing directory contents
import time,shutil

def ProcessFolder(SourceFolder,DestinationFolder):
    dirList=os.listdir(SourceFolder)    
    for fname in dirList: 
        SrcObjectName=SourceFolder+'/'+fname 
        DestObjectName=DestinationFolder+'/'+fname.lower()
        
        if os.path.isdir(SrcObjectName):
            print("DIR :"+SrcObjectName)
            if os.path.exists(DestObjectName)==False:
                os.makedirs(DestObjectName)
            ProcessFolder(SrcObjectName, DestObjectName)
        else:
            print("File :"+SrcObjectName)
            if os.path.exists(DestObjectName)==False:
                shutil.copyfile(SrcObjectName, DestObjectName)
            else:
                print("====> File Name Duplication Detected :")
                print("====> Source FileName:"+SrcObjectName)
                print("====> Destination FileName:"+DestObjectName)
                
                print("====> Import Aborted! Please resolve this issue before re-try importing.")
                exit()
            
        
        
    
    
if __name__ == '__main__':
    
    if len(sys.argv)<3:
        print("Sorry, you didn't supply enough paramters. Expected paramters are:")
        print("(1) Source Folder")
        print("(2) Destination Folder")        
        exit()
    
    SourceFolder=sys.argv[1]
    DestinationFolder=sys.argv[2]
    
    ProcessFolder(SourceFolder, DestinationFolder)
    
    
    
    
    