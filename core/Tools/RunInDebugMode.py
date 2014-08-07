import os, shlex, subprocess, time, logging,sys
import settingReader # Read the XML settings
import shutil
import glob
import locale

if __name__ == '__main__': 
    [Options]=settingReader.ParseParams("settings.xml")  
    
    JobUserName='Amr'
    JobID=204
    
    
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
    if (os.path.exists(DebugPathLog)):
        shutil.rmtree(DebugPathLog)
    if (os.path.exists(DebugPathOutput)):    
        shutil.rmtree(DebugPathOutput)
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
    for fl in glob.glob(DebugPathLog+"/pbs_script*"):
        print "Reading: "+fl
        
        f1=open(fl,'r')
        strText=f1.read()
        f1.close()
        strText=strText.replace(Options['Torque:ExecutableName'],Options['Torque:DebugName'])
        
        strText=strText.replace(Options['Torque:BaseLibPath'],Options['Torque:DebugLibPath'])
        
        strText=strText.replace(Options['WorkFlowSettings:WorkingDir'],Options['WorkFlowSettings:DebugDir'])
        
        f2=open(fl,'w')
        f2.write(strText)
        f2.close()
    
        ExecutionCommand='ssh g2 \"cd %s; qsub -q %s %s\"'%(DebugPathLog.encode(locale.getpreferredencoding()), "sstar".encode(locale.getpreferredencoding()), fl.encode(locale.getpreferredencoding()))
                                                            
        print ExecutionCommand
        stdout = subprocess.check_output(shlex.split(ExecutionCommand))
        pbs_id = stdout[:-1]
        print "PBSID: "+pbs_id
    
    
    