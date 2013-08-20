#!/usr/bin/env python

# logging --- http://docs.python.org/2/library/logging.html -- Event Logging
# shlex --- http://docs.python.org/2/library/shlex.html -- Lexical analyzer
# PBSPy --- http://code.google.com/p/py-pbs/ -- Python extension for OpenPBS/Torque


import os, shlex, subprocess, time, string,datetime,time
import requests
import json
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
import stat
import ParseProfileData
import traceback

class WorkFlow(object):

    

    def __init__(self,Options,dbaseobj,TorqueObj):
        
        logging.info('Work Flow Class Init')
        self.Options=Options
        self.dbaseobj=dbaseobj
        self.TorqueObj=TorqueObj
        self.LogReaderObj=LogReader.LogReader(Options)
        self.JobBaseDir=self.Options['Torque:outputbasedir']
        # Define the request API.
        
        self.CALLBackBase = Options['WorkFlowSettings:CallbackURL']
        self.api = {
               'get': self.CALLBackBase + 'job/?status=SUBMITTED',
               'update': self.CALLBackBase + 'job/%d/'}
        

      
        
    def json_handler(self,resp):       
        
        JobsCounter=0
        logging.info("Meta Info for current Jobs="+str(resp.json['meta']['total_count']))
        for json in resp.json['objects']:
            
            if self.AddNewJob(json)==True:
                JobsCounter=JobsCounter+1            
    
        return JobsCounter
    
    
    def AddNewJob(self,jsonObj):
        
        UIJobReference=jsonObj['id']
        JobParams=jsonObj['parameters']
        JobDatabase=jsonObj['database']
        JobUserName=jsonObj['user_id']['username']
        return self.ProcessNewJob(UIJobReference, JobParams, JobDatabase, JobUserName)
        
        
        
    def ProcessNewJob(self,UIJobReference,JobParams,JobDatabase,JobUserName):       
        
        try:
            ## If a Job with the Same UI_ID exists ...ensure that it is out of the watch List (By Error State)
            self.dbaseobj.RemoveOldJobFromWatchList(UIJobReference)
            ## 1- Prepare the Job Directory
            SubJobsCount=self.PrepareJobFolder(JobParams,JobUserName,UIJobReference,JobDatabase)
            CurrentJobType=EnumerationLookup.JobType.Simple
            if SubJobsCount>1:
               CurrentJobType=EnumerationLookup.JobType.Complex     
            
            
            logpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], JobUserName, str(UIJobReference),'log')                
            outputpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], JobUserName, str(UIJobReference),'output')
            old_dir = os.getcwd()
            os.chdir(logpath)
        except Exception as Exp:             
            data = {}              
            data['status'] = 'ERROR'
            data['error_message']="Workflow Cannot start this job. Please check the params " + str(Exp.args) 
            self.UpdateTAOUI(UIJobReference,EnumerationLookup.JobType.Simple, data)  
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logging.error(''.join('!! ' + line for line in lines))
            return False
        
        ###################Profiling####################################################
        try:                 
            self.ParseProfileDataObj=ParseProfileData.ParseProfileData(logpath,0,self.Options) 
            [Boxes,Tables,Galaxies,Trees]=self.ParseProfileDataObj.ParseFile()       
            logging.info('Number of Boxes='+str(Boxes))
            logging.info('Total Queries='+str(Tables))
            logging.info('Maximum Galaxies='+str(Galaxies))
            logging.info('Maximum Trees='+str(Trees))
        except Exception as Exp:
             logging.error("Error In Profiling")
             
        #############################################################################
        
        
        
                             
              
        ## Submit the Job to PBS and get back its ID
        for i in range(0,SubJobsCount):
            ## Add new Job and return its ID
            JobID=self.dbaseobj.AddNewJob(UIJobReference,CurrentJobType,JobParams,JobUserName,JobDatabase,i)
            ParamXMLName="params"+str(i)+".xml"       
            ############################################################
            ### Submit the Job to the PBS Queue
            PBSJobID=self.TorqueObj.Submit(JobUserName,JobID,logpath,outputpath,ParamXMLName,i)
            ## Store the Job PBS ID  
            if self.dbaseobj.UpdateJob_PBSID(JobID,PBSJobID)!=True:
                raise  Exception('Error in Process New Job','Update PBSID failed')
            
        os.chdir(old_dir)
                
        ## Update the Job Status to Queued            
        self.UpdateTAOUI(UIJobReference, CurrentJobType, data={'status': 'QUEUED'})        
        
        return True
        
        
    def PrepareJobFolder(self,JobParams,JobUserName,UIJobReference,JobDatabase):
        ## Read User Settings 
        BasedPath=os.path.join(self.Options['WorkFlowSettings:WorkingDir'],  JobUserName, str(UIJobReference))
        outputpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'],  JobUserName, str(UIJobReference),'output')
        logpath = os.path.join(self.Options['WorkFlowSettings:WorkingDir'],  JobUserName, str(UIJobReference),'log')
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
        logging.info("AudDataPath:"+AudDataPath)
        for file_name in src_files:
            full_file_name = os.path.join(AudDataPath, file_name)
            logging.info(full_file_name)
            if (os.path.isfile(full_file_name)):
                logging.info(full_file_name+"->"+logpath)
                shutil.copy(full_file_name, logpath)
            
        return SubJobsCount   
        
    
        
        
                
    def UpdateTAOUI(self,UIJobID,JobType,data):
        ## If the job Type is Simple Update it without any checking  
        Update=False
        if JobType==EnumerationLookup.JobType.Simple:      
            Update=True
        ## For complex jobs ... More checking is required
        else:
            RequestedStatus=data['status']
            
            if RequestedStatus=='IN_PROGRESS' or RequestedStatus=='ERROR':
                Update=True                
            else:
                Update=self.AllJobsInSameStatus(UIJobID,RequestedStatus)
                    
                 
                
        
        if Update==True:
            logging.info('Updating UI MasterDB. JobID ('+str(UIJobID)+').. '+data['status']) 
            UpdateURL=self.api['update']%UIJobID
            logging.info('Update Job Status:'+(self.api['update']%UIJobID))
            logging.info(str(data))       
            Response=requests.put(UpdateURL, json.dumps(data))
            logging.info('Response: '+str(Response.text))
            
    def AllJobsInSameStatus(self,UIReference_ID,RequestedStatus):
        StatusMapping={'QUEUED':EnumerationLookup.JobState.Queued,'COMPLETED':EnumerationLookup.JobState.Completed,'ERROR':EnumerationLookup.JobState.Error}
        RequestedState=StatusMapping[RequestedStatus]        
        
        ListofSubJobs=self.dbaseobj.GetJobsStatusbyUIReference(UIReference_ID)        
                
        for JobItem in ListofSubJobs:
            if JobItem['jobstatus']!=RequestedState:
                return False
        logging.info('***** All Jobs ('+str(UIReference_ID)+')Are In state:'+str(RequestedState))    
        return True
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
    
    
    
    def ChangePBSFilesmod(self,UserName,JobID,LocalJobID):
        
        JobName=self.Options['Torque:jobprefix']+UserName[:4]+'_'+str(LocalJobID)
        
        path = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], UserName, str(JobID),'log')
        old_dir = os.getcwd()
        os.chdir(path)
        
        listoffiles=glob.glob(JobName+".*")
        logging.info('Changing Mod for Files:'+str(listoffiles))
        for PBSFile in listoffiles:
            logging.info('Changing Mod for File:'+PBSFile)
            os.chmod(PBSFile,  stat.S_IRUSR|  stat.S_IWUSR |  stat.S_IRGRP )
        os.chdir(old_dir)     
        
    
    
    
    
    
    
    def GetJobstderrcontents(self,UserName,JobID,LocalJobID):
        
        JobName=self.Options['Torque:jobprefix']+UserName[:4]+'_'+str(LocalJobID)
        
        path = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], UserName, str(JobID),'log')
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
        CurrentJobs=self.TorqueObj.QueryPBSJob()    
        
        
        logging.info("PBS Jobs:"+str(CurrentJobs))
        
        logging.info("Database Jobs:"+str(CurrentJobs_PBSID))
        
        JobsStatus=[]
        for PBsID in CurrentJobs_PBSID:
                                
            
           
            PID=PBsID['pbsreferenceid'].split('.')[0]
            OldStatus=PBsID['jobstatus']
            UIReference_ID=PBsID['uireferenceid']
            UserName=PBsID['username']
            JobType=PBsID['jobtype']
            SubJobIndex=PBsID['subjobindex']
            JobID=PBsID['jobid']
            
            logging.info("Checking Job Status : JobID="+PID+"\tInPBSList="+str(PID in CurrentJobs))
            if PID in CurrentJobs:
                logging.info("Checking Job Status : JobID="+PID+"\tStatus="+str(CurrentJobs[PID]))
            
            ## Parse the Job Log File and Extract Current Job Status            
            JobDetails=self.LogReaderObj.ParseFile(UserName,UIReference_ID,SubJobIndex)
             
            
            
            
            ## 1- Change In Job Status to Running 
            if  PID in CurrentJobs and CurrentJobs[PID]=='R': 
                if OldStatus!=EnumerationLookup.JobState.Running:
                    self.UpdateJob_Running(PID,SubJobIndex,JobType, OldStatus, UIReference_ID, JobID)
                elif JobDetails!=None:
                    logging.info ("Job ("+str(UIReference_ID)+" ["+str(SubJobIndex)+"]) .. : Progress="+JobDetails['progress'])
                else:
                    logging.info ("Job ("+str(UIReference_ID)+") .. : Log File Does not exist") 
               
            ## 2-  Change In Job Status to Queued
            elif  PID in CurrentJobs and CurrentJobs[PID]=='Q': 
                if OldStatus!=EnumerationLookup.JobState.Queued:
                    self.UpdateJob_Queued(PID,SubJobIndex,JobType, OldStatus, UIReference_ID, JobID)
                else:
                    logging.info("Jobs Still Queued ...")
            ## 3- Job Status Unknown ... It is still in the queue but it is not Q or R !     
            elif  PID in CurrentJobs and CurrentJobs[PID]!='R' and CurrentJobs[PID]!='Q' : 
                logging.info('Job Status UNKnow '+str(UIReference_ID)+' :'+CurrentJobs[PID])              
            
            ## 4- Job Cannot Be Found in the queue ... In this case the Log File Status determine how its termination status    
            elif (PID not in CurrentJobs):
                
                ###### If The log file does not exist, Please put a dummy JobDetails
                if JobDetails==None:
                    JobDetails={'start':-1,'progress':'0%','end':0,'error':'','endstate':''}
                
                    
                if  JobDetails['endstate']=='successful':
                    ##### Job Terminated Successfully 
                    self.UpdateJob_EndSuccessfully(JobID,SubJobIndex,JobType, UIReference_ID, UserName, JobDetails) 
                    self.ChangePBSFilesmod(UserName, UIReference_ID, JobID)                   
                else:
                    ##### Job Terminated with error or was killed by the Job Queue                    
                    self.UpdateJob_EndWithError(JobID,SubJobIndex,JobType, UIReference_ID, UserName, JobDetails)
                    self.ChangePBSFilesmod(UserName, UIReference_ID, JobID)  
                    break    
            ###############################################################################################################
            ## 5- The Job didn't change its status... Show its progess information if Exists!        
            else:
                logging.info("Job Status Checking is not known!!")

    def UpdateJob_EndSuccessfully(self, JobID,SubJobIndex, JobType, UIReference_ID, UserName, JobDetails):
        
        data = {}  
        
        path = os.path.join(self.JobBaseDir, UserName, str(UIReference_ID))
        self.dbaseobj.SetJobComplete(JobID, path, JobDetails['end'])
        data['status'] = 'COMPLETED'
        
        path = os.path.join(self.JobBaseDir, UserName, str(UIReference_ID), 'output')
        data['output_path'] = path
        
        self.UpdateTAOUI(UIReference_ID,JobType, data)
        self.dbaseobj.AddNewEvent(JobID, EnumerationLookup.EventType.Normal, 'Updating Job (UI ID:' + str(UIReference_ID) + ', Status:' + data['status'] + ')')
        logging.info("Job (" + str(UIReference_ID) +" ["+str(SubJobIndex)+"]) ... Finished Successfully")
        Message = "Job (" + str(UIReference_ID) +" ["+str(SubJobIndex)+"]) Path:" + path + " Finished Successfully"
        emailreport.SendEmailToAdmin(self.Options, "Workflow update", Message)

    def UpdateJob_EndWithError(self, JobID,SubJobIndex, JobType, UIReference_ID, UserName, JobDetails):
        data = {}  
        
        TerminateAllOnError=(self.Options['WorkFlowSettings:TerminateSubJobsOnError']=='On')
        
        
        logging.info("Job (" + str(UIReference_ID) +" ["+str(SubJobIndex)+"]) ... Finished With Error")
        stderr = self.GetJobstderrcontents(UserName, UIReference_ID, JobID)
        data['status'] = 'ERROR'
        if JobDetails['error'] == '':
            JobDetails['error'] = stderr
        
        
        
        self.dbaseobj.SetJobFinishedWithError(JobID, JobDetails['error'], JobDetails['end'])
        data['error_message'] = 'Error:' + JobDetails['error']        
        
        if TerminateAllOnError==True:
            SubJobsList=self.dbaseobj.GetJobsStatusbyUIReference(UIReference_ID)
            for JobItem in SubJobsList:
                if JobItem['jobid']!=JobID:
                    self.TorqueObj.TerminateJob(JobItem['pbsreferenceid'].split('.')[0])
                    logging.info("Job (" + str(JobItem['jobid']) +" ["+str(JobItem['subjobindex'])+"]) ... Force Delete")
                    self.dbaseobj.SetJobFinishedWithError(JobItem['jobid'], 'Force Deleted', JobDetails['end'])
        
        if TerminateAllOnError==True and JobType==EnumerationLookup.JobType.Complex:
           data['error_message']=data['error_message']+" Please note that all other subjobs will be deleted also" 
        
        
        self.UpdateTAOUI(UIReference_ID,JobType, data)
        self.dbaseobj.AddNewEvent(JobID, EnumerationLookup.EventType.Normal, 'Updating Job (UI ID:' + str(UIReference_ID) + ', Status:' + data['status'] + ')')
        
        Message = "Job (" + str(UIReference_ID) +" ["+str(SubJobIndex)+"])  Finished With Error. The Error Message is:" + data['error_message']
        emailreport.SendEmailToAdmin(self.Options, "Job Finished With Error", Message)

    ## Update the Back-end DB and the UI that the job is running. There is no need for special handling in case of complex Jobs
    ## In this case one job is enough to turn the sate to running
    def UpdateJob_Running(self, PID,SubJobIndex, JobType, OldStatus, UIReference_ID, JobID):
        
        JobStartTime = datetime.datetime.now().timetuple()
        data = {}  
        try:
            JobStartTime = self.GetProcessStartTime(PID)
        except Exception as Exp:
            logging.error('Error In Getting Start time for Job ' + str(PID))
            logging.error(Exp)
        if EnumerationLookup.JobState.Running!=OldStatus:
            self.dbaseobj.SetJobRunning(JobID, "Job Running- PBSID" + PID, JobStartTime)
        data['status'] = 'IN_PROGRESS'        
        self.UpdateTAOUI(UIReference_ID,JobType, data)
        self.dbaseobj.AddNewEvent(JobID, EnumerationLookup.EventType.Normal, 'Updating Job (UI ID:' + str(UIReference_ID) + ', Status:' + data['status'] + ')')
        logging.info("Job (" + str(UIReference_ID) +" ["+str(SubJobIndex)+"]) ... Running")

    ## Update the Back-end DB and the UI that the job is Queued. In case of Multiple Lightcones, the UI will be updated with the last job
    def UpdateJob_Queued(self, PID,SubJobIndex, JobType, OldStatus, UIReference_ID, JobID):
        data = {} 
        if EnumerationLookup.JobState.Queued!=OldStatus: 
            self.dbaseobj.SetJobQueued(JobID, "Job Queued- PBSID" + PID)
        data['status'] = 'QUEUED' 
        
        
        self.UpdateTAOUI(UIReference_ID, JobType, data)
        
        self.dbaseobj.AddNewEvent(JobID, EnumerationLookup.EventType.Normal, 'Updating Job (UI ID:' + str(UIReference_ID) + ', Status:' + data['status'] + ')')
        logging.info("Job (" + str(UIReference_ID) +" ["+str(SubJobIndex)+"]) ... Queued")
        
    
                
        
            
            
            
            
        
        
        
        
        
                
            
        
        

    

