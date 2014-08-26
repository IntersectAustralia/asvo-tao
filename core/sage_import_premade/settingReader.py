import logging
import xml.etree.ElementTree as ET

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
    FieldsList=[]
    for sagefield in sageFieldsNode:       
        CurrentSAGEStruct.append([sagefield.text,sagefield.attrib['Type'],sagefield.text])
        FieldsList+=[sagefield.text.lower()]
    logging.info(FieldsList)
    f=open("MandatoryList.txt",'r')
    ListOfMandatoryFields=f.readlines()
    for Field in ListOfMandatoryFields:
        logging.info("Checking for Field "+Field)
        if(FieldsList.count(Field.strip('\n'))==0):
            logging.info("Current Fields List")
            logging.info(FieldsList)    
            raise Exception(Field.strip('\n')+" is missing! ")      
    ##################################################################################
    ## Load PostGres information
    ## Running Options and PostgreSQL DB information will take the form of ["Header"."Child"]
    pgNode=SettingsNode[1]
    RunningOptions[pgNode.tag+':TreeTablePrefix']= pgNode.findall('TreeTablePrefix')[0].text
    RunningOptions[pgNode.tag+':NewDBName']= pgNode.findall('NewDBName')[0].text
    RunningOptions[pgNode.tag+':NewDBAlias']= pgNode.findall('NewDBAlias')[0].text
    RunningOptions[pgNode.tag+':ServersCount']= pgNode.findall('ServersCount')[0].text
    RunningOptions[pgNode.tag+':ScienceModuleDBUserName']= pgNode.findall('ScienceModuleDBUserName')[0].text
    
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
       
    RunningSettingsNode=SettingsNode[3]
    Counter=0
    for TreeMapping in RunningSettingsNode:
        RunningOptions['TreeMapping_'+str(Counter)]=TreeMapping.text
        Counter=Counter+1
        
    
    return [CurrentSAGEStruct,RunningOptions]