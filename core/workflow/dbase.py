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
           
            
    
    def ExecuteNoQuerySQLStatment(self,SQLStatment):
        try:           
            #SQLStatment=string.lower(SQLStatment)  
            self.CurrentConnection.query(SQLStatment)              
        except Exception as Exp:
            logging.error(">>>>>Error While Executing Non-Query SQL Statement")
            logging.error(type(Exp))
            logging.error(Exp.args)
            logging.error(Exp)            
            logging.error("Current SQL Statement =\n"+SQLStatment)
            raw_input("Error: PLease press enter to continue.....")
    def ExecuteQuerySQLStatment(self,SQLStatment):
        try:            
            resultsList=self.CurrentConnection.query(SQLStatment).getresult()           
            return resultsList  
        except Exception as Exp:
            logging.error(">>>>>Error While Executing Query SQL Statement")
            logging.error(type(Exp))
            logging.error(Exp.args)
            logging.error(Exp)            
            logging.error("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
    def ExecuteQuerySQLStatmentAsDict(self,SQLStatment):
        try:            
            resultsList=self.CurrentConnection.query(SQLStatment).dictresult()           
            return resultsList  
        except Exception as Exp:
            logging.error(">>>>>Error While Executing Query SQL Statement")
            logging.error(type(Exp))
            logging.error(Exp.args)
            logging.error(Exp)            
            logging.error("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
    
    def AddNewEvent(self,AssociatedJobID,EventType,EventDesc):
        if self.Options['WorkFlowSettings:Events']=='On':
            INSERTEvent="INSERT INTO EVENTS (EventType,ASSOCIATEDJOBID,EVENTDESC) VALUES "
            INSERTEvent=INSERTEvent+"("+str(EventType)+","+str(AssociatedJobID)+",'"+EventDesc+"');"
            self.ExecuteNoQuerySQLStatment(INSERTEvent)
    def GetCurrentActiveJobs(self):
        SELECTActive="SELECT * From Jobs where JobStatus<"+str(EnumerationLookup.JobState.Completed)
        return self.ExecuteQuerySQLStatment(SELECTActive)
    
    def RemoveOldJobFromWatchList(self,UIReferenceID):
        UpdateSt='Update Jobs set JobStatus='+str(EnumerationLookup.JobState.Error)+' Where uireferenceid='+str(UIReferenceID)+' and JobStatus<'+str(EnumerationLookup.JobState.Completed)+';'
        UpdateSt=UpdateSt+' Update Jobs set latestjobversion=False where uireferenceid='+str(UIReferenceID)+';'
        self.ExecuteNoQuerySQLStatment(UpdateSt)
        
    def GetCurrentActiveJobs_pbsID(self):
        SELECTActive="SELECT jobid,pbsreferenceid,JobStatus,uireferenceid,username,subjobindex,jobtype From Jobs where JobStatus<"+str(EnumerationLookup.JobState.Completed)
        return self.ExecuteQuerySQLStatmentAsDict(SELECTActive)
    
    def SetJobComplete(self,JobID,Comment,ExecTime):
        logging.info('Job ('+str(JobID)+') Completed .... '+Comment)
        Updatest="UPDATE Jobs set JobStatus="+str(EnumerationLookup.JobState.Completed)+",completedate=insertdate+INTERVAL '"+str(ExecTime)+" seconds' ,jobstatuscomment='"+Comment+"' where JobID="+str(JobID)+";"
        Updatest=Updatest+"INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES("+str(JobID)+","+str(EnumerationLookup.JobState.Completed)+",'JobCompleted');"
        self.ExecuteNoQuerySQLStatment(Updatest)
    
    def SetJobFinishedWithError(self,JobID,Comment,ExecTime):
        Comment=pg.escape_string(Comment)
        if len(Comment)>500:
            Comment=Comment[:500]
        logging.info('Job ('+str(JobID)+') Finished With Error .... '+Comment)
        Updatest="UPDATE Jobs set JobStatus="+str(EnumerationLookup.JobState.Error)+",completedate=insertdate+INTERVAL '"+str(ExecTime)+" seconds',jobstatuscomment='"+Comment+"' where JobID="+str(JobID)+";"
        Updatest=Updatest+"INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES("+str(JobID)+","+str(EnumerationLookup.JobState.Error)+",'Error');"
        self.ExecuteNoQuerySQLStatment(Updatest)
            
    def SetJobRunning(self,JobID,OldStatus,Comment,JobStartTime):        
        if EnumerationLookup.JobState.Running!=OldStatus:
            Updatest="UPDATE Jobs set JobStatus="+str(EnumerationLookup.JobState.Running)+",jobstatuscomment='"+Comment+"', startdate='"+time.strftime('%d/%m/'+str(date.today().year)+' %H:%M:%S',JobStartTime)+"' where JobID="+str(JobID)+";"
            Updatest=Updatest+"INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES("+str(JobID)+","+str(EnumerationLookup.JobState.Running)+",'JobRunning');"
            self.ExecuteNoQuerySQLStatment(Updatest)
                    
    def SetJobQueued(self,JobID,OldStatus,Comment):        
        if EnumerationLookup.JobState.Queued!=OldStatus:
            Updatest="UPDATE Jobs set JobStatus="+str(EnumerationLookup.JobState.Queued)+",jobstatuscomment='"+Comment+"' where JobID="+str(JobID)+";"
            Updatest=Updatest+"INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES("+str(JobID)+","+str(EnumerationLookup.JobState.Queued)+",'JobWaiting');"
            self.ExecuteNoQuerySQLStatment(Updatest)
            
        
                
    def AddNewJob(self,UIReferenceID,JobType,XMLParams,UserName,Database,SubJobIndex):
        
        ## Encode the XML Params and remove un-replaceable unicode chars    
        XMLParamsASCII=XMLParams.encode('ascii','ignore')
        XMLParamsASCII=XMLParamsASCII.replace("\'","\"")       
        INSERTJobSt="INSERT INTO JOBS(UIReferenceID,JobType,UserName,XMLParams,Database,subjobindex) VALUES ("
        INSERTJobSt=INSERTJobSt+str(UIReferenceID)+","+str(JobType)+",'"+UserName+"','"+XMLParamsASCII+"','"+Database+"',"+str(SubJobIndex)+");"
        INSERTJobSt=INSERTJobSt+"SELECT currval('nextjobid');"
            
        ## Get Latest JobID
        JobID=self.ExecuteQuerySQLStatment(INSERTJobSt)[0][0]        
        self.AddNewEvent(JobID, 0, "Job Added")
        self.AddNewJobStatus(JobID,0, "JobAdded")
        
        return JobID
        

    def UpdateJob_PBSID(self,JobID,PBSID):
        UpdateStat=" update jobs set pbsreferenceid='"+PBSID+"' where jobid="+str(JobID)+";"
        self.ExecuteNoQuerySQLStatment(UpdateStat)
    
    
        
    def AddNewJobStatus(self,JobID,NewStatus,Comment):
        INSERTJobSt="INSERT INTO JobHistory(JobID,NewStatus,Comments) VALUES ("
        INSERTJobSt=INSERTJobSt+str(JobID)+","+str(NewStatus)+",'"+Comment+"');"
        
        self.ExecuteNoQuerySQLStatment(INSERTJobSt)
        
    def GetJob(self,JobID):
        SELECTJob="SELECT * From Jobs where JobID="+str(JobID)+";"
        return self.ExecuteQuerySQLStatment(SELECTJob)
    
    def GetJobbyUIReference(self,UIReferenceID):
        SELECTJob="SELECT * From Jobs where UIReferenceID="+str(UIReferenceID)+" and latestjobversion=True ;"
        return self.ExecuteQuerySQLStatment(SELECTJob)
    
    def GetJobsStatusbyUIReference(self,UIReferenceID):
        SELECTJob="SELECT jobid,jobstatus,subjobindex,pbsreferenceid From Jobs where UIReferenceID="+str(UIReferenceID)+" and latestjobversion=True;"
        return self.ExecuteQuerySQLStatmentAsDict(SELECTJob)
    
    

    

