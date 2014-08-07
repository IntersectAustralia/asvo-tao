import re,os
import lxml.etree as ET
import settingReader # Read the XML settings
import StringIO
import psycopg2
from psycopg2 import extras
import os, shlex, subprocess,string
import logging
import locale


class ParseProfileData(object):

    

    def __init__(self,JobPath,SubProcessID,Options,DatabaseName):        
        self.ProfileFileName=JobPath+"/params"+str(SubProcessID)+"_tao.Profile.log00000"
        logging.info("Profile FileName:"+self.ProfileFileName)
        self.Options=Options
        self.RunProfiling(JobPath,SubProcessID)
        
        
        self.LoadDBMetaData(DatabaseName)
        
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
    
    def ParseXMLParams(self,FileName):
        tree = ET.parse(FileName)
        NameSpace=re.findall('\{.*\}',tree.xpath('.')[0].tag)[0]
        NameSpace=NameSpace[1:-1]
        Modules=tree.xpath("/ns:tao/ns:workflow/*[@id]",namespaces={'ns':NameSpace})
        ListofModules=[]
        for Module in Modules:
             ListofModules.append(Module.tag.replace('{'+NameSpace+'}',''))
        return ListofModules
    
    def RunProfiling(self,JobPath,SubJobIndex):
        #stdout = subprocess.check_output(shlex.split('ssh g2 \"cd %s; qsub -q %s %s\"'%(path.encode(locale.getpreferredencoding()), queuename.encode(locale.getpreferredencoding()), ScriptFileName.encode(locale.getpreferredencoding()))))
        os.chdir(JobPath)
        
        FileName = os.path.join(JobPath, "runprofile.sh")
        
        BasicSettingPath=self.Options['Torque:BasicSettingsPath']
        ProfilingExecPath=self.Options['Torque:ProfilingExecutableName']
        XMlParamsPath=JobPath+"/params"+str(SubJobIndex)+".xml"
        self.ListofModules=self.ParseXMLParams(XMlParamsPath)
        ModulesStr="module load python fftw/x86_64/gnu/3.3.2-threaded gcc/4.7.1 cmake boost gsl hdf5/x86_64/gnu/1.8.9-openmpi-psm postgresql cfitsio/x86_64/gnu/3.290-threaded skymaker"
        CommandTxt="mpirun "+ ProfilingExecPath+" "+XMlParamsPath+" "+BasicSettingPath
        logging.info("Profiling String:"+CommandTxt)
        logging.info(shlex.split(CommandTxt.encode(locale.getpreferredencoding())))
        
        with open(FileName, 'w') as script:
            #script.write("#!/bin/bash\n")
            script.write("source /usr/local/modules/init/bash\n")
            script.write(ModulesStr+"\n")
            script.write(CommandTxt)
        
        #stdout = subprocess.check_output(shlex.split(CommandTxt.encode(locale.getpreferredencoding())))
        stdout = subprocess.check_output(shlex.split("sh runprofile.sh".encode(locale.getpreferredencoding())))
        os.remove(JobPath+"/tao.log."+str(SubJobIndex))
        logging.info("Profiling Execution Done")
            
    def ParseFile(self):
        f=open(self.ProfileFileName,'r')
        Lines=f.readlines()
        BoxesList=[]
        SumTables=0
        GalaxiesCount=0
        TotalTrees=0
        self.BoxesList=[]
        logging.info(self.resultsdict)
        for line in Lines:
            LineParts=line.split(':')
            if LineParts[1].strip()=='Boxes':
                self.BoxesList=self.ListBoxes(LineParts[2])                           
            elif LineParts[1].strip()=='Tables':
                TablesList=self.GetTables(LineParts[2])
                SumTables=SumTables+len(TablesList)
                for Table in TablesList:
                    print Table
                    GalaxiesCount=GalaxiesCount+self.resultsdict[Table][1]
                    TotalTrees=TotalTrees+self.resultsdict[Table][2]
         
        f.close()            
        f=open("Profile.txt",'wt')
        
        for Module in self.ListofModules:
            f.write(str(Module)+"\n")
        
            
        f.write('Number of Boxes='+str(len(self.BoxesList))+'\n')
        f.write('Total Queries='+str(SumTables)+'\n')
        f.write('Maximum Galaxies='+str(GalaxiesCount)+'\n')
        f.write('Maximum Trees='+str(TotalTrees)+'\n')
        f.close()
        return [(len(self.BoxesList)),SumTables,GalaxiesCount,TotalTrees]

                
#if __name__ == '__main__':
    
#     [Options]=settingReader.ParseParams("settings.xml")
#     ParseProfileDataObj=ParseProfileData('/home/amr/workspace/AppRun/params0_tao.Profile.log00000',Options)
#     [Boxes,Tables,Galaxies,Trees]=ParseProfileDataObj.ParseFile()
#     print 'Number of Boxes='+str(Boxes)
#     print 'Total Queries='+str(Tables)
#     print 'Maximum Galaxies='+str(Galaxies)
#     print 'Maximum Trees='+str(Trees)
