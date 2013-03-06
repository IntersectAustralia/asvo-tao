#!/usr/bin/env python

# logging --- http://docs.python.org/2/library/logging.html -- Event Logging
# shlex --- http://docs.python.org/2/library/shlex.html -- Lexical analyzer
# PBSPy --- http://code.google.com/p/py-pbs/ -- Python extension for OpenPBS/Torque


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

class WorkFlow(object):

    

    def __init__(self,Options,dbaseobj,TorqueObj):
        
        logging.info('Work Flow Class Init')
        self.Options=Options
        self.dbaseobj=dbaseobj
        self.TorqueObj=TorqueObj
        self.LogReaderObj=LogReader.LogReader(Options)
        # Define the request API.
        
        self.CALLBackBase = Options['WorkFlowSettings:CallbackURL']
        self.api = {
               'get': self.CALLBackBase + 'jobs/status/submitted',
               'update': self.CALLBackBase + 'jobs/%d'}
        

      
        
    def json_handler(self,resp):       
        
        JobsCounter=0
        for json in resp.json():
            
            if self.AddNewJob(json)==True:
                JobsCounter=JobsCounter+1            
    
        return JobsCounter
    
    
    def AddNewJob(self,jsonObj):
        
        UIJobReference=jsonObj['id']
        JobParams=jsonObj['parameters']
        JobDatabase=jsonObj['database']
        JobUserName=jsonObj['username']
        
        
        
        ## If a Job with the Same UI_ID exists ...ensure that it is out of the watch List (By Error State)
        self.dbaseobj.RemoveOldJobFromWatchList(UIJobReference)
        ## 1- Prepare the Job Directory
        SubJobsCount=self.PrepareJobFolder(JobParams,JobUserName,UIJobReference,JobDatabase)
        CurrentJobType=EnumerationLookup.JobType.Simple
        if SubJobsCount>1:
           CurrentJobType=EnumerationLookup.JobType.Complex     
        
        
        
                             
            
        ## Submit the Job to PBS and get back its ID
        for i in range(0,SubJobsCount):
            ## Add new Job and return its ID
            JobID=self.dbaseobj.AddNewJob(UIJobReference,CurrentJobType,JobParams,JobUserName,JobDatabase,i)
            ParamXMLName="params"+str(i)+".xml"
            PBSJobID=self.SubmitJobToPBS(JobID,JobUserName,UIJobReference,ParamXMLName,i)
            ## Store the Job PBS ID  
            self.dbaseobj.UpdateJob_PBSID(JobID,PBSJobID)
                
        ## Update the Job Status to Queued            
        #self.UpdateTAOUI(UIJobReference, data={'status': 'QUEUED'})
        return True
        
        
    def PrepareJobFolder(self,JobParams,JobUserName,UIJobReference,JobDatabase):
        ## Read User Settings 
        BasedPath=os.path.join(self.Options['WorkFlowSettings:WorkingDir'], 'jobs', JobUserName, str(UIJobReference))
        outputpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], 'jobs', JobUserName, str(UIJobReference),'output')
        logpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], 'jobs', JobUserName, str(UIJobReference),'log')
        AudDataPath=os.path.join(self.Options['Torque:AuxInputData'])
        
        
        ## If the Job's path exists ... Clear all its contents 
        if(os.path.exists(BasedPath)):
           logging.info('Path already exists ... Clearing Files....'+BasedPath) 
           shutil.rmtree(BasedPath)
           
        ## Create working folders     
        os.makedirs(outputpath)
        os.makedirs(logpath)
        
        
        ###############################################################
        #### Write params.xml (user version) to the output Directory
        with open(outputpath+'/params.xml', 'w') as file:
            file.write(JobParams.encode('utf8'))
            file.close()
        
        
        ## Parse the XML file to extract job Information and get if the job is complex or single lightcone
        ParseXMLParametersObj=ParseXML.ParseXMLParameters(outputpath+'/params.xml',self.Options)
        SubJobsCount=ParseXMLParametersObj.ParseFile(UIJobReference,JobDatabase,JobUserName)    
        
        ## Generate params?.xml files based on the requested jobscounts
        ParseXMLParametersObj.ExportTrees(logpath+"/params<index>.xml")    
        
        
        src_files = os.listdir(AudDataPath)
        for file_name in src_files:
            full_file_name = os.path.join(AudDataPath, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, logpath)
            
        return SubJobsCount   
        
    def SubmitJobToPBS(self,JobID,JobUserName,UIJobReference,ParamXMLName,SubJobIndex=0):
        
        ## Read User Settings      
        logpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], 'jobs', JobUserName, str(UIJobReference),'log')                
        
        old_dir = os.getcwd()
        os.chdir(logpath)           
                
        ############################################################
        ### Submit the Job to the PBS Queue
        PBSJobID=self.TorqueObj.Submit(JobUserName,JobID,logpath,ParamXMLName,SubJobIndex)
        
        ### Return back to the previous folder    
        os.chdir(old_dir)
        
        ## Return JobID
        return PBSJobID
                
    def UpdateTAOUI(self,UIJobID,data):        
        logging.info('Updating UI MasterDB. JobID ('+str(UIJobID)+').. '+data['status'])        
        requests.put(self.api['update']%UIJobID, data)
        
   
    def xml_handler(self,resp):
        xml = resp.xml
        self.dbaseobj.AddNewEvent(0,EnumerationLookup.EventType.Error,"XML Response Handler is not supported: "+xml)
        
        
    def GetNewJobsFromMasterDB(self):
        
        content_handlers = {'application/json': self.json_handler,'application/xml': self.xml_handler}
        ## 1- Check for any newly submitted jobs.
        logging.info('Checking For New Job')
        self.dbaseobj.AddNewEvent(0,EnumerationLookup.EventType.Normal,'Checking for new jobs.')
        new_jobs = 0
        WebserviceResponse = requests.get(self.api['get'])
        ResponseType = string.replace(WebserviceResponse.headers['content-type'],"; charset=utf-8","")
        
        #####################################################################
        if ResponseType in content_handlers:
            CallBackFunction=content_handlers[ResponseType]
            new_jobs_count = CallBackFunction(WebserviceResponse)
            if new_jobs_count>0:
                logging.info('Found '+str(new_jobs_count)+' New Jobs ')
                self.dbaseobj.AddNewEvent(0,EnumerationLookup.EventType.Normal,'Found '+str(new_jobs_count)+' New Jobs ')            
        else:
            logging.error('UnKnow Response type from webservice.. Current Content:  '+ResponseType)
            
    def GetProcessStartTime(self,PBSID):        
        return self.TorqueObj.GetJobStartTime(PBSID)
    
    def GetJobstderrcontents(self,UserName,JobID,LocalJobID):
        
        JobName='tao_'+UserName[:4]+'_'+str(LocalJobID)
        path = os.path.join(self.Options['WorkFlowSettings:WorkingDir'],'jobs', UserName, str(JobID),'log')
        old_dir = os.getcwd()
        os.chdir(path)
        stderrstring=''
        listoffiles=glob.glob(JobName+".e*")
        logging.info("Searching for File:"+JobName+".e*")
        counter=10
        while (len(listoffiles)==0 and counter>0):
            counter=counter-1
            logging.info('No stderr file found... Will retry for more '+str(counter)+' times')
            time.sleep(1)
            listoffiles=glob.glob(JobName+".e*")
            
        if len(listoffiles)>0:        
            stderrfile=listoffiles[0]                   
            logging.info('Job Finished With Error, reading error information from:'+stderrfile)
            LogFile = open(stderrfile, "r")
            stderrstring=pg.escape_string(LogFile.read())
        else:
            stderrstring='Cannot file the stderr file:'+JobName
        os.chdir(old_dir)     
        return stderrstring
    def ProcessJobs(self):
        
        ## Get Current Active Jobs (Job Status<Complete)
        CurrentJobs_PBSID=self.dbaseobj.GetCurrentActiveJobs_pbsID()
       
        
        if len(CurrentJobs_PBSID)==0:
            ## Nothing to do ... There are no Jobs in my Watch List
            return
        
        now=datetime.datetime.now()
        logging.info(str(len(CurrentJobs_PBSID))+" Jobs Found in the current watch list")
        self.dbaseobj.AddNewEvent(0,EnumerationLookup.EventType.Normal,'Checking for Current Jobs. Jobs Count='+str(len(CurrentJobs_PBSID)))
        
            
        
        
        ## Query PBS for current Jobs that belong to TAO
        CurrentJobs=self.TorqueObj.QueryPBSJob(CurrentJobs_PBSID)    
        
        
        logging.info(str(CurrentJobs))
        
        logging.info(str(CurrentJobs_PBSID))
        
        JobsStatus=[]
        for PBsID in CurrentJobs_PBSID:
            

            ## --------------------------------------------------------------------
            ## PBsID[0] ===> Workflow JobID
            ## PBsID[1] ===> Current PBS ID
            ## PBsID[2] ===> Old Status (Current Db Status) 
            ## PBsID[3] ===> UIReference_ID
            ## PBsID[4] ===> User Name
            ## ---------------------------------------------------------------------
            data = {}            
            
            
            PID=PBsID[1].split('.')[0]
            OldStatus=PBsID[2]
            UIReference_ID=PBsID[3]
            UserName=PBsID[4]
            
            ### **********************************************************************
            ## Parse the Job Log File and Extract Current Job Status            
            JobDetails=self.LogReaderObj.ParseFile(UserName,UIReference_ID)
             
            ### ***********************************************************************
            
            ###########################################################################################################
            ## 1- Change In Job Status to Running 
            if  PID in CurrentJobs and (CurrentJobs[PID]=='R' and OldStatus!=EnumerationLookup.JobState.Running) : 
                JobStartTime=datetime.datetime.now().timetuple()
                try:                                    
                    JobStartTime=self.GetProcessStartTime(PID)
                except Exception as Exp:
                    logging.error('Error In Getting Start time for Job '+str(PID))
                    logging.error(Exp)    
                    
                
                self.dbaseobj.SetJobRunning(PBsID[0],OldStatus,"Job Running- PBSID"+PID,JobStartTime)                
                data['status']='IN_PROGRESS'
                
                #requests.put(self.api['update']%UIReference_ID, data=data)
                self.UpdateTAOUI(UIReference_ID, data)
                
                self.dbaseobj.AddNewEvent(PBsID[0],EnumerationLookup.EventType.Normal,'Updating Job (UI ID:'+str(UIReference_ID)+', Status:'+data['status']+')')
                logging.info("Job ("+str(UIReference_ID)+") ... Running") 
            ############################################################################################################   
            ## 2-  Change In Job Status to Queued
            elif  PID in CurrentJobs and (CurrentJobs[PID]=='Q' and OldStatus!=EnumerationLookup.JobState.Queued): 
                self.dbaseobj.SetJobQueued(PBsID[0],OldStatus,"Job Queued- PBSID"+PID)                 
                data['status']='QUEUED'         
                #requests.put(self.api['update']%UIReference_ID, data=data)
                self.UpdateTAOUI(UIReference_ID, data)
                self.dbaseobj.AddNewEvent(PBsID[0],EnumerationLookup.EventType.Normal,'Updating Job (UI ID:'+str(UIReference_ID)+', Status:'+data['status']+')')
                logging.info("Job ("+str(UIReference_ID)+") ... Queued")
            ############################################################################################################
            ## 3- Job Status Unknown ... It is still in the queue but it is not Q or R !     
            elif  PID in CurrentJobs and CurrentJobs[PID]!='R' and CurrentJobs[PID]!='Q' : 
                logging.info('Job Status UNKnow '+str(UIReference_ID)+' :'+CurrentJobs[PID])              
            ############################################################################################################
            ## 4- Job Cannot Be Found in the queue ... In this case the Log File Status determine how its termination status    
            elif (PID not in CurrentJobs):
                
                ###### If The log file does not exist, Please put a dummy JobDetails
                if JobDetails==None:
                    JobDetails={'start':-1,'progress':'0%','end':0,'error':'','endstate':''}
                
                ##### Job Terminated Successfully    
                if  JobDetails['endstate']=='successful': 
                    path = os.path.join('jobs', PBsID[4], str(PBsID[3]))
                    self.dbaseobj.SetJobComplete(PBsID[0],PBsID[2],path,JobDetails['end'])                
                    data['status']='COMPLETED'
                    path = os.path.join('jobs', UserName, str(UIReference_ID),'output')                
                    data['output_path'] = path
                    
                    #requests.put(self.api['update']%UIReference_ID, data=data)
                    self.UpdateTAOUI(UIReference_ID, data)
                    self.dbaseobj.AddNewEvent(PBsID[0],EnumerationLookup.EventType.Normal,'Updating Job (UI ID:'+str(UIReference_ID)+', Status:'+data['status']+')')
                    logging.info ("Job ("+str(UIReference_ID)+") ... Finished Successfully")
                    Message="Job ("+str(UIReference_ID)+") Path:"+path+" Finished Successfully"
                    emailreport.SendEmailToAdmin(self.Options,"Workflow update",Message)
                ##### Job Terminated with error or was killed by the Job Queue    
                else:
                    
                    logging.info ("Job ("+str(UIReference_ID)+") ... Finished With Error")
                    
                    stderr=self.GetJobstderrcontents(UserName,UIReference_ID,PBsID[0])
                    
                      
                    
                    data['status']='ERROR'           
                    if JobDetails['error']=='':
                        JobDetails['error']=stderr
                    self.dbaseobj.SetJobFinishedWithError(PBsID[0],PBsID[2],JobDetails['error'],JobDetails['end'])                         
                    data['error_message'] = 'Error:'+JobDetails['error']                    
                    #requests.put(self.api['update']%UIReference_ID, data=data)
                    self.UpdateTAOUI(UIReference_ID, data)
                    self.dbaseobj.AddNewEvent(PBsID[0],EnumerationLookup.EventType.Normal,'Updating Job (UI ID:'+str(UIReference_ID)+', Status:'+data['status']+')')
                    Message="Job ("+str(UIReference_ID)+")  Finished With Error. The Error Message is:" + data['error_message']
                    emailreport.SendEmailToAdmin(self.Options,"Job Finished With Error",Message)    
            ###############################################################################################################
            ## 5- The Job didn't change its status... Show its progess information if Exists!        
            else:
                if JobDetails!=None:
                    logging.info ("Job ("+str(UIReference_ID)+") .. : Progress="+JobDetails['progress'])
                else:
                    logging.info ("Job ("+str(UIReference_ID)+") .. : Log File Does not exist")
                
        
            
            
            
            
        
        
        
        
        
                
            
        
        

    

