##
## @package torque
## Routines to simplify interaction with the PBS server.
##

import os, shlex, subprocess,string
import PBSPy.capi as pbs
import dbase
import EnumerationLookup
import locale
import time
import logging

class TorqueInterface(object):
    
    
    
    def __init__(self,Options,dbaseobj):
        self.Options=Options
        self.dbaseobj=dbaseobj
        self.ServerAddress=Options['Torque:ServerAddress'] # BPS Server Address
        self.ScriptFileName=Options['Torque:ScriptFileName'] # What to call the generated PBS script.
        self.InitDefaultparams()
        self.Connect()

    ##
    ## Connect to the PBS server.
    ##
    ## @returns PBSPy Server class.
    ##
    def Connect(self):
        try:
            self.Server = pbs.Server(self.ServerAddress)
            self.Server.connect()
            self.dbaseobj.AddNewEvent(0,EnumerationLookup.EventType.PBSEvent,"Connected to ("+self.ServerAddress+") Successfully")
        except Exception as Exp:
            self.dbaseobj.AddNewEvent(0,EnumerationLookup.EventType.Error,"Connection to ("+self.ServerAddress+") Failed \n"+Exp.args)
            logging.info(">>>>>Error While Connecting to PBS")
            logging.info(type(Exp))
            logging.info(Exp.args)
            logging.info(Exp) 
            raw_input("PLease press enter to continue.....")           
            
        

  

    ##
    ## Generate a dictionary of default parameters.
    ##
    ## @returns Dictionary of default parameters.
    ##
    def InitDefaultparams(self):
        self.DefaultParams = {'nodes': 1,'ppn': 1,
                              'wt_hours': 48,'wt_minutes': 0,'wt_seconds': 0}

    def SetJobParams(self,UserName,JobID,nodes,ppn,path,BasicSettingPath):    
            
        self.DefaultParams['executable'] = self.Options['Torque:ExecutableName']
        self.DefaultParams['name']='tao_'+UserName[:4]+'_'+str(JobID)
        self.DefaultParams['nodes'] = nodes        
        self.DefaultParams['ppn'] = ppn
        self.DefaultParams['path'] = path+"/params.xml"
        self.DefaultParams['basicsettingpath'] = BasicSettingPath
        

    ##
    ## Write a PBS script from a parameters dictionary.
    ##
    ## @param[IN]  params  Dictionary of parameters.
    ## @param[IN]  path    Where to write PBS script.
    ##
    def WritePBSScriptFile(self,UserName,JobID, nodes,ppn, path,BasicSettingPath):
        self.SetJobParams(UserName, JobID,nodes, ppn,path,BasicSettingPath)
        FileName = os.path.join(path, self.ScriptFileName)
        ##
        self.dbaseobj.AddNewEvent(JobID,EnumerationLookup.EventType.PBSEvent,"Adding New Job to PBS, Script Name="+self.ScriptFileName)
        ##
        
        with open(FileName, 'w') as script:
            script.write('''#!/bin/tcsh
            #PBS -N %(name)s
            #PBS -l nodes=%(nodes)d:ppn=%(ppn)d
            #PBS -l walltime=%(wt_hours)02d:%(wt_minutes)02d:%(wt_seconds)02d
            #PBS -d .
            source /usr/local/modules/init/tcsh
            module load gcc/4.6.2 mpich2 hdf5/x86_64/gnu/1.8.9-mpich2 boost
            setenv PATH /home/lhodkins/workspace/asvo-tao/science_modules/build-debug/bin:$PATH
            setenv LD_LIBRARY_PATH /home/lhodkins/workspace/asvo-tao/science_modules/build-debug/lib:$LD_LIBRARY_PATH
            mpiexec %(executable)s %(path)s %(basicsettingpath)s
            '''%self.DefaultParams)
        return FileName

    ##
    ## Submit a PBS job.
    ##
    ## @param[IN]  params  Parameter dictionary.
    ## @returns PBS job identifier.
    ##
    def Submit(self,UserName,JobID,path,nodes=1,ppn=1):
        BasicSettingPath=self.Options['Torque:BasicSettingsPath']
        ScriptFileName = self.WritePBSScriptFile(UserName,JobID, nodes,ppn, path,BasicSettingPath)
        
        
        stdout = subprocess.check_output(shlex.split('ssh g2 \"cd %s; qsub -q tao %s\"'%(path.encode(locale.getpreferredencoding()), ScriptFileName.encode(locale.getpreferredencoding()))))
        pbs_id = stdout[:-1] # remove trailing \n
    
        return pbs_id

    ##
    ## Query a PBS job.
    ##
    ## The character returned indicates the job state as follows:
    ##  Q = queued
    ##  R = running
    ##  C = complete --- Not Currently Available
    ##
    ## @param[IN]  pbs_id  PBS job identifier.
    ## @returns A character representing the job state.
    ##
    def QueryPBSJob(self,pbsIDs):        
        states = {}
        all_jobs = subprocess.check_output(shlex.split('ssh g2 qstat'))        
        lines = all_jobs.splitlines()[2:]
         
        CurrentJobs={} # Build dictionary with our jobs only
        for line in lines:
            LineParts=shlex.split(line)
            JobName=LineParts[1]            
            if JobName.find('tao_')==0:
                JobID=LineParts[0].split('.')[0]
                CurrentJobs[JobID]=LineParts[4]
        
            
         
        
        return CurrentJobs
    
    
    
    def GetJobStartTime(self,pbsID):
        JobStartTimeOutput = subprocess.check_output(shlex.split('ssh g2 showstart '+pbsID))
        Lines=JobStartTimeOutput.splitlines()
        for Line in Lines:
            
            if Line.find('Estimated Rsv based start in')!=-1:
               Line=Line.replace('Estimated Rsv based start in','')
               Index=Line.find('on')
               Line=Line[Index+2:].strip()               
               D=time.strptime(Line,'%a %b %d %H:%M:%S')               
               return D
               
        
        
    
        
