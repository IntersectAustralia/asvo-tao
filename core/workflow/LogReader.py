import os, shlex, subprocess,string,time
import EnumerationLookup
import settingReader # Read the XML settings
import logging



class LogReader(object):
      
    
    def __init__(self,Options):
        self.Options=Options
    
    def GetFileName(self,UserName,JobID,SubJobIndex):
        path = os.path.join(self.Options['WorkFlowSettings:WorkingDir'], UserName, str(JobID),'log','tao.log.'+str(SubJobIndex))        
        return path
    def ParseFile(self,CurrentJobRecord):
	UserName=CurrentJobRecord['username']
	JobID=CurrentJobRecord['uireferenceid']
	SubJobIndex=CurrentJobRecord['subjobindex']

        FilePath=self.GetFileName(UserName, JobID,SubJobIndex)
        JobDetails={'start':-1,'progress':'0%','end':-1,'error':'','endstate':''}
        counter=10
        while ((not os.path.exists(FilePath)) and counter>0):
            counter=counter-1
            logging.info('TAO LogFile not found... Will retry for more '+str(counter)+' times')
            time.sleep(1)
            
        if(os.path.exists(FilePath)):
            LogFile = open(FilePath, "r")
            FileLines=LogFile.readlines()            
        
            for Line in FileLines:
                JobDetails=self.ParseLine(Line,JobDetails)
            
            LogFile.close()
            return JobDetails
        else:
            logging.error(FilePath+' Not Found')
            return None
    
    def ParseLine(self,Line,JobDetails):  
        Line=Line.lower().strip('\n')    
        LineParts=Line.split(',')
        if len(LineParts)>=2:
            if LineParts[1]=='start':
                JobDetails['start']=float(LineParts[0])
            elif LineParts[1]=='end':
                JobDetails['end']=float(LineParts[0])
                JobDetails['endstate']=LineParts[2]                
            elif LineParts[1]=='progress':
                JobDetails['progress']=LineParts[2]
                JobDetails['end']=float(LineParts[0])
            elif LineParts[1]=='error':
                JobDetails['error']=LineParts[2]    
            
        return JobDetails
        
        
#if __name__ == '__main__':

    ## Read Running Setting from XML File
#    [Options]=settingReader.ParseParams("settings.xml")
    
#    LogReaderObj=LogReader(Options)
#    LogReaderObj.ParseFile('UserName', 100)
        
              
