import xml.etree.ElementTree as ET
import logging

## Helps reading XML setting file into a Hash Table of Running options and Tuples array which describes the SAGE fields and their data types
def ParseParams(FilePath):
    ## Init Return value
    CurrentSAGEStruct=[]
    RunningOptions=dict()
    
    ###############################################################################
    ###### Parse XML and load it as tree
    tree = ET.ElementTree(file=FilePath)
    SettingsNode = tree.getroot()   
    
    ################################################################################
    #### The first Node contain the sage fields and their data type mapping
    #### Load them into tuple list (ordered list- The order is important)
    sageFieldsNode=SettingsNode[0]
    for sagefield in sageFieldsNode:  
        ExportInDB=True
        if sagefield.attrib.has_key('DBExport') ==True:
            ExportInDB=(sagefield.attrib['DBExport']=="1")
        if sagefield.attrib.has_key('DBFieldName') ==False:     
            CurrentSAGEStruct.append([sagefield.text,sagefield.attrib['Type'],sagefield.text,ExportInDB])
        else:
            CurrentSAGEStruct.append([sagefield.text,sagefield.attrib['Type'],sagefield.attrib['DBFieldName'],ExportInDB])    
    ##################################################################################
    ## Load PostGres information
    ## Running Options and PostgreSQL DB information will take the form of ["Header"."Child"]
    pgNode=SettingsNode[1]
    RunningOptions[pgNode.tag+':TreeTablePrefix']= pgNode.findall('TreeTablePrefix')[0].text
    RunningOptions[pgNode.tag+':NewDBName']= pgNode.findall('NewDBName')[0].text
    RunningOptions[pgNode.tag+':ServersCount']= pgNode.findall('ServersCount')[0].text
    
    serversList=pgNode.findall('serverInfo')
    ServerIndex=0
    for pgfield in serversList:
       for pgserverinfo in pgfield:
           RunningOptions[pgNode.tag+':'+pgfield.tag+str(ServerIndex)+":"+pgserverinfo.tag]= pgserverinfo.text
       ServerIndex=ServerIndex+1     
    
    ##########################################################################   
    RunningSettingsNode=SettingsNode[2]
    for settingfield in RunningSettingsNode:
       RunningOptions[RunningSettingsNode.tag+':'+settingfield.tag]= settingfield.text
       
    
    
    
    return [CurrentSAGEStruct,RunningOptions]