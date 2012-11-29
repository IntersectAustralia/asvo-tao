#!/usr/bin/env python

# logging --- http://docs.python.org/2/library/logging.html -- Event Logging
# shlex --- http://docs.python.org/2/library/shlex.html -- Lexical analyzer
# PBSPy --- http://code.google.com/p/py-pbs/ -- Python extension for OpenPBS/Torque


import os, shlex, subprocess, time, string
import requests
from torque import *
import dbase
import EnumerationLookup

class WorkFlow(object):

    

    def __init__(self,Options,dbaseobj,TorqueObj):
        
        self.Options=Options
        self.dbaseobj=dbaseobj
        self.TorqueObj=TorqueObj

        # Define the request API.
        
        self.CALLBackBase = Options['WorkFlowSettings:CallbackURL']
        self.api = {
               'get': self.CALLBackBase + 'jobs/status/submitted',
               'update': self.CALLBackBase + 'jobs/%d'}
        

      
        
    def json_handler(self,resp):
        JobsCounter=0
        for json in resp.json:
            
            
            UIJobReference=json['id']
            JobParams=json['parameters']
            JobUserName=json['username']
            
            
            JobID=self.dbaseobj.AddNewJob(UIJobReference,0,JobParams,JobUserName)
            
            if JobID!=-1:     
                           
                JobsCounter=JobsCounter+1
                
                PBSJobID=self.SubmitJobToPBS(JobID,JobParams,JobUserName,UIJobReference)  
                self.dbaseobj.UpdateJob_PBSID(JobID,PBSJobID)
                
            
                self.UpdateMasterDB(UIJobReference, 'QUEUED')
            
    
        return JobsCounter
    
    def SubmitJobToPBS(self,JobID,JobParams,JobUserName,UIJobReference):
        
        
        path = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], 'jobs', JobUserName, str(UIJobReference))
        
        
        os.makedirs(path)
        old_dir = os.getcwd()
        os.chdir(path)

        with open('params.xml', 'w') as file:
            file.write(JobParams)

        PBSJobID=self.TorqueObj.Submit(JobUserName,JobID)
            
        os.chdir(old_dir)
        
        return PBSJobID
                
    def UpdateMasterDB(self,UIJobID,Status):
        requests.put(self.api['update']%UIJobID, data={'status': Status})
   
    def xml_handler(self,resp):
        xml = resp.xml
        self.dbaseobj.AddNewEvent(0,EnumerationLookup.EventType.Error,"XML Response Handler is not supported: "+xml)
        
        
    def GetNewJobsFromMasterDB(self):
        
        content_handlers = {'application/json': self.json_handler,'application/xml': self.xml_handler}
        # Check for any newly submitted jobs.
        self.dbaseobj.AddNewEvent(0,EnumerationLookup.EventType.Normal,'Checking for new jobs.')
        new_jobs = 0
        WebserviceResponse = requests.get(self.api['get'])
        ResponseType = string.replace(WebserviceResponse.headers['content-type'],"; charset=utf-8","")
        
        CallBackFunction=content_handlers[ResponseType]
        new_jobs_count = CallBackFunction(WebserviceResponse)
        
        self.dbaseobj.AddNewEvent(0,EnumerationLookup.EventType.Normal,'Found '+str(new_jobs_count)+' New Jobs ')            
    
    def ProcessJobs(self):
        
        CurrentJobs_PBSID=self.dbaseobj.GetCurrentActiveJobs_pbsID()
        
        
        JobsStatus=self.TorqueObj.QueryPBSJob(CurrentJobs_PBSID)    
        
        for job in JobsStatus:
            data = {}            
            data['status']=job[1]            
            if job[1]=='COMPLETED':
                path = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], 'jobs', job[2], str(job[0]))
                data['output_path'] = path
            requests.put(self.api['update']%job[0], data=data)
        
        

    

