import os, shlex, subprocess, time, string,datetime,time
import requests
from torque import *
import dbase
import EnumerationLookup
import shutil
import ParseXML
import logging
import LogReader
import emailreport
import glob
import pg

class SysCommands(object):

    

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
        for json in resp.json:
            
            if self.HandleNewCommand(json)==True:
                CommandsCounter=CommandsCounter+1            
    
        return CommandsCounter
    
    def CheckForNewCommands(self):
        logging.info("Checking for UI Commands")
        new_jobs = 0
        WebserviceResponse = requests.get(self.api['get'])
        ResponseType = string.replace(WebserviceResponse.headers['content-type'],"; charset=utf-8","")
        
        new_commands_count=self.json_handler(WebserviceResponse)
        if new_commands_count>0:
            logging.info(str(new_commands_count)+" Commands Recieved From the UI")
    
    def HandleNewCommand(self,jsonObj):
        
        UICommandID=jsonObj['commandid']
        UIJobID=jsonObj['jobid']
        CommandType=jsonObj['commandtext']
        CommandParams=jsonObj['commandparams']
        logging.info("New Command Found")
        logging.info("UICommandID:"+str(UICommandID))
        logging.info("UIJobID:"+str(UIJobID))
        logging.info("commandtext:"+str(CommandType))
        logging.info("CommandParams:"+str(CommandParams))
        
        CommandID=self.dbaseobj.AddNewCommand(UICommandID,commandtext,UIJobID,CommandParams)
        logging.info("Command Local ID:"+str(CommandID))        
        
        CommandFunction=FunctionsMap[CommandType]
        return CommandFunction(UICommandID,UIJobID,CommandParams)
        
    
    def Job_Stop_All(self,UICommandID,UIJobID,CommandParams):
        CurrentJobs_PBSID=self.dbaseobj.GetCurrentActiveJobs_pbsID()
        
        for PBsID in CurrentJobs_PBSID:
            PID=PBsID['pbsreferenceid'].split('.')[0]
            OldStatus=PBsID['jobstatus']
            UIReference_ID=PBsID['uireferenceid']
            UserName=PBsID['username']
            JobType=PBsID['jobtype']
            SubJobIndex=PBsID['subjobindex']
            JobID=PBsID['jobid']
            JobDetails={'start':-1,'progress':'0%','end':0,'error':'','endstate':''}
            self.UpdateJob_EndWithError(JobID,SubJobIndex,JobType, UIReference_ID, UserName, JobDetails)
        print("Job_Stop_All")
        return True
    def Job_Stop(self,UICommandID,UIJobID,CommandParams):
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
        
    def UpdateJob_EndWithError(self, JobID,SubJobIndex, JobType, UIReference_ID, UserName, JobDetails):
        data = {}        
        
        
        logging.info("Job (" + str(UIReference_ID) +" ["+str(SubJobIndex)+"]) ... Finished With Error")
        
        data['status'] = 'FORCETERMINATION'
        JobDetails['error'] = "JOB WAS TERMINATED BY ADMIN COMMAND"
        
        
        
        self.dbaseobj.SetJobFinishedWithError(JobID, JobDetails['error'], JobDetails['end'])
        data['error_message'] = 'Error:' + JobDetails['error']        
        
        
        
        
        self.UpdateTAOUI(UIReference_ID,JobType, data)
        
    def UpdateTAOUI(self,UIJobID,JobType,data):
        ## If the job Type is Simple Update it without any checking  
        
        RequestedStatus=data['status']       
        
        logging.info('Updating UI MasterDB. JobID ('+str(UIJobID)+').. '+data['status'])        
        requests.put(self.api['update']%UIJobID, data)        
                 
    
if __name__ == '__main__':
     [Options]=settingReader.ParseParams("settings.xml")
     FilePath="/home/amr/workspace/samplecommands.txt"
     dbaseObj=""#=dbase.DBInterface(self.Options)
     TorqueObj=""#torque.TorqueInterface(self.Options,self.dbaseObj)
     SysCommandsObj=SysCommands(Options,dbaseObj,TorqueObj)
     
     