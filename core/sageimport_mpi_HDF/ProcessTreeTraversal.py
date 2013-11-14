
import string,os
import sys # for listing directory contents
import logging
import time

from collections import deque

class Node(object):
    def __init__(self, LocalIndex=None,GlobalIndex=None,Descendant=None,SnapNum=None,BreadthFirstIndex=None,DepthFirstIndex=None,SubTreeSize=None):
        self.data = {'LocalIndex':LocalIndex,'GlobalIndex':GlobalIndex,'Descendant':Descendant,'SnapNum':SnapNum,'BreadthFirstIndex':BreadthFirstIndex,'DepthFirstIndex':DepthFirstIndex,'SubTreeSize':SubTreeSize}
        self.children = []
    
        
    def add_child(self, obj):
        self.children.append(obj)    
class ManageTreeIndex(object):
    
    def __init__(self):
        logging.info("Processing Tree Traversal")      
    
        
    def BuildTree(self,TreeData):
         
        
        
        
        
        self.ParentNode=None
        NodesList=[]
        ParentsList=[]
        for i  in range(0,len(TreeData)):
            CurrentValue=[TreeData['gobal galaxy index'][i],TreeData['descendant'][i],TreeData['snapshot'][i]]            
            NodesList.append([i,CurrentValue])
            ParentsList.append([])          
                
        
        CurrentIndex=0
        
        TopLevelList=[]
        
      
        
        for i  in range(0,len(TreeData)):
            ParentID=TreeData['descendant'][i]
            
            if ParentID>=0:      
                ParentsList[ParentID].append(i)
            else:
                
                LocalIndex=i
                GlobalIndex=TreeData['gobal galaxy index'][i]
                Descendant=TreeData['descendant'][i]
                SnapNum=TreeData['snapshot'][i]
                
                
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
  
    
    def TreeToList(self,CurrentNode,CurrentList):
        if CurrentNode.data['GlobalIndex']!=None:
            CurrentList[CurrentNode.data['GlobalIndex']]=CurrentNode.data        
        for child in CurrentNode.children:            
            self.TreeToList(child, CurrentList)
            
        
        




