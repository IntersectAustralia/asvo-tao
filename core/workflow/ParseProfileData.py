import re,os
import lxml.etree as ET
import settingReader # Read the XML settings
import StringIO
import psycopg2
from psycopg2 import extras


class ParseProfileData(object):

    

    def __init__(self,FileName,Options):        
        self.Options=Options
        self.ProfileFileName=FileName
        self.LoadDBMetaData("millennium_full_hdf5_dist")
        
    def LoadDBMetaData(self,DatabaseName):
        self.serverip=self.Options['PGDB:serverip']
        self.username=self.Options['PGDB:user']
        self.password=self.Options['PGDB:password']
        self.port=int(self.Options['PGDB:port'])
        self.DBName=self.Options['PGDB:NewDBName']    
        
        ConnectionStr="host="+self.serverip+" user="+self.username+" password="+self.password+" port="+str(self.port)+" dbname="+self.DBName    
        self.CurrentConnection=psycopg2.connect(ConnectionStr)
        self.CurrentConnection.autocommit=True
        self.ActiveCursor=self.CurrentConnection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        self.ActiveCursor.execute("select * from tablessummary where databasename='"+DatabaseName+"';")
        resultsList= self.ActiveCursor.fetchall() 
        self.resultsdict={}
        for row in resultsList:
            self.resultsdict[row[0]]= row[2:]
              
        
        
    
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
        return [(len(self.BoxesList)),SumTables,GalaxiesCount,TotalTrees]

                
if __name__ == '__main__':
     [Options]=settingReader.ParseParams("settings.xml")
     ParseProfileDataObj=ParseProfileData('/home/amr/workspace/AppRun/params0_tao.Profile.log00000',Options)
     [Boxes,Tables,Galaxies,Trees]=ParseProfileDataObj.ParseFile()
     print 'Number of Boxes='+str(Boxes)
     print 'Total Queries='+str(Tables)
     print 'Maximum Galaxies='+str(Galaxies)
     print 'Maximum Trees='+str(Trees)
