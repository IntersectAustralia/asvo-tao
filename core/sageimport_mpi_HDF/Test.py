import DBConnection
import settingReader # Read the XML settings
import logging,os
import PreprocessData # Perform necessary pre-processing (e.g. Create Tables)

def SetupLogFile():
    FilePath='logfile.log'
    if os.path.exists(FilePath):
        os.remove(FilePath)
    logging.basicConfig(filename=FilePath,level=logging.DEBUG,format='%(asctime)s %(message)s')

def TestDbConnection(CurrentSAGEStruct,Options):
    
    print("Start Database Connection Test!")
    
    DBConnectionObj=DBConnection.DBConnection(Options,True)
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("CREATE Database "+Options['PGDB:NewDBName']+";")
    DBConnectionObj.CloseConnections()
    DBConnectionObj=DBConnection.DBConnection(Options,False)
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("CREATE Table TestTable(JobID INTEGER,JOBName VARCHAR(500));")
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("Insert into TestTable values(%(id)s,%(name)s);",{'id':1,'name':'Test1'})
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("Insert into TestTable values(%(id)s,%(name)s);",{'id':2,'name':'Test2'})
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("Insert into TestTable values(%(id)s,%(name)s);",{'id':3,'name':'Test3'})
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("Insert into TestTable values(%(id)s,%(name)s);",{'id':4,'name':'Test4'})
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("Insert into TestTable values(%(id)s,%(name)s);",{'id':5,'name':'Test5'})
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("Insert into TestTable values(%(id)s,%(name)s);",{'id':6,'name':'Test6'})
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("Insert into TestTable values(%(id)s,%(name)s);",{'id':7,'name':'Test7'})
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("Insert into TestTable values(%(id)s,%(name)s);",{'id':8,'name':'Test8'})
    
    
    Restults=DBConnectionObj.ExecuteQuerySQLStatment("Select * from  TestTable;")
    print("Testing Dictionary Usage")
    print Restults[0]['jobname']
    print("Testing List Usage")
    print Restults
    
    DBConnectionObj.CloseConnections()
    DBConnectionObj=DBConnection.DBConnection(Options,True)
    DBConnectionObj.ExecuteNoQuerySQLStatment_On_AllServers("DROP Database "+Options['PGDB:NewDBName']+";")
    DBConnectionObj.CloseConnections()
    
    print("Database Connection Test Done!")


def testpreprocessing(CurrentSAGEStruct,Options):
    PreprocessDataObj=PreprocessData.PreprocessData(CurrentSAGEStruct,Options)
    ## 2) Open connection to the DB (ToMasterDB=True - Open connection to a default DB before creating the new DB)
    PreprocessDataObj.InitDBConnection(True)
    print("Init DB Connection ...Done")        
    ## 3) Create New DB (If a DB with the same name exists user will be asked if he want to drop it)
    PreprocessDataObj.CreateDB()
    print("Create DB ....Done")
    ## 4) a) Create "DataFiles" Table
    ##    b) read the header of each file and fill the table with the metadata ( the initial status of all the files is un-processed)
    ##    c) Each table will have an associated Table ID in this step 
    print("Start Preprocessing ...")
    PreprocessDataObj.FillTreeProcessingTable()
    print("End Preprocessing ...")
    ## 6) Close the DB connection
    PreprocessDataObj.DBConnection.CloseConnections()

if __name__ == '__main__':
    
    SetupLogFile()
    SettingFile="mill_mini_2servers_setting.xml"
    
    [CurrentSAGEStruct,Options]=settingReader.ParseParams(SettingFile)
    Options['PGDB:NewDBName']="testdb"
    testpreprocessing(CurrentSAGEStruct,Options)
    
    
    
    
    
    