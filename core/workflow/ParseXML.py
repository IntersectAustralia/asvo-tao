import re
import lxml.etree as ET
import settingReader # Read the XML settings
import StringIO


class ParseXMLParameters(object):

    

    def __init__(self,FileName,Options):
                 
        self.tree = ET.parse(FileName)
        self.NameSpace=re.findall('\{.*\}',self.tree.xpath('.')[0].tag)[0]
        self.NameSpace=self.NameSpace[1:-1]
        self.Options=Options
        self.WorkDirectory=self.Options['WorkFlowSettings:WorkingDir']
    
    def ParseFile(self,JobID,DatabaseName,JobUserName):
        #self.GetCurrentUser()
        #self.GetDocumentSignature()    
        self.SubJobsCount=self.GetSubJobsCount()
        self.ModifySEDFilePath()
        #self.ModifyFilterFilePath()
        self.SetBasicInformation(JobID,DatabaseName,JobUserName)
        return self.SubJobsCount
        
    def ExportTrees(self,FileName):
            
       
        if self.SubJobsCount>0:
            for i in range(0,self.SubJobsCount):
                FileNameWithIndex=FileName.replace('<index>',str(i))
                self.ExportTree(FileNameWithIndex,i)
        else:
            print("Error")
            raise  Exception('Error in SubJobsCount','SubJobsCount<=0!')        
    def ExportTree(self,FileName,SubJobIndex): 
         
        self.tree.xpath("/ns:tao/ns:subjobindex",namespaces={'ns':self.NameSpace})[0].text=str(SubJobIndex)
        with open(FileName,'w') as f:
            f.write(ET.tostring(self.tree,encoding='UTF-8',xml_declaration=True,pretty_print=True))       
        
           
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
        if len(self.stellarpopulationmodel)>0:
            self.stellarpopulationmodel=self.stellarpopulationmodel[0]
        self.stellarpopulationmodel.text=self.SEDDir+ self.stellarpopulationmodel.text
    def ModifyFilterFilePath(self):
        self.BandPassDIR=self.Options['Torque:maindatapath']+"/bandpass/"
        
        self.bandpassfilters=self.tree.xpath("ns:workflow/ns:filter/ns:bandpass-filters/ns:item",namespaces={'ns':self.NameSpace})
        
        for filter in self.bandpassfilters:
            filter.text=self.BandPassDIR+filter.text.lower()
                        
        
        
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
    
    
        
    def SetBasicInformation(self,JobID,Database,JobUserName):
        
        
        DBElement=ET.Element("{"+self.NameSpace+"}database")        
        DBElement.text=Database        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("{"+self.NameSpace+"}outputdir")        
        DBElement.text=self.WorkDirectory+"/jobs/"+JobUserName+"/"+str(JobID)+"/output/"        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("{"+self.NameSpace+"}logdir")        
        DBElement.text=self.WorkDirectory+"/jobs/"+JobUserName+"/"+str(JobID)+"/log/"        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("{"+self.NameSpace+"}bandpassdatapath")        
        DBElement.text= self.Options['Torque:maindatapath']+"/bandpass/"       
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("{"+self.NameSpace+"}subjobindex")        
        DBElement.text="none" 
             
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
                
if __name__ == '__main__':
     [Options]=settingReader.ParseParams("settings.xml")
     ParseXMLParametersObj=ParseXMLParameters('/home/amr/workspace/params.xml',Options)
     ParseXMLParametersObj.ModifySEDFilePath()
    
     ParseXMLParametersObj.SetBasicInformation(110, "Database", "TestUser")
     ParseXMLParametersObj.ExportTree('/home/amr/workspace/params.processed.xml', 0)
