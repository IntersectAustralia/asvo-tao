import pyfits
import sys,string,os



if __name__ == '__main__':
    FitsFileName=sys.argv[1]
    f = pyfits.open(FitsFileName)
    tbdata = f[1].data
    tbhdr = f[1].header
    for field in tbhdr:
        print field+":"+str(tbhdr[field])
    ColCount=tbhdr['TFIELDS']
    print "----------------------------------------------------------------------\n"
    print "Columns Count="+str(ColCount)
    for i in range(1,ColCount+1):
        print tbhdr['TTYPE'+str(i)]+":"+tbhdr['TUNIT'+str(i)]
    print "----------------------------------------------------------------------\n"    
    for row in tbdata:
        print row
    
        