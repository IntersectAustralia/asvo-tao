'''
Created on 28/09/2012

@author: Amr Hassan
'''
import SAGEReader
import settingReader
import PGDBInterface
import preprocessfiles
import string
import sys
from mpi4py import MPI

if __name__ == '__main__':
    
    
    comm = MPI.COMM_WORLD
    CommRank = comm.Get_rank()
    
    CommSize= comm.Get_size()
    print('SAGE Data Importing Tool ( MPI version)')
    
    print("MPI Starting .... My Rank is: "+str(CommRank)+"/"+str(CommSize))
    ##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Serial Section $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    ### Read Running Settings
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml")
    
    
    if CommRank==0:
        
        print("Server: Start Pre-processing files ...")
        sys.stdout.write("Do you want me to re-generate the files list and the DB (y/n)")
        sys.stdout.flush()
        RegenerateFileList=string.lower(sys.stdin.readline())
        
        #################### Preprocessing data files for the first time #####################################
        ################### This will import the files metadata into a DB table and create the new DB ######## 
        if RegenerateFileList=='y':
            print("Pre-processing data")
            PreprocessFilesObj=preprocessfiles.PreprocessFiles(CurrentSAGEStruct,Options)
            PreprocessFilesObj.InitDBConnection(True)
            PreprocessFilesObj.GetNonEmptyFilesList()
            PreprocessFilesObj.CreateDB()
            PreprocessFilesObj.ProcessAllFiles()
            PreprocessFilesObj.CloseConnections()
            
        ######################################################################################################
        if RegenerateFileList!='y':
            # Ask Him only if he refuse to re-generate the files list.            
            sys.stdout.write("Do you want me to re-generate all the tables (y/n)")
            sys.stdout.flush()
            RegenerateFileList=string.lower(sys.stdin.readline())
            
        if RegenerateFileList=='y':
            PreprocessFilesObj=preprocessfiles.PreprocessFiles(CurrentSAGEStruct,Options)
            PreprocessFilesObj.InitDBConnection(False)
            PreprocessFilesObj.GenerateAllTables()
            
            PreprocessFilesObj.CloseConnections()
    
        ## Tell All the other proceses that we are done and will start processing
        Mesg={"ProcessingDone":True}
        for i in range(1,CommSize):
            comm.send(Mesg,dest=i)    
    ##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ MPI Section $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    else:
        ## Wait for the server to finish - 
        #The server will send the message only if he did all the needed pre-processing or if the user don't want re-generate the files list
        
        print(str(CommRank)+":Waiting for the Server to finish pre-processing the files .... ")
        sys.stdout.flush()
        Mesg=comm.recv(source=0)
        print(str(CommRank)+": Message Recieved ....")
        
        
    #print("I'm ready to start... Press Any key to start ...")
    sys.stdout.flush()
    #sys.stdin.readline()    
    ## Open Connection to Postgres
    CurrentPGDB=PGDBInterface.DBInterface(CurrentSAGEStruct,Options)
    ## Init files reader
    Reader=SAGEReader.SAGEDataReader(CurrentSAGEStruct,Options,CurrentPGDB,CommSize,CommRank)
    ## Start Processing the files
    Reader.ProcessAllFiles()
    CurrentPGDB.CloseConnections()
    ## All data imported ... Processing done 
    print('Processing Done')