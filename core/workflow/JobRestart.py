
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


class JobRestart(object):
    
    def __init__(self,Options,dbaseobj,TorqueObj):
        
        logging.info('JobRestart Class Init')
        self.Options=Options
        self.dbaseobj=dbaseobj
        self.TorqueObj=TorqueObj        
        self.JobBaseDir=self.Options['Torque:outputbasedir']
        # Define the request API.
        
        self.CALLBackBase = Options['WorkFlowSettings:CallbackURL']
        self.api = {
               'get': self.CALLBackBase + 'job/?status=SUBMITTED',
               'update': self.CALLBackBase + 'job/%d/'}
        
    def CheckPendingJobs(self,JobRestartFunctionptr):
        logging.info("#####**** Begin Checking Pending Jobs")
        ListofJobs=self.dbaseobj.GetPendingJobsToRestart(30)
        for jobrecord in ListofJobs: 
            self.dbaseobj.SetJobAsRestarted(jobrecord['jobrestartid'])           
            JobRestartFunctionptr(jobrecord)
        logging.info("#####**** End Checking Pending Jobs")
        return True;
    
   
        
    def AddNewJob(self,JobRecord):
        
        
        #if (self.dbaseobj.AddJobToRestartList(JobRecord)==True):
        #    logging.info('Job ('+str(JobRecord['jobid'])+') Added to Restart List')
        #    return True
        #else:
        #    logging.info(JobRecord)            
        #    logging.info('Job ('+str(JobRecord['jobid'])+') Not added to Restart List')
        #    return False
        
        JobID=JobRecord['jobid']
        SubJobIndex=JobRecord['subjobindex']
        issequential=JobRecord['issequential']
        UIReference_ID=JobRecord['uireferenceid']
        UserName=JobRecord['username']
        
        
        return True;
        
        