import re,os
import lxml.etree as ET
import settingReader # Read the XML settings
import StringIO


class ParseProfileData(object):

    

    def __init__(self,FileName,Options):        
        self.Options=Options
        self.ProfileFileName=FileName
        
    def ParseFile(self):
        f=open(self.ProfileFileName,'r')
        Lines=f.readlines()
        for line in Lines:
            print line
        

                
if __name__ == '__main__':
     [Options]=settingReader.ParseParams("settings.xml")
     ParseProfileDataObj=ParseProfileData('/home/amr/workspace/AppRun/params0_tao.Profile.log00000',Options)
     ParseProfileDataObj.ParseFile()
