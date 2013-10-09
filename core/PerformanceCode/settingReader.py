import xml.etree.ElementTree as ET

## Helps reading XML setting file into a Hash Table of Running options and Tuples array which describes the SAGE fields and their data types
def ParseParams(FilePath):
    ## Init Return value    
    WorkFlowOptions=dict()
    
    ###############################################################################
    ###### Parse XML and load it as tree
    tree = ET.ElementTree(file=FilePath)
    SettingsNode = tree.getroot()        
    #################################################################################
    ## System DB Connection
    DBSettings=SettingsNode[0]
    for Sfield in DBSettings:
       WorkFlowOptions[DBSettings.tag+':'+Sfield.tag]= Sfield.text 
    ##################################################################################
    ## Load Workflow information
    ## Workflow settings will take the form of ["Header"."Child"]
    WorkFlowSettings=SettingsNode[1]
    for Sfield in WorkFlowSettings:
       WorkFlowOptions[WorkFlowSettings.tag+':'+Sfield.tag]= Sfield.text     
    ########################################################################## 
    # Load Torque Settings  
    TorqueSettings=SettingsNode[2]
    for Sfield in TorqueSettings:
       WorkFlowOptions[TorqueSettings.tag+':'+Sfield.tag]= Sfield.text
       
    
    
    
    return [WorkFlowOptions]