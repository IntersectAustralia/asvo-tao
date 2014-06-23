
import string,os
import sys # for listing directory contents
import logging
import time

import settingReader # Read the XML settings
import DBConnection # Interaction with the postgreSQL DB
from collections import deque

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)    



def FieldExists(DBConnection,ServerID,TableName):
    
    SqlStmt="SELECT column_name FROM information_schema.columns WHERE table_name='"+TableName+"' and column_name='traversalorder';"
    resultsList=DBConnection.ExecuteQuerySQLStatment(SqlStmt,ServerID)
    if len(resultsList)>0:
        return True
    else:
        return False
    
def BuildTree(TreeID,TreeData):
    
    ParentNode=None
    NodesList=[]
    ParentsList=[]
    for i  in range(0,len(TreeData)):
        NodesList.append([i,TreeData[i]])
        ParentsList.append([])
            
    
    
    CurrentIndex=0
    for i  in range(0,len(TreeData)):
        ParentID=TreeData[i][1]  
        if ParentID>0:      
            ParentsList[ParentID].append(i)
            
    
    
    i=0
    stack=[]
    ParentNode=Node(NodesList[-1])
    
    stack.append(ParentNode)
    while(len(stack)>0):                
        CurrentNode=stack.pop()        
        
    
        for Child in ParentsList[CurrentNode.data[0]]:
            ChildNode=Node(NodesList[Child])
            stack.append(ChildNode)
            CurrentNode.children.append(ChildNode)
           
    
    return BreadthFirst(ParentNode)         

def BreadthFirst(ParentNode):
    IDsList=[]
    index=0
    queue=deque([])
    queue.append(ParentNode)
    while (len(queue)>0):
        CurrentNode=queue.popleft()
        IDsList.append([CurrentNode.data[1][0],index])
        index=index+1        
        for child in CurrentNode.children:
            queue.append(child)
    #for id in IDsList:
    #    print id
    return IDsList      
        
        
        
    
    
def PrintNodes(CurrentNode,Level):
    Emptystr=" "*Level
    print Emptystr+str(CurrentNode.data[1][0])
    for child in CurrentNode.children:
        PrintNodes(child, Level+1)        
           
    

def SetupLogFile():
    FilePath='log/logfile_traversal.log'
    if os.path.exists(FilePath):
        os.remove(FilePath)
    logging.basicConfig(filename=FilePath,level=logging.DEBUG,format='%(asctime)s %(message)s')



if __name__ == '__main__':
    
    SettingFile=sys.argv[1]
    TableName=sys.argv[2]
    
    SetupLogFile()
    print("Start Processing - Setting File :"+SettingFile)
    print("Start Processing - Table Name :"+TableName)
    
    
    [CurrentSAGEStruct,Options]=settingReader.ParseParams(SettingFile)
    DBConnection=DBConnection.DBConnection(Options)
    print("Connection Open!")
    ServerID=DBConnection.GetServerID(TableName)
    print("Server ID is : "+str(ServerID))
    
    #############################################################
    ##### 1- Alter Table
    if FieldExists(DBConnection,ServerID,TableName)==False:
        SQLStmt="ALTER TABLE "+TableName+" ADD COLUMN traversalorder bigint;"
        DBConnection.ExecuteNoQuerySQLStatment(SQLStmt,ServerID)    
        print("Table Altered!")
    else:
        IndexStatment="DROP Index  IF EXISTS traversalorder_Index_"+TableName+";"
        DBConnection.ExecuteNoQuerySQLStatment(IndexStatment,ServerID)
        print("Field Already Exists!")
    
    ###############################################################
    ##### 2- Get List of Trees
    SQLStmt="select distinct globaltreeid from "+TableName+";"
    TreesList=DBConnection.ExecuteQuerySQLStatment(SQLStmt,ServerID)
    
    Counter=0
    
    
    
    for TreeID in TreesList:  
        print str(Counter)+"/"+str(len(TreesList))
        Counter=Counter+1
        SQLStmt="select globalgalaxyid,descendant,snapnum from "+TableName+" where globaltreeid="+str(TreeID[0])+";"
        TreeDetails=DBConnection.ExecuteQuerySQLStatment(SQLStmt,ServerID)
        MappingList=BuildTree(TreeID[0],TreeDetails)
    
        UpdateSt="Update "+TableName+" set traversalorder= CASE globalgalaxyid"
        
        for Map in MappingList:
            UpdateSt=UpdateSt+" WHEN "+str(Map[0])+" THEN "+str(Map[1])
        UpdateSt=UpdateSt+"END where globaltreeid="+str(TreeID[0])+";"    
        DBConnection.ExecuteNoQuerySQLStatment(UpdateSt,ServerID)
    
    
    CreateIndexStatment="Create Index traversalorder_Index_"+TableName+" on  "+TableName+" (traversalorder);"
    DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,ServerID)
    
    
    DBConnection.CloseConnections()
    print("Processing Done!")
    