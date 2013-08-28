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
     
    Datadict=numpy.sort(Datadict, order='mergerTreeIndex')
    numpy.save('numpyData.npy', Datadict)
    #Datadict=numpy.load('numpyData.npy')  
    
    OutputFile.create_dataset("galaxies", data=Datadict)
    ListOfUnique=numpy.unique(Datadict['mergerTreeIndex'])
    ArrayList=Datadict['mergerTreeIndex']
    GalaxyCountData=[]
    TreeStartIndexData=[]    
        
    for TreeId in  ListOfUnique:
        itemindex=numpy.where(Datadict['mergerTreeIndex']==TreeId)
        StartIndex=itemindex[0][0]
        TreeCount=len(itemindex[0])
        GalaxyCountData.append(TreeCount)
        TreeStartIndexData.append(StartIndex)
        print str(StartIndex)+":"+str(TreeCount)
        
        
    RedshiftData=[127, 79.9978940547546, 49.999592003264, 30.000062000124, 19.9156888582125, 18.2437217357837, 16.7245254258317, 15.3430738053213, 14.0859142818351,12.9407795683935, 11.8965695125097, 10.9438638399522, 10.0734613425465, 9.277914816642, 8.54991261829954, 7.88320363856021, 7.27218807646811,6.71158665895508, 6.19683339330695, 5.72386433931309, 5.28883354715367, 4.88844921801394, 4.51955578615033, 4.17946858652302, 3.86568282559933,3.57590511403156, 3.30809793168218, 3.06041903524444, 2.83118276274251, 2.61886150617016, 2.42204412383693, 2.23948544013269, 2.07002732324318,1.91263267041814, 1.76633590510361, 1.63027073376663, 1.50363653206282, 1.38571813694499, 1.27584621651946, 1.17341693743819, 1.07787458364588,0.988708115321206, 0.905462389030634, 0.827699146098959, 0.755035635998589, 0.687108801646618, 0.623590114933944, 0.564176601795049,0.508591428183505, 0.45657724738945, 0.407899442190241, 0.362340282631115, 0.319703436243807, 0.279801784299648, 0.242469084263011,0.207548627983249, 0.174897607673491, 0.144383423377236, 0.115883372333457, 0.0892878345066779, 0.0644933969474588, 0.0414030615167202,0.0199325416616944, 0]
    OutputFile.create_dataset("tree_counts", data=GalaxyCountData)
    OutputFile.create_dataset("tree_displs", data=TreeStartIndexData)
    OutputFile.create_dataset("snapshot_redshifts", data=RedshiftData)
    cosgroup=OutputFile.create_group("cosmology")
    cosgroup.create_dataset("hubble",  data=[73])
    cosgroup.create_dataset("omega_l",  data=[0.75])
    cosgroup.create_dataset("omega_m",  data=[0.25])
    #InputFile.close()
    OutputFile.close()