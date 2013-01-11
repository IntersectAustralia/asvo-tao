import re
import xml.etree.ElementTree as ET



class ParseXMLParameters(object):

    

    def __init__(self,FileName):
        self.tree = ET.ElementTree(file=FileName)
        self.NameSpace=re.findall('\{.*\}',self.tree.findall('.')[0].tag)[0]
    def ParseFile(self):
        self.GetCurrentUser()
        self.GetDocumentSignature()
        self.FindModules()
           
    def GetCurrentUser(self):
        self.UserName=self.tree.findall(self.NameSpace+"username")[0].text
    def GetDocumentSignature(self):
        self.Signature=self.tree.findall(self.NameSpace+"signature")[0].text
        print self.Signature
    def FindModules(self):        
        self.Modules=self.tree.findall(self.NameSpace+"workflow/"+self.NameSpace+"module")
        for Module in self.Modules:
            print Module.attrib['name'] 
            print('----------------------------------') 
            ModuleParams=Module.findall('*')
            for Param in ModuleParams:
                if Param.attrib.get('name') !=None:
                    print (Param.attrib['name']+":"+Param.text)
            
if __name__ == '__main__':
    
    
    ParseXMLParametersObj=ParseXMLParameters('/home/amr/tao.xml')
    ParseXMLParametersObj.ParseFile()

    
