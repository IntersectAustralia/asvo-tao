import re,os
import lxml.etree as ET
import settingReader # Read the XML settings
import StringIO
import logging

class ParseXMLParameters(object):

    

    def __init__(self,FileName,Options):
                 
        self.tree = ET.parse(FileName)
        self.NameSpace=re.findall('\{.*\}',self.tree.xpath('.')[0].tag)[0]
        self.NameSpace=self.NameSpace[1:-1]
        self.Options=Options
        self.WorkDirectory=self.Options['WorkFlowSettings:WorkingDir']
    
    def ParseFile(self,JobID,DatabaseName,JobUserName):
        
        
            
        self.SubJobsCount=self.GetSubJobsCount()       
        self.ModifyOutputPath()
        self.ReadRNGSeeds()
        self.SetBasicInformation(JobID,DatabaseName,JobUserName)
        SimulationName=self.GetSimulationName()
        return [self.SubJobsCount,SimulationName.lower()]
    
    def GetSimulationName(self):
        SimulationNode=None
        if self.IsSquentialJob()==False:
            logging.info("Parallel Job - Getting Simulation name from the Lightcone")
            SimulationNode=self.tree.xpath("ns:workflow/ns:light-cone/ns:simulation",namespaces={'ns':self.NameSpace})
        else:
            logging.info("Sequential Job - Getting Simulation name from the SQL")
            SimulationNode=self.tree.xpath("ns:workflow/ns:sql/ns:simulation",namespaces={'ns':self.NameSpace})
            logging.info(SimulationNode)
        
        SimulationName=""
        if len(SimulationNode)>0:
            SimulationName=SimulationNode[0].text
            return SimulationName
        else:            
            raise  Exception('Cannot Retrieved the simulation Name!')
            

    def ReadRNGSeeds(self):
        self.RNGSeedsArr=[]
        RNGSeedFields=self.tree.xpath("ns:workflow/ns:light-cone/ns:rng-seeds/ns:*",namespaces={'ns':self.NameSpace})
        if(len(RNGSeedFields)>0):
            if len(RNGSeedFields)!=self.SubJobsCount:
                raise  Exception('Incorect Number of RNG Seeds','SubJobsCount=='+str(self.SubJobsCount)+' while RNG Count ='+str(len(RNGSeedFields))+'!')
            for RNGSeed in RNGSeedFields:                
                self.RNGSeedsArr.append(RNGSeed.text)
                
            ParentNode=self.tree.xpath("ns:workflow/ns:light-cone/ns:rng-seeds",namespaces={'ns':self.NameSpace})[0]
            RNGNewNode=ET.Element("{"+self.NameSpace+"}rng-seed")        
            RNGNewNode.text="#RNGSeedValue" 
            ParentNode.getparent().append(RNGNewNode)
            ParentNode.getparent().remove(ParentNode)
        print self.RNGSeedsArr
          
        
            
        
        
    
    def IsSquentialJob(self):
        
        sqlModuleInstance=self.tree.xpath("ns:workflow/ns:sql",namespaces={'ns':self.NameSpace})
        if len(sqlModuleInstance)==0:
            logging.info("----- Parallel Job -----")
            return False
        else:
            logging.info("----- Sequential Job -----")
            return True    
        
    def ExportTrees(self,FileName):
            
       
        if self.SubJobsCount>0:
            for i in range(0,self.SubJobsCount):
                FileNameWithIndex=FileName.replace('<index>',str(i))
                self.ExportTree(FileNameWithIndex,i)
        else:            
            raise  Exception('Error in SubJobsCount','SubJobsCount<=0!')        
    def ExportTree(self,FileName,SubJobIndex): 
         
        self.tree.xpath("/ns:tao/ns:subjobindex",namespaces={'ns':self.NameSpace})[0].text=str(SubJobIndex)
        with open(FileName,'w') as f:
            strTree=ET.tostring(self.tree,encoding='UTF-8',xml_declaration=True,pretty_print=True)
            strTree=strTree.replace("&lt;OutputFileIndex&gt;",str(SubJobIndex))
            if len(self.RNGSeedsArr)>SubJobIndex:
                strTree=strTree.replace("#RNGSeedValue",str(self.RNGSeedsArr[SubJobIndex]))
            
            f.write(strTree)       
        
           
    def GetCurrentUser(self):
        self.UserName=self.tree.xpath("ns:username",namespaces={'ns':self.NameSpace})[0].text
    
    def GetSubJobsCount(self):
        NumofConesNode=self.tree.xpath("ns:workflow/ns:light-cone/ns:num-cones",namespaces={'ns':self.NameSpace})
        if len(NumofConesNode)>0:
            self.SubJobsCount=NumofConesNode[0].text
        else:
            self.SubJobsCount=1
        return int(self.SubJobsCount)
    def GetDocumentSignature(self):
        self.Signature=self.tree.xpath("ns:signature",namespaces={'ns':self.NameSpace})[0].text
        print self.Signature
        
    def ModifySEDFilePath(self):
        self.SEDDir=self.Options['Torque:maindatapath']+"/sed/"        
        self.stellarpopulationmodel=self.tree.xpath("ns:workflow/ns:sed/ns:single-stellar-population-model",namespaces={'ns':self.NameSpace})
        if len(self.stellarpopulationmodel)==0:
            return
        elif len(self.stellarpopulationmodel)>0:
            self.stellarpopulationmodel=self.stellarpopulationmodel[0]
        self.stellarpopulationmodel.text=self.SEDDir+ self.stellarpopulationmodel.text
    def ModifyFilterFilePath(self):
        self.BandPassDIR=self.Options['Torque:maindatapath']+"/bandpass/"
        
        self.bandpassfilters=self.tree.xpath("ns:workflow/ns:filter/ns:bandpass-filters/ns:item",namespaces={'ns':self.NameSpace})
        
        for filter in self.bandpassfilters:
            filter.text=self.BandPassDIR+filter.text.lower()
    
    def ModifyOutputPath(self):
        self.lfilename=self.tree.xpath("ns:workflow/ns:fits/ns:filename",namespaces={'ns':self.NameSpace})                    
        if len(self.lfilename)>0:
            self.filename=self.lfilename[0]
            strfileName, strfileExtension = os.path.splitext(self.filename.text)
            self.filename.text=strfileName+".<OutputFileIndex>"+strfileExtension
            
            
        
        self.lfilename=self.tree.xpath("ns:workflow/ns:votable/ns:filename",namespaces={'ns':self.NameSpace})                    
        if len(self.lfilename)>0:
            self.filename=self.lfilename[0]
            strfileName, strfileExtension = os.path.splitext(self.filename.text)
            self.filename.text=strfileName+".<OutputFileIndex>"+strfileExtension
        
        self.lfilename=self.tree.xpath("ns:workflow/ns:csv/ns:filename",namespaces={'ns':self.NameSpace})                    
        if len(self.lfilename)>0:
            self.filename=self.lfilename[0]
            strfileName, strfileExtension = os.path.splitext(self.filename.text)
            self.filename.text=strfileName+".<OutputFileIndex>"+strfileExtension
        
        self.lfilename=self.tree.xpath("ns:workflow/ns:hdf5/ns:filename",namespaces={'ns':self.NameSpace})                    
        if len(self.lfilename)>0:
            self.filename=self.lfilename[0]
            strfileName, strfileExtension = os.path.splitext(self.filename.text)
            self.filename.text=strfileName+".<OutputFileIndex>"+strfileExtension
        
    ## This function is used for debugging reasons only (not currently active)    
    def FindModules(self):        
        self.Modules=self.tree.xpath("ns:workflow/ns:module",namespaces={'ns':self.NameSpace})
        for Module in self.Modules:
            print Module.attrib['name'] 
            print('----------------------------------') 
            ModuleParams=Module.xpath('*')
            for Param in ModuleParams:
                if Param.attrib.get('name') !=None:
                    print (Param.attrib['name']+":"+Param.text)
    
    def escapeUserName(self,UserName):
        return ''.join(e for e in UserName if e.isalnum())
        
    def SetBasicInformation(self,JobID,Database,JobUserName):
        
        UserFolder=self.escapeUserName(JobUserName)
        DBElement=ET.Element("{"+self.NameSpace+"}database")        
        DBElement.text=Database        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("{"+self.NameSpace+"}outputdir")        
        DBElement.text=self.WorkDirectory+UserFolder+"/"+str(JobID)+"/output/"        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("{"+self.NameSpace+"}logdir")        
        DBElement.text=self.WorkDirectory+UserFolder+"/"+str(JobID)+"/log/"        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("{"+self.NameSpace+"}bandpassdatapath")        
        DBElement.text= self.Options['Torque:maindatapath']+"/bandpass/"       
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("{"+self.NameSpace+"}subjobindex")        
        DBElement.text="none" 
             
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        nodes=self.Options['Torque:Nodes']        
        ppn=self.Options['Torque:ProcessorNode']
        queuename=self.Options['Torque:JobsQueue']
        
        DBElement=ET.Element("{"+self.NameSpace+"}queue")        
        DBElement.text=queuename            
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("{"+self.NameSpace+"}nodes")        
        DBElement.text=str(nodes)            
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("{"+self.NameSpace+"}processorpernode")        
        DBElement.text=str(ppn)            
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
                
if __name__ == '__main__':
     [Options]=settingReader.ParseParams("settings.xml")
     ParseXMLParametersObj=ParseXMLParameters('/home/amr/workspace/params.xml',Options)
     
     ParseXMLParametersObj.ParseFile(110, "Database", "TestUser")
     ParseXMLParametersObj.ExportTrees('/home/amr/workspace/params.<index>.processed.xml')
