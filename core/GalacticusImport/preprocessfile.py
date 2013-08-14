import h5py
import numpy
import sys




if __name__ == '__main__':
    if len(sys.argv)<2:
        print("Error Not Enough Arguments")
        exit()
    InputFilePath=sys.argv[1]
    OutputFilePath=sys.argv[1]+".output.h5"
    #DataMapping={'float64':'>f8','int64':'>i8'}
    #DataMapping={'float64':'float64','int64':'int64'}
    print("Start Loading HDF5 File Done....")
    InputFile=h5py.File(InputFilePath,'r')
    OutputFile=h5py.File(OutputFilePath,'w')
    

    cosgroup=OutputFile.create_group("cosmology")
    cosgroup.create_dataset("hubble",  data=[0.0])
    cosgroup.create_dataset("omega_l",  data=[0.0])
    cosgroup.create_dataset("omega_m",  data=[0.0])
    
    
    
    Outputs=InputFile["Outputs"]
    GalaxyCountData=[]
    TreeStartIndexData=[]
    TreeIndexData=[]
    NextItemIndex=0
    
   
    
    #Datadict={}
    TotalCount=0
    dtypestr=""
    fieldNames=""
    DataTypeLists=[]
    for dset in Outputs["Output1/nodeData"]:    
        DataTypeLists+=[(str(dset),(str(Outputs["Output1/nodeData/"+str(dset)].dtype)))]
    
    DataTypeLists+=[('zoneid',numpy.int32)]
    
    
    DataTypeLists+=[('MetalsColdGas',numpy.float64)]
    DataTypeLists+=[('sfr',numpy.float64)]  
    DataTypeLists+=[('treeid',numpy.int64)]  
    
    
    
    
    
    
    TotalRecordsCount=0
    for Output in Outputs:
        FirstKey=Outputs[Output+"/nodeData"].keys()[0]        
        TotalRecordsCount=TotalRecordsCount+ len(Outputs[Output+"/nodeData/"+FirstKey][:])
    print "Total:"+str(TotalRecordsCount)
    Datadict = numpy.zeros(shape=(TotalRecordsCount,),dtype=DataTypeLists)
    

    EndIndex=0
    OutputCounter=0
   
    for Output in Outputs:
        print Output+"\t"+str(OutputCounter)+"/"+str(len(Outputs))
        OutputCounter=OutputCounter+1
        TreeIDsList=[]
        for LocalIndex in range(0,len(Outputs[Output+'/mergerTreeStartIndex'])):
                       
            if Outputs[Output+'/mergerTreeCount'][LocalIndex]>0:               
                TreeStartIndexData.append(NextItemIndex)
                GalaxyCountData.append(Outputs[Output+'/mergerTreeCount'][LocalIndex])
                TreeIndexData.append(Outputs[Output+'/mergerTreeIndex'][LocalIndex])  
                for i in range(0,Outputs[Output+'/mergerTreeCount'][LocalIndex]):
                    TreeIDsList.append(Outputs[Output+'/mergerTreeIndex'][LocalIndex])                          
                NextItemIndex=NextItemIndex+Outputs[Output+'/mergerTreeCount'][LocalIndex]
            
            TotalCount=TotalCount+ Outputs[Output+'/mergerTreeCount'][LocalIndex]    
        StartIndex=EndIndex        
        FirstKey=Outputs[Output+"/nodeData"].keys()[0] 
        EndIndex=StartIndex+len(Outputs[Output+"/nodeData/"+FirstKey][:])
        print str(StartIndex)+":"+ str(EndIndex)
        print len(Outputs[Output+"/nodeData/"+str(dset)][:])
        for dset in Outputs[Output+"/nodeData"]:                                
            Datadict[dset][StartIndex:EndIndex]=Outputs[Output+"/nodeData/"+str(dset)][:]
        ZoneIndex=int(Output.replace("Output","")) 
        print "ZoneIndex="+str(ZoneIndex)
        Datadict['zoneid'][StartIndex:EndIndex]=ZoneIndex
        Datadict['treeid'][StartIndex:EndIndex]=TreeIDsList            
        StartIndex=EndIndex+1
    
    Datadict['MetalsColdGas']=numpy.add(Datadict['diskAbundancesGasMetals'],Datadict['spheroidAbundancesGasMetals'])
    Datadict['sfr']=numpy.add(Datadict['interOutputDiskStarFormationRate'],Datadict['interOutputSpheroidStarFormationRate'])
         
    

    OutputFile.create_dataset("galaxies", data=Datadict)
    OutputFile.create_dataset("tree_counts", data=GalaxyCountData)
    OutputFile.create_dataset("tree_displs", data=TreeStartIndexData)
    OutputFile.create_dataset("snapshot_redshifts", data=[1]*64)

    InputFile.close()
    OutputFile.close()