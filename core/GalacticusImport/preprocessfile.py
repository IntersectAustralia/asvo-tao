import h5py
import numpy
import sys




if __name__ == '__main__':
    if len(sys.argv)<2:
        print("Error Not Enough Arguments")
        exit()
    InputFilePath=sys.argv[1]
    OutputFilePath=sys.argv[1]+".output2.h5"
    #DataMapping={'float64':'>f8','int64':'>i8'}
    #DataMapping={'float64':'float64','int64':'int64'}
    print("Start Loading HDF5 File Done....")
    InputFile=h5py.File(InputFilePath,'r')
    OutputFile=h5py.File(OutputFilePath,'w')
    

    '''cosgroup=OutputFile.create_group("cosmology")
    cosgroup.create_dataset("hubble",  data=[0.0])
    cosgroup.create_dataset("omega_l",  data=[0.0])
    cosgroup.create_dataset("omega_m",  data=[0.0])
    
    
    
    Outputs=InputFile["Outputs"]
    GalaxyCountData=[]
    TreeStartIndexData=[]
    TreeIndexData=[]
    NextItemIndex=0
    
   
    
    
   
    
    DataTypeLists=[]
    for dset in Outputs["Output15/nodeData"]:
        print "FieldName: "+str(dset)    
        DataTypeLists+=[(str(dset),(str(Outputs["Output15/nodeData/"+str(dset)].dtype)))]
    
    DataTypeLists+=[('zoneid',numpy.int32)]    
    DataTypeLists+=[('MetalsColdGas',numpy.float64)]
    DataTypeLists+=[('sfr',numpy.float64)]  
    DataTypeLists+=[('treeid',numpy.int64)]
    DataTypeLists+=[('galaxyglobalindex',numpy.int64)]  
    
  
    
    
    TotalRecordsCount=0
    for Output in Outputs:
        if len(Outputs[Output+"/nodeData"].keys())>0:
            FirstKey=Outputs[Output+"/nodeData"].keys()[0]        
            TotalRecordsCount=TotalRecordsCount+ len(Outputs[Output+"/nodeData/"+FirstKey][:])
    print "Total:"+str(TotalRecordsCount)
    Datadict = numpy.zeros(shape=(TotalRecordsCount,),dtype=DataTypeLists)
    
    

    EndIndex=0
    OutputCounter=0
    GalaxyGlobalIndex=0
    for Output in Outputs:
        
        if len(Outputs[Output+"/nodeData"].keys())>0:
            
            print Output+"\t"+str(OutputCounter)+"/"+str(len(Outputs))
            OutputCounter=OutputCounter+1
            TreeIDsList=[]
            GalaxyGlobalIndexList=[]
            for LocalIndex in range(0,len(Outputs[Output+'/mergerTreeStartIndex'])):
                           
                if Outputs[Output+'/mergerTreeCount'][LocalIndex]>0:               
                    #TreeStartIndexData.append(NextItemIndex)
                    #GalaxyCountData.append(Outputs[Output+'/mergerTreeCount'][LocalIndex])
                    TreeIndexData.append(Outputs[Output+'/mergerTreeIndex'][LocalIndex])  
                    for i in range(0,Outputs[Output+'/mergerTreeCount'][LocalIndex]):
                        TreeIDsList.append(Outputs[Output+'/mergerTreeIndex'][LocalIndex])
                        GalaxyGlobalIndexList.append(GalaxyGlobalIndex)  
                        GalaxyGlobalIndex=GalaxyGlobalIndex+1                        
                    #NextItemIndex=NextItemIndex+Outputs[Output+'/mergerTreeCount'][LocalIndex]
                
                    
            StartIndex=EndIndex        
            FirstKey=Outputs[Output+"/nodeData"].keys()[0] 
            EndIndex=StartIndex+len(Outputs[Output+"/nodeData/"+FirstKey][:])
            print str(StartIndex)+":"+ str(EndIndex)
            #print len(Outputs[Output+"/nodeData/"+str(dset)][:])
            for dset in Outputs[Output+"/nodeData"]:
                if dset in Datadict.dtype.fields:                                
                    Datadict[dset][StartIndex:EndIndex]=Outputs[Output+"/nodeData/"+str(dset)][:]
                else:
                    print "Field ("+dset+") does not exists"
            
            ZoneIndex=int(Output.replace("Output","")) 
            print "ZoneIndex="+str(ZoneIndex)
            Datadict['zoneid'][StartIndex:EndIndex]=ZoneIndex
            Datadict['treeid'][StartIndex:EndIndex]=TreeIDsList 
            Datadict['galaxyglobalindex'][StartIndex:EndIndex]= GalaxyGlobalIndexList  
                    
            StartIndex=EndIndex+1
        else:
            print "Skipping: "+Output
    
    Datadict['MetalsColdGas']=numpy.add(Datadict['diskAbundancesGasMetals'],Datadict['spheroidAbundancesGasMetals'])
    Datadict['sfr']=numpy.add(Datadict['interOutputDiskStarFormationRate'],Datadict['interOutputSpheroidStarFormationRate'])
    
    numpy.save('numpyDataunsorted.npy', Datadict)     
    numpy.sort(Datadict, order='mergerTreeIndex')
    numpy.save('numpyData.npy', Datadict)'''
    Datadict=numpy.load('numpyData.npy')
    OutputFile.create_dataset("galaxies", data=Datadict)
    ListOfUnique=numpy.unique(Datadict['mergerTreeIndex'])
    ArrayList=Datadict['mergerTreeIndex']
        
        
    for TreeId in  ListOfUnique:
        itemindex=numpy.where(Datadict['mergerTreeIndex']==TreeId)
        print itemindex
        
    
    OutputFile.create_dataset("tree_counts", data=GalaxyCountData)
    OutputFile.create_dataset("tree_displs", data=TreeStartIndexData)
    OutputFile.create_dataset("snapshot_redshifts", data=[1]*64)

    InputFile.close()
    OutputFile.close()