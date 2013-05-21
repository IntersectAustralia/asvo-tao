import os,string,sys
import settingReader # Read the XML settings
import DBConnection
import shlex, subprocess

def MoveTable(TableName,TableDBservers,DBConnection,CurrentSAGEStruct,Options):
    
    if(len(TableDBservers)==DBConnection.serverscount):
        print("Sorry , moving will not be possible in this case! Your table already in all database servers! ")
        return 
    DBName=Options['PGDB:NewDBName']
    print("Where do you want to move this table:")
    for i in range(0,DBConnection.serverscount):
        if i not in TableDBservers:
            print("("+str(i+1)+"): "+ DBConnection.DBservers[i]['serverip'])
    DestinationServerID=int(raw_input("Enter Server ID: "))-1
    print( "Moving Table "+TableName+ " To "+DBConnection.DBservers[DestinationServerID]['serverip'])
    
    SourceDbServer=DBConnection.DBservers[TableDBservers[0]]
    DestinationDbServer=DBConnection.DBservers[DestinationServerID]
    
    print("Step 1: Coping the table from "+SourceDbServer['serverip']+ " To "+DestinationDbServer['serverip'])    
    
    MoveTableStmt="pg_dump -p "+str(SourceDbServer['port'])+" -U "+SourceDbServer['username']+" --host="+SourceDbServer['serverip']+" -t "+TableName+" "+DBName+" | psql -p "+str(DestinationDbServer['port'])+" -U "+DestinationDbServer['username']+" --host="+DestinationDbServer['serverip']+" "+DBName
    stdout = os.system(MoveTableStmt)
    
    print("Step 1: Done")
    
    print("Step 2: Update Table Mapping")
    for i in TableDBservers:
        UpdateStmt="DELETE From table_db_mapping where TableName=\'"+TableName+"\'; Insert into table_db_mapping values(\'"+TableName+"\',\'"+DestinationDbServer['serverip']+"\',True ) ;"        
        DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(UpdateStmt)
    print("Step 2: Done")    
    
    print("Step 3: Drop the table from "+SourceDbServer['serverip'])
    
    DropStmt="Drop Table "+TableName+";"
    for i in TableDBservers:
        DBConnection.ExecuteNoQuerySQLStatment(DropStmt,i)
    
    print("Moving Table Done Successfully!")
    
def DropTable(TableName,TableDBservers,DBConnection,CurrentSAGEStruct,Options):
    
    
    DBName=Options['PGDB:NewDBName']
    print("From where do you want to drop this table:")
    for i in range(0,DBConnection.serverscount):
        if i in TableDBservers:
            print("("+str(i+1)+"): "+ DBConnection.DBservers[i]['serverip'])
    
    DestinationServerID=int(raw_input("Enter Server ID: "))-1
    print( "Dropping Table "+TableName+ " From "+DBConnection.DBservers[DestinationServerID]['serverip'])
    
    
    DestinationDbServer=DBConnection.DBservers[DestinationServerID]
       
    
    
    print("Step 1: Update Table Mapping")
    for i in TableDBservers:
        UpdateStmt="DELETE From table_db_mapping where TableName=\'"+TableName+"\' and nodename=\'"+DestinationDbServer['serverip']+"\' ;"        
        DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(UpdateStmt)
    print("Step 1: Done")    
    
    print("Step 2: Drop the table from "+DestinationDbServer['serverip'])
    
    DropStmt="Drop Table "+TableName+";"
    DBConnection.ExecuteNoQuerySQLStatment(DropStmt,DestinationServerID)
    
    print("Dropping Table Done Successfully!")   
    
    
    
    
    
def ReplicateTable(TableName,TableDBservers,DBConnection,CurrentSAGEStruct,Options):
    print("Replicate Table Parameters:")

    if(len(TableDBservers)==DBConnection.serverscount):
        print("Sorry , replication will not be possible in this case! Your table already in all database servers! ")
        return 
    DBName=Options['PGDB:NewDBName']
    print("Where do you want to replicate this table:")
    for i in range(0,DBConnection.serverscount):
        if i not in TableDBservers:
            print("("+str(i+1)+"): "+ DBConnection.DBservers[i]['serverip'])
    DestinationServerID=int(raw_input("Enter Server ID: "))-1
    print( "Copying Table "+TableName+ " To "+DBConnection.DBservers[DestinationServerID]['serverip'])
    
    SourceDbServer=DBConnection.DBservers[TableDBservers[0]]
    DestinationDbServer=DBConnection.DBservers[DestinationServerID]
    
    print("Step 1: Coping the table from "+SourceDbServer['serverip']+ " To "+DestinationDbServer['serverip'])    
    
    MoveTableStmt="pg_dump -p "+str(SourceDbServer['port'])+" -U "+SourceDbServer['username']+" --host="+SourceDbServer['serverip']+" -t "+TableName+" "+DBName+" | psql -p "+str(DestinationDbServer['port'])+" -U "+DestinationDbServer['username']+" --host="+DestinationDbServer['serverip']+" "+DBName
    stdout = os.system(MoveTableStmt)
    
    print("Step 1: Done")
    
    print("Step 2: Update Table Mapping")
    for i in TableDBservers:
        UpdateStmt="Insert into table_db_mapping values(\'"+TableName+"\',\'"+DestinationDbServer['serverip']+"\',True ) ;"        
        DBConnection.ExecuteNoQuerySQLStatment_On_AllServers(UpdateStmt)
        
    
        
    print("Replicate Table Done Successfully!")
    


def GetTableInformation(TableName,DBConnection):
    TableDBservers=[]
    SelectStm='SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\' and table_name=\''+TableName+'\';'
    IsInAnyDB=False
    for i in range(0,DBConnection.serverscount):
        
        Results=DBConnection.ExecuteQuerySQLStatment(SelectStm,i);
        if(Results != None and len(Results)>0):
            print("Table in Database : "+DBConnection.DBservers[i]['serverip'])
            IsInAnyDB=True
            TableDBservers.append(i)
    if IsInAnyDB==False:
        print('Table does not exist in any of the database I\'m currently connected to!')        
    
    return [IsInAnyDB,TableDBservers]    
        
if __name__ == '__main__':
    
    
    FunctionsMap={
                 'movetable':MoveTable,
                 'replicatetable':ReplicateTable,
                 'droptable':DropTable
                 }
    
    
    if len(sys.argv)<3:
        print("Error Not Enough Arguments")
        print("Param 1: Setting File Path")
        print("Param 2: Command to be Executed")
        exit()
    SettingFile=sys.argv[1]
    Command=sys.argv[2].lower()
    print('MultiDB Management Tools:')
    print('Current Select Operation: '+Command)
    print('Using DB Information from setting File: '+SettingFile)   
    
    [CurrentSAGEStruct,Options]=settingReader.ParseParams(SettingFile)
    DBConnection=DBConnection.DBConnection(Options,False)
    print('Current DB Servers:')
    for i in range(0,DBConnection.serverscount):
        print("("+str(i+1)+"): "+ DBConnection.DBservers[i]['serverip'])
    
    TableName=raw_input("Please enter table name:")
    [IsInAnyDB,TableDBservers]=GetTableInformation(TableName,DBConnection)    
    if(IsInAnyDB==True):
        CommandFunction=FunctionsMap[Command]
        CommandFunction(TableName,TableDBservers, DBConnection,CurrentSAGEStruct,Options)
        
    else:
        print("I can't Operate on this table! Table not found error")
    DBConnection.CloseConnections()
    