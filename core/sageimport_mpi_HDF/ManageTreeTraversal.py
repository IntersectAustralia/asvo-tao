
import string,os
import sys # for listing directory contents
import logging
import time

import settingReader # Read the XML settings
import DBConnection # Interaction with the postgreSQL DB
from collections import deque

class Node(object):
    def __init__(self, LocalIndex=None,GlobalIndex=None,Descendant=None,SnapNum=None,BreadthFirstIndex=None,DepthFirstIndex=None,SubTreeSize=None):
        self.data = {'LocalIndex':LocalIndex,'GlobalIndex':GlobalIndex,'Descendant':Descendant,'SnapNum':SnapNum,'BreadthFirstIndex':BreadthFirstIndex,'DepthFirstIndex':DepthFirstIndex,'SubTreeSize':SubTreeSize}
        self.children = []
    
        
    def add_child(self, obj):
        self.children.append(obj)    
class ManageTreeIndex(object):
    
    def __init__(self,DBConnection,Options):
        self.DBConnection=DBConnection
        self.Options=Options   

    def FieldExists(self,ServerID, TableName,FieldName):
               
        FieldName=FieldName.lower()
        SqlStmt="SELECT column_name FROM information_schema.columns WHERE table_name='"+TableName+"' and column_name='"+FieldName+"';"
        resultsList=self.DBConnection.ExecuteQuerySQLStatment(SqlStmt,ServerID)
        if len(resultsList)>0:
            return True
        else:
            return False
    def AddTreeTraversalFields(self,TableName):
        self.AddTreeTraversalField(TableName,'BreadthFirst_traversalorder')
        self.AddTreeTraversalField(TableName,'DepthFirst_traversalorder')
        self.AddTreeTraversalField(TableName,'Subtree_Count')
    
    def AddTreeIndices(self,TableName):
        self.AddIndexToTreeTraversalField(TableName,'BreadthFirst_traversalorder')  
        self.AddIndexToTreeTraversalField(TableName,'DepthFirst_traversalorder')
          
    def AddTreeTraversalField(self,TableName,FieldName):
        
        ServerID=self.DBConnection.GetServerID(TableName)
        
        if self.FieldExists(ServerID,TableName,FieldName)==False:
            SQLStmt="ALTER TABLE "+TableName+" ADD COLUMN "+FieldName+" bigint;"
            self.DBConnection.ExecuteNoQuerySQLStatment(SQLStmt,ServerID)    
            logging.info("Table Altered!")
        else:
            IndexStatment="DROP Index  IF EXISTS "+FieldName+"_Index_"+TableName+";"
            
            DBConnection.ExecuteNoQuerySQLStatment(IndexStatment,ServerID)
            IndexStatment="Update "+TableName+" set "+FieldName+"=null ;"
            DBConnection.ExecuteNoQuerySQLStatment(IndexStatment,ServerID)            
            logging.info("Field Already Exists!")
    
    def AddIndexToTreeTraversalField(self,TableName,FieldName):
        ServerID=self.DBConnection.GetServerID(TableName)
        CreateIndexStatment="Create Index "+FieldName+"_Index_"+TableName+" on  "+TableName+" ("+FieldName+");"
        DBConnection.ExecuteNoQuerySQLStatment(CreateIndexStatment,ServerID)  
    
    def BuildTree(self,TreeID,TreeData):
        
        self.ParentNode=None
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
                
                LocalIndex=i
                GlobalIndex=TreeData[i][0]
                Descendant=TreeData[i][1]
                SnapNum=TreeData[i][2]
                
                
                TopLevelList.append(Node(LocalIndex,GlobalIndex,Descendant,SnapNum))
                
      
        i=0
        stack=[]
        self.ParentNode=Node()
        self.ParentNode.children=TopLevelList
        
        for P in TopLevelList:      
            stack.append(P)
        
        
        while(len(stack)>0):                
            CurrentNode=stack.pop()        
            
            
            for Child in ParentsList[CurrentNode.data['LocalIndex']]:
                
                
                LocalIndex=NodesList[Child][0]
                GlobalIndex=NodesList[Child][1][0]
                Descendant=NodesList[Child][1][1]
                SnapNum=NodesList[Child][1][2]
                
                
                
                ChildNode=Node(LocalIndex,GlobalIndex,Descendant,SnapNum)
                stack.append(ChildNode)
                CurrentNode.children.append(ChildNode)
        
                 

    def BreadthFirst(self,ParentNode):
        
        index=0
        queue=deque([])
        for P in ParentNode.children:
            queue.append(P)
        while (len(queue)>0):
            CurrentNode=queue.popleft()        
            CurrentNode.data['BreadthFirstIndex']=index
            index=index+1        
            for child in CurrentNode.children:
                queue.append(child)
      
        
        
    def DepthFirst_PreOrder(self,ParentNode):
        
        
        index=0
        stack=[]
        
        for P in ParentNode.children:
            stack.append(P)
            
        while (len(stack)>0):
            CurrentNode=stack.pop()
            CurrentNode.data['DepthFirstIndex']=index
        
            index=index+1        
            for child in CurrentNode.children:
                stack.append(child)
      
           
      
    
    
    def CountChildNodes(self,CurrentNode):
        
        if(len(CurrentNode.children)==0):
            CurrentNode.data['SubTreeSize']=1
            return 1;
        else:
            Counter=1   
            for child in CurrentNode.children:
                Counter=Counter+self.CountChildNodes(child)
            CurrentNode.data['SubTreeSize']=Counter
            return Counter
         
    
    
    
    
    def PrintNodes(self,CurrentNode,Level):
        Emptystr=" "*Level
        if(CurrentNode.data['GlobalIndex']!=None):
            if len(CurrentNode.children)==0:
                print("<L"+str(Level)+" name=\""+str(CurrentNode.data)+"\"/>")
            else:
                print("<L"+str(Level)+" name=\""+str(CurrentNode.data)+"\">")
            
        for child in CurrentNode.children:
            self.PrintNodes(child, Level+1)        
        if(CurrentNode.data['GlobalIndex']!=None and len(CurrentNode.children)>0):
            print("</L"+str(Level)+">")   
    
    def TreeToList(self,CurrentNode,CurrentList):
        CurrentList.append(CurrentNode.data)
        for child in CurrentNode.children:
            self.TreeToList(child, CurrentList)
            
        
        

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
    #if 1==1:
    for TableIndex in range(0,51):
        TableName="tree_"+str(TableIndex)
        logging.info("******** Processing Table "+TableName+" **********")
        #############################################################
        ##### 1- Alter Table
        ManageTreeIndexObj.AddTreeTraversalFields(TableName)
        
        ###############################################################
        ##### 2- Get List of Trees
        ServerID=DBConnection.GetServerID(TableName)
        SQLStmt="select distinct globaltreeid from "+TableName+";"
        TreesList=DBConnection.ExecuteQuerySQLStatment(SQLStmt,ServerID)
        
        Counter=0
        
        
        #TreeID=TreesList[0]
        #TreeID[0]=24341
        #if 1==1:
        for TreeID in TreesList:  
            
            Counter=Counter+1
            SQLStmt="select globalindex,descendant,snapnum from "+TableName+" where globaltreeid="+str(TreeID[0])+" order by localgalaxyid;"
            TreeDetails=DBConnection.ExecuteQuerySQLStatment(SQLStmt,ServerID)
            
            logging.info(str(Counter)+"/"+str(len(TreesList))+":"+str(len(TreeDetails))+"\t"+str(TreeID[0]))
            
            ManageTreeIndexObj.BuildTree(TreeID[0],TreeDetails)
            BreadthFirstMappingList= ManageTreeIndexObj.BreadthFirst(ManageTreeIndexObj.ParentNode)
            DepthFirstMappingList=ManageTreeIndexObj.DepthFirst_PreOrder(ManageTreeIndexObj.ParentNode)
            ManageTreeIndexObj.CountChildNodes(ManageTreeIndexObj.ParentNode)
            #ManageTreeIndexObj.PrintNodes(ManageTreeIndexObj.ParentNode,0)
            
            ################## Get the Nodes as a List #####################################
            NodesList=[]
            ManageTreeIndexObj.TreeToList(ManageTreeIndexObj.ParentNode,NodesList)            
            TotalNodes=NodesList[0]['SubTreeSize']-1
            del NodesList[0]
            #################################################################################            
            
            
            UpdateSt=""
        
            if len(NodesList)!=len(TreeDetails) or len(TreeDetails)!=TotalNodes:
                print( str(TreeID[0])+": Error:"+str(len(NodesList))+"!="+str(len(TreeDetails)))
         
            
            #for Node in NodesList:            
            #    UpdateSt=UpdateSt+" Update "+TableName+" set BreadthFirst_traversalorder="+str(Node['BreadthFirstIndex'])+" , DepthFirst_traversalorder="+str(Node['DepthFirstIndex'])+" , Subtree_Count="+str(Node['SubTreeSize'])+"  where globalindex="+str(Node['GlobalIndex'])+"; \n"
            UpdateSt="UPDATE "+TableName+" SET BreadthFirst_traversalorder=myvalues.BreadthFirstIndex, \n"
            UpdateSt=UpdateSt+" DepthFirst_traversalorder=myvalues.DepthFirstIndex, \n"
            UpdateSt=UpdateSt+" Subtree_Count=myvalues.SubTreeSize From (VALUES  \n"
            
            for NodeI in NodesList:
                UpdateSt=UpdateSt+" ("+str(NodeI['GlobalIndex'])+","+str(NodeI['BreadthFirstIndex'])+","+str(NodeI['DepthFirstIndex'])+","+ str(NodeI['SubTreeSize'])+"),\n"
            
            UpdateSt=UpdateSt[:-2]
            UpdateSt=UpdateSt+") AS myvalues(GlobalIndex,BreadthFirstIndex,DepthFirstIndex,SubTreeSize)"
            UpdateSt=UpdateSt+" Where "+TableName+".globalindex=myvalues.GlobalIndex"
            
            DBConnection.ExecuteNoQuerySQLStatment(UpdateSt,ServerID)
            logging.info(".*.")
        
        ManageTreeIndexObj.AddTreeIndices(TableName)
    
    
    DBConnection.CloseConnections()
    logging.info("Processing Done!")
    