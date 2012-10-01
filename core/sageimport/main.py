'''
Created on 28/09/2012

@author: Amr Hassan
'''
import SAGEReader

if __name__ == '__main__':
    print('Starting Files Loading')
    

    
    Reader=SAGEReader.SAGEDataReader('/lustre/projects/p014_swin/raw_data/millennium/full/sage_output/')
    Reader.ProcessAllFiles()
    print('Processing Done')