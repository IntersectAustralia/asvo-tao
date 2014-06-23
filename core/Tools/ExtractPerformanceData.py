import re,os,sys
import lxml.etree as ET
import settingReader # Read the XML settings
import StringIO
import psycopg2
from psycopg2 import extras
import os, shlex, subprocess,string
import logging
import locale


class ParseProfileData(object):

    

    def __init__(self,FilePath,Options,DatabaseName):        
        self.ProfileFileName=FilePath
        print("FileName:"+self.ProfileFileName+"\t Database:"+DatabaseName)
        
        self.Options=Options               
        self.DatabaseName=DatabaseName
        
        
    def LoadDBMetaData(self):
        self.serverip=self.Options['PGDB:serverip']
        self.username=self.Options['PGDB:user']
        self.password=self.Options['PGDB:password']
        self.port=int(self.Options['PGDB:port'])
        self.DBName=self.Options['PGDB:NewDBName']    
        
        ConnectionStr="host="+self.serverip+" user="+self.username+" password="+self.password+" port="+str(self.port)+" dbname="+self.DBName    
        self.CurrentConnection=psycopg2.connect(ConnectionStr)
        self.CurrentConnection.autocommit=True
        self.ActiveCursor=self.CurrentConnection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        self.ActiveCursor.execute("select * from tablessummary where databasename='"+self.DatabaseName+"';")
        resultsList= self.ActiveCursor.fetchall() 
        if(len(resultsList)>0):
            self.resultsdict={}
            for row in resultsList:
                self.resultsdict[row[0]]= row[2:]
            return True
        else:
            return False
              
        
        
    
    def ListBoxes(self,BoxesListStr):    
        BoxesList=(eval(BoxesListStr))
        return BoxesList
           
    def GetTables(self,TablesListStr):
        TablesListStr=TablesListStr.replace(' ','').strip()
        TablesListStr=TablesListStr[1:-1]
        
        if len(TablesListStr)>0:
            TablesList=TablesListStr.split(',')        
            return TablesList
        else:
            return []
    
            
    def ParseFile(self):
        f=open(self.ProfileFileName,'r')
        Lines=f.readlines()
        BoxesList=[]
        SumTables=0
        GalaxiesCount=0
        TotalTrees=0
        self.BoxesList=[]
        for line in Lines:
            LineParts=line.split(':')
            if LineParts[1].strip()=='Boxes':
                self.BoxesList=self.ListBoxes(LineParts[2])                           
            elif LineParts[1].strip()=='Tables':
                TablesList=self.GetTables(LineParts[2])
                SumTables=SumTables+len(TablesList)
                for Table in TablesList:
                    GalaxiesCount=GalaxiesCount+self.resultsdict[Table][1]
                    TotalTrees=TotalTrees+self.resultsdict[Table][2]
         
        f.close()            
            
        
            
        
        return [(len(self.BoxesList)),SumTables,GalaxiesCount,TotalTrees]

class JobsDB(object):
   

    def __init__(self,Options):  
        self.Options=Options       
        
        self.serverip=self.Options['PGDB:serverip']
        self.username=self.Options['PGDB:user']
        self.password=self.Options['PGDB:password']
        self.port=int(self.Options['PGDB:port'])
        self.DBName=self.Options['PGDB:NewDBName']  

        ConnectionStr="host="+self.serverip+" user="+self.username+" password="+self.password+" port="+str(self.port)+" dbname="+self.DBName    
        self.CurrentConnection=psycopg2.connect(ConnectionStr)
        self.CurrentConnection.autocommit=True
        self.ActiveCursor=self.CurrentConnection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        self.ActiveCursor.execute("select jobid,uireferenceid,jobstatus,insertdate,completedate,startdate,completedate-startdate as elapsedtime, database,username from jobs where latestjobversion=true and jobstatus=3 and startdate is not null order by uireferenceid;")
        resultsList= self.ActiveCursor.fetchall() 
        for row in resultsList:
            FilePath="/lustre/projects/p014_swin/FTP/stagingjobs/"+row[8]+"/"+str(row[1])+"/log/params0_tao.Profile.log00000"
            Database=row[7]
            if (os.path.exists(FilePath)):                 
                
                ParseProfileDataObj=ParseProfileData(FilePath,Options,Database)
                if (ParseProfileDataObj.LoadDBMetaData()==True):
                    [BoxesCount,SumTables,GalaxiesCount,TotalTrees]=ParseProfileDataObj.ParseFile()
                    print('Total Execution='+str(row[6].total_seconds())+' seconds')
                    print('Number of Boxes='+str(BoxesCount))
                    print('Total Queries='+str(SumTables))
                    print('Maximum Galaxies='+str(GalaxiesCount))
                    print('Maximum Trees='+str(TotalTrees))
    
if __name__ == '__main__':
    
    
    [Options]=settingReader.ParseParams("settings.xml")
    JobsDBObs=JobsDB(Options)    
     
