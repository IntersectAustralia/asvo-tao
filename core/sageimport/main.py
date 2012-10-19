'''
Created on 28/09/2012

@author: Amr Hassan
'''
import SAGEReader
import settingReader
import MySQlDBInterface

if __name__ == '__main__':
    print('Starting Files Loading')
    
    ### Read Running Settings
    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml")
    ## Open Connection to MySQL
    CurrentMySQlDB=MySQlDBInterface.DBInterface(CurrentSAGEStruct,Options)
    ## Init files reader
    Reader=SAGEReader.SAGEDataReader(CurrentSAGEStruct,Options,CurrentMySQlDB)
    ## Start Processing the files
    Reader.ProcessAllFiles()
    CurrentMySQlDB.Close()
    ## All data imported ... Processing done 
    print('Processing Done')