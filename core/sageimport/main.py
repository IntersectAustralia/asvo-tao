'''
Created on 28/09/2012

@author: Amr Hassan
'''
import SAGEReader
import settingReader

if __name__ == '__main__':
    print('Starting Files Loading')
    

    [CurrentSAGEStruct,Options]=settingReader.ParseParams("settings.xml")
    Reader=SAGEReader.SAGEDataReader(CurrentSAGEStruct,Options)
    Reader.ProcessAllFiles()
    print('Processing Done')