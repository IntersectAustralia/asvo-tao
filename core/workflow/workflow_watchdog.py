#!/usr/bin/env python

import logging, logging.handlers
import sys
import time
from datetime import datetime
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from daemon import Daemon
import signal
import shlex, subprocess
## ----------------------------------------------------------------------------------------------

class WatchDogDaemon(Daemon):
   
    def PrepareLogFile(self):
        LOG_FILENAME = 'log/watchdog_logfile.log'
        self.WatchDogLoger = logging.getLogger() 
        self.WatchDogLoger.setLevel(logging.DEBUG)      
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.WatchDogLoger.addHandler(handler)
        
    def WatchDog(self):   
        self.RestartCounts=0     
        self.PrepareLogFile()
        self.AppRunning=True
        # Load any existing database information.
        
        logging.info('-----------------------------------------------------------------')
        logging.info('WatchDog Starting')
        
        path = '/tmp/'
        filename = 'daemon-workflow.pid'
        
        logging.info("Process ID= "+path+filename)
        

        self.observer = Observer()
        self.event_handler = MyEventHandler(self.observer, filename,self)

        self.observer.schedule(self.event_handler, path, recursive=False)
        self.observer.start()        
        while (self.AppRunning==True):
            time.sleep(10)    
        sys.exit(0)
        logging.info("WatchDog Terminated!")        
    
    def RestartApp(self):
        logging.info('Restarting the Application')
        stdout = subprocess.check_output(shlex.split('python /lustre/projects/p014_swin/programs/Workflow/main.py start'))
        logging.info('Starting Process Output ="'+stdout+'"')
        logging.info('Application Restart Done')
        
    def Event_Restart(self):
        
        RestartInterval=0
                
        if self.RestartCounts>0:
            CurrentTime=datetime.now()
            RestartInterval=(CurrentTime-self.LastRestartTime).total_seconds()
            logging.info("Time from last restart="+str(RestartInterval)+" seconds");
        
        self.RestartCounts=self.RestartCounts+1
        logging.info('Restart Count='+str(self.RestartCounts)) 
        self.LastRestartTime = datetime.now()
        if(self.RestartCounts<5):
            self.RestartApp()
            if RestartInterval>120:
                self.RestartCounts=0
            return True
        else:
            logging.info("Sorry I have to quit me ! Multiple restart in two minutes")            
            return False
            

    def HandleExit(self,signum, frame):        
        logging.info('I received Exit Code')   
        logging.error('I will Terminate the Service!' )       
        self.observer.stop() 
        sys.exit(0)
        logging.error('Service Terminated!' )
        
    def run(self):
        self.WatchDog()


## -----------------------------------------------------------------------------------------------


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer, filename,Daemon):
        
        self.observer = observer
        self.filename = filename
        self.WatchDogDaemon=Daemon

   
    def on_deleted(self, event):
        logging.info( "Event: "+str( event))
        
        if not event.is_directory and event.src_path.endswith(self.filename):
            logging.info( "Restarting Workflow Application")
            Return=self.WatchDogDaemon.Event_Restart()
            if Return==False:
                self.observer.stop() 
                self.WatchDogDaemon.AppRunning=False           
                logging.info("WatchDog Terminated!") 



if __name__ == "__main__":
    daemonobj = WatchDogDaemon('/tmp/daemon-workflow-watchdog.pid','/dev/null','log/watchdogout.log','log/watchdogerr.log')
    signal.signal(signal.SIGTERM, daemonobj.HandleExit)
    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                print('Starting App')                
                daemonobj.start()                
            elif 'stop' == sys.argv[1]:                                                     
                daemonobj.stop()                                
            else:
                logging.error("Unknown command")
                sys.exit(2)
            sys.exit(0)
    else:
            print "usage: %s start|stop" % sys.argv[0]
            sys.exit(2)