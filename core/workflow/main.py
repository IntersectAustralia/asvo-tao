import  workflow
import os, shlex, subprocess, time, logging,sys
import requests
import torque
import dbase
import settingReader # Read the XML settings
import logging, logging.handlers
from daemon import Daemon
import signal
import emailreport


class WorkflowDaemon(Daemon):

    

    def BackupLogFile(self):
        if os.path.exists('log/logfile.log'):
           LogFile=open('log/logfile.log')
           Contents=LogFile.read()
           LogFile.close()
           LogFileBackup=open('log/logfile.log.bak','a')
           LogFileBackup.write(Contents)
           LogFileBackup.close()
           os.remove('log/logfile.log')
    def PrepareLogFile(self):
        LOG_FILENAME = 'log/logfile.log'
        self.TAOLoger = logging.getLogger() 
        self.TAOLoger.setLevel(logging.DEBUG)      
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.TAOLoger.addHandler(handler)
        
    def Workflow(self):
        #self.BackupLogFile()
        self.PrepareLogFile()
        #logging.basicConfig(filename='log/logfile.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
        ## Read Running Setting from XML File
        [self.Options]=settingReader.ParseParams("settings.xml")
        
        ## Define Working Directory and the Sleep time between each Run
        WorkDirectory=self.Options['WorkFlowSettings:WorkingDir']
        self.SleepTime=int(self.Options['WorkFlowSettings:SleepTime'])
        
        
        # Change location to the working directory.
        os.chdir(WorkDirectory)
    
        
        # Load any existing database information.
        self.dbaseObj=dbase.DBInterface(self.Options)
        self.TorqueObj=torque.TorqueInterface(self.Options,self.dbaseObj)
        self.workflowObj=workflow.WorkFlow(self.Options,self.dbaseObj,self.TorqueObj)
        
        
        
        
        
        self.dbaseObj.AddNewEvent(0,0,"WorkFlow Started")
        
        logging.info('-----------------------------------------------------------------')
        logging.info('Workflow Starting')
        
        
        
        try:
         
            while True:
                self.workflowObj.GetNewJobsFromMasterDB()
                
                self.workflowObj.ProcessJobs()
                logging.info("Sleeping for "+str(self.SleepTime)+" Seconds")
                logging.info('-----------------------------------------------------------------')
                time.sleep(self.SleepTime)
        except Exception as Exp: 
            emailreport.SendEmailToAdmin(self.Options,"Error In WorkFlow",str(Exp.args))
            logging.error("Error In Main")
            logging.error(type(Exp))
            logging.error(Exp.args)
            logging.error(Exp)        
        finally: 
            logging.error('Finally: I will Terminate the DB Connection and Exit!' )       
            self.dbaseObj.CloseConnections()
            

    def HandleExit(self,signum, frame):        
        logging.info('I received Exit Code')   
        logging.error('I will Terminate the DB Connection and Exit!' )       
        self.dbaseObj.CloseConnections()  
        sys.exit(0)
        
    def run(self):
        self.Workflow()
        

# Entry point for the main workflow system.
if __name__ == '__main__':
    daemonobj = WorkflowDaemon('/tmp/daemon-workflow.pid','/dev/null','log/out.log','log/err.log')
    signal.signal(signal.SIGTERM, daemonobj.HandleExit)
    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                print('Starting App')                
                daemonobj.start()                
            elif 'stop' == sys.argv[1]: 
                #signal.signal(signal.SIGTERM, daemonobj.HandleExit)                                     
                daemonobj.stop()                                
            else:
                logging.error("Unknown command")
                sys.exit(2)
            sys.exit(0)
    else:
            print "usage: %s start|stop" % sys.argv[0]
            sys.exit(2)
    