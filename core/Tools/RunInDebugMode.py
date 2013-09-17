import os, shlex, subprocess, time, logging,sys
import settingReader # Read the XML settings
import shutil
import glob


if __name__ == '__main__': 
    [Options]=settingReader.ParseParams("settings.xml")  
    
    JobUserName='Amr'
    JobID=178
    
    
    JobPath=JobUserName+"/"+str(JobID)
    print 'Current Folder: '+JobPath
    print 'Working Directory:'+ Options['WorkFlowSettings:WorkingDir']
    print 'Debug Directory:'+ Options['WorkFlowSettings:DebugDir']
    
    JobPathLog=os.path.join(Options['WorkFlowSettings:WorkingDir'],  JobUserName, str(JobID),'log')
    JobPathOutput=os.path.join(Options['WorkFlowSettings:WorkingDir'],  JobUserName, str(JobID),'output')
    DebugPathLog = os.path.join(Options['WorkFlowSettings:DebugDir'],  JobUserName, str(JobID),'log')
    DebugPathOutput = os.path.join(Options['WorkFlowSettings:DebugDir'],  JobUserName, str(JobID),'output')
    
    
    #SrcJobPathLog=os.path.join(Options['WorkFlowSettings:WorkingDir'],  JobUserName, str(JobID))
    #DstJobPathLog=os.path.join(Options['WorkFlowSettings:DebugDir'],  JobUserName, str(JobID))
    
    
    ########################################################################
    ## Copy the files and clean un-used files
    shutil.copytree(JobPathLog,DebugPathLog)
    os.makedirs(DebugPathOutput)
    
    for fl in glob.glob(DebugPathLog+"/*.log*"):
        print "Removing: "+fl
        os.remove(fl)
    
    for fl in glob.glob(DebugPathLog+"/"+Options['Torque:jobprefix']+"*"):
        print "Removing: "+fl
        os.remove(fl)
    
    for fl in glob.glob(DebugPathLog+"/*.btr"):
        print "Removing: "+fl
        os.remove(fl)
    
    ######################################################################
    
    for fl in glob.glob(DebugPathLog+"/params*.xml"):
        
        f1=open(fl,'r')
        strText=f1.read()
        f1.close()
        strText=strText.replace(Options['WorkFlowSettings:WorkingDir'],Options['WorkFlowSettings:DebugDir'])
        
        f2=open(fl,'w')
        f2.write(strText)
        f2.close()
        print "Reading: "+fl
    
    
    
    
    