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
                 'Worflow_Resume':self.Worflow_Resume,                 
                 'Job_Output_Delete':self.Job_Output_Delete                 
                 }
        
    def json_handler(self,resp):       
        
        CommandsCounter=0
        print resp.json()        
        logging.info("Meta Info for current Commands="+str(resp.json()['meta']['total_count']))        
        for json in resp.json()['objects']:            
            if self.HandleNewCommand(json)==True:
                CommandsCounter=CommandsCounter+1            
    
        return CommandsCounter
    
    def GetJobData(self,JobUIID):
        AssociatedJobs=self.dbaseobj.GetJobsStatusbyUIReference(JobUIID)
        return AssociatedJobs
    
    def CheckForNewCommands(self):
        logging.info("Checking for UI Commands")
        new_jobs = 0
        WebserviceResponse = requests.get(self.commandapi['get'])     
        
        new_commands_count=self.json_handler(WebserviceResponse)
        if new_commands_count>0:
            logging.info(str(new_commands_count)+" Commands Recieved From the UI")
    
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
        #if CommandFunction(UICommandID,UIJobID,CommandParams)==True:
        self.dbaseobj.UpdateCommandStatus(CommandID,EnumerationLookup.CommandState.Completed)
        self.UpdateTAOCommandUI(UICommandID)
    
    def Job_Stop_All(self,UICommandID,UIJobID,CommandParams):
        CurrentJobs_PBSID=self.dbaseobj.GetCurrentActiveJobs_pbsID()
        
        for PBsID in CurrentJobs_PBSID:
            PID=PBsID['pbsreferenceid'].split('.')[0]
            JobStatus=PBsID['jobstatus']
            UIReference_ID=PBsID['uireferenceid']
            UserName=PBsID['username']
            JobType=PBsID['jobtype']
            SubJobIndex=PBsID['subjobindex']
            JobID=PBsID['jobid']
            
            JobDetails={'start':-1,'progress':'0%','end':0,'error':'','endstate':''}
            self.PauseJob(UICommandID, JobID, PID, JobStatus)
        print("Job_Stop_All")
        return True

    def PauseJob(self, UICommandID, JobID, PBSID, JobStatus):
        logging.info("COMMAND Job_Stop: JobID=" + str(JobID))
        logging.info("COMMAND Job_Stop: PBSID" + str(PBSID))
        logging.info("COMMAND Job_Stop: JobStatus=" + str(JobStatus))
        ##If it is running stop it
        if (JobStatus <= EnumerationLookup.JobState.Running and JobStatus > EnumerationLookup.JobState.NewJob):
            logging.info("COMMAND Job_Stop: JobID=" + str(JobID) + " , Terminating Job From Queue")
            #self.TorqueObj.TerminateJob(PBSID) ##If its status is running or before set it to pause
        if (JobStatus <= EnumerationLookup.JobState.Running):
            logging.info("COMMAND Job_Stop: JobID=" + str(JobID) + " , SetJob to Pause")
            self.dbaseobj.SetJobPaused(JobID, UICommandID)

    def Job_Stop(self,UICommandID,UIJobID,CommandParams):
        AssociatedJobsData=self.GetJobData(UIJobID)
        logging.info("COMMAND Job_Stop: JobUIID="+str(UIJobID)+" - Associated Jobs="+str(len(AssociatedJobsData)))
        
        for JobRow in AssociatedJobsData:
            JobID=JobRow['jobid']
            PBSID=JobRow['pbsreferenceid'].split('.')[0]
            JobStatus=JobRow['jobstatus']
            
            self.PauseJob(UICommandID, JobID, PBSID, JobStatus)
        self.UpdateTAOJobUI(UIJobID)        
        print("Job_Stop")
        return True
    def Job_Resume(self,UICommandID,UIJobID,CommandParams):
        logging.info("Job_Resume is not currently supported")
        return True
    def Workflow_Stop(self,UICommandID,UIJobID,CommandParams):
        self.KeepWorkFlowActive=False
        print("Workflow_Stop")
        return True
    def Worflow_Resume(self,UICommandID,UIJobID,CommandParams):
        self.KeepWorkFlowActive=True
        print("Worflow_Resume")
        return True    
    def Job_Output_Delete(self,UICommandID,UIJobID,CommandParams):
        print("Job_Output_Delete")
        JobUserName=CommandParams
        BasedPath=os.path.join(self.Options['WorkFlowSettings:WorkingDir'], JobUserName, str(UIJobID))
        outputpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], JobUserName, str(UIJobID),'output')
        
        
        if(os.path.exists(outputpath)):
           logging.info('Path already exists ... Clearing Files....'+outputpath) 
           shutil.rmtree(outputpath)
        
        
        
        return True
        
    
        
    def UpdateTAOJobUI(self,UIJobID):        
        
        data = {}                
        data['status'] = 'HELD'             
        data['error_message'] = "Status:JOB WAS TERMINATED BY ADMIN COMMAND"                
        logging.info('Updating UI MasterDB. JobID ('+str(UIJobID)+').. '+data['status'])        
        requests.put(self.api['update']%UIJobID, json.dumps(data))
    
    def UpdateTAOCommandUI(self,CommandID):        
        
        UpdateURL=self.commandapi['update']%CommandID
        data = {}                
        data['execution_status'] = 'COMPLETED'             
        data['execution_comment'] = ""                
        #logging.info('Updating UI MasterDB. CommandID ('+str(CommandID)+').. '+data['execution_status'])        
        print('Updating UI MasterDB. CommandID ('+str(CommandID)+').. '+data['execution_status'])
        print(UpdateURL)
        print(data)
        requests.put(UpdateURL, json.dumps(data))        
                 
    
if __name__ == '__main__':
     [Options]=settingReader.ParseParams("settings.xml")     
     dbaseObj=dbase.DBInterface(Options)
     TorqueObj=torque.TorqueInterface(Options,dbaseObj)
     SysCommandsObj=SysCommands(Options,dbaseObj,TorqueObj)
     SysCommandsObj.CheckForNewCommands()
     
     