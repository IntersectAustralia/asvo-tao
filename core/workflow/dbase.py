import pickle, os, logging,string
import pg
import EnumerationLookup
import locale
import time
from datetime import date
import logging

class DBInterface(object):
    
    
    def __init__(self,Options):
        ### Init DBConnection Object
        
        self.Options=Options     
        
        self.InitDBConnection(self.Options)
        self.IsOpen=False
        self.QueriesCount=0
        
    def InitDBConnection(self,Options):
        
        ####### PostgreSQL Backend Master DB ################# 
        self.serverip=Options['PGDB:serverip']
        self.username=Options['PGDB:user']
        self.password=Options['PGDB:password']
        self.port=int(Options['PGDB:port'])
        self.DBName=Options['PGDB:NewDBName']    
               
        
        self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname=self.DBName)
        logging.info('Connection to DB is open...')    
        self.IsOpen=True
        
    def CloseConnections(self):  
        if self.IsOpen==True:      
            self.CurrentConnection.close()        
            logging.info('Connection to DB is Closed...')
            self.IsOpen=False        
           
    def RestartConnection(self):
        if self.QueriesCount%20==0 and self.QueriesCount>0:
            self.CloseConnections()
            self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname=self.DBName)
            logging.info('Connection to DB - Restart...')    
            self.IsOpen=True
        
        self.QueriesCount=self.QueriesCount+1                
    
    def ExecuteNoQuerySQLStatment(self,SQLStatment):
        try:
            self.RestartConnection()          
            self.CurrentConnection.query(SQLStatment)  
            return True            
        except Exception as Exp:
            logging.error(">>>>>Error While Executing Non-Query SQL Statement")
            logging.error(type(Exp))
            logging.error(Exp.args)
            logging.error(Exp)            
            logging.error("Current SQL Statement =\n"+SQLStatment)
            return False
            
    def ExecuteQuerySQLStatment(self,SQLStatment):
        try: 
            self.RestartConnection()                    
            resultsList=self.CurrentConnection.query(SQLStatment).getresult()           
            return resultsList  
        except Exception as Exp:
            logging.error(">>>>>Error While Executing Query SQL Statement")
            logging.error(type(Exp))
            logging.error(Exp.args)
            logging.error(Exp)            
            logging.error("Current SQL Statement =\n"+SQLStatment)
            
    def ExecuteQuerySQLStatmentAsDict(self,SQLStatment):
        try:
            self.RestartConnection()
                    
            resultsList=self.CurrentConnection.query(SQLStatment).dictresult()           
            return resultsList  
        except Exception as Exp:
            logging.error(">>>>>Error While Executing Query SQL Statement")
            logging.error(type(Exp))
            logging.error(Exp.args)
            logging.error(Exp)            
            logging.error("Current SQL Statement =\n"+SQLStatment)
            
    ########################################################################################################################################   
    ########################################################################################################################################
    #######################################No Query Functions###############################################################################
    
    def AddNewEvent(self,AssociatedJobID,EventType,EventDesc):
        if self.Options['WorkFlowSettings:Events']=='On':
            INSERTEvent="INSERT INTO EVENTS (EventType,ASSOCIATEDJOBID,EVENTDESC) VALUES "
            INSERTEvent=INSERTEvent+"("+str(EventType)+","+str(AssociatedJobID)+",'"+EventDesc+"');"
            return self.ExecuteNoQuerySQLStatment(INSERTEvent)
    
    def RemoveOldJobFromWatchList(self,UIReferenceID):
        UpdateSt='Update Jobs set JobStatus='+str(EnumerationLookup.JobState.Error)+' Where uireferenceid='+str(UIReferenceID)+' and JobStatus<'+str(EnumerationLookup.JobState.Completed)+';'
        UpdateSt=UpdateSt+' Update Jobs set latestjobversion=False where uireferenceid='+str(UIReferenceID)+';'
        return self.ExecuteNoQuerySQLStatment(UpdateSt)
    
    
    def SetJobComplete(self,JobID,Comment,ExecTime):
        logging.info('Job ('+str(JobID)+') Completed .... '+Comment)
        Updatest="UPDATE Jobs set JobStatus="+str(EnumerationLookup.JobState.Completed)+",completedate=insertdate+INTERVAL '"+str(ExecTime)+" seconds' ,jobstatuscomment='"+Comment+"' where JobID="+str(JobID)+";"
        Updatest=Updatest+"INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES("+str(JobID)+","+str(EnumerationLookup.JobState.Completed)+",'JobCompleted');"
        return self.ExecuteNoQuerySQLStatment(Updatest)
    
    def SetJobFinishedWithError(self,JobID,Comment,ExecTime):
        Comment=pg.escape_string(Comment)
        if len(Comment)>500:
            Comment=Comment[:500]
        logging.info('Job ('+str(JobID)+') Finished With Error .... '+Comment)
        Updatest="UPDATE Jobs set JobStatus="+str(EnumerationLookup.JobState.Error)+",completedate=insertdate+INTERVAL '"+str(ExecTime)+" seconds',jobstatuscomment='"+Comment+"' where JobID="+str(JobID)+";"
        Updatest=Updatest+"INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES("+str(JobID)+","+str(EnumerationLookup.JobState.Error)+",'Error');"
        return self.ExecuteNoQuerySQLStatment(Updatest)
    
    
    def SetJobRunning(self,JobID,Comment,JobStartTime):
            Updatest="UPDATE Jobs set JobStatus="+str(EnumerationLookup.JobState.Running)+",jobstatuscomment='"+Comment+"', startdate='"+time.strftime('%d/%m/'+str(date.today().year)+' %H:%M:%S',JobStartTime)+"' where JobID="+str(JobID)+";"
            Updatest=Updatest+"INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES("+str(JobID)+","+str(EnumerationLookup.JobState.Running)+",'JobRunning');"
            return self.ExecuteNoQuerySQLStatment(Updatest)
                    
    def SetJobQueued(self,JobID,Comment):       
            Updatest="UPDATE Jobs set JobStatus="+str(EnumerationLookup.JobState.Queued)+",jobstatuscomment='"+Comment+"' where JobID="+str(JobID)+";"
            Updatest=Updatest+"INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES("+str(JobID)+","+str(EnumerationLookup.JobState.Queued)+",'JobWaiting');"
            return self.ExecuteNoQuerySQLStatment(Updatest)
    def SetJobNew(self,JobID,Comment):       
            Updatest="UPDATE Jobs set JobStatus="+str(EnumerationLookup.JobState.NewJob)+",jobstatuscomment='"+Comment+"' where JobID="+str(JobID)+";"
            Updatest=Updatest+"INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES("+str(JobID)+","+str(EnumerationLookup.JobState.NewJob)+",'Job Restarted');"
            return self.ExecuteNoQuerySQLStatment(Updatest)
            
    def SetJobPaused(self,JobID,UICommandID): 
           Updatest="UPDATE Jobs set JobStatus="+str(EnumerationLookup.JobState.Paused)+",jobstatuscomment='PAUSED BY WORKFLOW COMMAND ID="+str(UICommandID)+"' where JobID="+str(JobID)+";"
           logging.info(Updatest)
           return self.ExecuteNoQuerySQLStatment(Updatest)     
    
    def AddNewJob(self,JobInformation):       
            
        ## Encode the XML Params and remove un-replaceable unicode chars    
        XMLParamsASCII=JobInformation['JobParams'].encode('ascii','ignore')
        XMLParamsASCII=XMLParamsASCII.replace("\'","\"")
        
               
        INSERTJobSt="INSERT INTO JOBS(UIReferenceID,JobType,UserName,XMLParams,Database,subjobindex,issequential) VALUES ("

        INSERTJobSt=INSERTJobSt+str(JobInformation['UIJobReference'])+","+str(JobInformation['CurrentJobType'])+",'"
        INSERTJobSt=INSERTJobSt+JobInformation['JobUserName']+"','"+XMLParamsASCII+"','"+JobInformation['JobDatabase']+"',"+str(JobInformation['SubJobIndex'])+","+JobInformation['Issequential']+");"           
        INSERTJobSt=INSERTJobSt+"SELECT currval('nextjobid');"
            
        ## Get Latest JobID
        JobID=self.ExecuteQuerySQLStatment(INSERTJobSt)[0][0]        
        self.AddNewEvent(JobID, 0, "Job Added")
        self.AddNewJobStatus(JobID,0, "JobAdded")
        
        return JobID


    def UpdateJob_PBSID(self,JobID,PBSID):
        UpdateStat=" update jobs set pbsreferenceid='"+PBSID+"' where jobid="+str(JobID)+";"
        return self.ExecuteNoQuerySQLStatment(UpdateStat)
    
    
        
    def AddNewJobStatus(self,JobID,NewStatus,Comment):
        INSERTJobSt="INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES ("
        INSERTJobSt=INSERTJobSt+str(JobID)+","+str(NewStatus)+",'"+Comment+"');"
        
        return self.ExecuteNoQuerySQLStatment(INSERTJobSt)
    
    ########################################################################################################################################   
    ########################################################################################################################################
    #######################################Query Functions#################################################################################    
        
    def GetCurrentActiveJobs(self):
        SELECTActive="SELECT * From Jobs where JobStatus<"+str(EnumerationLookup.JobState.Completed+" and latestjobversion=True ;")
        return self.ExecuteQuerySQLStatment(SELECTActive)    
    
    def GetCurrentUserActiveJobs(self,UserName):
        SELECTActive="SELECT * From Jobs where JobStatus<"+str(EnumerationLookup.JobState.Completed)+" and latestjobversion=True and username='"+UserName+"';"
        return self.ExecuteQuerySQLStatment(SELECTActive)    
    
    def GetRunningJobsWithTheSameUIReferenceID(self,UIReferenceID):
        SelectSt='SELECT jobid,pbsreferenceid,JobStatus,uireferenceid,username from jobs Where uireferenceid='+str(UIReferenceID)+' and JobStatus<'+str(EnumerationLookup.JobState.Completed)+';'        
        return self.ExecuteQuerySQLStatmentAsDict(SelectSt)
        
    def GetCurrentActiveJobs_pbsID(self):
        SELECTActive="SELECT jobid,pbsreferenceid,JobStatus,uireferenceid,username,subjobindex,jobtype,issequential From Jobs where latestjobversion=True and JobStatus<"+str(EnumerationLookup.JobState.Completed)+" and pbsreferenceid is not null"
        return self.ExecuteQuerySQLStatmentAsDict(SELECTActive)
        
    def GetJob(self,JobID):
        SELECTJob="SELECT * From Jobs where JobID="+str(JobID)+";"
        return self.ExecuteQuerySQLStatment(SELECTJob)
    
    def GetJobbyUIReference(self,UIReferenceID):
        SELECTJob="SELECT * From Jobs where UIReferenceID="+str(UIReferenceID)+" and latestjobversion=True ;"
        return self.ExecuteQuerySQLStatmentAsDict(SELECTJob)
    
    def GetJobsStatusbyUIReference(self,UIReferenceID):
        
        SELECTJob="SELECT jobid,jobstatus,subjobindex,pbsreferenceid,uireferenceid,username,jobtype,issequential From Jobs where UIReferenceID="+str(UIReferenceID)+" and latestjobversion=True;"
        return self.ExecuteQuerySQLStatmentAsDict(SELECTJob)
    
   
    #########################################################################################################################
    ########## Commands DB Access ###############################################

    def AddNewCommand(self,UICommandID,commandtext,UIJobID,AdditionalParams):
        
          
        INSERTJobSt="INSERT INTO COMMANDS(UICommandID,commandtext,UIJobID,AdditionalParams) VALUES ("
        INSERTJobSt=INSERTJobSt+str(UICommandID)+",'"+commandtext+"',"+str(UIJobID)+",'"+AdditionalParams+"');"
        INSERTJobSt=INSERTJobSt+"SELECT currval('NextCommandID');"
            
        ## Get Latest JobID
        CommandID=self.ExecuteQuerySQLStatment(INSERTJobSt)[0][0]        
        self.AddNewEvent(CommandID, 0, "Command Added")
        
        
        return CommandID

    def UpdateCommandStatus(self,CommandID,NewStatus):
        
        Updatest="UPDATE Commands set ExecStatus="+str(NewStatus)+",COMPELETEDATE=CURRENT_TIMESTAMP where CommandID="+str(CommandID)+";"
            
        return self.ExecuteNoQuerySQLStatment(Updatest)

    #########################################################################################################################
    ########## Job Restart  #######################################################
    def SetJobAsRestarted(self,RestartJobID):
        Updatest="update jobrestartlist set hasbeenrestarted=true where jobrestartid="+str(RestartJobID)+";"
        self.ExecuteNoQuerySQLStatment(Updatest)
    
    def RemoveAllJobsWithUIReferenceID(self,UIReferenceID):
        
        DeletedJobs="DELETE From jobrestartlist where UIReferenceID="+str(UIReferenceID)+";"
        return self.ExecuteNoQuerySQLStatment(DeletedJobs)    
    def GetPendingJobsToRestart(self,MinutesLimit):
        selectst="select * from jobrestartlist where inserttimestamp <= (now() - interval '"+str(MinutesLimit)+" minutes') and hasbeenrestarted=false;"
        return self.ExecuteQuerySQLStatmentAsDict(selectst)
        
    def AddJobToRestartList(self,JobRecord):
        JobID=JobRecord['jobid']
        SubJobIndex=JobRecord['subjobindex']
        issequential=JobRecord['issequential']
        UIReference_ID=JobRecord['uireferenceid']
        UserName=JobRecord['username']
        
        ## Check if this Job Already exists
        selectst="Select * from jobrestartlist where jobid="+str(JobID)+"  and hasbeenrestarted=false;"
        if (len(self.ExecuteQuerySQLStatmentAsDict(selectst))>0):
            logging.info(str(JobID)+": Excluded because and active job with the same ID is already there")
            return False
        ## Check How Many time it was restarted
        selectst="Select * from jobrestartlist where jobid="+str(JobID)+";"
        MaximumRestartTime=int(self.Options['WorkFlowSettings:MaximumRestartTime'])
        if (len(self.ExecuteQuerySQLStatmentAsDict(selectst))>=MaximumRestartTime):
            logging.info(str(JobID)+": Excluded because number of restart times exceeded")
            return False
        
        
        
        
        InsertSt="insert into jobrestartlist(jobid,uireferenceid,jobusername,subjobindex,issequential) values"
        InsertSt=InsertSt+"("+str(JobID)+","+str(UIReference_ID)+",'"+UserName+"',"+ str(SubJobIndex)+","+str(issequential=='t').lower()+" );"
        self.ExecuteNoQuerySQLStatment(InsertSt)
        
        return True
        
        
        
        
        
        
    
