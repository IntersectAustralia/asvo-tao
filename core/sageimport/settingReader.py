import xml.etree.ElementTree as ET

def ParseParams(FilePath):
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
        CurrentSAGEStruct.append([sagefield.text,sagefield.attrib['Type']])
    
    ##################################################################################
    ##### Load mysql information
    mysqlNode=SettingsNode[1]
    for mysqlfield in mysqlNode:
       RunningOptions[mysqlNode.tag+':'+mysqlfield.tag]= mysqlfield.text    
    ##################################################################################
    
    RunningSettingsNode=SettingsNode[2]
    for settingfield in RunningSettingsNode:
       RunningOptions[RunningSettingsNode.tag+':'+settingfield.tag]= settingfield.text
       
    print RunningOptions
    
    
    return [CurrentSAGEStruct,RunningOptions]