'''
Created on 28/09/2012
Main File
Execute the importing code 
@author: Amr Hassan
'''
## Import Helper modules
import string
import sys # for listing directory contents
from mpi4py import MPI # MPI Implementation
import time

import SAGEReader # Read the SAGE Files into memory
import settingReader # Read the XML settings
import PGDBInterface # Interaction with the postgreSQL DB
import preprocessfiles # Perform necessary pre-processing (e.g. Create Tables)
import AnalyzeTables
import UpdateMasterTables
import DBConnection


if __name__ == '__main__':
    
    ## MPI already initiated in the import statement
    ## Get The current Process Rank and the total number of processes
    start= time.clock()  
    comm = MPI.COMM_WORLD
    CommRank = comm.Get_rank()
    
    CommSize= comm.Get_size()
    
    if CommRank==0:
        print('SAGE Data Importing Tool ( MPI version)')
    
    #print("MPI Starting .... My Rank is: "+str(CommRank)+"/"+str(CommSize))
    
    
    ##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Serial Section $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    
    ### Read Running Settings
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml")
    
    ## This section will be executed only by the server ... All the nodes must wait until this is performed
    if CommRank==0:
        
        print("Server: Start Pre-processing files ...")
        sys.stdout.write("\033[0;33m"+"Do you want me to re-generate the files list and the DB (y/n)?\033[0m\n")
        sys.stdout.flush()
        RegenerateFileList=string.lower(sys.stdin.readline()).strip()
        
        #################### Preprocessing data files for the first time #####################################
        ################### This will import the files metadata into a DB table and create the new DB ######## 
        if RegenerateFileList=='y':
            sys.stdout.write("Pre-processing data\n")
            sys.stdout.flush()
            ## 1) Init the class with DB option 
            PreprocessFilesObj=preprocessfiles.PreprocessFiles(CurrentSAGEStruct,Options)
            ## 2) Open connection to the DB (ToMasterDB=True - Open connection to a default DB before creating the new DB)
            PreprocessFilesObj.InitDBConnection(True)
            ## 3) Get List of data files where the file size is > 0 byte
            PreprocessFilesObj.GetNonEmptyFilesList()
            ## 4) Create New DB (If a DB with the same name exists user will be asked if he want to drop it)
            PreprocessFilesObj.CreateDB()
            ## 5) a)Create "DataFiles" Table
            ##    b) read the header of each file and fill the table with the metadata ( the initial status of all the files is un-processed)
            ##    c) Each table will have an associated Table ID in this step 
            PreprocessFilesObj.ProcessAllFiles()
            ## 6) Close the DB connection
            PreprocessFilesObj.DBConnection.CloseConnections()
            
        ######################################################################################################
        if RegenerateFileList!='y':
            # Ask Him only if he refuse to re-generate the files list.            
            sys.stdout.write("Do you want me to re-generate all the tables (y/n)\n")
            sys.stdout.flush()
            RegenerateFileList=string.lower(sys.stdin.readline()).strip()
            
        if RegenerateFileList=='y':
            ## 1) Init Class
            PreprocessFilesObj=preprocessfiles.PreprocessFiles(CurrentSAGEStruct,Options)
            ## 2) Open Database connection
            PreprocessFilesObj.InitDBConnection(False)
            ## 3) Create All tables required for the importing of the current dataset using the information in "DataFiles" table 
            PreprocessFilesObj.GenerateAllTables()
            ## 4) Close the DB connection
            PreprocessFilesObj.DBConnection.CloseConnections()
    
        ## Tell All the other processes that we are done and will start processing
        Mesg={"ProcessingDone":True}
        for i in range(1,CommSize):
            comm.send(Mesg,dest=i)    
    ##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ MPI Section $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    else:
        ## Wait for the server to finish - 
        #The server will send the message only if he did all the needed pre-processing or if the user don't want re-generate the files list
        
        #print(str(CommRank)+":Waiting for the Server to finish pre-processing the files .... ")
        #sys.stdout.flush()
        Mesg=comm.recv(source=0)
        #print(str(CommRank)+": Message Recieved ....")
        
        
    
    sys.stdout.flush()
        
    ## Open Connection to Postgres
    CurrentPGDB=PGDBInterface.DBInterface(CurrentSAGEStruct,Options,CommRank)
    ## Init files reader
    Reader=SAGEReader.SAGEDataReader(CurrentSAGEStruct,Options,CurrentPGDB,CommSize,CommRank)
    ## Start Processing the files
    ## This will get all unprocessed file and distribute them using Modulus operator
    Reader.ProcessAllFiles()
    
    ## All data imported ... Processing done 
    
    if CommRank!=0:
        Mesg={"ImportProcessingDone":True}
        comm.send(Mesg,dest=0)
    
    
    ## Analyze Tables Batch processing to Complete BSP missing Information
    if CommRank==0:
        print("Process (Server): Waiting for other Nodes to Finish ...")
        for i in range(1,CommSize):
            Mesg=comm.recv(source=i)
             
        print("Process (Server): All Nodes Finish ...")
            
        print('Starting PostProcessing: Generate Tables Statistics and BSP Tree Information')
        ProcessTablesObj=AnalyzeTables.ProcessTables(Options)
        ProcessTablesObj.GetTablesList()
    
        ProcessTablesObj.SummarizeLocationInfo()  
        ProcessTablesObj.ValidateImportProcess()       
        ProcessTablesObj.CloseConnections()
    
        MasterTablesUpdateObj=UpdateMasterTables.MasterTablesUpdate(Options,CurrentPGDB)
        MasterTablesUpdateObj.CreateRedshiftTable()
        MasterTablesUpdateObj.FillRedshiftData()
        MasterTablesUpdateObj.CreateMetadataTable()
        MasterTablesUpdateObj.FillMetadataTable()
        end= time.clock()
        sys.stdout.write("\033[0;33m"+str(CommRank)+": Total Processing Time="+str((end-start))+" seconds\033[0m\n")
        sys.stdout.flush()
        
    
    
    
    CurrentPGDB.CloseConnections()
    print(str(CommRank)+':Processing Done')