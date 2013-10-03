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
import stat,sys
import ParseProfileData
import traceback
import JobRestart

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
        
        self.JobRestartObj=JobRestart.JobRestart(Options,dbaseobj,TorqueObj)
      
        
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
        
    def JobWithSameIDRunning(self,UIJobReference):    
        ListOfJobs=self.dbaseobj.GetRunningJobsWithTheSameUIReferenceID(UIJobReference)
        if len(ListOfJobs)==0:
            logging.info("## No Jobs with the same ID exists ##")
            return False
        else:
            logging.info("## **** Jobs with the same ID exists **** ##")
            logging.info("## **** Checking if these jobs are really running **** ##")
        logging.info("List of Jobs with the same ID:"+str(ListOfJobs))
        ## Query PBS for current Jobs that belong to TAO
        CurrentJobs=self.TorqueObj.QueryPBSJob()          
        
        logging.info("Current PBS Jobs:"+str(CurrentJobs))
        JobRunning=False
        for JobRecord in ListOfJobs:
            if JobRecord['pbsreferenceid'].split('.')[0] in CurrentJobs:
                JobRunning=True
        
        
        if JobRunning==True:
            data = {}  
            logging.info("Fatal Error .. Job of the same UIreferenceID is running or in a new state")           
            logging.info("###### Fatal Error : Job With the same UI ReferneceID is running ! I can't accept this new Job request ######")
            logging.info("###### I will have to set this job to Error State ######")
            data['status'] = 'ERROR'
            data['error_message'] = 'Error: Job With the same UI Reference ID is already running'
            self.UpdateTAOUI(UIJobReference,EnumerationLookup.JobType.Simple, data)
            Message = "Job (" + str(UIJobReference) +" Finished With Error. The Error Message is:" + data['error_message']
            emailreport.SendEmailToAdmin(self.Options, "Job ReferenceID Replicated!", Message)       
            return True
        else:
            logging.info("There is no jobs actually running on PBS")
            return False
        
    def ProcessNewJob(self,UIJobReference,JobParams,JobDatabase,JobUserName):       
        
        IsSequential=False
        try:
            ## Handling for a very special case. Job Status turned to submitted while it is already running or queued! 
            ## In this case the job Will be rejected and an email to the Admin will be sent to indicate this
            if(self.JobWithSameIDRunning(UIJobReference)==True):                         
                return False
            ## If a Job with the Same UI_ID exists ...ensure that it is out of the watch List (By Error State)
            self.dbaseobj.RemoveOldJobFromWatchList(UIJobReference)
            self.dbaseobj.RemoveAllJobsWithUIReferenceID(UIJobReference)
        
            ## 1- Prepare the Job Directory
            [SubJobsCount,IsSequential]=self.PrepareJobFolder(JobParams,JobUserName,UIJobReference,JobDatabase)
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
        
        
        
        JobInformation = {'UIJobReference': UIJobReference,'CurrentJobType': CurrentJobType,
                              'JobParams': JobParams,'JobUserName': JobUserName,'JobDatabase': JobDatabase,
                              'SubJobIndex':0,'Issequential':str(IsSequential).lower()}                     
              
        ## Submit the Job to PBS and get back its ID
        for i in range(0,SubJobsCount):
            ## Add new Job and return its ID
            JobInformation['SubJobIndex']=i
            JobID=self.dbaseobj.AddNewJob(JobInformation)
                   
            ############################################################
            ### Submit the Job to the PBS Queue
            
            
            PBSJobID=self.TorqueObj.Submit(UIJobReference,JobUserName,JobID,i,IsSequential)
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
        
        #self.CopyDirectoryContents(AudDataPath+"/stellar_populations",logpath)     
        self.CopyDirectoryContents(AudDataPath+"/bandpass_filters",logpath,True)
        self.CopyDirectoryContents(AudDataPath,logpath,False)
            
        return [SubJobsCount,ParseXMLParametersObj.IsSquentialJob()]   
        
    
    def CopyDirectoryContents(self,SrcPath,DstPath,CopySubDirs):
        src_files = os.listdir(SrcPath)
        logging.info("Copying File - Source Path:"+SrcPath)
        logging.info("Copying File - Dest Path:"+DstPath)
        for file_name in src_files:
            full_file_name = os.path.join(SrcPath, file_name)
            logging.info(full_file_name)
            if (os.path.isfile(full_file_name)):
                logging.info(full_file_name+"->"+DstPath)
                shutil.copy(full_file_name, DstPath)
            elif CopySubDirs==True:
                DstSubFolder=os.path.join(DstPath,file_name)
                logging.info("Content is a directory - Dest Path:"+DstSubFolder)
                os.makedirs(DstSubFolder)
                self.CopyDirectoryContents(full_file_name, DstSubFolder)    
        
                
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
    
    
    
    def ChangePBSFilesmod(self,CurrentJobRecord):

        UserName=CurrentJobRecord['username']
        JobID=CurrentJobRecord['uireferenceid']
        LocalJobID=CurrentJobRecord['jobid']
        
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
        
    
    
    
    def RestartJob(self,RestartJobRecrod):
        logging.info("####### Restarting Job #####")
        logging.info(RestartJobRecrod)
        
        JobID=RestartJobRecrod['jobid']
        JobUserName=RestartJobRecrod['jobusername']
        UIJobReference=RestartJobRecrod['uireferenceid']
        IsSequential=RestartJobRecrod['issequential']
        SubJobID=RestartJobRecrod['subjobindex']
        
        
        PBSJobID=self.TorqueObj.Submit(UIJobReference,JobUserName,JobID,SubJobID,IsSequential)
        ## Store the Job PBS ID  
        if self.dbaseobj.UpdateJob_PBSID(JobID,PBSJobID)!=True:
            raise  Exception('Error in Process New Job','Update PBSID failed')
                
        self.dbaseobj.SetJobNew(JobID,'Job Restart')          
        ## Update the Job Status to Queued            
        self.UpdateTAOUI(UIJobReference, EnumerationLookup.JobType.Complex, data={'status': 'QUEUED'})
        
    
    
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
        
        
        if len(CurrentJobs_PBSID)>0:          
        
            now=datetime.datetime.now()
            logging.info(str(len(CurrentJobs_PBSID))+" Jobs Found in the current watch list")
            self.dbaseobj.AddNewEvent(0,EnumerationLookup.EventType.Normal,'Checking for Current Jobs. Jobs Count='+str(len(CurrentJobs_PBSID)))
            
                
            
            
            ## Query PBS for current Jobs that belong to TAO
            CurrentJobs=self.TorqueObj.QueryPBSJob()    
            
            
            logging.info("PBS Jobs:"+str(CurrentJobs))
            
            logging.info("Database Jobs:"+str(CurrentJobs_PBSID))
            
            JobsStatus=[]
            for CurrentJobRecord in CurrentJobs_PBSID:
                                    
                
               
                CurrentJobRecord['pbsreferenceid']=CurrentJobRecord['pbsreferenceid'].split('.')[0]
                pbsreferenceid=CurrentJobRecord['pbsreferenceid']
                jobstatus=CurrentJobRecord['jobstatus']          
                uireferenceid=CurrentJobRecord['uireferenceid']
                
                
                
                logging.info("Checking Job Status : JobID="+pbsreferenceid+"\tInPBSList="+str(pbsreferenceid in CurrentJobs))
                if pbsreferenceid in CurrentJobs:
                    logging.info("Checking Job Status : JobID="+pbsreferenceid+"\tStatus="+str(CurrentJobs[pbsreferenceid]))
                
                ## Parse the Job Log File and Extract Current Job Status            
                JobDetails=self.LogReaderObj.ParseFile(CurrentJobRecord)
                 
                
                
                
                ## 1- Change In Job Status to Running 
                if  pbsreferenceid in CurrentJobs and CurrentJobs[pbsreferenceid]=='R': 
                    if jobstatus!=EnumerationLookup.JobState.Running:
                        self.UpdateJob_Running(CurrentJobRecord)
                    elif JobDetails!=None:
                        logging.info ("Job ("+str(uireferenceid)+" ["+str(CurrentJobRecord['subjobindex'])+"]) .. : Progress="+JobDetails['progress'])
                    else:
                        logging.info ("Job ("+str(uireferenceid)+") .. : Log File Does not exist") 
                   
                ## 2-  Change In Job Status to Queued
                elif  pbsreferenceid in CurrentJobs and CurrentJobs[pbsreferenceid]=='Q': 
                    if jobstatus!=EnumerationLookup.JobState.Queued:
                        self.UpdateJob_Queued(CurrentJobRecord)
                    else:
                        logging.info("Jobs Still Queued ...")
                ## 3- Job Status Unknown ... It is still in the queue but it is not Q or R !     
                elif  pbsreferenceid in CurrentJobs and CurrentJobs[pbsreferenceid]!='R' and CurrentJobs[pbsreferenceid]!='Q' : 
                    logging.info('Job Status UNKnow '+str(uireferenceid)+' :'+CurrentJobs[pbsreferenceid])              
                
                ## 4- Job Cannot Be Found in the queue ... In this case the Log File Status determine how its termination status    
                elif (pbsreferenceid not in CurrentJobs):
                    
                    ###### If The log file does not exist, Please put a dummy JobDetails
                    if JobDetails==None:
                        JobDetails={'start':-1,'progress':'0%','end':0,'error':'','endstate':''}
                    
                        
                    if  JobDetails['endstate']=='successful':
                        ##### Job Terminated Successfully 
                        self.UpdateJob_EndSuccessfully(CurrentJobRecord, JobDetails) 
                        self.ChangePBSFilesmod(CurrentJobRecord)                   
                    else:
                        ##### Job Terminated with error or was killed by the Job Queue                    
                        self.UpdateJob_EndWithError(CurrentJobRecord, JobDetails)
                        self.ChangePBSFilesmod(CurrentJobRecord)  
                        break    
                ###############################################################################################################
                ## 5- The Job didn't change its status... Show its progess information if Exists!        
                else:
                    logging.info("Job Status Checking is not known!!")

        self.JobRestartObj.CheckPendingJobs(self.RestartJob)

    def UpdateJob_EndSuccessfully(self, CurrentJobRecord, JobDetails):
        
        JobID=CurrentJobRecord['jobid']
        SubJobIndex=CurrentJobRecord['subjobindex']
        JobType=CurrentJobRecord['jobtype']
        UIReference_ID=CurrentJobRecord['uireferenceid']
        UserName=CurrentJobRecord['username']
        
        
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

    def UpdateJob_EndWithError(self,CurrentJobRecord , JobDetails):
        
        JobAddedForRestart=False
        
        JobID=CurrentJobRecord['jobid']
        SubJobIndex=CurrentJobRecord['subjobindex']
        JobType=CurrentJobRecord['jobtype']
        UIReference_ID=CurrentJobRecord['uireferenceid']
        UserName=CurrentJobRecord['username']
        
        data = {}  
        
        TerminateAllOnError=(self.Options['WorkFlowSettings:TerminateSubJobsOnError']=='On')
        
        
        logging.info("Job (" + str(UIReference_ID) +" ["+str(SubJobIndex)+"]) ... Finished With Error")
        stderr = self.GetJobstderrcontents(UserName, UIReference_ID, JobID)
        data['status'] = 'ERROR'
        if JobDetails['error'] == '':
            JobDetails['error'] = stderr
        
        if (self.JobRestartObj.AddNewJob(CurrentJobRecord,stderr)==True):
            JobAddedForRestart=True
        
        
        self.dbaseobj.SetJobFinishedWithError(JobID, JobDetails['error'], JobDetails['end'])
        data['error_message'] = 'Error:' + JobDetails['error']        
        
        if TerminateAllOnError==True:
            SubJobsList=self.dbaseobj.GetJobsStatusbyUIReference(UIReference_ID)
            for JobItem in SubJobsList:
                if JobItem['jobid']!=JobID:
                    self.TorqueObj.TerminateJob(JobItem['pbsreferenceid'].split('.')[0])
                    logging.info("Job (" + str(JobItem['jobid']) +" ["+str(JobItem['subjobindex'])+"]) ... Force Delete")
                    self.dbaseobj.SetJobFinishedWithError(JobItem['jobid'], 'Force Deleted', JobDetails['end'])
                    self.JobRestartObj.AddNewJob(JobItem,stderr)
                    
                        
        
        if TerminateAllOnError==True and JobType==EnumerationLookup.JobType.Complex:
           data['error_message']=data['error_message']+" Please note that all other subjobs will be deleted also" 
           if JobAddedForRestart==True:
               data['error_message']=data['error_message']+"  \n\r Please note that this job will be restarted Automatically after 30 Minutes"
        
        
        self.UpdateTAOUI(UIReference_ID,JobType, data)
        self.dbaseobj.AddNewEvent(JobID, EnumerationLookup.EventType.Normal, 'Updating Job (UI ID:' + str(UIReference_ID) + ', Status:' + data['status'] + ')')
        
        Message = "Job (" + str(UIReference_ID) +" ["+str(SubJobIndex)+"])  Finished With Error. The Error Message is:" + data['error_message']
        
        emailreport.SendEmailToAdmin(self.Options, "Job Finished With Error", Message)

    ## Update the Back-end DB and the UI that the job is running. There is no need for special handling in case of complex Jobs
    ## In this case one job is enough to turn the sate to running
    def UpdateJob_Running(self, CurrentJobRecord):
        
        PID=CurrentJobRecord['pbsreferenceid']
        SubJobIndex=CurrentJobRecord['subjobindex']
        JobType=CurrentJobRecord['jobtype']
        OldStatus=CurrentJobRecord['jobstatus']
        UIReference_ID=CurrentJobRecord['uireferenceid']
        JobID=CurrentJobRecord['jobid']
        
        
        
        
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
    def UpdateJob_Queued(self,CurrentJobRecord):
        
        
        PID=CurrentJobRecord['pbsreferenceid']
        SubJobIndex=CurrentJobRecord['subjobindex']
        JobType=CurrentJobRecord['jobtype']
        OldStatus=CurrentJobRecord['jobstatus']
        UIReference_ID=CurrentJobRecord['uireferenceid']
        JobID=CurrentJobRecord['jobid']
        
        
        
        data = {} 
        if EnumerationLookup.JobState.Queued!=OldStatus: 
            self.dbaseobj.SetJobQueued(JobID, "Job Queued- PBSID" + PID)
        data['status'] = 'QUEUED' 
        
        
        self.UpdateTAOUI(UIReference_ID, JobType, data)
        
        self.dbaseobj.AddNewEvent(JobID, EnumerationLookup.EventType.Normal, 'Updating Job (UI ID:' + str(UIReference_ID) + ', Status:' + data['status'] + ')')
        logging.info("Job (" + str(UIReference_ID) +" ["+str(SubJobIndex)+"]) ... Queued")
        
    
                
        
            
            
            
            
        
        
        
        
        
                
            
        
        

    

