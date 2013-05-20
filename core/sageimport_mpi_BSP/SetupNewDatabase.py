import logging

class SetupNewDatabase(object):

    def __init__(self,Options,CurrentSAGEStruct):
        self.Options=Options
        self.CurrentSAGEStruct=CurrentSAGEStruct


    def SetNewDatabase(self):
        self.DBName=self.Options['PGDB:NewDBName']
        self.DBAlias=self.Options['PGDB:NewDBAlias']
        self.BoxSizeX=self.Options['RunningSettings:SimulationBoxX']
        self.BoxSizeY=self.Options['RunningSettings:SimulationBoxY']
        self.BSPCellSize=self.Options['RunningSettings:BSPCellSize']
        logging.info("Send To Server: DBName:"+self.DBName)
        logging.info("Send To Server: DBAlias:"+self.DBAlias)
        logging.info("Send To Server: BoxSizeX:"+self.BoxSizeX)
        logging.info("Send To Server: BoxSizeY:"+self.BoxSizeY)
        logging.info("Send To Server: BSPCellSize"+self.BSPCellSize)
        for field in self.CurrentSAGEStruct:
            if field[3]==1:
                FieldDT=field[1]
                FieldName=field[2]
                logging.info("Send To Server: Field ("+FieldName+"):"+FieldDT)






