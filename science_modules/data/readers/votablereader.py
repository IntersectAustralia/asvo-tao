#This file needs the following
#http://stsdas.stsci.edu/astrolib/vo-0.8.tar.gz
# https://github.com/atpy/atpy/downloads

import atpy
import sys,string,os



if __name__ == '__main__':
    voFileName=sys.argv[1]
    tbl = atpy.Table(voFileName)
    for column in tbl.columns:
        print column+":"+str(tbl.columns[column])
        
    for rowindx in range(1,len(tbl)):
        print tbl.row(rowindx)
    