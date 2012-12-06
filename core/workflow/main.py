import  workflow
import os, shlex, subprocess, time, logging
import requests
import torque
import dbase
import settingReader # Read the XML settings




# Entry point for the main workflow system.
if __name__ == '__main__':

    [Options]=settingReader.ParseParams("settings.xml")
    
    WorkDirectory=Options['WorkFlowSettings:WorkingDir']
    SleepTime=int(Options['WorkFlowSettings:SleepTime'])
    
    
    # Change location to the working directory.
    os.chdir(WorkDirectory)

    
    # Load any existing database information.
    dbaseObj=dbase.DBInterface(Options)
    TorqueObj=torque.TorqueInterface(Options,dbaseObj)
    workflowObj=workflow.WorkFlow(Options,dbaseObj,TorqueObj)
    
    
    
    
    
    dbaseObj.AddNewEvent(0,0,"WorkFlow Started")
    
    
    
    
     
    while 1:
        workflowObj.GetNewJobsFromMasterDB()
        workflowObj.ProcessJobs()
        print("Sleeping for "+str(SleepTime)+" Seconds")
        time.sleep(SleepTime)

    dbaseObj.CloseConnections()