import h5py
import numpy
import sys




if __name__ == '__main__':
    if len(sys.argv)<2:
        print("Error Not Enough Arguments")
        exit()
    InputFilePath=sys.argv[1]
    OutputFilePath=sys.argv[1]+".output.h5"
    
    print("Start Loading HDF5 File Done....")
    InputFile=h5py.File(InputFilePath,'r')
    OutputFile=h5py.File(OutputFilePath,'w')
    #dset=OutputFile.create_dataset("Test", (100,), 'f',maxshape=(None,))
    
    Outputs=InputFile["Outputs"]
    GalaxyCountData=[]
    TreeStartIndexData=[]
    TreeIndexData=[]
    NextItemIndex=0
    Datadict={}
    TotalCount=0
    for Output in Outputs:
        print Output
        for LocalIndex in range(0,len(Outputs[Output+'/mergerTreeStartIndex'])):
            TotalCount=TotalCount+ Outputs[Output+'/mergerTreeCount'][LocalIndex]           
            if Outputs[Output+'/mergerTreeCount'][LocalIndex]>0:               
                TreeStartIndexData.append(NextItemIndex)
                GalaxyCountData.append(Outputs[Output+'/mergerTreeCount'][LocalIndex])
                TreeIndexData.append(Outputs[Output+'/mergerTreeIndex'][LocalIndex])                
                NextItemIndex=NextItemIndex+Outputs[Output+'/mergerTreeCount'][LocalIndex]
                
         
        for dset in Outputs[Output+"/nodeData"]:
            if dset not in Datadict:
                Datadict[dset]=[]
            #for delem in Outputs[Output+"/nodeData/"+str(dset)]:
            Datadict[dset]=Datadict[dset]+list(Outputs[Output+"/nodeData/"+str(dset)][:])           
            print dset+":"+str(len(Datadict[dset]))+"/"+str(TotalCount)+"\t\t"+str(TreeStartIndexData[-1])+"+"+str(GalaxyCountData[-1])
    
    InputFile.close()
    OutputFile.close()
    