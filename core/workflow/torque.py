##
## @package torque
## Routines to simplify interaction with the PBS server.
##

import os, shlex, subprocess,string
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
        

    ##
    ## Connect to the PBS server.
    ##
    ## @returns PBSPy Server class.
    ##
       
            
        

  

    ##
    ## Generate a dictionary of default parameters.
    ##
    ## @returns Dictionary of default parameters.
    ##
    def InitDefaultparams(self):
        self.DefaultParams = {'nodes': 1,'ppn': 1,
                              'wt_hours': 168,'wt_minutes': 0,'wt_seconds': 0}

    ##
    ## Write a PBS script from a parameters dictionary.
    ##
    ## @param[IN]  params  Dictionary of parameters.
    ## @param[IN]  path    Where to write PBS script.
    ##
    def WritePBSScriptFile(self,UIJobReference,UserName,JobID, ppn,SubJobIndex):
                
        logpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], UserName, str(UIJobReference),'log')  
        outputpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], UserName, str(UIJobReference),'output')
        
        
        self.DefaultParams['executable'] = self.Options['Torque:ExecutableName']
        self.DefaultParams['name']=self.Options['Torque:jobprefix']+UserName[:4]+'_'+str(JobID)
        self.DefaultParams['nodes'] = int(self.Options['Torque:Nodes'])        
        self.DefaultParams['ppn'] = ppn
        self.DefaultParams['subjobindex'] = SubJobIndex
        self.DefaultParams['UIJobReference'] = UIJobReference
        self.DefaultParams['path'] = logpath+"/"+"params"+str(SubJobIndex)+".xml"
        self.DefaultParams['basicsettingpath'] = self.Options['Torque:BasicSettingsPath']
        self.DefaultParams['outputpath'] = outputpath
        self.DefaultParams['MergeScriptName'] = self.Options['Torque:MergeScriptName']
        self.DefaultParams['BaseLibPath']=self.Options['Torque:BaseLibPath']
        
        
        FileName = os.path.join(logpath, self.ScriptFileName+str(SubJobIndex))
        ##
        self.dbaseobj.AddNewEvent(JobID,EnumerationLookup.EventType.PBSEvent,"Adding New Job to PBS, Script Name="+self.ScriptFileName+str(SubJobIndex))
        ##
        
        with open(FileName, 'w') as script:
            script.write('''#!/bin/tcsh
            #PBS -N %(name)s
            #PBS -l nodes=%(nodes)d:ppn=%(ppn)d
            #PBS -l walltime=%(wt_hours)02d:%(wt_minutes)02d:%(wt_seconds)02d
            #PBS -d .
            source /usr/local/modules/init/tcsh
            module load boost gsl hdf5/x86_64/gnu/1.8.9-openmpi-psm postgresql            
            module load cfitsio/x86_64/gnu/3.290 skymaker/x86_64/gnu/3.3.3
            setenv PSM_SHAREDCONTEXTS_MAX %(ppn)d
            
            mpiexec %(executable)s %(path)s %(basicsettingpath)s
            %(MergeScriptName)s %(outputpath)s %(subjobindex)d %(UIJobReference)d
            cd %(outputpath)s
            tar -czf images.%(UIJobReference)d.tar.gz image.*.fits
            rm image.*.fits
            '''%self.DefaultParams)
        return FileName

    ##
    ## Submit a PBS job.
    ##
    ## @param[IN]  params  Parameter dictionary.
    ## @returns PBS job identifier.
    ##
    def Submit(self,UIJobReference,UserName,JobID,SubJobIndex,IsSquentialJob=False):
        
        
        
        ppn=1
        if IsSquentialJob==False:      
            ppn=int(self.Options['Torque:ProcessorNode'])
        queuename=self.Options['Torque:JobsQueue']        
        
        ScriptFileName = self.WritePBSScriptFile(UIJobReference,UserName,JobID, ppn,SubJobIndex)        
        logpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], UserName, str(UIJobReference),'log')  
               
        
        stdout = subprocess.check_output(shlex.split('ssh g2 \"cd %s; qsub -q %s %s\"'%(logpath.encode(locale.getpreferredencoding()), queuename.encode(locale.getpreferredencoding()), ScriptFileName.encode(locale.getpreferredencoding()))))
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
    def QueryPBSJob(self):        
        states = {}
        all_jobs = subprocess.check_output(shlex.split('ssh g2 qstat'))        
        lines = all_jobs.splitlines()[2:]
         
        CurrentJobs={} # Build dictionary with our jobs only
        for line in lines:
            LineParts=shlex.split(line)
            JobName=LineParts[1]            
            if JobName.find(self.Options['Torque:jobprefix'])==0:
                JobID=LineParts[0].split('.')[0]
                CurrentJobs[JobID]=LineParts[4]
        
            
         
        
        return CurrentJobs
    
    def TerminateJob(self,PBSID):
         try:
            logging.info("Trying to Terminate Job "+PBSID+" from the PBS queue....")
            output=subprocess.check_output(shlex.split('ssh g2 qdel '+PBSID))
            logging.info("Trying to Terminate Job "+PBSID+" : qdel output was:"+output)
         except Exception as Exp:
            logging.error(">>>>>Error While Terminating Job "+PBSID)
            logging.error(type(Exp))
            logging.error(Exp.args)
            logging.error(Exp)          
        
    
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
               
        
        
    
        
