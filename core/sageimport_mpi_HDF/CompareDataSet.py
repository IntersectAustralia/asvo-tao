from numpy import genfromtxt
import string
import numpy
import sys # for listing directory contents


if __name__ == '__main__':
    #if len(sys.argv)<2:
    #    print("Error Not Enough Arguments")
    #    exit()
    File1='/home/amr/workspace/tao.output.0.csv'#sys.argv[1]
    File2='/home/amr/workspace/tao.output.0.csv'#sys.argv[2]
    my_data1 = genfromtxt(File1, delimiter=',',names=True)
    my_data2 = genfromtxt(File2, delimiter=',',names=True)
    
    

    
    print my_data1
