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

class SysCommands(object):
# 1- From UI Id get JobID or Jobs IDs

    

    def __init__(self,Options,dbaseobj,TorqueObj):
        
        logging.info('SysCommands Class Init')
        self.Options=Options
        self.dbaseobj=dbaseobj
        self.TorqueObj=TorqueObj
        self.LogReaderObj=LogReader.LogReader(Options)
        # Define the request API.
        
        self.CALLBackBase = Options['WorkFlowSettings:CommandsURL']
        self.api = {
               'get': self.CALLBackBase + 'commands/submitted',
               'update': self.CALLBackBase + 'commands/update'}
        
        self.FunctionsMap={
                 'Job_Stop_All':self.Job_Stop_All,
                 'Job_Stop':self.Job_Stop,
                 'Job_Resume':self.Job_Resume,
                 'Workflow_Stop':self.Workflow_Stop,
                 'Worflow_Resume':self.Worflow_Resume,
                 'Lighcone_acceleration_on':self.Lighcone_acceleration_on,
                 'Lighcone_acceleration_off':self.Lighcone_acceleration_off,
                 'Job_Output_Delete':self.Job_Output_Delete                 
                 }
        
    def json_handler(self,resp):       
        
        CommandsCounter=0
        
        for json in resp.json():
            
            if self.HandleNewCommand(json)==True:
                CommandsCounter=CommandsCounter+1            
    
        return CommandsCounter
    
    def GetJobData(self,JobUIID):
        AssociatedJobs=self.dbaseobj.GetJobsStatusbyUIReference(JobUIID)
        return AssociatedJobs
    
    def CheckForNewCommands(self):
        logging.info("Checking for UI Commands")
        new_jobs = 0
        WebserviceResponse = requests.get(self.api['get'])
        
        #ResponseType = string.replace(WebserviceResponse.headers['content-type'],"; charset=utf-8","")
        
        new_commands_count=self.json_handler(WebserviceResponse)
        if new_commands_count>0:
            logging.info(str(new_commands_count)+" Commands Recieved From the UI")
    
    def HandleNewCommand(self,jsonObj):
        
        UICommandID=jsonObj['commandid']
        UIJobID=jsonObj['jobid']
        commandtext=jsonObj['commandtext']
        CommandParams=jsonObj['commandparams']
        logging.info("New Command Found")
        logging.info("UICommandID:"+str(UICommandID))
        logging.info("UIJobID:"+str(UIJobID))
        logging.info("commandtext:"+str(commandtext))
        logging.info("CommandParams:"+str(CommandParams))
        
        CommandID=self.dbaseobj.AddNewCommand(UICommandID,commandtext,UIJobID,CommandParams)
        logging.info("Command Local ID:"+str(CommandID))        
        
        CommandFunction=self.FunctionsMap[commandtext]
        if CommandFunction(UICommandID,UIJobID,CommandParams)==True:
            self.dbaseobj.UpdateCommandStatus(CommandID,EnumerationLookup.CommandState.Completed)
        
    
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
        self.UpdateTAOUI(UIJobID)        
        print("Job_Stop")
        return True
    def Job_Resume(self,UICommandID,UIJobID,CommandParams):
        print("Job_Resume")
        return True
    def Workflow_Stop(self,UICommandID,UIJobID,CommandParams):
        print("Workflow_Stop")
        return True
    def Worflow_Resume(self,UICommandID,UIJobID,CommandParams):
        print("Worflow_Resume")
        return True
    def Lighcone_acceleration_on(self,UICommandID,UIJobID,CommandParams):
        print("Lighcone_acceleration_on")
        return True
    def Lighcone_acceleration_off(self,UICommandID,UIJobID,CommandParams):
        print("Lighcone_acceleration_off")
        return True
    def Job_Output_Delete(self,UICommandID,UIJobID,CommandParams):
        print("Job_Output_Delete")
        return True
        
    
        
    def UpdateTAOUI(self,UIJobID):        
        
        data = {}                
        data['status'] = 'HELD'             
        data['error_message'] = "Status:JOB WAS TERMINATED BY ADMIN COMMAND"                
        logging.info('Updating UI MasterDB. JobID ('+str(UIJobID)+').. '+data['status'])        
        requests.put(self.api['update']%UIJobID, data)        
                 
    
if __name__ == '__main__':
     [Options]=settingReader.ParseParams("localsettings.xml")     
     dbaseObj=dbase.DBInterface(Options)
     TorqueObj=torque.TorqueInterface(Options,dbaseObj)
     SysCommandsObj=SysCommands(Options,dbaseObj,TorqueObj)
     SysCommandsObj.CheckForNewCommands()
     
     