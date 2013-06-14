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
import PreprocessData # Perform necessary pre-processing (e.g. Create Tables)
import AnalyzeTables
import UpdateMasterTables
import logging
import os
import SetupNewDatabase

def SetupLogFile(CommRank):
    FilePath='log/logfile'+str(CommRank)+'.log'
    if os.path.exists(FilePath):
        os.remove(FilePath)
    logging.basicConfig(filename=FilePath,level=logging.DEBUG,format='%(asctime)s %(message)s')



if __name__ == '__main__':
    
    if len(sys.argv)<2:
        print("Error Not Enough Arguments")
        exit()
    SettingFile=sys.argv[1]
    
    ## MPI already initiated in the import statement
    ## Get The current Process Rank and the total number of processes
    start= time.clock()  
    comm = MPI.COMM_WORLD
    CommRank = comm.Get_rank()
    
    CommSize= comm.Get_size()
    
    
    SetupLogFile(CommRank)
    
    if CommRank==0:
        logging.info('SAGE Data Importing Tool ( MPI version)')
    
    #logging.info("MPI Starting .... My Rank is: "+str(CommRank)+"/"+str(CommSize))
    
    
    ##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Serial Section $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    
    ### Read Running Settings
    [CurrentSAGEStruct,Options]=settingReader.ParseParams(SettingFile)
    
     ## 1) Init the class with DB option 
    PreprocessDataObj=PreprocessData.PreprocessData(CurrentSAGEStruct,Options)
    ## 2) Open connection to the DB (ToMasterDB=True - Open connection to a default DB before creating the new DB)
    PreprocessDataObj.InitDBConnection(True)        
    ## 3) Create New DB (If a DB with the same name exists user will be asked if he want to drop it)
    
    
    ## This section will be executed only by the server ... All the nodes must wait until this is performed
    if CommRank==0:   
        
        PreprocessDataObj.CreateDB()    
         
        logging.info("Generate Tables")                    
        
        ## 3) Create All tables required for the importing of the current dataset using the information in "DataFiles" table
        PreprocessDataObj.GenerateAllTables()
        ## 4) Close the DB connection
        PreprocessDataObj.DBConnection.CloseConnections()
    
        ## Tell All the other processes that we are done and will start processing
    logging.info("Reaching First Barrier")
    comm.Barrier()
    logging.info("Barrier Released")    
        
    PreprocessDataObj.InitDBConnection(False) 
    ## 4) a) Create "DataFiles" Table
    ##    b) read the header of each file and fill the table with the metadata ( the initial status of all the files is un-processed)
    ##    c) Each table will have an associated Table ID in this step 
    PreprocessDataObj.FillTreeProcessingTable(CommSize,CommRank)
    ## 6) Close the DB connection
    PreprocessDataObj.DBConnection.CloseConnections()
    logging.info("Reaching Second Barrier")
    comm.Barrier()
    logging.info("Barrier Released")    
        
    
            
    ## Open Connection to Postgres
    CurrentPGDB=PGDBInterface.DBInterface(CurrentSAGEStruct,Options,CommRank)
    ## Init files reader
    Reader=SAGEReader.SAGEDataReader(CurrentSAGEStruct,Options,CurrentPGDB,CommSize,CommRank)
    ## Start Processing the files
    ## This will get all unprocessed file and distribute them using Modulus operator
    Reader.ProcessAllTrees()
    
    ## All data imported ... Processing done 
    
    logging.info("Reaching Third Barrier")
    comm.Barrier()
    logging.info("Barrier Released")    
    
    
    ## Analyze Tables Batch processing to Complete BSP missing Information
    if CommRank==0:  
        
             
        logging.info("Process (Server): All Nodes Finish ...")
        logging.info("Process (Server): Generating Index on All tables ...")
        RegenerateTablesList=Options["RunningSettings:RegenerateTables"]
        if RegenerateTablesList=='yes':
            ## 1) Init Class
            PreprocessDataObj=PreprocessData.PreprocessData(CurrentSAGEStruct,Options)
            ## 2) Open Database connection
            PreprocessDataObj.InitDBConnection(False)
            ## 3) Create All tables required for the importing of the current dataset using the information in "DataFiles" table
            PreprocessDataObj.GenerateTablesIndex()
            ## 4) Close the DB connection
            PreprocessDataObj.DBConnection.CloseConnections()
        
        logging.info("Process (Server): End Generating Index on All tables ...")
        
            
        logging.info('Starting PostProcessing: Generate Tables Statistics and BSP Tree Information')
        ProcessTablesObj=AnalyzeTables.ProcessTables(Options)
        for si in range(0,ProcessTablesObj.DBConnection.serverscount):
            ProcessTablesObj.GetTablesList(si)
    
        ProcessTablesObj.SummarizeLocationInfo()  
        #ProcessTablesObj.ValidateImportProcess()       
        ProcessTablesObj.CloseConnections()
    
        MasterTablesUpdateObj=UpdateMasterTables.MasterTablesUpdate(Options,CurrentPGDB)
        MasterTablesUpdateObj.CreateRedshiftTable()
        MasterTablesUpdateObj.FillRedshiftData()
        MasterTablesUpdateObj.CreateMetadataTable()
        MasterTablesUpdateObj.FillMetadataTable()
        end= time.clock()
        logging.info(str(CommRank)+": Total Processing Time="+str((end-start))+" seconds")
        SetupNewDatabaseObj= SetupNewDatabase.SetupNewDatabase(Options,CurrentSAGEStruct)
        SetupNewDatabaseObj.SetNewDatabase()
        
    
    
    
    CurrentPGDB.CloseConnections()
    logging.info(str(CommRank)+':Processing Done')
    