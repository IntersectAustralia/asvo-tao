import os, shlex, subprocess, time, string,datetime,time
import requests
import dbase
import EnumerationLookup
import shutil
import ParseXML
import logging
import LogReader
import emailreport
import glob
import pg
import settingReader
import torque
import json

class SysCommands(object):
# 1- From UI Id get JobID or Jobs IDs

    

    def __init__(self,Options,dbaseobj,TorqueObj):
        
        logging.info('SysCommands Class Init')
        self.Options=Options
        self.dbaseobj=dbaseobj
        self.TorqueObj=TorqueObj
        self.KeepWorkFlowActive=True
        self.LogReaderObj=LogReader.LogReader(Options)
        # Define the request API.
        
        self.CommandCALLBackBase = Options['WorkFlowSettings:CallbackURL']
        self.commandapi = {
               'get': self.CommandCALLBackBase + 'workflowcommand/?execution_status=SUBMITTED',
               'update': self.CommandCALLBackBase + 'workflowcommand/%d/'}              
        
        self.CALLBackBase = Options['WorkFlowSettings:CallbackURL']
        self.api = {
               'get': self.CALLBackBase + 'job/?status=SUBMITTED',
               'update': self.CALLBackBase + 'job/%d/'}
        
        self.FunctionsMap={
                 'Job_Stop_All':self.Job_Stop_All,
                 'Job_Stop':self.Job_Stop,
                 'Job_Resume':self.Job_Resume,
                 'Workflow_Stop':self.Workflow_Stop,
                 'Workflow_Resume':self.Workflow_Resume,                 
                 'Job_Output_Delete':self.Job_Output_Delete                 
                 }
        
    def json_handler(self,resp):       
        
        CommandsCounter=0
        logging.info(resp.json)        
        logging.info("Meta Info for current Commands="+str(resp.json['meta']['total_count']))        
        for json in resp.json['objects']:            
            if self.HandleNewCommand(json)==True:
                CommandsCounter=CommandsCounter+1            
    
        return CommandsCounter
    
    def GetJobData(self,JobUIID):
        AssociatedJobs=self.dbaseobj.GetJobsStatusbyUIReference(JobUIID)
        return AssociatedJobs
    
    def CheckForNewCommands(self):
        
        try:
            logging.info("Checking for UI Commands")
            new_jobs = 0
            WebserviceResponse = requests.get(self.commandapi['get'])     
            
            new_commands_count=self.json_handler(WebserviceResponse)
            if new_commands_count>0:
                logging.info(str(new_commands_count)+" Commands Recieved From the UI")
        except Exception as Exp: 
            logging.error("Error in CheckForNewCommands")
            logging.error(type(Exp))
            logging.error(Exp.args)
            logging.error(Exp) 
    def HandleNewCommand(self,jsonObj):
        
        command=jsonObj['command']        
        UICommandID=jsonObj['id']        
        UIJobID=-1
        if jsonObj['job_id']!=None:
            UIJobID=jsonObj['job_id']['id']        
        CommandParams=jsonObj['parameters']
                
        logging.info("New Command Found")
        logging.info("UICommandID:"+str(UICommandID))
        logging.info("UIJobID:"+str(UIJobID))
        logging.info("commandtext:"+str(command))
        logging.info("CommandParams:"+str(CommandParams))
               
               
        
        CommandID=self.dbaseobj.AddNewCommand(UICommandID,command,UIJobID,CommandParams)
        logging.info("Command Local ID:"+str(CommandID))        
        
        CommandFunction=self.FunctionsMap[command]
        [ExecutionSucceeded,Message]=CommandFunction(UICommandID,UIJobID,CommandParams)
        if ExecutionSucceeded==True:
            self.dbaseobj.UpdateCommandStatus(CommandID,EnumerationLookup.CommandState.Completed)
            self.UpdateTAOCommandUI(UICommandID,True,Message)
        else:
            self.dbaseobj.UpdateCommandStatus(CommandID,EnumerationLookup.CommandState.Error)
            self.UpdateTAOCommandUI(UICommandID,False,Message)
        
    
    def Job_Stop_All(self,UICommandID,UIJobID,CommandParams):
        CurrentJobs_PBSID=self.dbaseobj.GetCurrentActiveJobs_pbsID()
        
        for PBsID in CurrentJobs_PBSID:
            PID=""
            if JobRow['pbsreferenceid']!=None:                
                PID=PBsID['pbsreferenceid'].split('.')[0]
            else:
                logging.info("Sorry This Job doesn't have pbsID. Job ID"+str(JobID))
                return [False,'Job '+str(JobID)+' is Missing its PBSID!']
            
            JobStatus=PBsID['jobstatus']
            UIReference_ID=PBsID['uireferenceid']
            UserName=PBsID['username']
            JobType=PBsID['jobtype']
            SubJobIndex=PBsID['subjobindex']
            JobID=PBsID['jobid']
            
            JobDetails={'start':-1,'progress':'0%','end':0,'error':'','endstate':''}
            [ExecutionResult,Message]=self.PauseJob(UICommandID, JobID, PID, JobStatus)
            if ExecutionResult==True:
                self.UpdateTAOJobUI(UIReference_ID) 
        logging.info("Job_Stop_All")
        return [True,'']

    def PauseJob(self, UICommandID, JobID, PBSID, JobStatus):
        logging.info("COMMAND Job_Stop: JobID=" + str(JobID))
        logging.info("COMMAND Job_Stop: PBSID" + str(PBSID))
        logging.info("COMMAND Job_Stop: JobStatus=" + str(JobStatus))
        ##If it is running stop it
        if (JobStatus <= EnumerationLookup.JobState.Running and JobStatus > EnumerationLookup.JobState.NewJob):
            logging.info("COMMAND Job_Stop: JobID=" + str(JobID) + " , Terminating Job From Queue")
            self.TorqueObj.TerminateJob(PBSID) ##If its status is running or before set it to pause
            self.dbaseobj.SetJobPaused(JobID, UICommandID)
            return [True,'']
        if (JobStatus <= EnumerationLookup.JobState.Running):
            logging.info("COMMAND Job_Stop: JobID=" + str(JobID) + " , SetJob to Pause")
            self.dbaseobj.SetJobPaused(JobID, UICommandID)
            return [True,'']
        else:
            return [False,'Job Is Not Running!']
        
    def Job_Stop(self,UICommandID,UIJobID,CommandParams):
        AssociatedJobsData=self.GetJobData(UIJobID)
        logging.info("COMMAND Job_Stop: JobUIID="+str(UIJobID)+" - Associated Jobs="+str(len(AssociatedJobsData)))
        ExecutionResult=False
        Message=''
        for JobRow in AssociatedJobsData:
            JobID=JobRow['jobid']
            
            
            PBSID=""
            if JobRow['pbsreferenceid']!=None:                
                PBSID=JobRow['pbsreferenceid'].split('.')[0]
            else:
                logging.info("Sorry This Job doesn't have pbsID. Job ID"+str(JobID))
                return [False,'The job does not have a queue ID!']
            JobStatus=JobRow['jobstatus']
            
            [ExecutionResult,Message]=self.PauseJob(UICommandID, JobID, PBSID, JobStatus)
        if ExecutionResult==True:
            self.dbaseobj.RemoveAllJobsWithUIReferenceID(UIJobID)
            self.UpdateTAOJobUI(UIJobID)                    
            logging.info("Job_Stop")
            return [True,'']
        else:
            return [False,Message]
    def Job_Resume(self,UICommandID,UIJobID,CommandParams):
        logging.info("Job_Resume is not currently supported")
        return [False,'Not Supported']
    def Workflow_Stop(self,UICommandID,UIJobID,CommandParams):
        self.KeepWorkFlowActive=False
        logging.info("Workflow_Stop")
        return [True,'']
    def Workflow_Resume(self,UICommandID,UIJobID,CommandParams):
        self.KeepWorkFlowActive=True
        logging.info("Workflow_Resume")
        return [True,'']    
    def Job_Output_Delete(self,UICommandID,UIJobID,CommandParams):
        logging.info("Job_Output_Delete")
        JobUserName=CommandParams
        BasedPath=os.path.join(self.Options['WorkFlowSettings:WorkingDir'], JobUserName, str(UIJobID))
        
        
        if (JobUserName==""):
            return [False,'User Name was not provided!']
        if(os.path.exists(BasedPath)):
           logging.info('Path already exists ... Clearing Files....'+BasedPath) 
           shutil.rmtree(BasedPath)
        
        
        
        return [True,'']
        
    
        
    def UpdateTAOJobUI(self,UIJobID):        
        
        data = {}                
        data['status'] = 'HELD'             
        data['error_message'] = "Status:JOB WAS TERMINATED BY ADMIN COMMAND"                
        logging.info('Updating UI MasterDB. JobID ('+str(UIJobID)+').. '+data['status'])        
        requests.put(self.api['update']%UIJobID, json.dumps(data))
    
    def UpdateTAOCommandUI(self,CommandID,IsCompleted,Message):        
        
        UpdateURL=self.commandapi['update']%CommandID
        data = {}      
        if IsCompleted==True:          
            data['execution_status'] = 'COMPLETED'             
            data['execution_comment'] = Message
        else:
            data['execution_status'] = 'ERROR'             
            data['execution_comment'] = Message
                
        logging.info('Updating UI MasterDB. CommandID ('+str(CommandID)+').. '+data['execution_status'])
        logging.info(UpdateURL)
        logging.info(data)
        requests.put(UpdateURL, json.dumps(data))        
                 
    
if __name__ == '__main__':
     [Options]=settingReader.ParseParams("settings.xml")     
     dbaseObj=dbase.DBInterface(Options)
     TorqueObj=torque.TorqueInterface(Options,dbaseObj)
     SysCommandsObj=SysCommands(Options,dbaseObj,TorqueObj)
     SysCommandsObj.CheckForNewCommands()
     
     