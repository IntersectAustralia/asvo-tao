import os, shlex, subprocess, time, logging,sys

import logging, logging.handlers
import dbase
import settingReader
import os
from os import listdir
from os.path import isfile, join
from subprocess import call
import pyfits
import h5py
import shutil
import numpy
import lxml.etree as ET
import traceback



def TAOGetFileSize(FullFilePath):
    total_size = os.path.getsize(FullFilePath)
    return total_size

def TAOGetTotalRecords(FullFilePath):
    try:
        logging.info( '\t'+FullFilePath)       
        if  FullFilePath.find('.csv')!=-1:
            fi=open(FullFilePath,'r')
            RC=len(fi.readlines())            
            return RC-1
        elif  FullFilePath.find('.fits')!=-1 and FullFilePath.find('image')==-1:
            Reader = pyfits.open(FullFilePath)
            return Reader[1].data.shape[0]
            
        elif FullFilePath.find('.xml')!=-1:
            tree = ET.parse(FullFilePath)
            NameSpace=re.findall('\{.*\}',tree.xpath('.')[0].tag)[0]
            NameSpace=NameSpace.strip('{').strip('}')
            TABLEDATANode=tree.xpath("/ns:VOTABLE/ns:RESOURCE/ns:TABLE/ns:DATA/ns:TABLEDATA",namespaces={'ns':NameSpace})
            return len(TABLEDATANode[0].getchildren())
        elif FullFilePath.find('.hdf5')!=-1:
            Reader = h5py.File(FullFilePath,'r')
            RowsCount=0
            for Dset in Reader:
                if type(Reader[Dset])==h5py._hl.group.Group:
                    for SubDataset in Reader[Dset]:
                        #print Dset+"/"+SubDataset
                        RowsCount=RowsCount+Reader[Dset+"/"+SubDataset].shape[0]
                        break
                    else:
                        #print Dset
                        RowsCount=RowsCount+Reader[Dset].shape[0]
                        break
    
            Reader.close()
            return RowsCount
        else:
            logging.info( '**********'+FullFilePath)
            return 0
        #print 'End: '+CurrentPath+'/'+f
    except Exception as Exp:
        logging.info( "Error: " + FullFilePath)
        logging.info( Exp)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        #logging.info(''.join('!' + line for line in lines))
        return 0

    

    
