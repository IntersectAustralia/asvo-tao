'''
Created on 28/09/2012

@author: Amr Hassan
'''
import SAGEReader
import settingReader
import PGDBInterface
import preprocessfiles
import string

if __name__ == '__main__':
    
    ### Read Running Settings
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml")
    
    print('SAGE Data Importing Tool ( MPI version)')
    userselection=string.lower(raw_input("Do you want me to regenerate the files list and the DB (y/n)"))
    #################### Preprocessing data files for the first time #####################################
    ################### This will import the files metadata into a DB table and create the new DB ######## 
    if userselection=='y':
        print("Preprocessing data")
        PreprocessFilesObj=preprocessfiles.PreprocessFiles(CurrentSAGEStruct,Options)
        PreprocessFilesObj.InitDBConnection(True)
        PreprocessFilesObj.GetNonEmptyFilesList()
        PreprocessFilesObj.CreateDB()
        PreprocessFilesObj.ProcessAllFiles()
        PreprocessFilesObj.CloseConnections()
        
    ######################################################################################################
    userselection=string.lower(raw_input("Do you want me to regenerate all the tables (y/n)"))
    if userselection=='y':
        PreprocessFilesObj=preprocessfiles.PreprocessFiles(CurrentSAGEStruct,Options)
        PreprocessFilesObj.InitDBConnection(False)
        PreprocessFilesObj.GenerateAllTables()
        PreprocessFilesObj.CloseConnections()
    ## Open Connection to Postgres
    CurrentPGDB=PGDBInterface.DBInterface(CurrentSAGEStruct,Options)
    ## Init files reader
    Reader=SAGEReader.SAGEDataReader(CurrentSAGEStruct,Options,CurrentPGDB)
    ## Start Processing the files
    Reader.ProcessAllFiles()
    CurrentPGDB.CloseConnections()
    ## All data imported ... Processing done 
    print('Processing Done')