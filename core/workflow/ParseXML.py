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
        self.WorkDirectory=Options['WorkFlowSettings:WorkingDir']
    
    def ParseFile(self,JobID,DatabaseName):
        self.GetCurrentUser()
        #self.GetDocumentSignature()        
        self.SetBasicInformation(JobID,DatabaseName)
        
        
        
    def ExportTree(self,FileName): 
        with open(FileName,'w') as f:
            f.write(ET.tostring(self.tree,encoding='UTF-8',xml_declaration=True,pretty_print=True))       
        
           
    def GetCurrentUser(self):
        self.UserName=self.tree.xpath("ns:username",namespaces={'ns':self.NameSpace})[0].text
    def GetDocumentSignature(self):
        self.Signature=self.tree.xpath("ns:signature",namespaces={'ns':self.NameSpace})[0].text
        print self.Signature
    def FindModules(self):        
        self.Modules=self.tree.xpath("ns:workflow/ns:module",namespaces={'ns':self.NameSpace})
        for Module in self.Modules:
            print Module.attrib['name'] 
            print('----------------------------------') 
            ModuleParams=Module.xpath('*')
            for Param in ModuleParams:
                if Param.attrib.get('name') !=None:
                    print (Param.attrib['name']+":"+Param.text)
    def SetBasicInformation(self,JobID,Database):
        
        
        DBElement=ET.Element("database")        
        DBElement.text=Database        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("OutputDir")        
        DBElement.text=self.WorkDirectory+"/jobs/"+self.UserName+"/"+str(JobID)+"/output/"        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("LogDir")        
        DBElement.text=self.WorkDirectory+"/jobs/"+self.UserName+"/"+str(JobID)+"/log/"        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
                
      
