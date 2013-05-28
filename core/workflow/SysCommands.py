import os, shlex, subprocess, time, string,datetime,time
import requests
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

class SysCommands(object):

    

    def __init__(self,Options,dbaseobj,TorqueObj):
        
        logging.info('SysCommands Class Init')
        self.Options=Options
        self.dbaseobj=dbaseobj
        self.TorqueObj=TorqueObj
        self.LogReaderObj=LogReader.LogReader(Options)
        # Define the request API.
        
        self.CALLBackBase = Options['WorkFlowSettings:CommandsURL']
        self.api = {
               'get': self.CALLBackBase + 'commands/submitted',
               'update': self.CALLBackBase + 'commands/update'}
        
        self.FunctionsMap={
                 'Job_Stop_All':self.Job_Stop_All,
                 'Job_Stop':self.Job_Stop,
                 'Job_Resume':self.Job_Resume,
                 'Workflow_Stop':self.Workflow_Stop,
                 'Worflow_Resume':self.Worflow_Resume,
                 'Lighcone_acceleration_on':self.Lighcone_acceleration_on,
                 'Lighcone_acceleration_off':self.Lighcone_acceleration_off,
                 'Job_Output_Delete':self.Job_Output_Delete                 
                 }
        
    def json_handler(self,resp):       
        
        CommandsCounter=0
        for json in resp.json:
            
            if self.HandleNewCommand(json)==True:
                CommandsCounter=CommandsCounter+1            
    
        return CommandsCounter
    
    def CheckForNewCommands(self):
        logging.info("Checking for UI Commands")
        new_jobs = 0
        WebserviceResponse = requests.get(self.api['get'])
        ResponseType = string.replace(WebserviceResponse.headers['content-type'],"; charset=utf-8","")
        
        new_commands_count=self.json_handler(WebserviceResponse)
        if new_commands_count>0:
            logging.info(str(new_commands_count)+" Commands Recieved From the UI")
    
    def HandleNewCommand(self,jsonObj):
        
        UICommandID=jsonObj['commandid']
        UIJobID=jsonObj['jobid']
        CommandType=jsonObj['commandtext']
        CommandParams=jsonObj['commandparams']
        logging.info("New Command Found")
        logging.info("UICommandID:"+str(UICommandID))
        logging.info("UIJobID:"+str(UIJobID))
        logging.info("commandtext:"+str(CommandType))
        logging.info("CommandParams:"+str(CommandParams))
        
        CommandID=self.dbaseobj.AddNewCommand(UICommandID,commandtext,UIJobID,CommandParams)
        logging.info("Command Local ID:"+str(CommandID))        
        
        CommandFunction=FunctionsMap[CommandType]
        return CommandFunction()
        
    
    def Job_Stop_All(self):
        print("Job_Stop_All")
        return True
    def Job_Stop(self):
        print("Job_Stop")
        return True
    def Job_Resume(self):
        print("Job_Resume")
        return True
    def Workflow_Stop(self):
        print("Workflow_Stop")
        return True
    def Worflow_Resume(self):
        print("Worflow_Resume")
        return True
    def Lighcone_acceleration_on(self):
        print("Lighcone_acceleration_on")
        return True
    def Lighcone_acceleration_off(self):
        print("Lighcone_acceleration_off")
        return True
    def Job_Output_Delete(self):
        print("Job_Output_Delete")
        return True
        
         
                 
    
if __name__ == '__main__':
     [Options]=settingReader.ParseParams("settings.xml")
     FilePath="/home/amr/workspace/samplecommands.txt"
     dbaseObj=""#=dbase.DBInterface(self.Options)
     TorqueObj=""#torque.TorqueInterface(self.Options,self.dbaseObj)
     SysCommandsObj=SysCommands(Options,dbaseObj,TorqueObj)
     
     