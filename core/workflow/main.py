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
import SysCommands
import traceback

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
        self.SysCommandsObj=SysCommands.SysCommands(self.Options,self.dbaseObj,self.TorqueObj)
     
        
        
        
        
        self.dbaseObj.AddNewEvent(0,0,"WorkFlow Started")
        
        logging.info('-----------------------------------------------------------------')
        logging.info('Workflow Starting')
        
        
        
        ErrorCounter=0
         
        while True:
            
            try:            
                self.SysCommandsObj.CheckForNewCommands()
                
                if self.SysCommandsObj.KeepWorkFlowActive==True:
                    logging.info("Workflow is Active")
                    self.workflowObj.GetNewJobsFromMasterDB()            
                    self.workflowObj.ProcessJobs()
                else:
                    logging.info("Workflow disabled")
                    
                logging.info("Sleeping for "+str(self.SleepTime)+" Seconds")
                logging.info('-----------------------------------------------------------------')
                
                ErrorCounter=0
            except Exception as Exp:
                if ErrorCounter<=5:
                    emailreport.SendEmailToAdmin(self.Options,"Error In WorkFlow",str(Exp.args))
                logging.error("Error In Main")
                logging.error(type(Exp))
                logging.error(Exp.args)
                logging.error(Exp)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                logging.error(''.join('!! ' + line for line in lines))
                ErrorCounter=ErrorCounter+1
                # Restart All Objects
                self.dbaseObj=dbase.DBInterface(self.Options)
                self.TorqueObj=torque.TorqueInterface(self.Options,self.dbaseObj)
                self.workflowObj=workflow.WorkFlow(self.Options,self.dbaseObj,self.TorqueObj)
                self.SysCommandsObj=SysCommands.SysCommands(self.Options,self.dbaseObj,self.TorqueObj)
            finally:
                time.sleep(self.SleepTime+(ErrorCounter*10))
                        
            

    def HandleExit(self,signum, frame):        
        logging.info('I received Exit Code')   
        logging.error('I will Terminate the DB Connection and Exit!' )       
        self.dbaseObj.CloseConnections()  
        sys.exit(0)
        
    def run(self):
        self.Workflow()
        

# Entry point for the main workflow system.
if __name__ == '__main__':
    
    [Options]=settingReader.ParseParams("settings.xml")    
    ProcessIDFile=Options['WorkFlowSettings:ProcessID']
       
    daemonobj = WorkflowDaemon('/tmp/'+ProcessIDFile,'/dev/null','log/out.log','log/err.log')
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
    