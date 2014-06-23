import re,os,sys
import StringIO
import os, shlex, subprocess,string
import logging
import locale


if __name__ == '__main__':
    InputFilePath=sys.argv[1]
    InputFile = open(InputFilePath, 'r')
    MetadataFile = open("metadata.csv", 'w')
    
    DataLines=InputFile.readlines()
    Header=DataLines[0]
    DataHeader=Header.rstrip().split(";")
    DataGrid=[]
    for Field in DataHeader:
        DataGrid.append([])
    
    for Line in DataLines[1:]:
        DataCells= Line.rstrip().split(";")
        
        for i in range(0,len(DataCells)):
            
            DataGrid[i].append(DataCells[i])
    
            
    for i in range(1,len(DataHeader)):
        LinesCounter=0
        FileName = (DataHeader[i]+".dati")
        
        MetadataFile.write('\"skymapper/'+FileName+'\",\"'+FileName+'\",\"Skymapper Telescope, \"\n')
        
        OutputFile=open("skymapper/"+FileName,"w")
        
        
        FileStr=""
        for j in range(0,len(DataLines)-1):
            
            if (DataGrid[i][j]!=""):
                FileStr+= (DataGrid[0][j]+"\t"+DataGrid[i][j]+"\n")
                LinesCounter+=1
        FileStr=str(LinesCounter)+"\n"+FileStr
        OutputFile.write(FileStr.rstrip())
        OutputFile.close()
    MetadataFile.close()