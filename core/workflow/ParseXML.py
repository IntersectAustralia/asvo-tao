import re
import lxml.etree as ET
import settingReader # Read the XML settings


class ParseXMLParameters(object):

    

    def __init__(self,FileName,Options):        
        self.tree = ET.parse(FileName)
        self.NameSpace=re.findall('\{.*\}',self.tree.xpath('.')[0].tag)[0]
        self.NameSpace=self.NameSpace[1:-1]
        self.Options=Options
        self.WorkDirectory=Options['WorkFlowSettings:WorkingDir']
    def ParseFile(self,JobID):
        self.GetCurrentUser()
        self.GetDocumentSignature()        
        self.GetDatabase(JobID)
        
        
        
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
    def GetDatabase(self,JobID):
        FModules=self.tree.xpath("ns:workflow/ns:light-cone",namespaces={'ns':self.NameSpace})
        if len(FModules)>0:
            self.LightConeModule=FModules[0]
        else:
            raise Exception('Error In Getting Database information','Light Cone module cannot be found!')
        self.Simulation=self.LightConeModule.xpath("ns:simulation",namespaces={'ns':self.NameSpace})[0].text
        self.GalaxyModel=self.LightConeModule.xpath("ns:galaxy-model",namespaces={'ns':self.NameSpace})[0].text
        DBElement=ET.Element("database")        
        DBElement.text=self.Simulation+":"+self.GalaxyModel        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("OutputDir")        
        DBElement.text=self.WorkDirectory+"/"+self.UserName+"/"+str(JobID)+"/output/"        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        DBElement=ET.Element("LogDir")        
        DBElement.text=self.WorkDirectory+"/"+self.UserName+"/"+str(JobID)+"/log/"        
        self.tree.xpath("/ns:tao",namespaces={'ns':self.NameSpace})[0].append(DBElement)
        
        
        
        
if __name__ == '__main__':
    
    
    [Options]=settingReader.ParseParams("settings.xml")
    
    ParseXMLParametersObj=ParseXMLParameters('/home/amr/tao.xml',Options)
    ParseXMLParametersObj.ParseFile(101)
    ParseXMLParametersObj.ExportTree("/home/amr/tao01.xml")

    
