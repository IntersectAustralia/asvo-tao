'''
Created on 28/09/2012
Main File
Execute the importing code 
@author: Amr Hassan
'''
## Import Helper modules
import string
import sys # for listing directory contents

import time


import DataReader # Read the SAGE Files into memory
import settingReader # Read the XML settings
import PGDBInterface # Interaction with the postgreSQL DB
import PreprocessData # Perform necessary pre-processing (e.g. Create Tables)
import UpdateMasterTables
import logging
import os
import SetupNewDatabase

def SetupLogFile():
    FilePath='log/logfile.log'
    if os.path.exists(FilePath):
        os.remove(FilePath)
    logging.basicConfig(filename=FilePath,level=logging.DEBUG,format='%(asctime)s %(message)s')



if __name__ == '__main__':
    
    if len(sys.argv)<2:
        print("Error Not Enough Arguments")
        exit()
    SettingFile=sys.argv[1]
    ResumeProcessing=True
    if len(sys.argv)==3:
        ResumeProcessing=(sys.argv[1]=='True')
    
    ## MPI already initiated in the import statement
    ## Get The current Process Rank and the total number of processes
    start= time.clock()  
    
    
    SetupLogFile()
    
    
    logging.info('TAO Data Importing Tool ( Single Thread version)')   
    
    ### Read Running Settings
    [CurrentSAGEStruct,Options]=settingReader.ParseParams(SettingFile)    
     ## 1) Init the class with DB option 
    PreprocessDataObj=PreprocessData.PreprocessData(CurrentSAGEStruct,Options)
    ## 2) Open connection to the DB (ToMasterDB=True - Open connection to a default DB before creating the new DB)
    PreprocessDataObj.InitDBConnection(True)        
    ## 3) Create New DB (If a DB with the same name exists user will be asked if he want to drop it)
       
    ## This section will be executed only by the server ... All the nodes must wait until this is performed
       
        
    PreprocessDataObj.CreateDB()    
         
    logging.info("Generate Tables")                    
        
    ## 3) Create All tables required for the importing of the current dataset using the information in "DataFiles" table
    PreprocessDataObj.GenerateAllTables()
        ## 4) Close the DB connection
    PreprocessDataObj.DBConnection.CloseConnections()
    
    ## Tell All the other processes that we are done and will start processing
        
    PreprocessDataObj.InitDBConnection(False) 
    ## 4) a) Create "DataFiles" Table
    ##    b) read the header of each file and fill the table with the metadata ( the initial status of all the files is un-processed)
    ##    c) Each table will have an associated Table ID in this step 
    PreprocessDataObj.FillTreeProcessingTable(CommSize,CommRank)
    ## 6) Close the DB connection
    
    PreprocessDataObj.AddTreeProcessingIndex()  
        
      
    PreprocessDataObj.DBConnection.CloseConnections()
            
    ## Open Connection to Postgres
    CurrentPGDB=PGDBInterface.DBInterface(CurrentSAGEStruct,Options,CommRank)
    ## Init files reader
    Reader=DataReader.DataReader(CurrentSAGEStruct,Options,CurrentPGDB,CommSize,CommRank)
    ## Start Processing the files
    ## This will get all unprocessed file and distribute them using Modulus operator
    Reader.ProcessAllTrees()
    
   
        
             
    RegenerateTablesList=Options["RunningSettings:RegenerateTables"]
    
    ## 1) Init Class
    PreprocessDataObj=PreprocessData.PreprocessData(CurrentSAGEStruct,Options)
    ## 2) Open Database connection
    PreprocessDataObj.InitDBConnection(False)
    ## 3) Create All tables required for the importing of the current dataset using the information in "DataFiles" table
    PreprocessDataObj.CreateIndexOnTreeSummaryTable()
    PreprocessDataObj.GenerateTablesIndex(CommSize,CommRank)
    ## 4) Close the DB connection
    PreprocessDataObj.DBConnection.CloseConnections()
        
        
        
        
               
            
    MasterTablesUpdateObj=UpdateMasterTables.MasterTablesUpdate(Options,CurrentPGDB)
    MasterTablesUpdateObj.CreateRedshiftTable()
    MasterTablesUpdateObj.FillRedshiftData()
    MasterTablesUpdateObj.CreateMetadataTable()
    MasterTablesUpdateObj.FillMetadataTable()
    MasterTablesUpdateObj.SetupSecurity()
        
    
    
    
    end= time.clock()
    logging.info(str(CommRank)+": Total Processing Time="+str((end-start))+" seconds")
    SetupNewDatabaseObj= SetupNewDatabase.SetupNewDatabase(Options,CurrentSAGEStruct)
    SetupNewDatabaseObj.SetNewDatabase()
        
    
    
    
    CurrentPGDB.CloseConnections()
    logging.info(str(CommRank)+':Processing Done')
    