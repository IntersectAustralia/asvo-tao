import pickle, os, logging,string
import pg
import EnumerationLookup


class DBInterface(object):
    
    def __init__(self,Options):
        '''
        Constructor
        '''
        self.Options=Options     
        
        self.InitDBConnection()
        
    def InitDBConnection(self):
        
        ####### PostgreSQL Simulation DB ################# 
        self.serverip=self.Options['PGDB:serverip']
        self.username=self.Options['PGDB:user']
        self.password=self.Options['PGDB:password']
        self.port=int(self.Options['PGDB:port'])
        self.DBName=self.Options['PGDB:NewDBName']
        
        if self.password==None:
            print('Password for user:'+username+' is not defined')
            self.password=getpass.getpass('Please enter password:')
        
        # Take care that the connection will be opened to standard DB 'master'
        # This is temp. until the actual database is created
        self.CurrentConnection=pg.connect(host=self.serverip,user=self.username,passwd=self.password,port=self.port,dbname=self.DBName)
        print('Connection to DB is open...')    

    def CloseConnections(self):        
        self.CurrentConnection.close()        
        print('Connection to DB is Closed...')        
           
            
    
    def ExecuteNoQuerySQLStatment(self,SQLStatment):
        try:           
            SQLStatment=string.lower(SQLStatment)  
            self.CurrentConnection.query(SQLStatment)              
        except Exception as Exp:
            print(">>>>>Error While Executing Non-Query SQL Statement")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
    def ExecuteQuerySQLStatment(self,SQLStatment):
        try:            
            resultsList=self.CurrentConnection.query(SQLStatment).getresult()           
            return resultsList  
        except Exception as Exp:
            print(">>>>>Error While Executing Query SQL Statement")
            print(type(Exp))
            print(Exp.args)
            print(Exp)            
            print("Current SQL Statement =\n"+SQLStatment)
            raw_input("PLease press enter to continue.....")
    
    def AddNewEvent(self,AssociatedJobID,EventType,EventDesc):
        INSERTEvent="INSERT INTO EVENTS (EventType,ASSOCIATEDJOBID,EVENTDESC) VALUES "
        INSERTEvent=INSERTEvent+"("+str(EventType)+","+str(AssociatedJobID)+",'"+EventDesc+"');"
        self.ExecuteNoQuerySQLStatment(INSERTEvent)
    def GetCurrentActiveJobs(self):
        SELECTActive="SELECT * From Jobs where JobStatus<"+str(EnumerationLookup.JobState.Completed)
        return self.ExecuteQuerySQLStatment(SELECTActive)

    def AddNewJob(self,UIReferenceID,JobType,XMLParams,UserName):
        
        if self.GetJobbyUIReference(UIReferenceID)!=None:
        
            INSERTJobSt="INSERT INTO JOBS(UIReferenceID,JobType,UserName,XMLParams) VALUES ("
            INSERTJobSt=INSERTJobSt+str(UIReferenceID)+","+str(JobType)+",'"+UserName+"','"+XMLParams+"');"
        
            self.ExecuteNoQuerySQLStatment(INSERTJobSt)
            
            JobID=self.ExecuteQuerySQLStatment("SELECT currval('nextjobid')")[0][0]
            self.AddNewEvent(JobID, 0, "Job Added")
            self.AddNewJobStatus(JobID,0, "JobAdded")
            
            return JobID
        else:
            print("Job Already exists")
            return -1

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
        SELECTJob="SELECT * From Jobs where UIReferenceID="+str(UIReferenceID)+";"
        return self.ExecuteQuerySQLStatment(SELECTJob)
    
    

    

