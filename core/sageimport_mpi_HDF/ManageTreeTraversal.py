
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
class ManageTreeIndex(object):
    
    def __init__(self,DBConnection,Options):
        self.DBConnection=DBConnection
        self.Options=Options   

    def FieldExists(self,ServerID, TableName):
               
        
        SqlStmt="SELECT column_name FROM information_schema.columns WHERE table_name='"+TableName+"' and column_name='traversalorder';"
        resultsList=self.DBConnection.ExecuteQuerySQLStatment(SqlStmt,ServerID)
        if len(resultsList)>0:
            return True
        else:
            return False
        
    def AddTreeTraversalField(self,TableName):
        
        ServerID=self.DBConnection.GetServerID(TableName)
        
        if self.FieldExists(ServerID,TableName)==False:
            SQLStmt="ALTER TABLE "+TableName+" ADD COLUMN traversalorder bigint;"
            self.DBConnection.ExecuteNoQuerySQLStatment(SQLStmt,ServerID)    
            logging.info("Table Altered!")
        else:
            IndexStatment="DROP Index  IF EXISTS traversalorder_Index_"+TableName+";"
            DBConnection.ExecuteNoQuerySQLStatment(IndexStatment,ServerID)
            logging.info("Field Already Exists!")
    
    def AddIndexToTreeTraversal(self,TableName):
        ServerID=self.DBConnection.GetServerID(TableName)
        CreateIndexStatment="Create Index traversalorder_Index_"+TableName+" on  "+TableName+" (traversalorder);"
        DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,ServerID)  
    
    def BuildTree(self,TreeID,TreeData):
        
        ParentNode=None
        NodesList=[]
        ParentsList=[]
        for i  in range(0,len(TreeData)):
            NodesList.append([i,TreeData[i]])
            ParentsList.append([])          
        
        
        
        CurrentIndex=0
        
        TopLevelList=[]
        
        for i  in range(0,len(TreeData)):
            ParentID=TreeData[i][1]  
            if ParentID>=0:      
                ParentsList[ParentID].append(i)
            else:
                TopLevelList.append(Node([i,TreeData[i]]))
                
        #for i  in range(0,len(TreeData)):
        #    print(str(NodesList[i])+"-->"+str(ParentsList[i]))    
        
        
        i=0
        stack=[]
        ParentNode=Node(None)
        ParentNode.children=TopLevelList
        
        for P in TopLevelList:
            #print("***"+str(P.data))
            stack.append(P)
        
        
        while(len(stack)>0):                
            CurrentNode=stack.pop()        
            
            
            for Child in ParentsList[CurrentNode.data[0]]:
                ChildNode=Node(NodesList[Child])
                stack.append(ChildNode)
                CurrentNode.children.append(ChildNode)
        #print("<tree>")       
        #self.PrintNodes(ParentNode, 0)
        #print("</tree>")
        return self.BreadthFirst(ParentNode)         

    def BreadthFirst(self,ParentNode):
        IDsList=[]
        index=0
        queue=deque([])
        for P in ParentNode.children:
            queue.append(P)
        while (len(queue)>0):
            CurrentNode=queue.popleft()
            IDsList.append([CurrentNode.data[1][0],index])
            index=index+1        
            for child in CurrentNode.children:
                queue.append(child)
      
        return IDsList      
        
        
      
    
    
    def PrintNodes(self,CurrentNode,Level):
        Emptystr=" "*Level
        if(CurrentNode.data!=None):
            if len(CurrentNode.children)==0:
                print("<L"+str(Level)+" name=\""+str(CurrentNode.data)+"\"/>")
            else:
                print("<L"+str(Level)+" name=\""+str(CurrentNode.data)+"\">")
            
        for child in CurrentNode.children:
            self.PrintNodes(child, Level+1)        
        if(CurrentNode.data!=None and len(CurrentNode.children)>0):
            print("</L"+str(Level)+">")   
    

def SetupLogFile():
    FilePath='log/logfile_traversal.log'
    if os.path.exists(FilePath):
        os.remove(FilePath)
    logging.basicConfig(filename=FilePath,level=logging.DEBUG,format='%(asctime)s %(message)s')



if __name__ == '__main__':
    
    SettingFile=sys.argv[1]
    TableName=sys.argv[2]
    
    SetupLogFile()
    logging.info("Start Processing - Setting File :"+SettingFile)
    logging.info("Start Processing - Table Name :"+TableName)
    
    
    [CurrentSAGEStruct,Options]=settingReader.ParseParams(SettingFile)
    DBConnection=DBConnection.DBConnection(Options)
    logging.info("Connection Open!")
    
    ManageTreeIndexObj=ManageTreeIndex(DBConnection,Options)
    #############################################################
    ##### 1- Alter Table
    ManageTreeIndexObj.AddTreeTraversalField(TableName)
    
    ###############################################################
    ##### 2- Get List of Trees
    ServerID=DBConnection.GetServerID(TableName)
    SQLStmt="select distinct globaltreeid from "+TableName+";"
    TreesList=DBConnection.ExecuteQuerySQLStatment(SQLStmt,ServerID)
    
    Counter=0
    
    
    #TreeID=TreesList[0]
    #TreeID[0]=18602
    #if 1==1:
    for TreeID in TreesList:  
        
        Counter=Counter+1
        SQLStmt="select globalgalaxyid,descendant,snapnum from "+TableName+" where globaltreeid="+str(TreeID[0])+" order by localgalaxyid;"
        TreeDetails=DBConnection.ExecuteQuerySQLStatment(SQLStmt,ServerID)
        
        logging.info(str(Counter)+"/"+str(len(TreesList))+":"+str(len(TreeDetails))+"\t"+str(TreeID[0]))
        MappingList=ManageTreeIndexObj.BuildTree(TreeID[0],TreeDetails)
        
        UpdateSt="Update "+TableName+" set traversalorder= CASE globalgalaxyid \n"
        if len(MappingList)!=len(TreeDetails):
            print( str(TreeID[0])+": Error:"+str(len(MappingList))+"!="+str(len(TreeDetails)))
        #Count=0
        #for Record in TreeDetails:
        #    Found=False
            
        #    for Map in MappingList:
        #        if Map[0]==Record[0]:
        #            Found=True
        #            break
        #    if Found==False:
        #        print "Missing:"+str(Count)+":"+str(Record)
        #    Count=Count+1    
        
        for Map in MappingList:
            UpdateSt=UpdateSt+" WHEN "+str(Map[0])+" THEN "+str(Map[1])+"\n"
            #print(str(Map[0])+":"+str(Map[1]))
        UpdateSt=UpdateSt+" END where globaltreeid="+str(TreeID[0])+";"    
        DBConnection.ExecuteNoQuerySQLStatment(UpdateSt,ServerID)
        logging.info(".*.")
    
    ManageTreeIndexObj.AddIndexToTreeTraversal(TableName)
    
    
    DBConnection.CloseConnections()
    logging.info("Processing Done!")
    