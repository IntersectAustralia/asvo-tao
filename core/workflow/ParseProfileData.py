import re,os
import lxml.etree as ET
import settingReader # Read the XML settings
import StringIO


class ParseProfileData(object):

    

    def __init__(self,FileName,Options):        
        self.Options=Options
        self.ProfileFileName=FileName
    
    def ListBoxes(self,BoxesListStr):    
        BoxesList=(eval(BoxesListStr))
        return BoxesList
           
    def CountTables(self,TablesListStr):
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
        for line in Lines:
            LineParts=line.split(':')
            if LineParts[1].strip()=='Boxes':
                BoxesList=self.ListBoxes(LineParts[2]) 
                print (BoxesList)            
            elif LineParts[1].strip()=='Tables':
                TablesList=self.CountTables(LineParts[2])
                SumTables=SumTables+len(TablesList)
                print (TablesList) 
        print 'Total Queries='+str(SumTables)

                
if __name__ == '__main__':
     [Options]=settingReader.ParseParams("settings.xml")
     ParseProfileDataObj=ParseProfileData('/home/amr/workspace/AppRun/log/params0_tao.Profile.log00000',Options)
     ParseProfileDataObj.ParseFile()
